# fastapi 서버 실행하는법
### 1. 로컬로 레파지토리 땡겨오기
### 2. 로컬에 fastAPI와 uvicorn 설치하기
```python
pip install fastapi uvicorn
```
### 3. root directory(main.py가 있는 디렉토리리)에서 다음 실행
```python
python -m uvicorn main:app --reload
```