import asyncio
from datetime import datetime
import time

from modules.predictions.services import PredictionService
from modules.votes.services import VoteService


async def collect(interval: int):
    """Collect new data every interval seconds.

    Args:
        interval (int): Interval in seconds.
    """
    prediction_service = PredictionService()
    vote_service = VoteService(prediction_service=prediction_service)
    while True:
        await vote_service.import_votes()
        print(datetime.strftime(datetime.now(), "%M:%S.%f")[:-3])
        time.sleep(interval)


if __name__ == "__main__":
    asyncio.run(collect(5 * 60))
