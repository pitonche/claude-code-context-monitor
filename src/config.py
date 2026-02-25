"""Configuration constants for Claude Code Odometer Monitor"""
from pathlib import Path


MODEL_INFO = {
    "claude-opus-4-6":            {"name": "Opus 4.6",   "limit": 200000},
    "claude-opus-4-5-20251101":   {"name": "Opus 4.5",   "limit": 200000},
    "claude-sonnet-4-6":          {"name": "Sonnet 4.6",  "limit": 200000},
    "claude-sonnet-4-5-20250929": {"name": "Sonnet 4.5",  "limit": 200000},
    "claude-haiku-4-5-20251001":  {"name": "Haiku 4.5",   "limit": 200000},
}

DEFAULT_MODEL_NAME = "Unknown"
DEFAULT_MODEL_LIMIT = 200000


class Config:
    """Main configuration for the odometer monitor"""

    # Plan settings (defaults, overridden dynamically)
    PLAN_LIMIT = DEFAULT_MODEL_LIMIT
    PLAN_NAME = DEFAULT_MODEL_NAME

    # Polling settings
    REFRESH_INTERVAL_MS = 2000  # 2 seconds

    # Startup delay settings
    STARTUP_DELAY_MS = 1500  # Initial delay before first check
    STARTUP_MAX_RETRIES = 10  # Maximum retry attempts
    STARTUP_RETRY_INTERVAL_MS = 500  # 500ms between retries

    # Claude Code directories
    CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

    # Window settings
    WINDOW_WIDTH = 420
    WINDOW_HEIGHT = 240  # Increased to accommodate project name label
    ALWAYS_ON_TOP = True

    # Color thresholds and values
    COLOR_SAFE = "#28A745"      # Green (0-70%)
    COLOR_WARNING = "#FFC107"   # Amber (70-90%)
    COLOR_DANGER = "#FF6B35"    # Orange (90-95%)
    COLOR_CRITICAL = "#DC3545"  # Red (95-100%)
    COLOR_INACTIVE = "#808080"  # Gray (no session)

    # Theme colors
    BG_COLOR = "#2C2C2C"       # Dark background
    TEXT_COLOR = "#FFFFFF"      # White text
    TEXT_SECONDARY = "#AAAAAA"  # Gray text

    # Compress button settings
    COMPRESS_THRESHOLD = 70.0  # Enable button at 70% usage

    # Auto-close settings
    AUTO_CLOSE_ENABLED = True  # Enable auto-close when Claude Code exits
    AUTO_CLOSE_PROCESS_NAME = "claude.exe"  # Windows process name
    AUTO_CLOSE_CHECK_INTERVAL_MS = 5000  # Check every 5 seconds
    AUTO_CLOSE_GRACE_PERIOD_MS = 10000  # Wait 10s after last process exits

    # Persistence
    CONFIG_DIR = Path.home() / ".claude-monitor"
    POSITION_FILE = CONFIG_DIR / "position.json"
