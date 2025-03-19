#!/usr/bin/env python

import argparse
import logging
import sys
from i3ipc import Connection
from enum import Enum


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    CENTER = "center"


class WindowManager:
    def __init__(self, i3_connection):
        self.i3 = i3_connection
        self.window, self.workspace = self._get_active_window_and_workspace()

    def _get_active_window_and_workspace(self):
        window = self.i3.get_tree().find_focused()
        workspace = window.workspace() if window else None

        if not window or not workspace:
            logging.error("No active window or workspace found.")
            sys.exit(1)

        return window, workspace

    @property
    def is_floating_window(self):
        return self.window.floating == "user_on"

    @property
    def workspace_position(self):
        return self.workspace.rect.x, self.workspace.rect.y

    @property
    def workspace_size(self):
        return self.workspace.rect.width, self.workspace.rect.height

    @property
    def window_position(self):
        return self.window.rect.x, self.window.rect.y

    @property
    def window_size(self):
        return self.window.rect.width, self.window.rect.height

    def get_next_workspace(self, direction: str, current_workspace):
        workspaces = sorted(self.i3.get_workspaces(), key=lambda ws: ws.num)
        current_index = next(
            (i for i, ws in enumerate(workspaces) if ws.num == current_workspace.num),
            None,
        )

        if current_index is None:
            return None

        if direction == Direction.RIGHT and current_index + 1 < len(workspaces):
            return workspaces[current_index + 1].name
        elif direction == Direction.LEFT and current_index - 1 >= 0:
            return workspaces[current_index - 1].name

        return None

    def move_window_to_workspace(self, workspace_name):
        self.i3.command(f"workspace {workspace_name}")
        self.window.command(f"move container to workspace {workspace_name}")
        self.window.command("focus")

    def move_window_to_position(self, x: int, y: int):
        self.window.command(f"move position {x} {y}")

    def move_nonfloat_wingow(self, direction):
        self.window.command(f"move {direction.value}")


class I3Snapper:
    def __init__(self):
        self.window_manager = WindowManager(Connection())
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    def calculate_new_position(self, direction: str, margin: int):
        workspace_x, workspace_y = self.window_manager.workspace_position
        workspace_width, workspace_height = self.window_manager.workspace_size

        window_x, window_y = self.window_manager.window_position
        window_width, window_height = self.window_manager.window_size

        logging.info(f"Current window position: x={window_x}, y={window_y}")
        logging.info(
            f"Workspace dimensions: x={workspace_x}, y={workspace_y}, "
            f"width={workspace_width}, height={workspace_height}"
        )

        if direction == Direction.LEFT and window_x <= workspace_x + margin:
            return "next_workspace"
        elif (
            direction == Direction.RIGHT
            and window_x + window_width >= workspace_x + workspace_width - margin
        ):
            return "next_workspace"

        match direction:
            case Direction.LEFT:
                return workspace_x + margin, max(workspace_y + margin, window_y)
            case Direction.RIGHT:
                return workspace_x + workspace_width - window_width - margin, max(
                    workspace_y + margin, window_y
                )
            case Direction.UP:
                return max(workspace_x + margin, window_x), workspace_y + margin
            case Direction.DOWN:
                return max(
                    workspace_x + margin, window_x
                ), workspace_y + workspace_height - window_height - margin
            case Direction.CENTER:
                center_x = workspace_x + (workspace_width - window_width) // 2
                center_y = workspace_y + (workspace_height - window_height) // 2
                return center_x, center_y
            case _:
                return None

    def snap_window(self, direction: str, margin: int = 15):
        workspace = self.window_manager.workspace

        if not self.window_manager.is_floating_window:
            self.window_manager.move_nonfloat_wingow(direction=direction)
            logging.info(f"Not floating window moved {direction}.")
            sys.exit(1)

        new_position = self.calculate_new_position(direction=direction, margin=margin)

        if new_position == "next_workspace":
            next_workspace = self.window_manager.get_next_workspace(
                direction=direction, current_workspace=workspace
            )
            if next_workspace:
                self.window_manager.move_window_to_workspace(
                    workspace_name=next_workspace
                )
                logging.info(f"Window moved to next workspace: {next_workspace}.")
            else:
                logging.warning("No next workspace available.")
        elif new_position:
            new_x, new_y = new_position
            self.window_manager.move_window_to_position(new_x, new_y)
            logging.info(f"Window snapped to {direction} with a margin of {margin}px.")
        else:
            logging.error(f"Unknown direction: {direction}")
            sys.exit(1)

    def run(self):
        parser = argparse.ArgumentParser(description="Snap floating windows in i3wm.")
        parser.add_argument(
            "direction",
            type=lambda x: Direction(x),
            choices=list(Direction),
            help="Snapping direction.",
        )
        parser.add_argument(
            "-m",
            "--margin",
            type=int,
            default=15,
            help="Margin from the edge in pixels.",
        )
        args = parser.parse_args()
        self.snap_window(args.direction, args.margin)


if __name__ == "__main__":
    snapper = I3Snapper()
    snapper.run()
