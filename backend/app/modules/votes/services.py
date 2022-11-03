import asyncio
from datetime import datetime
import httpx
from typing import Any, Coroutine, Dict, Optional

from app.db import get_database
from app.modules.predictions.services import PredictionService
from app.handler import worker

from .defaults import brazilian_states


class VoteService:
    def __init__(self, prediction_service: PredictionService):
        self.db = get_database()
        self.prediction_service = prediction_service

    async def import_votes(self):
        """Asyncronously imports vote data to the database."""
        states = brazilian_states
        tasks = await self._create_tasks(states)
        voting_info = await asyncio.gather(*tasks)
        vote_obj = {"request_time": datetime.now(), "request_json": voting_info}
        self._save_votes(vote_obj)

        worker.enqueue(self.prediction_service.make_prediction, vote_obj)

    def get_last_vote(self) -> Optional[Dict[str, Any]]:
        """Fetches the last vote document from the database.

        Returns:
            Dict[str, Any]: The last vote document.
        """

        last_vote_obj = self.db["votes"].find().sort("date", -1).limit(1).next()
        return last_vote_obj

    def get_all_votes(self) -> Optional[list[Dict[str, Any]]]:
        """Fetches all the vote documents in the database.

        Returns:
            Optional[list[Dict[str, Any]]]: A list containing all the vote documents in the database.
        """

        return list(self.db["votes"].find({}))

    async def _request_votes(self, url: str) -> Any:
        """Asyncronously requests voting data.

        Args:
            url (str): The request url

        Returns:
            Any: Json data of the request.
        """
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
        if r.status_code == 200:
            return r.json()

    async def _create_tasks(self, states: list[str]) -> list[Coroutine]:
        """Creates multiple tasks to be executed concurrently.

        Args:
            states (list[str]): A list of states.

        Returns:
            list[Coroutine]: list of Coroutines to be executed concurrently.
        """
        tasks = []
        for state in states:
            url = f"https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/{state.lower()}/{state.lower()}-c0001-e000545-r.json"
            tasks.append(self._request_votes(url))
        return tasks

    def _save_votes(self, vote_obj: Dict[str, Any]) -> bool:
        """Saves voting data to the database.

        Args:
            vote_obj (Dict[str, Any]): A dictionary containing voting data and the time of request.

        Returns:
            bool: True if successful.
        """

        self.db["votes"].insert_one(vote_obj)
        return True
