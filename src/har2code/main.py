"""Convert HAR data to Python code."""

import argparse
import json

from .mime import exts_type, load_custom_fallback_mime_map
from .parser import parse_codes
from .tostr import code_to_str


def main():
    """Convert HAR file to Python code."""
    parser = argparse.ArgumentParser(description="Convert HAR file to Python code.")
    parser.add_argument("har_file", help="Path to the HAR file.")
    parser.add_argument(
        "--library",
        choices=["requests", "httpx"],
        default="requests",
        help="Python library to use for the generated code. Default is requests.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding of the HAR file. Default is utf-8.",
    )
    parser.add_argument(
        "--no-files",
        type=exts_type,
        default="json",
        help=(
            "File extension of the response content to be not saved. etc. json,js; "
            "Default is json.",
        ),
    )
    parser.add_argument(
        "--fallback-mime-map",
        default=".fallback_mime_map.json",
        help=(
            "Path to a custom JSON file defining MIME type -> file extension mappings. "
            "The file should be a JSON object where keys are MIME types "
            'and values are extensions, e.g., {"application/wasm": ".wasm"}. '
            "If the file exists, it will override "
            "or extend the default FALLBACK_MIME_MAP."
        ),
    )
    args = parser.parse_args()
    load_custom_fallback_mime_map(args.fallback_mime_map)

    with open(args.har_file, "r", encoding="utf-8") as fp:
        har_data = json.load(fp)

    print(code_to_str(parse_codes(har_data, args.no_files), args.library))


if __name__ == "__main__":
    main()
