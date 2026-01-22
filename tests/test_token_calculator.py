"""Unit tests for token_calculator module"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from token_calculator import TokenCalculator
from config import Config


def test_max5_percentage():
    """Test percentage calculation for Max5 plan"""
    calc = TokenCalculator(plan_limit=88000)
    total, pct = calc.calculate_usage(75120)

    # Check percentage is approximately 85.36%
    assert abs(pct - 85.36) < 0.01, f"Expected ~85.36%, got {pct:.2f}%"
    assert total == 75120
    print("[PASS] test_max5_percentage passed")


def test_color_thresholds():
    """Test color determination at different usage levels"""
    calc = TokenCalculator()

    # Test each threshold
    assert calc.get_color_for_percentage(50) == Config.COLOR_SAFE, "50% should be green"
    assert calc.get_color_for_percentage(80) == Config.COLOR_WARNING, "80% should be amber"
    assert calc.get_color_for_percentage(93) == Config.COLOR_DANGER, "93% should be orange"
    assert calc.get_color_for_percentage(97) == Config.COLOR_CRITICAL, "97% should be red"

    print("[PASS] test_color_thresholds passed")


def test_compress_threshold():
    """Test compress button enable threshold"""
    calc = TokenCalculator()

    assert not calc.should_enable_compress(50), "Should be disabled at 50%"
    assert not calc.should_enable_compress(69.9), "Should be disabled at 69.9%"
    assert calc.should_enable_compress(70), "Should be enabled at 70%"
    assert calc.should_enable_compress(85), "Should be enabled at 85%"

    print("[PASS] test_compress_threshold passed")


def test_get_usage_data():
    """Test complete usage data retrieval"""
    calc = TokenCalculator(plan_limit=88000)
    data = calc.get_usage_data(44000)  # 50% usage

    assert data["tokens"] == 44000
    assert abs(data["percentage"] - 50.0) < 0.01
    assert data["color"] == Config.COLOR_SAFE
    assert not data["compress_enabled"]
    assert data["plan_limit"] == 88000

    print("[PASS] test_get_usage_data passed")


if __name__ == "__main__":
    print("Running token_calculator tests...\n")

    try:
        test_max5_percentage()
        test_color_thresholds()
        test_compress_threshold()
        test_get_usage_data()

        print("\n[SUCCESS] All tests passed!")
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error running tests: {e}")
        sys.exit(1)
