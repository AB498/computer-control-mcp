# Use a lightweight Python base image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency file(s)
COPY pyproject.toml .
COPY src/ src/
COPY README.md README.md

# Install build backend (Hatchling)
RUN pip install --upgrade pip && \
    pip install hatchling && \
    pip install -e .

# Copy any additional files (e.g. configs, CLI, entrypoints)
COPY . .

# Default command (can be overridden)
CMD ["python", "-m", "computer_control_mcp"]
