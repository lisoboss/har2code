"""Define the data model for Python code."""

from dataclasses import dataclass
from typing import Any, Dict, List

from . import har


@dataclass
class Flie:
    """Define the data model for file."""

    file_name: str
    filename: str

    def __str__(self):
        """Convert file to string."""
        return f"({self.file_name!r}, open({self.filename!r}, 'rb'))"

    def __repr__(self):
        """Convert file to string."""
        return self.__str__()


@dataclass
class Cookie:
    """Define the data model for cookie."""

    name: str
    value: str
    path: str
    domain: str
    expires: str
    httpOnly: bool
    secure: bool


@dataclass
class Request:
    """Define the data model for request."""

    method: str
    url: str
    headers: Dict[str, Any]
    cookies: List[Cookie]
    params: Dict[str, Any]
    data: Dict[str, Any]
    json: Dict[str, Any]
    files: Dict[str, Any]


@dataclass
class Response:
    """Define the data model for response."""

    status: int
    httpVersion: str
    headers: List[har.Header]
    content: str


@dataclass
class PythonCode:
    """Define the data model for python code."""

    time: str
    request: Request
    response: Response
