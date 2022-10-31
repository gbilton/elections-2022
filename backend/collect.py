import asyncio
from datetime import datetime
import time
from services import PredictionService, StateService, VoteService


async def main(interval: int):
    """Collect new data every interval seconds.

    Args:
        interval (int): Interval in seconds.
    """
    while True:
        state_service = StateService()
        prediction_service = PredictionService()
        state_service.import_states()
        vote_service = VoteService(
            state_service=state_service, prediction_service=prediction_service
        )
        await vote_service.import_votes()
        print(datetime.strftime(datetime.now(), "%M:%S.%f")[:-3])
        time.sleep(interval)


if __name__ == "__main__":
    asyncio.run(main(5 * 60))
