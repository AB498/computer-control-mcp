# Computer Control MCP

MCP server that provides computer control capabilities, like mouse, keyboard, OCR, etc. using PyAutoGUI, RapidOCR, ONNXRuntime. With Zero External Dependencies.

## Quick Usage (MCP Setup Using `uvx`)

```json
{
  "mcpServers": {
    "computer-control-mcp": {
      "command": "uvx",
      "args": ["computer-control-mcp"]
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

### Running as a Module

You can run the package as a module:

```bash
python -m computer_control_mcp
```

## Development

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/AB498/computer-control-mcp.git
cd computer-control-mcp

# Install in development mode
pip install -e .
```

Or with uv:

```bash
# Clone the repository
git clone https://github.com/AB498/computer-control-mcp.git
cd computer-control-mcp

# Install in development mode
uv pip install -e .
```

### Running Tests

```bash
python -m pytest
```

## API Reference

See the [API Reference](docs/api.md) for detailed information about the available functions and classes.

## License

MIT
