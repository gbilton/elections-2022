import asyncio
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services import PredictionService, StateService, VoteService


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/predictions")
async def get_predictions():
    pass


@app.get("/predictions/last")
async def get_last_prediction():
    pass
