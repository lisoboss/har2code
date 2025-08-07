"""Convert HAR data to Python code."""

import argparse
import json

from .parser import parse_codes
from .tostr import code_to_str


def main():
    """Convert HAR file to Python code."""
    parser = argparse.ArgumentParser(description="Convert HAR file to Python code.")
    parser.add_argument("har_file", help="Path to the HAR file.")
    parser.add_argument(
        "--library",
        choices=["requests", "httpx"],
        default="httpx",
        help="Python library to use for the generated code.",
    )
    args = parser.parse_args()

    with open(args.har_file, "r") as f:
        har_data = json.load(f)

    print(code_to_str(parse_codes(har_data), args.library))


if __name__ == "__main__":
    main()
