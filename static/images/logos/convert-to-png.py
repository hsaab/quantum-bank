#!/usr/bin/env python3
"""
PNG Export Script for Quantum Bank Logo (Python version)

This script converts the SVG logos to PNG format using cairosvg.

Requirements:
pip install cairosvg

Usage:
python3 convert-to-png.py
"""

import os
from typing import List, Tuple

try:
    import cairosvg
except ImportError:
    print("❌ cairosvg not found. Please install it:")
    print("   pip install cairosvg")
    exit(1)

conversions: List[Tuple[str, str, int]] = [
    ("quantum-bank-logo.svg", "quantum-bank-logo.png", 512),
    ("quantum-bank-logo.svg", "quantum-bank-logo-1024.png", 1024),
    ("quantum-bank-logo.svg", "quantum-bank-logo-256.png", 256),
    ("quantum-bank-logo.svg", "quantum-bank-logo-128.png", 128),
    ("quantum-bank-logo-white.svg", "quantum-bank-logo-white.png", 512),
    ("quantum-bank-logo-black.svg", "quantum-bank-logo-black.png", 512),
    ("favicon-16x16.svg", "favicon-16x16.png", 16),
    ("favicon-32x32.svg", "favicon-32x32.png", 32),
    ("apple-touch-icon.svg", "apple-touch-icon.png", 180),
]


def convert_svg_to_png():
    print("🎨 Converting SVG logos to PNG...\n")

    for input_file, output_file, size in conversions:
        try:
            if not os.path.exists(input_file):
                print(f"⚠️  Skipping {input_file} (file not found)")
                continue

            cairosvg.svg2png(
                url=input_file,
                write_to=output_file,
                output_width=size,
                output_height=size,
            )
            print(f"✓ Created {output_file} ({size}x{size})")
        except Exception as e:
            print(f"✗ Failed to convert {input_file}: {str(e)}")

    print("\n✨ Done! All PNGs created.")


if __name__ == "__main__":
    convert_svg_to_png()
