"""Process monitoring for Claude Code instances"""
import logging

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from .config import Config
except ImportError:
    from config import Config

class ProcessMonitor:
    """Monitors Claude Code process lifecycle"""

    def __init__(self, process_name: str = "claude.exe"):
        self.process_name = process_name
        self.enabled = PSUTIL_AVAILABLE and Config.AUTO_CLOSE_ENABLED

        if not PSUTIL_AVAILABLE:
            logging.warning(
                "psutil not available - auto-close disabled. "
                "Install with: pip install psutil"
            )

    def has_running_instances(self) -> bool:
        """Check if any Claude Code processes are running"""
        if not self.enabled:
            return True  # Assume running if monitoring disabled

        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == self.process_name:
                    return True
            return False
        except (psutil.Error, Exception) as e:
            logging.warning(f"Process check failed: {e}")
            return True  # Fail-safe: assume running on error

    def should_auto_close(self) -> bool:
        """Determine if monitor should auto-close"""
        if not self.enabled:
            return False
        return not self.has_running_instances()
