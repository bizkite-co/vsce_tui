# vsce-ext-manager.py (working name)

import csv
import subprocess
import os
import sys
import termios
import tty

# --- Configuration ---
CSV_FILE = os.path.expanduser("~/.config/vsce-ext-manager.csv")  # Linux-specific path

# --- Data Model ---
def load_extensions():
    """Loads extensions from the CSV file or creates it if it doesn't exist."""
    extensions = []
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)  # Force deletion of the CSV file
    # Get extensions from stdin (piped from `code --list-extensions`)
    ext_list_output = subprocess.check_output(
        "code-insiders --list-extensions", shell=True, text=True  # Use code-insiders
    ).strip()

    for line in ext_list_output.split('\n'):
        if "." in line:  # Skip lines that don't look like extension IDs
            extensions.append({'extension_id': line, 'status': 'Installed', 'changed': False})

    save_extensions(extensions) # Save to create initial file
    return extensions

def save_extensions(extensions):
    """Saves the extensions to the CSV file."""
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['extension_id', 'status', 'changed']  # Include 'changed'
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(extensions)

# --- TUI ---
def getch():
    """Reads a single character from stdin without echoing to the screen."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def display_tui(extensions):
    """Displays the text-based UI and handles user input."""
    current_index = 0
    viewport_start = 0
    terminal_height = os.get_terminal_size().lines
    viewport_size = terminal_height - 3  # Leave space for header and prompt

    if sys.stdin.isatty():  # Interactive mode
        while True:
            # Clear the screen (cross-platform)
            os.system('cls' if os.name == 'nt' else 'clear')

            print("VS Code Extension Manager (Press 't' to toggle, 'q' to quit and apply, 'x' to quit without applying)")

            # Display only the extensions within the viewport
            for i in range(viewport_start, min(viewport_start + viewport_size, len(extensions))):
                ext = extensions[i]
                status_char = "I" if ext['status'] == 'Installed' else "U"
                marker = ">" if i == current_index else " "
                print(f"{marker} [{status_char}] {ext['extension_id']}")

            key = getch().lower()

            if key == 'q':
                apply_changes(extensions)  # Apply changes before quitting
                break
            elif key == 'x':
                break  # Quit without applying changes
            elif key == 't':
                if extensions[current_index]['status'] == 'Installed':
                    extensions[current_index]['status'] = 'Uninstalled'
                else:
                    extensions[current_index]['status'] = 'Installed'
                extensions[current_index]['changed'] = True  # Mark as changed
            elif key == 'j': # Down
                current_index = min(current_index + 1, len(extensions) - 1)
                # Adjust viewport if necessary
                if current_index >= viewport_start + viewport_size:
                    viewport_start += 1
            elif key == 'k': # Up
                current_index = max(current_index - 1, 0)
                # Adjust viewport if necessary
                if current_index < viewport_start:
                    viewport_start -= 1
            elif key == '\x1b':  # Escape sequence (for arrow keys)
                next_char = getch()
                if next_char == '[':
                    third_char = getch()
                    if third_char == 'A':  # Up arrow
                        current_index = max(current_index - 1, 0)
                        if current_index < viewport_start:
                            viewport_start -= 1
                    elif third_char == 'B':  # Down arrow
                        current_index = min(current_index + 1, len(extensions) - 1)
                        if current_index >= viewport_start + viewport_size:
                            viewport_start += 1
                    # Ignore right/left arrows (C and D)

    else:  # Piped input mode - just display once
        print("VS Code Extension Manager (Extensions loaded from pipe)")
        for i, ext in enumerate(extensions):
            status_char = "I" if ext['status'] == 'Installed' else "U"
            print(f"  [{status_char}] {ext['extension_id']}")
        print("Changes will be applied when you run the script interactively.")


# --- VS Code Interaction ---
def apply_changes(extensions):
    """Applies the changes (install/uninstall) to VS Code."""
    for ext in extensions:
        if ext['changed']:  # Only process changed extensions
            if ext['status'] == 'Installed':
                print(f"Installing {ext['extension_id']}...")
                subprocess.run(['code-insiders', '--install-extension', ext['extension_id']], check=False) # Use code-insiders
            #  Do nothing if status is 'Uninstalled' - just keep it in the CSV

# --- Main ---
def main():
    """Main function."""
    extensions = load_extensions()
    display_tui(extensions)
    save_extensions(extensions) # Always save, even if no changes are applied
    # apply_changes(extensions) is now called within display_tui when 'q' is pressed

if __name__ == "__main__":
    main()