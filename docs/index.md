# Computer Control MCP Documentation

Welcome to the Computer Control MCP documentation.

## Overview

Computer Control MCP is a Python package that provides computer control capabilities using PyAutoGUI through a Model Context Protocol (MCP) server.

## Installation

```bash
pip install computer-control-mcp
```

Or with uv:

```bash
uv pip install computer-control-mcp
```

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

## API Reference

See the [API Reference](api.md) for detailed information about the available functions and classes.
