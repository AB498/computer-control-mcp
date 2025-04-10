"""
Entry point for running the Computer Control MCP as a module.

This module serves as the main entry point for the package.
When executed directly (e.g., with `python -m computer_control_mcp`),
it will run the MCP server.

When used with `uvx computer-control-mcp`, it will also run the server.

For CLI functionality, use:
    computer-control-mcp <command>
    uvx computer-control-mcp <command>
"""

from computer_control_mcp.core import main as run_server

def main():
    """Main entry point for the package."""
    # Always run the server when the module is executed directly
    print("Starting Computer Control MCP server...")
    run_server()

if __name__ == "__main__":
    main()
