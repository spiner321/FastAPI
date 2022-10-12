# 코드의 가독성을 위해 type hint를 제공하는 class 생성

from pydantic import BaseModel #  type hint를 제공하는 모듈
from typing import Union

class BlogText(BaseModel):
    id: int
    text: str
    ad: Union[int, None] = None
    probability: Union[float, None] = None