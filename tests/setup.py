#!/usr/bin/env python
"""
Backward compatibility setup.py file for Computer Control MCP.
This file is provided for backward compatibility with tools that don't support pyproject.toml.
"""

import setuptools

if __name__ == "__main__":
    try:
        setuptools.setup()
    except Exception as e:
        print(f"Error: {e}")
        print("\nThis package uses pyproject.toml for configuration.")
        print("Please use a PEP 517 compatible build tool like pip or build.")
        print("For example: pip install .")
