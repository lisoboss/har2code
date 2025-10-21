"""Define the tools."""

from email.message import Message
from typing import Dict, Tuple


def parse_header(header_value: str) -> Tuple[str, Dict]:
    """Parse header value."""
    # 兼容替代 cgi.parse_header
    # 输入: 'text/html; charset=UTF-8'
    # 输出: ('text/html', {'charset': 'UTF-8'})

    msg = Message()
    # 这里加上前缀防止空格或冒号问题
    if ":" not in header_value:
        header_value = f"Content-Type: {header_value}"
    msg["Content-Type"] = header_value.split(":", 1)[1].strip()

    main_value = msg.get_content_type()
    params = {}
    msg_params = msg.get_params()
    if msg_params is not None:
        for k, v in msg_params[1:]:  # 第一个是主类型，后面才是参数
            params[k] = v

    return main_value, params
