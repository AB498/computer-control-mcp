# API Reference

## Core Module

The core module provides the main functionality of the Computer Control MCP package.

### Mouse Control

- `mcp.click_screen(x: int, y: int) -> str`: Click at the specified screen coordinates
- `mcp.move_mouse(x: int, y: int) -> str`: Move the mouse to the specified screen coordinates
- `mcp.drag_mouse(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5) -> str`: Drag the mouse from one position to another

### Keyboard Control

- `mcp.type_text(text: str) -> str`: Type the specified text at the current cursor position
- `mcp.press_key(key: str) -> str`: Press the specified keyboard key

### Window Management

- `mcp.list_windows() -> List[Dict[str, Any]]`: List all open windows on the system
- `mcp.activate_window(title_pattern: str, use_regex: bool = False) -> str`: Activate a window by matching its title

### Screen Capture

- `mcp.take_screenshot(mode: str = "all_windows", title_pattern: str = None, use_regex: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]`: Take screenshots based on the specified mode
- `mcp.get_screen_size() -> Dict[str, Any]`: Get the current screen resolution

## CLI Module

The CLI module provides a command-line interface for interacting with the Computer Control MCP.

### Commands

- `server`: Run the MCP server
- `click`: Click at specified coordinates
- `type`: Type text at current cursor position
- `screenshot`: Take a screenshot
- `list-windows`: List all open windows
- `gui`: Launch the GUI test harness

## GUI Module

The GUI module provides a graphical user interface for testing the Computer Control MCP functionality.

### Classes

- `TestHarnessGUI`: Main GUI class for testing the Computer Control MCP functionality
