FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy application code
COPY . /app

# Install required Python packages
RUN pip install -e .

# Default command to start the MCP server
CMD ["python", "src/computer_control_mcp/core.py"]