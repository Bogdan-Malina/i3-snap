# i3-snap

A Python script for snapping floating windows in i3 window manager. It allows quick placement of floating windows into predefined positions (left, right, top, bottom) while maintaining customizable margins.

## Installation

Ensure you have `i3ipc` installed:

```sh
pip install i3ipc
```

Clone the repository:

```sh
git clone https://github.com/Bogdan-Malina/i3-snap.git
cd i3-snap
```

## Usage

Run the script with the desired snapping direction:

```sh
./i3_snap.py <direction> [-m MARGIN]
```

### Arguments

- `<direction>`: `t` (top), `b` (bottom), `l` (left), `r` (right).
- `-m, --margin` (optional): Margin in pixels (default: 15).

### Examples

Snap the active floating window to the left:

```sh
./i3_snap.py l
```

Snap to the right with a custom margin:

```sh
./i3_snap.py r -m 20
```

## Notes

- The script works only with floating windows.
- Ensure you have `i3` and `i3ipc` installed before running.
