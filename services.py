import asyncio
from datetime import datetime
from typing import Any, Coroutine, Dict, Optional
import pandas as pd
import httpx

from db import get_database
from exceptions import InvalidData, NotFound
from schemas import Candidate, StateVotingInfo
from handler import worker


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


class PredictionService:
    def _get_all_states_voting_info(
        self, voting_info: list[Dict[str, Any]]
    ) -> list[StateVotingInfo]:
        return [self._get_state_voting_info(state_voting_info) for state_voting_info in voting_info]

    def _get_state_voting_info(self, state_voting_info: Dict[str, Any]) -> StateVotingInfo:
        last_update_time = state_voting_info["hg"]
        state = state_voting_info["cdabr"]
        percentage_of_votes_counted = float(state_voting_info["pst"].replace(",", "."))
        candidates = self._get_all_candidates_information(state_voting_info)

        return StateVotingInfo(
            last_update_time=last_update_time,
            state=state,
            percentage_of_votes_counted=percentage_of_votes_counted,
            candidates=candidates,
        )

    def _get_all_candidates_information(self, state_) -> list[Candidate]:
        candidates_info = state_["cand"]
        return [self._get_candidate_info(candidate_info) for candidate_info in candidates_info]

    def _get_candidate_info(self, candidate_info: Dict[str, Any]) -> Candidate:
        name = candidate_info["nm"].title()
        votes = int(candidate_info["vap"])
        percentage = float(candidate_info["pvap"].replace(",", "."))
        return Candidate(name=name, votes=votes, percentage_of_votes=percentage)

    def _clean_voting_info(self, voting_info: list[Dict[str, Any]]) -> list[StateVotingInfo]:
        return self._get_all_states_voting_info(voting_info)

    def calculate_prediction(self, clean_voting_info: list[StateVotingInfo]):
        result = []
        for state_voting_info in clean_voting_info:
            percentage_of_votes_counted = state_voting_info.percentage_of_votes_counted
            for candidate in state_voting_info.candidates:
                projected_votes = round(candidate.votes * 100 / percentage_of_votes_counted)
                result.append(
                    {
                        "name": candidate.name,
                        "projected_votes": projected_votes,
                        "state:": state_voting_info.state,
                    }
                )

        df = pd.DataFrame(result)
        projection_df = (
            df.groupby(["name"])
            .sum(numeric_only=True)
            .sort_values(by="projected_votes", ascending=False)
        )
        total_votes = projection_df["projected_votes"].sum()
        projection_df["percentage"] = projection_df["projected_votes"] / total_votes
        return projection_df

    def make_prediction(self, vote_obj: dict[str, Any]):
        voting_info = vote_obj["request_json"]
        clean_voting_info = self._clean_voting_info(voting_info)
        prediction_df = self.calculate_prediction(clean_voting_info)
        prediction = {
            "lula": prediction_df.loc["Lula", "percentage"],
            "bolsonaro": prediction_df.loc["Jair Bolsonaro", "percentage"],
            "time_": vote_obj["request_time"],
        }
        self.save_prediction(prediction)

    def save_prediction(self, prediction: Dict[str, Any]) -> bool:
        """Saves a prediction to the database.

        Args:
            prediction (Dict[str, Any]): A dictionary with the prediction information.

        Returns:
            bool: True if successful.
        """
        db = get_database()
        db["predictions"].insert_one(prediction)
        return True


class VoteService:
    def __init__(self, state_service: StateService, prediction_service: PredictionService):
        self.state_service = state_service
        self.prediction_service = prediction_service

    async def import_votes(self):
        """Asyncronously imports vote data to the database."""
        states = self.state_service.get_states()
        tasks = await self._create_tasks(states)
        voting_info = await asyncio.gather(*tasks)
        vote_obj = {"request_time": datetime.now(), "request_json": voting_info}
        self._save_votes(vote_obj)

        worker.enqueue(self.prediction_service.make_prediction, vote_obj)

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
            url = f"https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/{state.lower()}/{state.lower()}-c0001-e000544-r.json"
            tasks.append(self._request_votes(url))
        return tasks

    def _save_votes(self, vote_obj: Dict[str, Any]) -> bool:
        """Saves voting data to the database.

        Args:
            vote_obj (Dict[str, Any]): A dictionary containing voting data and the time of request.

        Returns:
            bool: True if successful.
        """
        db = get_database()
        db["votes"].insert_one(vote_obj)
        return True

    def get_last_vote(self):
        pass

    def get_all_votes(self):
        pass


if __name__ == "__main__":
    state_service = StateService()
    prediction_service = PredictionService()
    state_service.import_states()
    vote_service = VoteService(state_service=state_service, prediction_service=prediction_service)
    asyncio.run(vote_service.import_votes())
