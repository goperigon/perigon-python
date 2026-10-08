"""CI environment validation for integration tests."""
import os


def test_perigon_api_key_format():
    """Validate that PERIGON_API_KEY follows the expected sk-* convention."""
    api_key = os.environ.get("PERIGON_API_KEY", "")
    assert api_key.startswith("sk-"), (
        f"Expected PERIGON_API_KEY to start with 'sk-', got: {api_key}"
    )
