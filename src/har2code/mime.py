"""Define the tools for MIME type."""

import json
import mimetypes
import os
from typing import List, Optional, Tuple

from .utils import parse_header

_office_document = "application/vnd.openxmlformats-officedocument"
FALLBACK_MIME_MAP = {
    "application/json": ".json",
    "application/javascript": ".js",
    "application/x-javascript": ".js",
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


def load_custom_fallback_mime_map(filename: str) -> None:
    """Load custom MIME types."""
    try:
        with open(filename, "rb") as fp:
            FALLBACK_MIME_MAP.update(json.load(fp))
    except FileNotFoundError:
        pass


def mime_parse(mime: str | None) -> Tuple[str | None, str]:
    """Parse MIME type."""
    if mime is None:
        return None, "UTF-8"

    mime_type, params = parse_header(mime)
    encoding = params.get("charset") or "UTF-8"
    return mime_type, encoding


def guess_extension_from_mime(mime: Optional[str]) -> Optional[str]:
    """Convert MIME type to extension."""
    if not mime:
        return None

    ext = mimetypes.guess_extension(mime)
    if ext:
        return ext

    if mime in FALLBACK_MIME_MAP:
        return FALLBACK_MIME_MAP[mime]

    return None


def guess_extension_from_url_path(path: str) -> Optional[str]:
    """Guess extension from URL path."""
    ext = os.path.splitext(path)[1].lower()
    if ext:
        return ext

    return None


def guess_extension(mime: Optional[str], path: str) -> str:
    """Guess extension from MIME type and URL path."""
    uext = guess_extension_from_url_path(path)
    mext = guess_extension_from_mime(mime)

    if (
        uext != mext
        and uext is not None
        and mext is not None
        and uext not in mimetypes.types_map
    ):
        uext = None

    return uext or mext or ".bin"


def exts_type(exts: str) -> List[str]:
    """Convert exts to list."""
    # "json,js" -> ["json","js"]
    return list(set([e.strip().lstrip(".") for e in exts.split(",") if e.strip()]))
