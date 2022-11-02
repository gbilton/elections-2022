from fastapi import APIRouter

from .services import PredictionService
from .schemas import Prediction

prediction_router = APIRouter()


@prediction_router.get("/predictions", response_model=list[Prediction])
async def get_predictions():
    """Fetch all predictions

    Returns:
        list[Prediction]: A list of predictions
    """
    prediction_service = PredictionService()
    predictions = prediction_service.get_all_predictions()
    return predictions


@prediction_router.get("/predictions/last", response_model=Prediction)
async def get_last_prediction():
    """Fetch the last prediction

    Returns:
        Prediction: The last prediction
    """
    prediction_service = PredictionService()
    last_prediction = prediction_service.get_last_prediction()
    return last_prediction
