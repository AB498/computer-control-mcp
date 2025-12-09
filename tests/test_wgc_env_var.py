import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from computer_control_mcp.core import _should_use_wgc_by_default
import os

def test_wgc_env_var():
    """Test the WGC environment variable pattern matching"""
    print("Testing WGC environment variable pattern matching...")
    
    # Test with no environment variable set
    if 'COMPUTER_CONTROL_MCP_WGC_PATTERNS' in os.environ:
        del os.environ['COMPUTER_CONTROL_MCP_WGC_PATTERNS']
    
    result = _should_use_wgc_by_default("OBS Studio")
    print(f"Without env var - 'OBS Studio': {result} (expected: False)")
    
    # Test with environment variable set
    os.environ['COMPUTER_CONTROL_MCP_WGC_PATTERNS'] = "obs, discord, game"
    
    test_cases = [
        ("OBS Studio", True),
        ("Discord", True),
        ("My Game", True),
        ("Notepad", False),
        ("Google Chrome", False),
        ("obs studio", True),  # Test case insensitivity
        ("DISCORD APP", True),  # Test case insensitivity
    ]
    
    for window_title, expected in test_cases:
        result = _should_use_wgc_by_default(window_title)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{window_title}': {result} (expected: {expected})")
    
    # Clean up
    if 'COMPUTER_CONTROL_MCP_WGC_PATTERNS' in os.environ:
        del os.environ['COMPUTER_CONTROL_MCP_WGC_PATTERNS']

if __name__ == "__main__":
    test_wgc_env_var()