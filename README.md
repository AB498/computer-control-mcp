# Computer Control MCP 🤖

> MCP server for powerful computer control: mouse, keyboard, OCR, and more. Zero external dependencies.

<div align="center">
  <a href="https://discord.gg/ZeeqSBpjU2"><img src="https://img.shields.io/discord/1095854826786668545?style=for-the-badge" alt="Discord"></a>
  <a href="https://img.shields.io/badge/License-MIT-yellow.svg"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://pypi.org/project/computer-control-mcp"><img src="https://img.shields.io/pypi/v/computer-control-mcp?style=for-the-badge" alt="PyPI version"></a>
</div>

<br>

<p align="center">
  <img src="https://github.com/AB498/computer-control-mcp/blob/main/demonstration.gif?raw=true" alt="MCP Computer Control Demo" width="700"/>
</p>

## ✨ Features

- **Mouse & Keyboard Control**: Full control over mouse movements, clicks, drags, and keyboard input.
- **Screen & Window Management**: Capture screenshots, get screen size, list open windows, and bring them to the foreground.
- **OCR**: Extract text and coordinates from screenshots using RapidOCR.
- **Zero Dependencies**: No external dependencies required for the core functionality.

## 🚀 Quick Usage

<details>
<summary>Click to expand</summary>

### MCP Setup (using `uvx`)

*Note: Running `uvx computer-control-mcp@latest` for the first time will download Python dependencies (~70MB). Subsequent runs are instant.*

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

### Global Install (using `pip`)

```bash
pip install computer-control-mcp
```
Then run the server with:
```bash
computer-control-mcp
```

</details>

## 🛠️ Available Tools

| Category                | Tool                                                                                                                                                           | Description                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Mouse Control**       | `click_screen(x, y)`                                                                                                                                           | Click at specified screen coordinates.                                   |
|                         | `move_mouse(x, y)`                                                                                                                                             | Move the mouse cursor to specified coordinates.                          |
|                         | `drag_mouse(from_x, from_y, to_x, to_y, duration)`                                                                                                             | Drag the mouse from one position to another.                             |
| **Keyboard Control**    | `type_text(text)`                                                                                                                                              | Type the specified text at the current cursor position.                  |
|                         | `press_key(key)`                                                                                                                                               | Press a specified keyboard key.                                          |
| **Screen & Window**     | `take_screenshot(...)`                                                                                                                                         | Capture the screen or a window with optional OCR.                        |
|                         | `get_screen_size()`                                                                                                                                            | Get the current screen resolution.                                       |
|                         | `list_windows()`                                                                                                                                               | List all open windows.                                                   |
|                         | `activate_window(title_pattern, ...)`                                                                                                                          | Bring a specified window to the foreground.                              |

## 👨‍💻 Development

<details>
<summary>Click to expand</summary>

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
</details>

## 📖 API Reference

See the [API Reference](docs/api.md) for detailed information about the available functions and classes.

## 🤝 Contributors

<a href="https://github.com/hemangjoshi37a" title="hemangjoshi37a">
  <img src="https://avatars.githubusercontent.com/u/12392345?v=4" width="50" height="50" alt="hemangjoshi37a">
</a>
<a href="https://github.com/AB498" title="AB498">
  <img src="https://avatars.githubusercontent.com/u/52972436?v=4" width="50" height="50" alt="AB498">
</a>

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
  For more information or help, reach out via <a href="mailto:abcd49800@gmail.com">Email</a> or join our <a href="https://discord.gg/ZeeqSBpjU2">Discord</a>.
</div>