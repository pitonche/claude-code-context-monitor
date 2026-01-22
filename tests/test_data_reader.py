"""Unit tests for data_reader module"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_reader import extract_tokens_from_entry


def test_token_extraction_complete():
    """Test token extraction with all token types"""
    entry = {
        "type": "assistant",
        "message": {
            "usage": {
                "input_tokens": 1000,
                "output_tokens": 500,
                "cache_read_input_tokens": 200,
                "cache_creation": {
                    "ephemeral_5m_input_tokens": 100
                }
            }
        }
    }

    tokens = extract_tokens_from_entry(entry)
    expected = 1000 + 500 + 200 + 100  # 1800 total

    assert tokens == expected, f"Expected {expected} tokens, got {tokens}"
    print("[PASS] test_token_extraction_complete passed")


def test_token_extraction_minimal():
    """Test token extraction with only basic tokens"""
    entry = {
        "type": "assistant",
        "message": {
            "usage": {
                "input_tokens": 500,
                "output_tokens": 250,
            }
        }
    }

    tokens = extract_tokens_from_entry(entry)
    expected = 500 + 250  # 750 total

    assert tokens == expected, f"Expected {expected} tokens, got {tokens}"
    print("[PASS] test_token_extraction_minimal passed")


def test_token_extraction_non_assistant():
    """Test that non-assistant entries return 0 tokens"""
    entry = {
        "type": "user",
        "message": {
            "usage": {
                "input_tokens": 1000,
                "output_tokens": 500,
            }
        }
    }

    tokens = extract_tokens_from_entry(entry)
    assert tokens == 0, f"Expected 0 tokens for user entry, got {tokens}"
    print("[PASS] test_token_extraction_non_assistant passed")


def test_token_extraction_missing_fields():
    """Test graceful handling of missing fields"""
    entry = {
        "type": "assistant",
        "message": {
            "usage": {}
        }
    }

    tokens = extract_tokens_from_entry(entry)
    assert tokens == 0, f"Expected 0 tokens for empty usage, got {tokens}"
    print("[PASS] test_token_extraction_missing_fields passed")


def test_token_extraction_cache_only():
    """Test extraction with cache tokens only"""
    entry = {
        "type": "assistant",
        "message": {
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_input_tokens": 1500,
                "cache_creation": {
                    "ephemeral_5m_input_tokens": 500
                }
            }
        }
    }

    tokens = extract_tokens_from_entry(entry)
    expected = 1500 + 500  # 2000 total

    assert tokens == expected, f"Expected {expected} tokens, got {tokens}"
    print("[PASS] test_token_extraction_cache_only passed")


if __name__ == "__main__":
    print("Running data_reader tests...\n")

    try:
        test_token_extraction_complete()
        test_token_extraction_minimal()
        test_token_extraction_non_assistant()
        test_token_extraction_missing_fields()
        test_token_extraction_cache_only()

        print("\n[PASS] All tests passed!")
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Error running tests: {e}")
        sys.exit(1)
