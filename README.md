# Computer Control MCP

### MCP server that provides computer control capabilities, like mouse, keyboard, OCR, etc. using PyAutoGUI, RapidOCR, ONNXRuntime. Similar to 'computer-use' by Anthropic. With Zero External Dependencies.

* *Only tested on Windows. Should work on other platforms.*

<div style="text-align:center;font-family: monospace; display: flex; align-items: center; justify-content: center; width: 100%; gap: 10px">
        <a href="https://discord.gg/ZeeqSBpjU2"><img src="https://img.shields.io/discord/1095854826786668545" alt="Discord"></a>
        <a href="https://img.shields.io/badge/License-MIT-yellow.svg"><img
                src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</div>

---

![MCP Computer Control Demo](https://github.com/AB498/computer-control-mcp/blob/main/demonstration.gif?raw=true)

## Quick Usage (MCP Setup Using `uvx`)

***Note:** Running `uvx computer-control-mcp@latest` for the first time will download python dependencies (around 70MB) which may take some time. Recommended to run this in a terminal before using it as MCP. Subsequent runs will be instant.* 

```json
{
  "mcpServers": {
    "computer-control-mcp": {
      "command": "uvx",
      "args": ["computer-control-mcp@latest"]
    }
  }
}
```

OR install globally with `pip`:
```bash
pip install computer-control-mcp
```
Then run the server with:
```bash
computer-control-mcp # instead of uvx computer-control-mcp, so you can use the latest version, also you can `uv cache clean` to clear the cache and `uvx` again to use latest version.
```

## Features

- Control mouse movements and clicks
- Type text at the current cursor position
- Take screenshots of the entire screen or specific windows with optional saving to downloads directory
- Extract text from screenshots using OCR (Optical Character Recognition)
- List and activate windows
- Press keyboard keys
- Drag and drop operations

## Available Tools

### Mouse Control
- `click_screen(x: int, y: int)`: Click at specified screen coordinates
- `move_mouse(x: int, y: int)`: Move mouse cursor to specified coordinates
- `drag_mouse(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5)`: Drag mouse from one position to another

### Keyboard Control
- `type_text(text: str)`: Type the specified text at current cursor position
- `press_key(key: str)`: Press a specified keyboard key

### Screen and Window Management
- `take_screenshot(title_pattern: str = None, use_regex: bool = False, threshold: int = 60, with_ocr_text_and_coords: bool = False, scale_percent_for_ocr: int = 100, save_to_downloads: bool = False)`: Capture screen or window with optional OCR
- `get_screen_size()`: Get current screen resolution
- `list_windows()`: List all open windows
- `activate_window(title_pattern: str, use_regex: bool = False, threshold: int = 60)`: Bring specified window to foreground

## Development

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/AB498/computer-control-mcp.git
cd computer-control-mcp

# Install in development mode
pip install -e .

# Start server
python -m computer_control_mcp.core
```

### Running Tests

```bash
python -m pytest
```

## API Reference

See the [API Reference](docs/api.md) for detailed information about the available functions and classes.

## License

MIT

## For more information or help

- [Email (abcd49800@gmail.com)](mailto:abcd49800@gmail.com)
- [Discord (CodePlayground)](https://discord.gg/ZeeqSBpjU2)
