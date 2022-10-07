from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# app.get('/')은 FastAPI에게 바로 아래에 있는 함수가 다음으로 이동하는 요청을 처리한다는 것을 알려준다.
@app.get('/') # 경로 동작 데코레이터
async def root():
    return {'message': 'Hello World'}


## 타입이 있는 매개변수 ##
# "매개변수" 또는 "변수"를 경로에 선언할 수 있다.
@app.get('/items/{item_id}')
async def read_item(item_id: int): # 경로 매개변수 타입 선언 가능
    return {'item_id': item_id}
    

## 순서 문제 ##
# 경로 동작은 순차적으로 평가되므로 고정 경로를 먼저 선언해야 한다.
# 고정 경로를 먼저 선언하지 않을 경우 매개변수의 값을 me라고 인식한다.
@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}

@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


## 사전 정의 값 ##
# str과 Enum을 상속하는 서브 클래스
# str을 상속함으로써 API문서는 값이 str형이어야 하는 것을 알게 되고 제대로 렌더링할 수 있게 된다.
class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'
    
@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet: # 열거체 ModelName의 열거형 멤버
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": # 열거형 값 가져오기
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


## 경로를 포함하는 경로 매개변수 ##
@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}