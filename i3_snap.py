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

    def __calculate_new_position_and_size(
        self, direction: str, window, workspace, margin: int
    ):
        workspace_x, workspace_y, workspace_width, workspace_height = (
            self.__get_workspace_dimensions(workspace)
        )
        half_width = workspace_width // 2
        half_height = workspace_height // 2

        logging.info(
            f"Current window position: x={window.rect.x}, y={window.rect.y}, "
            f"width={window.rect.width}, height={window.rect.height}"
        )
        logging.info(
            f"Workspace dimensions: x={workspace_x}, y={workspace_y}, "
            f"width={workspace_width}, height={workspace_height}"
        )

        match direction:
            case "l":
                return (
                    workspace_x + margin,
                    workspace_y + margin,
                    half_width - 2 * margin,
                    workspace_height - 2 * margin,
                )
            case "r":
                return (
                    workspace_x + half_width + margin,
                    workspace_y + margin,
                    half_width - 2 * margin,
                    workspace_height - 2 * margin,
                )
            case "t":
                return (
                    workspace_x + margin,
                    workspace_y + margin,
                    workspace_width - 2 * margin,
                    half_height - 2 * margin,
                )
            case "b":
                return (
                    workspace_x + margin,
                    workspace_y + half_height + margin,
                    workspace_width - 2 * margin,
                    half_height - 2 * margin,
                )
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

        new_position_and_size = self.__calculate_new_position_and_size(
            direction, window, workspace, margin
        )

        if new_position_and_size:
            new_x, new_y, new_width, new_height = new_position_and_size
            window.command(f"move position {new_x} {new_y}")
            window.command(f"resize set {new_width} {new_height}")
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
