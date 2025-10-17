"""Define the data model for HAR data."""

# HAR file format
# see https://w3c.github.io/web-performance/specs/HAR/Overview.html#sec-har-encoding
#

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dacite import from_dict


@dataclass
class Cookie:
    """
    Define the data model for HAR cookie.

    @property name [string] - The name of the cookie.
    @property value [string] - The cookie value.
    @property path [string, optional] - The path pertaining to the cookie.
    @property domain [string, optional] - The host of the cookie.
    @property expires [string, optional] - Cookie expiration time.
        (ISO 8601 - YYYY-MM-DDThh:mm:ss.sTZD, e.g. 2009-07-24T19:20:30.123+02:00).
    @property httpOnly [boolean, optional] - Set to true if the cookie is HTTP only,
        false otherwise.
    @property secure [boolean, optional] (new in 1.2) - True if the cookie was
        transmitted over ssl, false otherwise.
    @property comment [string, optional] (new in 1.2) - A comment provided by the
        user or the application.
    """

    name: str
    value: str
    path: Optional[str]
    domain: Optional[str]
    expires: Optional[str]
    httpOnly: Optional[bool]
    secure: Optional[bool]
    comment: Optional[str]


@dataclass
class Header:
    """Define the data model for HAR header."""

    name: str
    value: str
    comment: Optional[str]


@dataclass
class queryString:
    """Define the data model for HAR queryString."""

    name: str
    value: str
    comment: Optional[str]


@dataclass
class Param:
    """
    Define the data model for HAR param.

    @property name [string] - name of a posted parameter.
    @property value [string, optional] - value of a posted parameter or content of
        a posted file.
    @property fileName [string, optional] - name of a posted file.
    @property contentType [string, optional] - content type of a posted file.
    @property comment [string, optional] (new in 1.2) - A comment provided by
        the user or the application.

    List of posted parameters, if any (embedded in <postData> object).
    """

    name: str
    value: Optional[str]
    fileName: Optional[str]
    contentType: Optional[str]
    comment: Optional[str]


@dataclass
class Content:
    """
    Define the data model for HAR content.

    @property size [number] - Length of the returned content in bytes.
        Should be equal to response.bodySize if there is no compression
        and bigger when the content has been compressed.
    @property compression [number, optional] - Number of bytes saved.
        Leave out this field if the information is not available.
    @property mimeType [string] - MIME type of the response text
        (value of the Content-Type response header).
        The charset attribute of the MIME type is included (if available).
    @property text [string, optional] - Response body sent from the server
        or loaded from the browser cache.
        This field is populated with textual content only.
        The text field is either HTTP decoded text or a encoded (e.g. "base64")
        representation of the response body.
        Leave out this field if the information is not available.
    @property encoding [string, optional] (new in 1.2) - Encoding used for response
        text field e.g "base64".
        Leave out this field if the text field is HTTP decoded
        (decompressed & unchunked),
        than trans-coded from its original character set into UTF-8.
    @property comment [string, optional] (new in 1.2) - A comment provided by the user
        or the application.

    Before setting the text field, the HTTP response is decoded
        (decompressed & unchunked),
        than trans-coded from its original character set into UTF-8. Additionally,
        it can be encoded using e.g. base64. Ideally,
        the application should be able to unencode a base64 blob
        and get a byte-for-byte identical resource to
        what the browser operated on.

    @example
    <html><head></head><body/></html>
    {
        "size": 33,
        "compression": 0,
        "mimeType": "text/html; charset=utf-8",
        "text": "PGh0bWw+PGhlYWQ+PC9oZWFkPjxib2R5Lz48L2h0bWw+XG4=",
        "encoding": "base64",
        "comment": ""
    }
    """

    size: Optional[int]
    compression: Optional[int]
    mimeType: Optional[str]
    text: Optional[str]
    encoding: Optional[str]
    comment: Optional[str]


# NOTE: 此类暂时未启用，计划在后续版本中实现
@dataclass
class Cache:
    """
    Define the data model for HAR cache.

    @property beforeRequest [object, optional] - State of a cache entry before
        the request. Leave out this field if the information is not available.
    @property afterRequest [object, optional] - State of a cache entry after
        the request. Leave out this field if the information is not available.
    @property comment [string, optional] (new in 1.2) - A comment provided by
        the user or the application.
    """

    beforeRequest: Optional[Dict[str, Any]]
    afterRequest: Optional[Dict[str, Any]]
    comment: Optional[str]


@dataclass
class PostData:
    """
    Define the data model for HAR postData.

    @property mimeType [string] - Mime type of posted data.
    @property params [array] - List of posted parameters
        (in case of URL encoded parameters).
    @property text [string] - Plain text posted data
    @property comment [string, optional] (new in 1.2)
        - A comment provided by the user or the application.

    Note that text and params fields are mutually exclusive.
    """

    mimeType: Optional[str]
    params: Optional[List[Param]]
    text: Optional[str]
    comment: Optional[str]


@dataclass
class Request:
    """Define the data model for HAR request."""

    method: str
    url: str
    httpVersion: str
    cookies: List[Cookie]
    headers: List[Header]
    queryString: List[queryString]
    postData: Optional[PostData]
    headersSize: int
    bodySize: int


@dataclass
class Response:
    """Define the data model for HAR response."""

    _charlesStatus: Optional[str]  # Only for Charles Proxy
    status: int
    statusText: Optional[str]
    httpVersion: str
    cookies: List[Cookie]
    headers: List[Header]
    content: Content
    redirectURL: Optional[str]
    headersSize: int
    bodySize: int


@dataclass
class Entry:
    """Define the data model for HAR entry."""

    startedDateTime: str
    time: int
    request: Request
    response: Response
    cache: Cache
    timings: Dict[str, Any]


@dataclass
class Har:
    """Define the data model for HAR file."""

    entries: List[Entry]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Har":
        """Convert HAR data to Python code."""
        return from_dict(data_class=cls, data=data.get("log", {}))
