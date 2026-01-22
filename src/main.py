"""Main entry point for Claude Code Odometer Monitor"""
import tkinter as tk
import json
from pathlib import Path
try:
    from .config import Config
    from .ui_widget import OdometerWidget
    from .compress_handler import create_compress_handler
except ImportError:
    from config import Config
    from ui_widget import OdometerWidget
    from compress_handler import create_compress_handler


def load_window_position(root: tk.Tk) -> bool:
    """
    Load saved window position from config file.

    Args:
        root: tkinter root window

    Returns:
        True if position was loaded successfully
    """
    if not Config.POSITION_FILE.exists():
        return False

    try:
        with open(Config.POSITION_FILE, "r") as f:
            data = json.load(f)

        x = data.get("x")
        y = data.get("y")

        if x is not None and y is not None:
            # Validate position is on screen
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            if 0 <= x < screen_width and 0 <= y < screen_height:
                root.geometry(f"+{x}+{y}")
                return True

    except (json.JSONDecodeError, OSError):
        pass

    return False


def save_window_position(root: tk.Tk):
    """
    Save current window position to config file.

    Args:
        root: tkinter root window
    """
    try:
        # Ensure config directory exists
        Config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        # Get current position
        x = root.winfo_x()
        y = root.winfo_y()

        # Save to file
        data = {"x": x, "y": y}
        with open(Config.POSITION_FILE, "w") as f:
            json.dump(data, f)

    except OSError:
        # Silently fail if can't save position
        pass


def save_and_quit(root: tk.Tk):
    """
    Save window position and quit application.

    Args:
        root: tkinter root window
    """
    save_window_position(root)
    root.quit()


def main():
    """Main application entry point"""

    # Create root window
    root = tk.Tk()

    # Initialize odometer widget
    odometer = OdometerWidget(root)

    # Initialize compress handler
    compress_handler = create_compress_handler(root)
    odometer.set_compress_callback(compress_handler.execute_compress)

    # Load saved window position (or center if first run)
    if not load_window_position(root):
        # Center window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - Config.WINDOW_WIDTH) // 2
        y = (screen_height - Config.WINDOW_HEIGHT) // 2
        root.geometry(f"+{x}+{y}")

    # Start refresh loop
    def refresh():
        odometer.update_display()
        root.after(Config.REFRESH_INTERVAL_MS, refresh)

    # Initial update
    odometer.update_display()

    # Schedule first refresh
    root.after(Config.REFRESH_INTERVAL_MS, refresh)

    # Save position on close
    root.protocol("WM_DELETE_WINDOW", lambda: save_and_quit(root))

    # Run main loop
    root.mainloop()


if __name__ == "__main__":
    main()
