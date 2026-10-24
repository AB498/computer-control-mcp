"""
Server module for Computer Control MCP.

This module provides a simple way to run the MCP server.
"""

import sys

from computer_control_mcp.core import main as run_server

def main():
    """Run the MCP server."""
    # Must go to stderr: stdout carries the MCP JSON-RPC protocol.
    print("Starting Computer Control MCP server...", file=sys.stderr)
    run_server()

if __name__ == "__main__":
    main()
