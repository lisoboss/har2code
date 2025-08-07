"""Convert HAR data to Python code string."""

from typing import List

from .models import code as py_code


def code_to_str(codes: List[py_code.PythonCode], library: str = "httpx") -> str:
    """Convert code to string."""
    if library == "httpx":
        return to_httpx(codes)
    elif library == "requests":
        return to_requests(codes)
    else:
        raise ValueError(f"Unknown library: {library}")


def to_response(response: py_code.Response) -> List[str]:
    """Convert response to string."""
    code_str = []
    if response.status:
        comment = ['""""', f"Response: {response.httpVersion} {response.status}", ""]
        if response.headers:
            for header in response.headers:
                comment.append(f"{header.name}: {header.value}")
        if response.content:
            comment.append("")
            comment.append(response.content)
        comment.append('"""')
        code_str.append("\n".join(comment))
    return code_str


def to_request(request: py_code.Request) -> List[str]:
    """Convert request to string."""
    code_str = []
    code_str.append(f'url = "{request.url}"')
    if request.headers:
        code_str.append(f"headers = {request.headers!r}")
    else:
        code_str.append("headers = None")
    if request.cookies:
        code_str.append(f"cookies = {request.cookies!r}")
    else:
        code_str.append("cookies = None")
    if request.params:
        code_str.append(f"params = {request.params!r}")
    else:
        code_str.append("params = None")

    if request.data:
        code_str.append(f"data = {request.data!r}")
    else:
        code_str.append("data = None")

    if request.json:
        code_str.append(f"json = {request.json!r}")
    else:
        code_str.append("json = None")

    if request.files:
        code_str.append(f"files = {request.files!r}")
    else:
        code_str.append("files = None")
    return code_str


def to_code_head(code: py_code.PythonCode) -> List[str]:
    """Convert code head to string."""
    code_str = []
    code_str.append("############## ======== HAR2CODE ======== ###############")
    code_str.append(f"# timestamp: {code.timestamp}")
    code_str.append(f"# time: {code.time}")
    code_str.append(f"# datetime: {code.datetime}")
    code_str.append("#")
    return code_str


def to_code_tail(code: py_code.PythonCode) -> List[str]:
    """Convert code tail to string."""
    code_str = []
    code_str.append("")
    code_str.append("")
    return code_str


def to_httpx(codes: List[py_code.PythonCode]) -> str:
    """Convert HAR data to Python httpx code."""
    code_str = []
    code_str.append("import httpx")
    for code in codes:
        request = code.request
        response = code.response

        # code head
        code_str.extend(to_code_head(code))

        # request
        code_str.extend(to_request(request))
        code_str.append("with httpx.Client() as client:")
        code_str.append(
            f'    response = client.request("{request.method}", url, headers=headers, '
            f"cookies=cookies, params=params, data=data, json=json, files=files)"
        )

        # response
        code_str.extend(to_response(response))

        # code tail
        code_str.extend(to_code_tail(code))
    return "\n".join(code_str)


def to_requests(codes: List[py_code.PythonCode]) -> str:
    """Convert HAR data to Python requests code."""
    code_str = []
    code_str.append("import requests")
    for code in codes:
        request = code.request
        response = code.response

        # code head
        code_str.extend(to_code_head(code))

        # request
        code_str.extend(to_request(request))
        code_str.append(
            f'response = requests.request("{request.method}", url, headers=headers, '
            f"cookies=cookies, params=params, data=data, json=json, files=files)"
        )

        # response
        code_str.extend(to_response(response))

        # code tail
        code_str.extend(to_code_tail(code))
    return "\n".join(code_str)
