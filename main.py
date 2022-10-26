from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import Prediction

from services import PredictionService


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/predictions", response_model=list[Prediction])
async def get_predictions():
    """Fetch all predictions

    Returns:
        list[Prediction]: A list of predictions
    """
    prediction_service = PredictionService()
    predictions = prediction_service.get_all_predictions()
    return predictions


@app.get("/predictions/last", response_model=Prediction)
async def get_last_prediction():
    """Fetch the last prediction

    Returns:
        Prediction: The last prediction
    """
    prediction_service = PredictionService()
    last_prediction = prediction_service.get_last_prediction()
    return last_prediction
