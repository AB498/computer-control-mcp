"""
Entry point for running the Computer Control MCP as a module.

This module serves as the main entry point for the package.
When executed directly (e.g., with `python -m computer_control_mcp`),
it will run the CLI interface.

For CLI functionality, use:
    computer-control-mcp <command>
    python -m computer_control_mcp <command>
"""

from computer_control_mcp.cli import main as cli_main

def main():
    """Main entry point for the package."""
    # Run the CLI when the module is executed directly
    cli_main()

if __name__ == "__main__":
    main()
