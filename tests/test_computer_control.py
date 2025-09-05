"""
Tests for the Computer Control MCP package.
"""

import pytest
from unittest.mock import Mock, patch
import json
import sys
import tkinter as tk
from tkinter import ttk
import asyncio
import os
import ast
from computer_control_mcp.core import mcp

# Helper function to print request/response JSON, skipping non-serializable properties
def print_json_data(name, request_data=None, response_data=None):
    def serialize(obj):
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            return str(obj)

    print(f"\n===== TEST: {name} =====", file=sys.stderr)
    if isinstance(request_data, dict):
        serializable_request = {k: serialize(v) for k, v in request_data.items()}
        print(f"REQUEST: {json.dumps(serializable_request, indent=2)}", file=sys.stderr)
    elif request_data is not None:
        print(f"REQUEST: {serialize(request_data)}", file=sys.stderr)
    if response_data is not None:
        if isinstance(response_data, dict):
            serializable_response = {k: serialize(v) for k, v in response_data.items()}
            print(
                f"RESPONSE: {json.dumps(serializable_response, indent=2)}",
                file=sys.stderr,
            )
        else:
            print(f"RESPONSE: {serialize(response_data)}", file=sys.stderr)
    print("======================\n", file=sys.stderr)


# Test drag_mouse tool
@pytest.mark.asyncio
async def test_drag_mouse():
    # Test data
    test_window = tk.Tk()
    test_window.title("Test Drag Mouse")
    test_window.geometry("400x400")

    # Update the window to ensure coordinates are calculated
    test_window.update_idletasks()
    test_window.update()

    # Window title coordinates
    window_x = test_window.winfo_x()
    window_y = test_window.winfo_y()

    screen_width = test_window.winfo_screenwidth()
    screen_height = test_window.winfo_screenheight()
    center_x = screen_width // 2
    center_y = screen_height // 2
    request_data = {
        "from_x": window_x + 55,
        "from_y": window_y + 15,
        "to_x": center_x,
        "to_y": center_y,
        "duration": 1.0,
    }

    print(f"starting coordinates: x={window_x}, y={window_y}", file=sys.stderr)

    # Create an event to track completion
    drag_complete = asyncio.Event()

    async def perform_drag():
        try:
            result = await mcp.call_tool("drag_mouse", request_data)
            print(f"Result: {result}", file=sys.stderr)
        finally:
            drag_complete.set()

    # Start the drag operation
    drag_task = asyncio.create_task(perform_drag())

    # Keep updating the window while waiting for drag to complete
    while not drag_complete.is_set():
        test_window.update()
        await asyncio.sleep(0.01)  # Small delay to prevent high CPU usage

    # Wait for drag operation to complete
    await drag_task

    window_x_end = test_window.winfo_x()
    window_y_end = test_window.winfo_y()
    print(f'ending coordinates: x={window_x_end}, y={window_y_end}', file=sys.stderr)

    assert window_y_end != window_y and window_x_end != window_x

    test_window.destroy()


# Test list_windows tool
@pytest.mark.asyncio
async def test_list_windows():
    # open tkinter
    test_window = tk.Tk()
    test_window.title("Test Window")
    test_window.geometry("400x400")

    # Update the window to ensure coordinates are calculated
    test_window.update_idletasks()
    test_window.update()

    # list all windows
    result = await mcp.call_tool("list_windows", {})

    # check if "Test Window" is in the list
    # Parse the TextContent objects to extract the JSON data
    window_data = []
    for item in result:
        if hasattr(item, 'text'):
            try:
                window_info = json.loads(item.text)
                window_data.append(window_info)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {item.text}", file=sys.stderr)

    print(f"Result: {window_data}")

    assert any(window.get("title") == "Test Window" for window in window_data)

    test_window.destroy()

# Test screenshot with downloads
@pytest.mark.asyncio
async def test_take_screenshot():
    # Take a screenshot of the whole screen and save to downloads
    results = await mcp.call_tool("take_screenshot", {'save_to_downloads': True, 'mode': 'whole_screen'})

    for result in results:
        # Check if file_path is in the result
        if hasattr(result, 'text'):
            try:
                result_dict = json.loads(result.text)
                print(f"Screenshot result: {result_dict['title']}", file=sys.stderr)
                assert 'file_path' in result_dict, "file_path should be in the result"
                file_path = result_dict['file_path']

                # Check if the file exists
                assert os.path.exists(file_path), f"File {file_path} should exist"
                print(f"Screenshot saved to: {file_path}", file=sys.stderr)

                # Clean up - remove the file
                os.remove(file_path)
                print(f"Removed test file: {file_path}", file=sys.stderr)
            except (ValueError, SyntaxError, AttributeError) as e:
                print(f"Error processing result: {e}", file=sys.stderr)
                assert False, f"Error processing result: {e}"

    assert True, "Successfully tested screenshot with downloads"
