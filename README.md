# Computer Control MCP 🤖

> A powerful, local, and secure MCP server for controlling your computer with zero external dependencies.

<div align="center">
  <a href="https://pypi.org/project/computer-control-mcp"><img src="https://img.shields.io/pypi/v/computer-control-mcp?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://discord.gg/ZeeqSBpjU2"><img src="https://img.shields.io/discord/1095854826786668545?style=for-the-badge" alt="Discord"></a>
  <a href="https://github.com/AB498/computer-control-mcp/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AB498/computer-control-mcp?style=for-the-badge" alt="License: MIT"></a>
</div>

<br>

<p align="center">
  <img src="https://github.com/AB498/computer-control-mcp/blob/main/demonstration.gif?raw=true" alt="MCP Computer Control Demo" width="700"/>
</p>

## 🤔 Why Computer Control MCP?

- **Local & Secure**: All operations are executed locally on your machine, ensuring your data and actions remain private.
- **Zero External Dependencies**: Get up and running in seconds without a complex setup process.
- **Powerful Automation**: Programmatically control your entire desktop environment, from simple clicks to complex workflows.
- **Extensible**: The project is designed to be easily extended with new tools and capabilities.

## ✨ Features

- **Mouse & Keyboard Control**: Full control over mouse movements, clicks, drags, and keyboard input.
- **Screen & Window Management**: Capture screenshots, get screen size, list open windows, and bring them to the foreground.
- **OCR**: Extract text and coordinates from screenshots using the powerful RapidOCR engine.

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

The following tools are available for use:

| Category                | Tool                                                              | Description                                         |
| ----------------------- | ----------------------------------------------------------------- | --------------------------------------------------- |
| **Mouse Control**       | `click_screen(x, y)`                                              | Clicks at the specified screen coordinates.         |
|                         | `move_mouse(x, y)`                                                | Moves the mouse cursor to the specified coordinates.|
|                         | `drag_mouse(from_x, from_y, to_x, to_y, duration)`                | Drags the mouse from one position to another.       |
| **Keyboard Control**    | `type_text(text)`                                                 | Types the specified text at the current position.   |
|                         | `press_key(key)`                                                  | Presses a specified keyboard key.                   |
| **Screen & Window**     | `take_screenshot(...)`                                            | Captures the screen or a window with optional OCR.  |
|                         | `get_screen_size()`                                               | Gets the current screen resolution.                 |
|                         | `list_windows()`                                                  | Lists all open windows.                             |
|                         | `activate_window(title_pattern, ...)`                             | Brings a specified window to the foreground.        |

<details>
<summary>More on `take_screenshot`</summary>

`take_screenshot(title_pattern: str = None, use_regex: bool = False, threshold: int = 60, with_ocr_text_and_coords: bool = False, scale_percent_for_ocr: int = 100, save_to_downloads: bool = False)`

- `title_pattern`: A string to match against window titles. If `None`, the entire screen is captured.
- `use_regex`: If `True`, `title_pattern` is treated as a regular expression.
- `threshold`: The confidence threshold for matching the `title_pattern` (0-100).
- `with_ocr_text_and_coords`: If `True`, OCR is performed on the screenshot to extract text and coordinates.
- `scale_percent_for_ocr`: The percentage to scale the image by before performing OCR.
- `save_to_downloads`: If `True`, the screenshot is saved to your "Downloads" folder.

</details>

## ⚙️ Under the Hood

This MCP leverages a powerful stack of Python libraries:

- **PyAutoGUI**: For all mouse and keyboard automation.
- **RapidOCR**: For fast and accurate text recognition from images.
- **ONNXRuntime**: Powers the OCR engine, ensuring high performance.

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

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/hemangjoshi37a">
        <img src="https://avatars.githubusercontent.com/u/12392345?v=4" width="100px;" alt="Hemang Joshi"/><br />
        <sub><b>Hemang Joshi</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/AB498">
        <img src="https://avatars.githubusercontent.com/u/52972436?v=4" width="100px;" alt="AB498"/><br />
        <sub><b>AB498</b></sub>
      </a>
    </td>
  </tr>
</table>

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
  For more information or help, reach out via <a href="mailto:abcd49800@gmail.com">Email</a> or join our <a href="https://discord.gg/ZeeqSBpjU2">Discord</a>.
</div>
