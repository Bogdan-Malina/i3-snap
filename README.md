
# i3-snap

`i3-snap` is a script for managing window positions in i3wm. It allows snapping floating windows to screen edges, centering them, or moving them between workspaces.

## Features

- Move floating windows left, right, up, down, or center them.
- Automatically move a window to the next workspace when reaching the edge.
- Supports setting a margin from the screen edges.
- Works with non-floating windows using standard i3 commands.

## Installation

### Requirements

- `python` (>=3.6)
- `i3ipc`

Install dependencies:

```sh
pip install i3ipc
```

Save `i3-snap` to a convenient location and make it executable:

```sh
chmod +x i3-snap.py
```

## Usage

```sh
./i3-snap.py <direction> [-m MARGIN]
```

### Arguments

- `<direction>` – snapping direction (`left`, `right`, `up`, `down`, `center`).
- `-m`, `--margin` – margin from the edge (default: 15px).

### Examples

Snap a window to the left edge:

```sh
./i3-snap.py left
```

Snap to the right edge with a 30px margin:

```sh
./i3-snap.py right -m 30
```

## Automation

Add key bindings to `~/.config/i3/config`:

```
bindsym $mod+Left exec ~/scripts/i3-snap.py left
bindsym $mod+Right exec ~/scripts/i3-snap.py right
bindsym $mod+Up exec ~/scripts/i3-snap.py up
bindsym $mod+Down exec ~/scripts/i3-snap.py down
```
