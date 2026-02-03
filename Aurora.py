#!/usr/bin/env python3
"""
Simple script to run Aurora package as a standalone script
"""
import sys
import os

# Add project root to sys.path so absolute imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run the main module
from aurora import main

main.main()  # assuming your main.py has a main() function
