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
    screenshot_parser.add_argument("--title", help="Window title pattern to capture a specific window")
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
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    args = parse_args()

    if args.command == "server":
        run_server()

    elif args.command == "click":
        import asyncio
        content, _ = asyncio.run(mcp.call_tool("click_screen", {"x": args.x, "y": args.y}))
        print(content[0].text)

    elif args.command == "type":
        import asyncio
        content, _ = asyncio.run(mcp.call_tool("type_text", {"text": args.text}))
        print(content[0].text)

    elif args.command == "screenshot":
        import asyncio
        import base64

        tool_args = {
            "use_regex": args.regex,
            "save_to_downloads": not args.no_save
        }
        if args.title:
            tool_args["title_pattern"] = args.title

        result = asyncio.run(mcp.call_tool("take_screenshot", tool_args))
        content = result[0] if isinstance(result, tuple) else result

        if args.output:
            image_data = base64.b64decode(content[0].data)
            with open(args.output, "wb") as f:
                f.write(image_data)
            print(f"Screenshot saved to {args.output}")
        else:
            print("Screenshot taken successfully")

    elif args.command == "list-windows":
        import asyncio
        import json
        content, _ = asyncio.run(mcp.call_tool("list_windows", {}))

        windows = []
        for item in content:
            if hasattr(item, 'text'):
                try:
                    window_info = json.loads(item.text)
                    windows.append(window_info)
                except json.JSONDecodeError:
                    print(f"Failed to parse window info: {item.text}")

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
