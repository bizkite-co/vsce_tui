# vsce_tui

A TUI tool for managing VS Code extensions.

## Installation

```bash
pip install vsce_tui
```

## Usage

```bash
code --list-extensions | vsce_tui
```

Use the arrow keys (or 'j' and 'k') to navigate, 't' to toggle extension status, and 'q' to quit and apply changes.

## Development

```bash
git clone https://github.com/bizkite-co/vsce_tui # Replace with your repo
cd vsce_tui
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
.venv\Scripts\activate  # On Windows
pip install -e .