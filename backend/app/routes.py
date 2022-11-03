from fastapi import FastAPI

from app.modules.predictions.routes import prediction_router


def init_app(app: FastAPI):
    app.include_router(prediction_router, tags=["Predictions"])
