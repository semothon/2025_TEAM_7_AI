# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ocr import OCR
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/univ-auth")
async def receive_image(file: UploadFile = File(...)):
    # 파일 이름과 content type 확인
    print(f"받은 파일: {file.filename}, 타입: {file.content_type}")
    # 파일 저장
    contents = await file.read()
    with open(f"uploaded_{file.filename}", "wb") as f:
        f.write(contents)
    # 이미지 로드
    img = cv2.imread(f"uploaded_{file.filename}")
    if img is None:
        return JSONResponse(content={
            "success": False,
            "filename": file.filename,
            "message": "서버에서 이미지를 읽는 데 실패했습니다."
        })
    # OCR 수행
    ocr = OCR()
    success, student_info = ocr.run(img)
    # OCR 결과 반환
    return JSONResponse(content={
        "success": success,
        "message": "University ID Card OCR Data",
        "data": student_info
    })