"""Define the tools for MIME type."""

import cgi
import mimetypes
from typing import Tuple

_office_document = "application/vnd.openxmlformats-officedocument"
FALLBACK_MIME_MAP = {
    "application/json": ".json",
    "application/javascript": ".js",
    "application/xml": ".xml",
    "text/html": ".html",
    "text/plain": ".txt",
    "text/css": ".css",
    "text/markdown": ".md",
    "text/csv": ".csv",
    "application/x-www-form-urlencoded": ".txt",
    "application/octet-stream": ".bin",
    "application/x-protobuf": ".pb",
    "application/x-rar-compressed": ".rar",
    "application/zip": ".zip",
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "application/msword": ".doc",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.ms-powerpoint": ".ppt",
    _office_document + ".spreadsheetml.sheet": ".xlsx",
    _office_document + ".wordprocessingml.document": ".docx",
    _office_document + ".presentationml.presentation": ".pptx",
}


def mime_parse(mime: str | None) -> Tuple[str | None, str]:
    """Parse MIME type."""
    if mime is None:
        return None, "UTF-8"

    mime_type, params = cgi.parse_header(mime)
    encoding = params.get("charset") or "UTF-8"
    return mime_type, encoding


def mime_to_extension(mime: str) -> str:
    """Convert MIME type to extension."""
    if not mime:
        return ".bin"

    ext = mimetypes.guess_extension(mime)
    if ext:
        return ext

    if mime in FALLBACK_MIME_MAP:
        return FALLBACK_MIME_MAP[mime]

    return ".bin"
