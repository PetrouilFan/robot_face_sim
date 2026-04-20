#!/usr/bin/env python3
"""
Main entry point for Robot Face Simulator
Run with: uv run main.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from robot_face_sim.app.simulator import main

if __name__ == "__main__":
    main()
