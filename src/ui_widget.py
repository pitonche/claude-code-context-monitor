"""Odometer UI widget using tkinter"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
try:
    from .config import Config, MODEL_INFO, DEFAULT_MODEL_NAME, DEFAULT_MODEL_LIMIT
    from .data_reader import get_current_usage, extract_project_name
    from .token_calculator import TokenCalculator
except ImportError:
    from config import Config, MODEL_INFO, DEFAULT_MODEL_NAME, DEFAULT_MODEL_LIMIT
    from data_reader import get_current_usage, extract_project_name
    from token_calculator import TokenCalculator


# Base sizes — the reference dimensions fonts were designed for
BASE_WIDTH = 280
BASE_HEIGHT = 160


class OdometerWidget:
    """Floating odometer widget displaying token usage"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.calculator = TokenCalculator()

        # Configure root window
        self.root.title("Context Monitor")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.BG_COLOR)
        self.root.minsize(200, 120)

        # Make window draggable
        self._drag_data = {"x": 0, "y": 0}
        self.root.bind("<Button-1>", self._on_drag_start)
        self.root.bind("<B1-Motion>", self._on_drag_motion)

        # Track resize
        self._last_width = Config.WINDOW_WIDTH
        self._last_height = Config.WINDOW_HEIGHT
        self.root.bind("<Configure>", self._on_resize)

        # Create UI elements
        self._create_widgets()

    def _scale(self, base_size: int) -> int:
        """Scale a font size based on current window dimensions relative to base."""
        w = self.root.winfo_width() or BASE_WIDTH
        h = self.root.winfo_height() or BASE_HEIGHT
        factor = min(w / BASE_WIDTH, h / BASE_HEIGHT)
        return max(int(base_size * factor), 6)

    def _on_resize(self, event):
        """Handle window resize — rescale fonts and progress bar."""
        if event.widget != self.root:
            return
        w, h = event.width, event.height
        if w == self._last_width and h == self._last_height:
            return
        self._last_width = w
        self._last_height = h
        self._rescale_ui(w, h)

    def _rescale_ui(self, w, h):
        """Rescale all UI elements to match current window size."""
        factor = min(w / BASE_WIDTH, h / BASE_HEIGHT)

        self.title_label.config(font=("Arial", max(int(10 * factor), 6)))
        self.project_label.config(font=("Arial", max(int(8 * factor), 6)))
        self.percentage_label.config(font=("Arial", max(int(36 * factor), 10), "bold"))
        self.token_label.config(font=("Arial", max(int(10 * factor), 6)))
        self.plan_label.config(font=("Arial", max(int(9 * factor), 6)))
        # Resize progress bar
        bar_w = w - 20
        bar_h = max(int(20 * factor), 8)
        self.progress_canvas.config(width=bar_w, height=bar_h)
        self.progress_canvas.coords(self.progress_bg, 0, 0, bar_w, bar_h)
        # Recalculate foreground width from current percentage
        pct_text = self.percentage_label.cget("text")
        try:
            pct = float(pct_text.replace("%", ""))
        except ValueError:
            pct = 0
        fg_w = int((pct / 100) * bar_w)
        fg_w = min(fg_w, bar_w)
        self.progress_canvas.coords(self.progress_fg, 0, 0, fg_w, bar_h)

    def _create_widgets(self):
        """Create all UI elements"""

        # Title label
        self.title_label = tk.Label(
            self.root,
            text="Context Monitor",
            font=("Arial", 10),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_SECONDARY,
        )
        self.title_label.pack(pady=(5, 0))

        # Project name label
        self.project_label = tk.Label(
            self.root,
            text="No active session",
            font=("Arial", 8),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_SECONDARY,
        )
        self.project_label.pack(pady=(0, 5))

        # Large percentage display
        self.percentage_label = tk.Label(
            self.root,
            text="0.0%",
            font=("Arial", 36, "bold"),
            bg=Config.BG_COLOR,
            fg=Config.COLOR_SAFE,
        )
        self.percentage_label.pack(pady=(0, 5))

        # Progress bar (using Canvas)
        self.progress_canvas = tk.Canvas(
            self.root,
            width=260,
            height=20,
            bg=Config.BG_COLOR,
            highlightthickness=0,
        )
        self.progress_canvas.pack(pady=(0, 5))

        # Progress bar background
        self.progress_bg = self.progress_canvas.create_rectangle(
            0, 0, 260, 20,
            fill="#444444",
            outline=""
        )

        # Progress bar foreground
        self.progress_fg = self.progress_canvas.create_rectangle(
            0, 0, 0, 20,
            fill=Config.COLOR_SAFE,
            outline=""
        )

        # Token count label
        self.token_label = tk.Label(
            self.root,
            text="0 / 200,000 tokens",
            font=("Arial", 10),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_COLOR,
        )
        self.token_label.pack()

        # Plan label
        self.plan_label = tk.Label(
            self.root,
            text=f"[{Config.PLAN_NAME}]",
            font=("Arial", 9),
            bg=Config.BG_COLOR,
            fg=Config.TEXT_SECONDARY,
        )
        self.plan_label.pack(pady=(0, 5))


    def _on_drag_start(self, event):
        """Handle drag start event"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag_motion(self, event):
        """Handle drag motion event"""
        x = self.root.winfo_x() + (event.x - self._drag_data["x"])
        y = self.root.winfo_y() + (event.y - self._drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def update_display(self):
        """Update display with current token usage"""
        total_tokens, session_path, model_id = get_current_usage()

        if session_path is None:
            self._show_no_session()
            return

        # Update model info dynamically
        if model_id and model_id in MODEL_INFO:
            info = MODEL_INFO[model_id]
            self.calculator.plan_limit = info["limit"]
            self.plan_label.config(text=f"[{info['name']}]")
        elif model_id:
            self.plan_label.config(text=f"[{model_id}]")

        # Extract and display project name
        project_name = extract_project_name(session_path)
        self.project_label.config(text=f"📁 {project_name}")

        # Get usage data
        usage_data = self.calculator.get_usage_data(total_tokens)

        # Update percentage label
        pct = usage_data["percentage"]
        color = usage_data["color"]
        self.percentage_label.config(
            text=f"{pct:.1f}%",
            fg=color
        )

        # Update progress bar using current window width
        w = self.root.winfo_width() or BASE_WIDTH
        h = self.root.winfo_height() or BASE_HEIGHT
        factor = min(w / BASE_WIDTH, h / BASE_HEIGHT)
        bar_w = w - 20
        bar_h = max(int(20 * factor), 8)
        self.progress_canvas.config(width=bar_w, height=bar_h)
        self.progress_canvas.coords(self.progress_bg, 0, 0, bar_w, bar_h)
        fg_w = int((pct / 100) * bar_w)
        fg_w = min(fg_w, bar_w)
        self.progress_canvas.coords(self.progress_fg, 0, 0, fg_w, bar_h)
        self.progress_canvas.itemconfig(self.progress_fg, fill=color)

        # Update token count label
        tokens = usage_data["tokens"]
        limit = usage_data["plan_limit"]
        self.token_label.config(
            text=f"{tokens:,} / {limit:,} tokens",
            fg=Config.TEXT_COLOR
        )

    def _show_no_session(self):
        """Show 'No active session' state"""
        self.project_label.config(text="No active session")

        self.percentage_label.config(
            text="--",
            fg=Config.COLOR_INACTIVE
        )

        # Reset progress bar
        self.progress_canvas.coords(self.progress_fg, 0, 0, 0, 20)

        self.token_label.config(
            text="Waiting for Claude Code...",
            fg=Config.TEXT_SECONDARY
        )

