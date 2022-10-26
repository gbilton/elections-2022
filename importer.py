import asyncio
from datetime import datetime
from typing import Any, Coroutine, Dict, Optional
import pandas as pd
import httpx

from db import get_database
from exceptions import InvalidData, NotFound


class StateService:
    def import_states(self) -> None:
        """Imports a list of brazilian state from the internet to the database."""
        states = self._request_states()
        self._save_states({"states": states})

    def _request_states(self) -> list[str]:
        """Gets a list of all brazilian states.

        Returns:
            list[str]: A list of all brazilian states.
        """
        URL = (
            "https://www.oobj.com.br/bc/article/quais-os-c%C3%B3digos-de-cada-uf-no-brasil-465.html"
        )
        dfs = pd.read_html(URL)
        states = sorted(dfs[0]["UF"].to_list())
        self._validate_states(states)
        return states

    def _save_states(self, states: Dict[str, list[str]]) -> bool:
        """Saves all states to database if not already saved.

        Args:
            states (list[str]): list of all brazilian states
        """
        try:
            _ = self.get_states()
        except NotFound:
            db = get_database()
            db["states"].insert_one(states)
            return True
        return False

    def get_states(self) -> list[str]:
        """Fetches a list of states from the database.

        Raises:
            NotFound: raised if there are no states in the database.
            InvalidData: raised if the data from the database is incorrect.

        Returns:
            list[str]: A list of brazilian states.
        """
        db = get_database()
        states: Optional[Dict[str, list[str]]] = db["states"].find_one()
        if not states:
            raise NotFound("No states found.")

        state_list = states["states"]
        self._validate_states(state_list)
        return state_list

    def _validate_states(self, state_list: list[str]) -> None:
        """Checks if the state data is valid.

        Args:
            state_list (list[str]): The list of states.
        """
        self._validate_states_len(state_list)
        self._validate_states_name(state_list)

    def _validate_states_len(self, state_list: list[str]) -> None:
        """Checks if there are 27 states.

        Args:
            state_list (list[str]): The list of states.

        Raises:
            InvalidData: If there are not 27 states, the data is invalid.
        """
        if len(state_list) != 27:
            raise InvalidData("The number of states is incorrect.")

    def _validate_states_name(self, state_list: list[str]) -> None:
        """Checks if all state names have length of 2.

        Args:
            state_list (list[str]): A list with all states
        """
        for state_name in state_list:
            if len(state_name) != 2:
                raise InvalidData(f"Invalid state name: {state_name}")


class VoteService:
    def __init__(self, state_service: StateService):
        self.state_service = state_service

    async def import_votes(self):
        states = self.state_service.get_states()
        tasks = await self._create_tasks(states)
        votes = await asyncio.gather(*tasks)
        vote_obj = {"request_time": datetime.now(), "request_json": votes}
        self._save_votes(vote_obj)

    async def _request_votes(self, url: str) -> Any:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
        if r.status_code == 200:
            return r.json()

    async def _create_tasks(self, states: list[str]) -> list[Coroutine]:
        tasks = []
        for state in states:
            url = f"https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/{state.lower()}/{state.lower()}-c0001-e000544-r.json"
            tasks.append(self._request_votes(url))
        return tasks

    def _save_votes(self, vote_obj: Dict[str, Any]) -> bool:
        db = get_database()
        db["votes"].insert_one(vote_obj)
        return True

    def _calculate_prediction(self):
        pass

    def _save_prediction(self):
        pass


if __name__ == "__main__":
    state_service = StateService()
    state_service.import_states()
    vote_service = VoteService(state_service)
    asyncio.run(vote_service.import_votes())
