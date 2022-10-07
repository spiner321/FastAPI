from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# app.get('/')은 FastAPI에게 바로 아래에 있는 함수가 다음으로 이동하는 요청을 처리한다는 것을 알려준다.
@app.get('/') # 경로 동작 데코레이터
async def root():
    return {'message': 'Hello World'}