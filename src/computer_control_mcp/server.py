"""
Server module for Computer Control MCP.

This module provides a simple way to run the MCP server.
"""

from computer_control_mcp.core import main as run_server

def main():
    """Run the MCP server."""
    print("Starting Computer Control MCP server...")
    run_server()

if __name__ == "__main__":
    main()
