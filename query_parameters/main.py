## 기본값 ##
# 경로 매개변수의 일부가 아닌 다른 함수 매개변수를 선언할 때, '쿼리' 매개변수로 자동으로 해석.
# 쿼리 매개변수는 경로에서 고정된 부분이 아니므로 선택절일 수 있고 기본값을 가질 수 있다.
from fastapi import FastAPI

app = FastAPI() 

fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]

@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


## 선택적 매개변수 ##
# 기본값을 None으로 설정하여 선택적 매개변수 선언 가능.
from typing import Union

@app.get('/items/{item_id}')
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {'item_id': item_id, 'q': q}
    return {'item_id': item_id}
    

## 쿼리 매개변수 형변환 ##
# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=True
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=yes
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


## 여러 경로/쿼리 매개변수 ##
# 특정 순서로 선언할 필요가 없다.
# 매개변수들은 이름으로 감지된다.
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item