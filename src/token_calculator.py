"""Token calculation and percentage logic"""
try:
    from .config import Config
except ImportError:
    from config import Config


class TokenCalculator:
    """Handles token usage calculations and color determination"""

    def __init__(self, plan_limit: int = Config.PLAN_LIMIT):
        """
        Initialize calculator with plan limit.

        Args:
            plan_limit: Maximum tokens for the plan (default: Max5 = 88,000)
        """
        self.plan_limit = plan_limit

    def calculate_usage(self, total_tokens: int) -> tuple[int, float]:
        """
        Calculate usage percentage from total tokens.

        Args:
            total_tokens: Total token count

        Returns:
            Tuple of (total_tokens, percentage)
        """
        percentage = (total_tokens / self.plan_limit) * 100
        return total_tokens, percentage

    def get_color_for_percentage(self, pct: float) -> str:
        """
        Get color code based on usage percentage.

        Color mapping:
        - 0-70%: Green (safe)
        - 70-90%: Amber (warning)
        - 90-95%: Orange (danger)
        - 95-100%+: Red (critical)

        Args:
            pct: Usage percentage

        Returns:
            Hex color code string
        """
        if pct < 70:
            return Config.COLOR_SAFE
        elif pct < 90:
            return Config.COLOR_WARNING
        elif pct < 95:
            return Config.COLOR_DANGER
        else:
            return Config.COLOR_CRITICAL

    def should_enable_compress(self, pct: float) -> bool:
        """
        Determine if compress button should be enabled.

        Args:
            pct: Usage percentage

        Returns:
            True if percentage exceeds compress threshold (70%)
        """
        return pct >= Config.COMPRESS_THRESHOLD

    def get_usage_data(self, total_tokens: int) -> dict:
        """
        Get complete usage data for display.

        Args:
            total_tokens: Total token count

        Returns:
            Dictionary with keys: tokens, percentage, color, compress_enabled
        """
        tokens, pct = self.calculate_usage(total_tokens)
        color = self.get_color_for_percentage(pct)
        compress_enabled = self.should_enable_compress(pct)

        return {
            "tokens": tokens,
            "percentage": pct,
            "color": color,
            "compress_enabled": compress_enabled,
            "plan_limit": self.plan_limit,
        }
