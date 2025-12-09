import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from computer_control_mcp.core import take_screenshot, _wgc_screenshot
import tempfile
import os

def test_wgc_screenshot():
    """Test WGC screenshot functionality"""
    print("Testing WGC screenshot functionality...")
    
    # Test if WGC is available
    try:
        from windows_capture import WindowsCapture
        wgc_available = True
        print("Windows Graphics Capture API is available")
    except ImportError:
        wgc_available = False
        print("Windows Graphics Capture API is not available")
    
    if wgc_available:
        # Try to capture the desktop window (usually available)
        try:
            # Get the first available window title
            import pywinctl as gw
            windows = gw.getAllWindows()
            if windows:
                window_title = windows[0].title
                print(f"Attempting to capture window: {window_title}")
                
                # Test the internal WGC function
                result = _wgc_screenshot(window_title)
                if result:
                    image_bytes, width, height = result
                    print(f"Successfully captured window: {width}x{height}")
                    
                    # Save to a temporary file to verify
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        tmp.write(image_bytes)
                        print(f"Saved test screenshot to: {tmp.name}")
                        # Clean up
                        os.unlink(tmp.name)
                else:
                    print("Failed to capture window with WGC")
            else:
                print("No windows found to capture")
        except Exception as e:
            print(f"Error during WGC test: {e}")
    else:
        print("Skipping WGC tests as the API is not available")

def test_take_screenshot_with_wgc():
    """Test take_screenshot function with WGC enabled"""
    print("\nTesting take_screenshot with WGC...")
    
    try:
        # Test with WGC enabled (will fall back if not available)
        result = take_screenshot(use_wgc=True)
        print("take_screenshot with WGC completed")
        print(f"Result type: {type(result)}")
    except Exception as e:
        print(f"Error in take_screenshot with WGC: {e}")

if __name__ == "__main__":
    test_wgc_screenshot()
    test_take_screenshot_with_wgc()