# 업로드된 파일을 전달받기 위해 먼저 python-multipart를 설치
# 업로드된 파일들은 '폼 데이터'의 형태로 전송

## File 임포트 ##
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}