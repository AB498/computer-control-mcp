#!/usr/bin/env python3
"""
Computer Control MCP - Core Implementation
A compact ModelContextProtocol server that provides computer control capabilities
using PyAutoGUI for mouse/keyboard control.
"""

import json
import sys
import time
import os
from typing import Dict, Any, List, Optional, Union, Callable
import base64
from io import BytesIO
import re
from difflib import SequenceMatcher
import asyncio

# --- Auto-install dependencies if needed ---
try:
    import pyautogui
    from mcp.server.fastmcp import FastMCP, Image
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import PIL.Image
    import pygetwindow as gw
except ImportError:
    print("Installing required dependencies...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "mcp[cli]", "watchdog", "pillow", "pygetwindow"])
    import pyautogui
    from mcp.server.fastmcp import FastMCP, Image
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import PIL.Image
    import pygetwindow as gw

DEBUG = True  # Set to False in production
RELOAD_ENABLED = True  # Set to False to disable auto-reload

# Create FastMCP server instance at module level
mcp = FastMCP("ComputerControlMCP", version="1.0.0")

def log(message: str) -> None:
    """Log a message to stderr."""
    print(f"STDOUT: {message}", file=sys.stderr)

# --- MCP Function Handlers ---

@mcp.tool()
def hello_world(name: str) -> str:
    """Simple hello world function to test MCP functionality."""
    return f"Hello, {name}! Welcome to the Model Context Protocol."

@mcp.tool()
def click_screen(x: int, y: int) -> str:
    """Click at the specified screen coordinates."""
    try:
        pyautogui.click(x=x, y=y)
        return f"Successfully clicked at coordinates ({x}, {y})"
    except Exception as e:
        return f"Error clicking at coordinates ({x}, {y}): {str(e)}"

@mcp.tool()
def get_screen_size() -> Dict[str, Any]:
    """Get the current screen resolution."""
    try:
        width, height = pyautogui.size()
        return {
            "width": width,
            "height": height,
            "message": f"Screen size: {width}x{height}"
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": f"Error getting screen size: {str(e)}"
        }

@mcp.tool()
def type_text(text: str) -> str:
    """Type the specified text at the current cursor position."""
    try:
        pyautogui.typewrite(text)
        return f"Successfully typed text: {text}"
    except Exception as e:
        return f"Error typing text: {str(e)}"

@mcp.tool()
def take_screenshot(mode: str = "all_windows", title_pattern: str = None, use_regex: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Take screenshots based on the specified mode and return both images and window information.

    Args:
        mode: One of "all_windows" (default), "single_window", "whole_screen"
        title_pattern: Required when mode is "single_window", pattern to match window title
        use_regex: If True, treat the pattern as a regex, otherwise use fuzzy matching

    Returns:
        Dictionary or list of dictionaries containing window info and screenshot image
    """
    try:
        # Helper function to convert PIL Image to MCP Image
        def pil_to_mcp_image(pil_img):
            img_byte_arr = BytesIO()
            pil_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return Image(data=img_byte_arr.getvalue(), format="png")

        # Helper function to create error image
        def create_error_image():
            error_img = PIL.Image.new('RGB', (100, 50), color='red')
            return pil_to_mcp_image(error_img)

        # Helper function to get window info
        def get_window_info(window):
            return {
                "title": window.title,
                "left": window.left,
                "top": window.top,
                "width": window.width,
                "height": window.height,
                "is_active": window.isActive,
                "is_visible": window.visible,
                "is_minimized": window.isMinimized,
                "is_maximized": window.isMaximized
            }

        # Get all windows
        windows = gw.getAllWindows()

        if mode == "whole_screen":
            # Take screenshot of the entire screen
            screenshot = pyautogui.screenshot()
            width, height = pyautogui.size()
            return {
                "type": "whole_screen",
                "width": width,
                "height": height,
                "image": pil_to_mcp_image(screenshot)
            }

        elif mode == "single_window":
            if not title_pattern:
                log("title_pattern is required when mode is 'single_window'")
                return {
                    "error": "title_pattern is required when mode is 'single_window'",
                    "image": create_error_image()
                }

            # Find matching window
            matched_window = None
            best_match_ratio = 0

            for window in windows:
                if not window.title:
                    continue

                if use_regex:
                    # Use regex matching
                    if re.search(title_pattern, window.title, re.IGNORECASE):
                        matched_window = window
                        break
                else:
                    # Use fuzzy matching
                    match_ratio = SequenceMatcher(None, title_pattern.lower(), window.title.lower()).ratio()
                    if match_ratio > best_match_ratio and match_ratio > 0.6:  # Threshold for fuzzy matching
                        best_match_ratio = match_ratio
                        matched_window = window

            if not matched_window:
                log(f"No window found matching pattern: {title_pattern}")
                return {
                    "error": f"No window found matching pattern: {title_pattern}",
                    "image": create_error_image()
                }

            # Take screenshot of the specific window
            screenshot = pyautogui.screenshot(region=(
                matched_window.left,
                matched_window.top,
                matched_window.width,
                matched_window.height
            ))

            return {
                "type": "single_window",
                "window_info": get_window_info(matched_window),
                "image": pil_to_mcp_image(screenshot)
            }

        elif mode == "all_windows":
            # Take screenshots of all windows
            results = []
            for window in windows:
                if window.title and window.visible and not window.isMinimized:
                    try:
                        screenshot = pyautogui.screenshot(region=(
                            window.left,
                            window.top,
                            window.width,
                            window.height
                        ))
                        results.append({
                            "type": "window",
                            "window_info": get_window_info(window),
                            "image": pil_to_mcp_image(screenshot)
                        })
                    except Exception as e:
                        log(f"Error taking screenshot of window '{window.title}': {str(e)}")
                        results.append({
                            "type": "window",
                            "window_info": get_window_info(window),
                            "error": str(e),
                            "image": create_error_image()
                        })

            return results

        else:
            log(f"Invalid mode: {mode}. Must be one of 'all_windows', 'single_window', 'whole_screen'")
            return {
                "error": f"Invalid mode: {mode}. Must be one of 'all_windows', 'single_window', 'whole_screen'",
                "image": create_error_image()
            }

    except Exception as e:
        log(f"Error taking screenshot: {str(e)}")
        return {
            "error": str(e),
            "image": create_error_image()
        }

@mcp.tool()
def move_mouse(x: int, y: int) -> str:
    """Move the mouse to the specified screen coordinates."""
    try:
        pyautogui.moveTo(x=x, y=y)
        return f"Successfully moved mouse to coordinates ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse to coordinates ({x}, {y}): {str(e)}"

@mcp.tool()
async def drag_mouse(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5) -> str:
    """
    Drag the mouse from one position to another.

    Args:
        from_x: Starting X coordinate
        from_y: Starting Y coordinate
        to_x: Ending X coordinate
        to_y: Ending Y coordinate
        duration: Duration of the drag in seconds (default: 0.5)

    Returns:
        Success or error message
    """
    try:
        # First move to the starting position
        pyautogui.moveTo(x=from_x, y=from_y)
        # Then drag to the destination
        log('starting drag')
        await asyncio.to_thread(pyautogui.dragTo, x=to_x, y=to_y, duration=duration)
        log('done drag')
        return f"Successfully dragged from ({from_x}, {from_y}) to ({to_x}, {to_y})"
    except Exception as e:
        return f"Error dragging from ({from_x}, {from_y}) to ({to_x}, {to_y}): {str(e)}"

@mcp.tool()
def press_key(key: str) -> str:
    """Press the specified keyboard key."""
    try:
        pyautogui.press(key)
        return f"Successfully pressed key: {key}"
    except Exception as e:
        return f"Error pressing key {key}: {str(e)}"

@mcp.tool()
def list_windows() -> List[Dict[str, Any]]:
    """List all open windows on the system."""
    try:
        windows = gw.getAllWindows()
        result = []
        for window in windows:
            if window.title:  # Only include windows with titles
                result.append({
                    "title": window.title,
                    "left": window.left,
                    "top": window.top,
                    "width": window.width,
                    "height": window.height,
                    "is_active": window.isActive,
                    "is_visible": window.visible,
                    "is_minimized": window.isMinimized,
                    "is_maximized": window.isMaximized
                })
        return result
    except Exception as e:
        log(f"Error listing windows: {str(e)}")
        return [{"error": str(e)}]

@mcp.tool()
def activate_window(title_pattern: str, use_regex: bool = False) -> str:
    """
    Activate a window (bring it to the foreground) by matching its title.

    Args:
        title_pattern: Pattern to match window title
        use_regex: If True, treat the pattern as a regex, otherwise use fuzzy matching

    Returns:
        Success or error message
    """
    try:
        # Get all windows
        windows = gw.getAllWindows()

        # Find matching window
        matched_window = None
        best_match_ratio = 0

        for window in windows:
            if not window.title:
                continue

            if use_regex:
                # Use regex matching
                if re.search(title_pattern, window.title, re.IGNORECASE):
                    matched_window = window
                    break
            else:
                # Use fuzzy matching
                match_ratio = SequenceMatcher(None, title_pattern.lower(), window.title.lower()).ratio()
                if match_ratio > best_match_ratio and match_ratio > 0.6:  # Threshold for fuzzy matching
                    best_match_ratio = match_ratio
                    matched_window = window

        if not matched_window:
            log(f"No window found matching pattern: {title_pattern}")
            return f"Error: No window found matching pattern: {title_pattern}"

        # Activate the window
        matched_window.activate()

        return f"Successfully activated window: '{matched_window.title}'"
    except Exception as e:
        log(f"Error activating window: {str(e)}")
        return f"Error activating window: {str(e)}"

def main():
    """Main entry point for the MCP server."""
    # Set up PyAutoGUI safety features
    pyautogui.FAILSAFE = True

    # Set up auto-reload if enabled
    if RELOAD_ENABLED:
        log("Auto-reload enabled. Server will restart when code changes are detected.")
        # Set up file watcher for auto-reload
        class FileChangeHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path.endswith('.py'):
                    log(f"Detected change in {event.src_path}. Restarting server...")
                    os._exit(0)  # Exit with success code to trigger restart

        observer = Observer()
        observer.schedule(FileChangeHandler(), path='.', recursive=False)
        observer.start()

    try:
        # Run the server
        log("Starting FastMCP server...")
        mcp.run()

    except KeyboardInterrupt:
        log("Server shutting down...")
        if RELOAD_ENABLED:
            observer.stop()
            observer.join()
    except Exception as e:
        log(f"Error: {str(e)}")
        if RELOAD_ENABLED:
            observer.stop()
            observer.join()

if __name__ == "__main__":
    main()
