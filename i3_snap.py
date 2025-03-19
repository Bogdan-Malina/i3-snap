#!/usr/bin/env python

import argparse
import logging
import sys
from i3ipc import Connection


class I3Snapper:
    def __init__(self):
        self.i3 = Connection()
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    def __get_active_window(self):
        window = self.i3.get_tree().find_focused()
        workspace = window.workspace() if window else None
        return window, workspace

    def __is_valid_floating_window(self, window):
        return window and window.floating == "user_on"

    def __get_workspace_dimensions(self, workspace):
        return (
            workspace.rect.x,
            workspace.rect.y,
            workspace.rect.width,
            workspace.rect.height,
        )

    def __calculate_new_position(self, direction: str, window, workspace, margin: int):
        workspace_x, workspace_y, workspace_width, workspace_height = (
            self.__get_workspace_dimensions(workspace)
        )

        logging.info(f"Current window position: x={window.rect.x}, y={window.rect.y}")
        logging.info(
            f"Workspace dimensions: x={workspace_x}, y={workspace_y}, "
            f"width={workspace_width}, height={workspace_height}"
        )

        match direction:
            case "l":
                return workspace_x + margin, max(workspace_y + margin, window.rect.y)
            case "r":
                return workspace_x + workspace_width - window.rect.width - margin, max(
                    workspace_y + margin, window.rect.y
                )
            case "t":
                return max(workspace_x + margin, window.rect.x), workspace_y + margin
            case "b":
                return max(
                    workspace_x + margin, window.rect.x
                ), workspace_y + workspace_height - window.rect.height - margin
            case _:
                return None

    def snap_window(self, direction: str, margin: int = 15):
        window, workspace = self.__get_active_window()

        if not window or not workspace:
            logging.error("No active window or workspace found.")
            sys.exit(1)

        if not self.__is_valid_floating_window(window):
            logging.warning("Window is not floating. Snapping not performed.")
            sys.exit(1)

        new_position = self.__calculate_new_position(
            direction, window, workspace, margin
        )

        if new_position:
            new_x, new_y = new_position
            window.command(f"move position {new_x} {new_y}")
            logging.info(f"Window snapped to {direction} with a margin of {margin}px.")
        else:
            logging.error(f"Unknown direction: {direction}")
            sys.exit(1)

    def run(self):
        parser = argparse.ArgumentParser(description="Snap floating windows in i3wm.")
        parser.add_argument(
            "direction", choices=["t", "b", "l", "r"], help="Snapping direction."
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
