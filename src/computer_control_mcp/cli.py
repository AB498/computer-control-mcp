"""
Command-line interface for Computer Control MCP.

This module provides a command-line interface for interacting with the Computer Control MCP.
"""

import argparse
import sys
from computer_control_mcp.core import mcp, main as run_server

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Computer Control MCP CLI")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Server command
    server_parser = subparsers.add_parser("server", help="Run the MCP server")

    # Click command
    click_parser = subparsers.add_parser("click", help="Click at specified coordinates")
    click_parser.add_argument("x", type=int, help="X coordinate")
    click_parser.add_argument("y", type=int, help="Y coordinate")

    # Type text command
    type_parser = subparsers.add_parser("type", help="Type text at current cursor position")
    type_parser.add_argument("text", help="Text to type")

    # Screenshot command
    screenshot_parser = subparsers.add_parser("screenshot", help="Take a screenshot")
    screenshot_parser.add_argument("--mode", choices=["all_windows", "single_window", "whole_screen"],
                                  default="whole_screen", help="Screenshot mode")
    screenshot_parser.add_argument("--title", help="Window title pattern (for single_window mode)")
    screenshot_parser.add_argument("--regex", action="store_true", help="Use regex for title matching")
    screenshot_parser.add_argument("--output", help="Output file path (if not provided, saves to downloads directory)")
    screenshot_parser.add_argument("--no-save", action="store_true", help="Don't save images to downloads directory")

    # List windows command
    subparsers.add_parser("list-windows", help="List all open windows")

    # GUI command
    subparsers.add_parser("gui", help="Launch the GUI test harness")

    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    args = parse_args()

    if args.command == "server":
        run_server()

    elif args.command == "click":
        # Call the tool using the call_tool method
        import asyncio
        result = asyncio.run(mcp.call_tool("click_screen", {"x": args.x, "y": args.y}))
        print(result)

    elif args.command == "type":
        # Call the tool using the call_tool method
        import asyncio
        result = asyncio.run(mcp.call_tool("type_text", {"text": args.text}))
        print(result)

    elif args.command == "screenshot":
        if args.mode == "single_window" and not args.title:
            print("Error: --title is required for single_window mode")
            sys.exit(1)

        # Call the tool using the call_tool method
        import asyncio
        result = asyncio.run(mcp.call_tool("take_screenshot", {
            "mode": args.mode,
            "title_pattern": args.title,
            "use_regex": args.regex,
            "save_to_downloads": not args.no_save
        }))

        if args.output:
            # Save the screenshot to a specific file path provided by user
            with open(args.output, "wb") as f:
                f.write(result.image.data)
            print(f"Screenshot saved to {args.output}")
        elif hasattr(result, 'file_path'):
            # If image was saved to downloads, show the path
            print(f"Screenshot saved to {result.file_path}")
        else:
            print("Screenshot taken successfully")

        # If we have multiple results (all_windows mode)
        if args.mode == "all_windows" and isinstance(result, list):
            print("\nAll screenshots:")
            for i, item in enumerate(result):
                if hasattr(item, 'file_path'):
                    window_title = item.window_info.title if hasattr(item, 'window_info') else f"Window {i+1}"
                    print(f"{i+1}. {window_title}: {item.file_path}")

    elif args.command == "list-windows":
        # Call the tool using the call_tool method
        import asyncio
        result = asyncio.run(mcp.call_tool("list_windows", {}))

        # Parse the result
        windows = []
        for item in result:
            if hasattr(item, 'text'):
                try:
                    import json
                    window_info = json.loads(item.text)
                    windows.append(window_info)
                except json.JSONDecodeError:
                    print(f"Failed to parse window info: {item.text}")

        # Display the windows
        for i, window in enumerate(windows):
            print(f"{i+1}. {window.get('title')} ({window.get('width')}x{window.get('height')})")

    elif args.command == "gui":
        from computer_control_mcp.gui import main as run_gui
        run_gui()

    else:
        # When no command is specified, run the server by default
        print("MCP server started!")
        run_server()

if __name__ == "__main__":
    main()
