FROM python:3.11-alpine

# Install dependencies without running prepare
WORKDIR /app
RUN pip install -e .

# Copy source and run setup to download WASM parsers
COPY . ./

# Default command to start the MCP server
CMD ["python", "src/computer_control_mcp/core.py"]
