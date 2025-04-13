#!/usr/bin/env python3
"""
Computer Control MCP - Core Implementation
A compact ModelContextProtocol server that provides computer control capabilities
using PyAutoGUI for mouse/keyboard control.
"""

import shutil
import sys
import os
from typing import Dict, Any, List, Optional, Tuple
from io import BytesIO
import re
import asyncio
import uuid
import datetime
from pathlib import Path
import tempfile

# --- Auto-install dependencies if needed ---
import pyautogui
from mcp.server.fastmcp import FastMCP, Image
import pygetwindow as gw
from fuzzywuzzy import fuzz, process

from rapidocr import RapidOCR
import cv2
from rapidocr_onnxruntime import RapidOCR, VisRes


DEBUG = True  # Set to False in production
RELOAD_ENABLED = True  # Set to False to disable auto-reload

# Create FastMCP server instance at module level
mcp = FastMCP("ComputerControlMCP", version="1.0.0")


def log(message: str) -> None:
    """Log a message to stderr."""
    print(f"STDOUT: {message}", file=sys.stderr)


def get_downloads_dir() -> Path:
    """Get the OS downloads directory."""
    if os.name == "nt":  # Windows
        import winreg

        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            downloads_dir = winreg.QueryValueEx(key, downloads_guid)[0]
        return Path(downloads_dir)
    else:  # macOS, Linux, etc.
        return Path.home() / "Downloads"


def save_image_to_downloads(
    image, prefix: str = "screenshot", directory: Path = None
) -> Tuple[str, bytes]:
    """Save an image to the downloads directory and return its absolute path.

    Args:
        image: Either a PIL Image object or MCP Image object
        prefix: Prefix for the filename (default: 'screenshot')
        directory: Optional directory to save the image to

    Returns:
        Tuple of (absolute_path, image_data_bytes)
    """
    # Create a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{prefix}_{timestamp}_{unique_id}.png"

    # Get downloads directory
    downloads_dir = directory or get_downloads_dir()
    filepath = downloads_dir / filename

    # Handle different image types
    if hasattr(image, "save"):  # PIL Image
        image.save(filepath)
        # Also get the bytes for returning
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()
    elif hasattr(image, "data"):  # MCP Image
        img_bytes = image.data
        with open(filepath, "wb") as f:
            f.write(img_bytes)
    else:
        raise TypeError("Unsupported image type")

    log(f"Saved image to {filepath}")
    return str(filepath.absolute()), img_bytes


def _find_matching_window(
    windows: any,
    title_pattern: str = None,
    use_regex: bool = False,
    threshold: int = 60,
) -> Optional[Dict[str, Any]]:
    """Helper function to find a matching window based on title pattern.

    Args:
        windows: List of window dictionaries
        title_pattern: Pattern to match window title
        use_regex: If True, treat the pattern as a regex, otherwise use fuzzy matching
        threshold: Minimum score (0-100) required for a fuzzy match

    Returns:
        The best matching window or None if no match found
    """
    if not title_pattern:
        log("No title pattern provided, returning None")
        return None

    # For regex matching
    if use_regex:
        for window in windows:
            if re.search(title_pattern, window["title"], re.IGNORECASE):
                log(f"Regex match found: {window['title']}")
                return window
        return None

    # For fuzzy matching using fuzzywuzzy
    # Extract all window titles
    window_titles = [window["title"] for window in windows]

    # Use process.extractOne to find the best match
    best_match_title, score = process.extractOne(
        title_pattern, window_titles, scorer=fuzz.partial_ratio
    )
    log(f"Best fuzzy match: '{best_match_title}' with score {score}")

    # Only return if the score is above the threshold
    if score >= threshold:
        # Find the window with the matching title
        for window in windows:
            if window["title"] == best_match_title:
                return window

    return None


# --- MCP Function Handlers ---


@mcp.tool()
def tool_version() -> str:
    """Get the version of the tool."""
    return "0.2.7"


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
            "message": f"Screen size: {width}x{height}",
        }
    except Exception as e:
        return {"error": str(e), "message": f"Error getting screen size: {str(e)}"}


@mcp.tool()
def type_text(text: str) -> str:
    """Type the specified text at the current cursor position."""
    try:
        pyautogui.typewrite(text)
        return f"Successfully typed text: {text}"
    except Exception as e:
        return f"Error typing text: {str(e)}"


@mcp.tool()
def take_screenshot(
    title_pattern: str = None,
    use_regex: bool = False,
    threshold: int = 60,
    with_ocr_text_and_coords: bool = False,
    scale_percent_for_ocr: int = 100,
    save_to_downloads: bool = False,
) -> Image | List[Tuple[List[List[int]], str, float]]:
    """
    Get screenshot and  OCR text with absolute coordinates (returned after adding the window offset from true (0, 0) of screen to the OCR coordinates, so clicking is on-point. Recommended to click in the middle of OCR Box) and confidence from window with the specified title pattern.
    If no title pattern is provided, get screenshot of entire screen and all text on the screen.

    Args:
        title_pattern: Pattern to match window title, if None, take screenshot of entire screen
        use_regex: If True, treat the pattern as a regex, otherwise best match with fuzzy matching
        threshold: Minimum score (0-100) required for a fuzzy match
        with_ocr_text_and_coords: If True, get OCR text with absolute coordinates from the screenshot
        scale_percent_for_ocr: Percentage to scale the image down before processing, you wont need this most of the time unless your pc is extremely old or slow
        save_to_downloads: If True, save the screenshot to the downloads directory and return the absolute path

    Returns:
        Returns a single screenshot as MCP Image object, if with_ocr_text_and_coords is True, returns a MCP Image object followed by list of UI elements as [[4 corners of box], text, confidence], "content type image not supported" means preview isnt supported but Image object is there.
    """
    try:

        all_windows = gw.getAllWindows()

        # Convert to list of dictionaries for _find_matching_window
        windows = []
        for window in all_windows:
            if window.title:  # Only include windows with titles
                windows.append(
                    {
                        "title": window.title,
                        "window_obj": window,  # Store the actual window object
                    }
                )

        log(f"Found {len(windows)} windows")
        window = _find_matching_window(windows, title_pattern, use_regex, threshold)
        window = window["window_obj"] if window else None

        # Store the currently active window

        # Take the screenshot
        if not window:
            log("No matching window found, taking screenshot of entire screen")
            screenshot = pyautogui.screenshot()
        else:
            current_active_window = gw.getActiveWindow()
            log(f"Taking screenshot of window: {window.title}")
            # Activate the window and wait for it to be fully in focus
            window.activate()
            pyautogui.sleep(0.5)  # Wait for 0.5 seconds to ensure window is active
            screenshot = pyautogui.screenshot(
                region=(window.left, window.top, window.width, window.height)
            )
            # Restore the previously active window
            if current_active_window:
                try:
                    current_active_window.activate()
                    pyautogui.sleep(0.2)  # Wait a bit to ensure previous window is restored
                except Exception as e:
                    log(f"Error restoring previous window: {str(e)}")

        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp())

        # Save screenshot and get filepath
        filepath, _ = save_image_to_downloads(
            screenshot, prefix="screenshot", directory=temp_dir
        )

        # Create Image object from filepath
        image = Image(filepath)

        if not with_ocr_text_and_coords:
            return image  # MCP Image object

        # Copy from temp to downloads
        if save_to_downloads:
            log("Copying screenshot from temp to downloads")
            shutil.copy(filepath, get_downloads_dir())

        image_path = image.path
        img = cv2.imread(image_path)

        # Lower down resolution before processing
        width = int(img.shape[1] * scale_percent_for_ocr / 100)
        height = int(img.shape[0] * scale_percent_for_ocr / 100)
        dim = (width, height)
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # save resized image to pwd
        # cv2.imwrite("resized_img.png", resized_img)
        engine = RapidOCR()
        vis = VisRes()

        result, elapse_list = engine(resized_img)
        boxes, txts, scores = list(zip(*result))
        boxes = [
            [[x + window.left, y + window.top] if window else [x, y] for x, y in box]
            for box in boxes
        ]
        zipped_results = list(zip(boxes, txts, scores))

        return [image, *zipped_results]

    except Exception as e:
        log(f"Error in screenshot or getting UI elements: {str(e)}")
        import traceback

        stack_trace = traceback.format_exc()
        log(f"Stack trace:\n{stack_trace}")
        return f"Error in screenshot or getting UI elements: {str(e)}\nStack trace:\n{stack_trace}"


@mcp.tool()
def move_mouse(x: int, y: int) -> str:
    """Move the mouse to the specified screen coordinates."""
    try:
        pyautogui.moveTo(x=x, y=y)
        return f"Successfully moved mouse to coordinates ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse to coordinates ({x}, {y}): {str(e)}"


@mcp.tool()
async def drag_mouse(
    from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5
) -> str:
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
        log("starting drag")
        await asyncio.to_thread(pyautogui.dragTo, x=to_x, y=to_y, duration=duration)
        log("done drag")
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
                result.append(
                    {
                        "title": window.title,
                        "left": window.left,
                        "top": window.top,
                        "width": window.width,
                        "height": window.height,
                        "is_active": window.isActive,
                        "is_visible": window.visible,
                        "is_minimized": window.isMinimized,
                        "is_maximized": window.isMaximized,
                        "screenshot": pyautogui.screenshot(
                            region=(
                                window.left,
                                window.top,
                                window.width,
                                window.height,
                            )
                        ),
                    }
                )
        return result
    except Exception as e:
        log(f"Error listing windows: {str(e)}")
        return [{"error": str(e)}]


@mcp.tool()
def activate_window(
    title_pattern: str, use_regex: bool = False, threshold: int = 60
) -> str:
    """
    Activate a window (bring it to the foreground) by matching its title.

    Args:
        title_pattern: Pattern to match window title
        use_regex: If True, treat the pattern as a regex, otherwise use fuzzy matching
        threshold: Minimum score (0-100) required for a fuzzy match

    Returns:
        Success or error message
    """
    try:
        # Get all windows
        all_windows = gw.getAllWindows()

        # Convert to list of dictionaries for _find_matching_window
        windows = []
        for window in all_windows:
            if window.title:  # Only include windows with titles
                windows.append(
                    {
                        "title": window.title,
                        "window_obj": window,  # Store the actual window object
                    }
                )

        # Find matching window using our improved function
        matched_window_dict = _find_matching_window(
            windows, title_pattern, use_regex, threshold
        )

        if not matched_window_dict:
            log(f"No window found matching pattern: {title_pattern}")
            return f"Error: No window found matching pattern: {title_pattern}"

        # Get the actual window object
        matched_window = matched_window_dict["window_obj"]

        # Activate the window
        matched_window.activate()

        return f"Successfully activated window: '{matched_window.title}'"
    except Exception as e:
        log(f"Error activating window: {str(e)}")
        return f"Error activating window: {str(e)}"


def main():
    """Main entry point for the MCP server."""
    pyautogui.FAILSAFE = True

    try:
        # Run the server
        mcp.run()

    except KeyboardInterrupt:
        log("Server shutting down...")
    except Exception as e:
        log(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
