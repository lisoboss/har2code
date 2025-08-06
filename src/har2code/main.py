"""Convert HAR data to Python code."""

import argparse
import json
from typing import Any, Dict


def har_to_code(har_data: Dict[str, Any], library: str = "httpx") -> str:
    """Convert HAR data to Python code."""
    code = []
    for entry in har_data.get("log", {}).get("entries", []):
        request = entry.get("request", {})
        method = request.get("method", "GET")
        url = request.get("url", "")
        headers = {h["name"]: h["value"] for h in request.get("headers", [])}
        cookies = {c["name"]: c["value"] for c in request.get("cookies", [])}
        params = {p["name"]: p["value"] for p in request.get("queryString", [])}

        if library == "requests":
            code.append("import requests")
            code.append(f'url = "{url}"')
            if headers:
                code.append(f"headers = {json.dumps(headers, indent=4)}")
            if cookies:
                code.append(f"cookies = {json.dumps(cookies, indent=4)}")
            if params:
                code.append(f"params = {json.dumps(params, indent=4)}")

            code.append(
                f'response = requests.request("{method}", url, headers=headers, '
                f"cookies=cookies, params=params)"
            )
        else:  # httpx
            code.append("import httpx")
            code.append(f'url = "{url}"')
            if headers:
                code.append(f"headers = {json.dumps(headers, indent=4)}")
            if cookies:
                code.append(f"cookies = {json.dumps(cookies, indent=4)}")
            if params:
                code.append(f"params = {json.dumps(params, indent=4)}")

            code.append("with httpx.Client() as client:")
            code.append(
                f'    response = client.request("{method}", url, headers=headers, '
                f"cookies=cookies, params=params)"
            )

    return "\n".join(code)


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

    code = har_to_code(har_data, args.library)
    print(code)


if __name__ == "__main__":
    main()
