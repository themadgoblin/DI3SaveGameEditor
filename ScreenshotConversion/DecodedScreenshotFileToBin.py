#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

def extract_hex_blob(text: str) -> str:
    """
    Extracts the hex data between SCREENSHOT = $ and the next $.
    """
    pattern = re.compile(r'SCREENSHOT\s*=\s*\$(.*?)\$', re.DOTALL)
    match = pattern.search(text)
    if not match:
        raise ValueError("Could not find a hex blob after SCREENSHOT = $")
    hex_blob = match.group(1)
    return re.sub(r'\s+', '', hex_blob)

def extract_value(text: str, key: str) -> str:
    """
    Extracts the integer value for a given key, e.g. SCREENSHOT_WIDTH = 424
    """
    pattern = re.compile(rf'{re.escape(key)}\s*=\s*(\d+)')
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Could not find value for {key}")
    return match.group(1)

def main():
    p = argparse.ArgumentParser(
        description="Extract hex blob after SCREENSHOT, save as binary, and print dimensions."
    )
    p.add_argument("input_file", type=Path, help="Path to the input text file")
    p.add_argument(
        "-o", "--output", type=Path,
        help="Path for the output .bin file (defaults to same name as input with .bin)"
    )
    args = p.parse_args()

    # Read the entire file
    try:
        content = args.input_file.read_text()
    except Exception as e:
        print(f"Error reading {args.input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract width and height
    try:
        width  = extract_value(content, "SCREENSHOT_WIDTH")
        height = extract_value(content, "SCREENSHOT_HEIGHT")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract and clean hex blob
    try:
        hex_data = extract_hex_blob(content)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to bytes
    try:
        bin_data = bytes.fromhex(hex_data)
    except ValueError as e:
        print(f"Error converting hex to binary: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    out_path = args.output or args.input_file.with_suffix(".bin")

    # Write binary data
    try:
        out_path.write_bytes(bin_data)
    except Exception as e:
        print(f"Error writing to {out_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Print results
    print(f"Wrote {len(bin_data)} bytes to {out_path}")
    print(f"SCREENSHOT_WIDTH  = {width}")
    print(f"SCREENSHOT_HEIGHT = {height}")

if __name__ == "__main__":
    main()
