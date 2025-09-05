#!/usr/bin/env python
"""
Simple script to run the Computer Control MCP server.
"""

# import sys
# import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
# from computer_control_mcp.core import main

from computer_control_mcp.core import main

if __name__ == "__main__":
    print("Starting Computer Control MCP server...")
    main()
