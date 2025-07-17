# README
## 프로젝트 설명

2025 경희대학교 세모톤 7팀이 개발한 Loopin의 AI 모듈입니다. FAST API 패키지를 이용해 Backend Server로부터 받은 요청을 처리합니다.

### Loopin이란?
대학생들을 위한 실명 기반 취미 모임 플랫폼입니다.

### /ocr
학생증 이미지를 읽어 학교 인증 및 학과 정보 추출을 수행합니다.
- OpenCV 기반 이미지 전처리 및 윤곽선 추출
- EasyOCR을 활용한 문자 인식
- 주의: 경희대학교 학생증만 지원(색상 평균값으로 신형/구형 구분 가능)

### /recommender
사용자가 텍스트로 원하는 모임에 대한 설명을 입력하면 LLM을 통해 처리, 등록된 모임 중 설명에 가장 부합하는 모임을 1~5개 추천해줍니다.
- 사용자 정보와 자연어 텍스트로 된 원하는 모임에 대한 설명을 입력받아 모임을 추천해주는 기능을 수행합니다.
- Lang-Cahin을 이용해 자연어로 구성된 요청 사항과 구조화된 모임 정보들을 비교하여 요청과 유사한 모임들의 ID를 반환해줍니다.

---

## 설치 방법

### 가상환경 세팅

##### Windows
윈도우 환경에서는 evn 폴더의 yaml 파일을 통해 가상환경 설치 권장
```
conda env create -f ocr_evn.yaml
conda env create -f rec_evn.yaml
```

##### Linux
ocr 의존 패키지
```
conda create -n semothon_team_7_ocr python=3.11

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install easyocr
pip install matplotlib
pip install imutils
```
recommender 의존 패키지
```
conda create -n semothon_team_7_rec python=3.11.11
conda activate semothon_team_7_rec

conda install fastapi uvicorn
conda install langchain -c conda-forge
pip install langchain-openai
pip install tiktoken
conda install python-dotenv
```

### fastapi 서버 실행
1. 로컬로 저장소 클론
2. 로컬에 fastAPI와 uvicorn 설치
```python
pip install fastapi uvicorn
```
3. root directory(main.py가 있는 디렉토리)에서 다음 실행
```python
python -m uvicorn main:app --reload
```