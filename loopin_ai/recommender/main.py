from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from basemodels import *
import recommender as rec

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend")
def recommend(request: RecommendRequest):
    print("🙋‍♂️ user:", request.user.username)
    print("🧠 content:", request.content)
    
    party_list: list[dict] = [party.model_dump() for party in request.parties]
    result_list = rec.make_recommendation(party_list, request.content)
    return JSONResponse(content={"ids": result_list})
