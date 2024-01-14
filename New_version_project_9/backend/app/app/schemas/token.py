from typing import Optional

from pydantic import BaseModel

"""
https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
