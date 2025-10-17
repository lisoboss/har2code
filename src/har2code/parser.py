"""Define the parser tools."""

import base64
import json
import secrets
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

from .mime import guess_extension, mime_parse
from .models import code, har

OUTPUT = Path("out")
OUTPUT.mkdir(exist_ok=True)
with open(OUTPUT / ".gitignore", "w") as f:
    f.write("*")


def parse_content(content: har.Content, exclude_exts: List[str], url_path: str) -> str:
    """Parse content and add code to the list."""
    mime, encoding = mime_parse(content.mimeType)
    content_encoding = content.encoding
    content_text = content.text or ""
    raw_content = None
    filename = None

    if content.size is not None and content.size > 0:
        ext = guess_extension(mime, url_path)

        if content_encoding is not None and content_encoding == "base64":
            raw_content = base64.b64decode(content_text or "")

        if ext.lstrip(".") not in exclude_exts:
            if raw_content is None:
                raw_content = content_text.encode()

            filename = OUTPUT / f"binary-{secrets.token_hex(4)}{ext}"
        else:
            if raw_content is not None:
                try:
                    content_text = raw_content.decode(encoding)
                except UnicodeDecodeError:
                    # fallback: 保存为 bin
                    filename = OUTPUT / f"unknown-{secrets.token_hex(4)}.bin"

        if filename is not None and raw_content is not None:
            with open(filename, "wb") as f:
                f.write(raw_content)
            content_text = f"=== Save to file: {filename} ==="

    return content_text or ""


def parse_post_data(post_data: har.PostData | None) -> dict[str, Any]:
    """Parse post data and add code to the list."""
    data: dict[str, Any] | str | None = None
    json_dict: dict[str, Any] | None = None
    files: dict[str, Any] | None = None

    if not post_data:
        return dict(data=data, json=json_dict, files=files)

    mime, _ = mime_parse(post_data.mimeType)

    params = post_data.params
    text = post_data.text

    if mime is None:
        data = text
    elif mime.startswith("application/json"):
        try:
            json_dict = json.loads(text or "")
        except Exception:
            data = text  # fallback
    elif mime.startswith("application/x-www-form-urlencoded"):
        data = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(text).items()}
    elif mime.startswith("multipart/form-data"):
        data = {}
        files = {}
        for param in params or []:
            name = param.name
            file_name = param.fileName
            value = param.value
            if file_name:
                # 模拟文件上传，value 是文件内容
                filename = (
                    OUTPUT
                    / f"binary-{secrets.token_hex(4)}-{file_name.replace('/', '_')}"
                )
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(value or ""))
                files[name] = code.Flie(file_name, str(filename))
            else:
                data[name] = value
    else:
        data = text or None
    return dict(
        data=data,
        json=json_dict,
        files=files,
    )


def parse_param(queries: List[har.queryString]) -> Dict[str, Any]:
    """Parse header and add code to the list."""
    return {query.name: query.value for query in queries}


def parse_header(headers: List[har.Header]) -> Dict[str, Any]:
    """Parse header and add code to the list."""
    return {header.name: header.value for header in headers}


def parse_cookie(cookie: har.Cookie) -> code.Cookie | None:
    """Parse cookie and add code to the list."""
    if cookie:
        return code.Cookie(**asdict(cookie))  # ✅ 安全转换
    else:
        return None


def parse_response(
    response: har.Response, exclude_exts: List[str], url_path: str
) -> code.Response:
    """Parse response and add code to the list."""
    return code.Response(
        status=response.status,
        httpVersion=response.httpVersion,
        headers=response.headers,
        content=parse_content(response.content, exclude_exts, url_path),
    )


def parse_request(request: har.Request) -> code.Request:
    """Parse request and add code to the list."""
    kwargs = dict(
        method=request.method,
        url=request.url,
        headers=parse_header(request.headers),
        cookies=[
            cookie
            for cookie in [parse_cookie(cookie) for cookie in request.cookies]
            if cookie
        ],
        params=parse_param(request.queryString),
        **parse_post_data(request.postData),
    )
    return code.Request(**kwargs)


def parse_codes(
    har_data: Dict[str, Any], exclude_exts: List[str]
) -> List[code.PythonCode]:
    """Parse HAR data to Python code."""
    entries = har.Har.from_dict(har_data).entries
    codes = []
    for entry in entries:
        codes.append(
            code.PythonCode(
                timestamp=datetime.fromisoformat(entry.startedDateTime).timestamp(),
                time=f"{entry.time}, {entry.startedDateTime}",
                datetime=entry.startedDateTime,
                request=parse_request(entry.request),
                response=parse_response(
                    entry.response, exclude_exts, urlparse(entry.request.url).path
                ),
            )
        )
    return sorted(codes, key=lambda x: x.timestamp)
