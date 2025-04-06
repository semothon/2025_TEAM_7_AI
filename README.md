# README

## 가상환경 세팅하는 법
#### Windows
윈도우 환경에서는 evn 폴더의 yaml 파일을 통해 가상환경 설치 권장
```
conda env create -f ocr_evn.yaml
conda env create -f rec_evn.yaml
```
#### Linux
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

## fastapi 서버 실행하는법
#### 1. 로컬로 레파지토리 땡겨오기
#### 2. 로컬에 fastAPI와 uvicorn 설치하기
```python
pip install fastapi uvicorn
```
#### 3. root directory(main.py가 있는 디렉토리리)에서 다음 실행
```python
python -m uvicorn main:app --reload
```