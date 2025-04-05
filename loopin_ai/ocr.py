import easyocr
import torch
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import ImageFont, ImageDraw, Image
from enum import Enum
import idcard

class University(Enum):
    UNKNOWN = 0
    KYUNGHEE = 1



# easyocr은 tesseract보다 느리지만 다중언어 인식이 뛰어나고 인식률이 높다.

# 샘플 이미지 위치
SAMPLE_IMAGE_PATH = Path(__file__).parent.parent / Path('img/sample1.jpg')
DEPARTMENT_DATA_PATH = Path(__file__).parent.parent / Path('data/departments.csv')
dapartments_table = np.loadtxt(str(DEPARTMENT_DATA_PATH), dtype=str, delimiter=',', encoding='utf-8')
print(dapartments_table[1][2])

# 이미지 파일 읽기
# 파일 경로 대신 OpenCV image object(numpy array) 또는 이미지 파일을 바이트로 전달할 수도 있다.
src:np.ndarray = cv2.imread(str(SAMPLE_IMAGE_PATH))
if src is None:
    print("Image load failed!")
    sys.exit()

# 학교명 탐색
reader = easyocr.Reader(['en', 'ko'], gpu=torch.cuda.is_available())
result = reader.readtext(src, detail = 1)
university = University.UNKNOWN
for i, elem in enumerate(result):
    text = elem[1]
    intersection = len(set.intersection(*[set("KYUNG HEE"), set(text)]))
    union = len(set.union(*[set("KYUNG HEE"), set(text)]))
    jaccard_similarity = intersection / float(union)
    print(f"Jaccard Similarity: {jaccard_similarity:.2f}")
    if jaccard_similarity > 0.75:
        university = University.KYUNGHEE
        break
print(f"University: {university.name}")

# 이미지 전처리: 회색조 변환, 가우시안 블러, 캐니 엣지 검출
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3,), 0)
edged = cv2.Canny(gray, 75, 200)

# 오츠 알고리즘 이진화 후 윤곽선 검출
ret, otsu = cv2.threshold(gray, -1,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(otsu, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

origin_area = src.shape[0] * src.shape[1]
min_area = origin_area * 0.5  # 최소 면적 설정
max_area = origin_area * 0.99  # 최대 면적 설정

# 설정한 면적 범위 안에서 외곽선 찾으면 크롭, 아니면 원본 이미지 전체를 학생증으로 인식
crop_img = src.copy()
for cnt in contours:
    area = cv2.contourArea(cnt)
    if min_area < area < max_area: # 학생증 영역을 찾기 위한 면적 범위
        x, y, width, height = cv2.boundingRect(cnt)
        crop_img = crop_img[y:y+height, x:x+width]
        break

# 신형 학생증이면 선명한 붉은톤, 구형 학생증이면 흰 톤
b, g, r = cv2.split(crop_img)
plt.imshow(crop_img)
plt.show()
is_legacy_card = b.mean() + g.mean() > r.mean()
id_card: idcard.IDCard = None
print(university)
if(university == University.KYUNGHEE):
    if is_legacy_card:
        print("Legacy ID Card detected.")
        id_card = idcard.KyungheeLagacy(crop_img)
    else:
        print("New ID Card detected.")
        # id_card = idcard.Kyunghee(crop_img)
else:
    print("Unknown ID Card detected.")