# Computer Control MCP

A Python package that provides computer control capabilities using PyAutoGUI through a Model Context Protocol (MCP) server.

## Project Structure

```
computer-control-mcp/
├── docs/                  # Documentation
│   ├── index.md          # Main documentation
│   └── api.md            # API reference
├── src/                  # Source code
│   └── computer_control_mcp/  # Main package
│       ├── __init__.py   # Package initialization
│       ├── __main__.py   # Entry point for running as a module
│       ├── core.py       # Core functionality
│       ├── cli.py        # Command-line interface
│       └── gui.py        # GUI for testing
├── tests/                # Test files
│   ├── conftest.py       # Pytest configuration
│   └── test_computer_control.py  # Tests for core functionality
├── LICENSE               # MIT license
├── MANIFEST.in           # Package manifest
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## Installation

```bash
pip install computer-control-mcp
```

Or with uv:

```bash
uv pip install computer-control-mcp
```

## Features

- Control mouse movements and clicks
- Type text at the current cursor position
- Take screenshots of the entire screen or specific windows
- List and activate windows
- Press keyboard keys
- Drag and drop operations

## Usage

### Basic Example

```python
from computer_control_mcp.core import mcp

# Click at specific coordinates
mcp.click_screen(x=100, y=100)

# Type text
mcp.type_text(text="Hello, world!")

# Take a screenshot
screenshot = mcp.take_screenshot(mode="whole_screen")
```

### Command-line Interface

```bash
# Run the MCP server
computer-control-mcp server

# Click at coordinates
computer-control-mcp click 100 100

# Type text
computer-control-mcp type "Hello, world!"

# Take a screenshot
computer-control-mcp screenshot --mode whole_screen

# List all windows
computer-control-mcp list-windows

# Launch the GUI test harness
computer-control-mcp gui
```

### Running as a Module

You can run the package as a module:

```bash
python -m computer_control_mcp
```

## Development

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/computer-control-mcp.git
cd computer-control-mcp

# Create a virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Unix/macOS

# Install in development mode
pip install -e .
```

### Running Tests

```bash
python -m pytest
```

## API Reference

See the [API Reference](docs/api.md) for detailed information about the available functions and classes.

## License

MIT
