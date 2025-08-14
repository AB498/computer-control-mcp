#!/usr/bin/env python
"""
Simple script to run the Computer Control MCP CLI.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from computer_control_mcp.cli import main

if __name__ == "__main__":
    main()
