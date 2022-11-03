from typing import Any, Dict, Optional
import pymongo
import pandas as pd

from app.db import get_database
from app.modules.votes.schemas import StateVotingInfo, Candidate


class PredictionService:
    def __init__(self):
        self.db = get_database()

    def make_prediction(self, vote_obj: dict[str, Any]):
        """Calculates and saves a prediction based on the vote document.

        Args:
            vote_obj (dict[str, Any]): object containing the vote request json and the request time.
        """
        voting_info = vote_obj["request_json"]
        clean_voting_info = self._clean_voting_info(voting_info)
        try:
            prediction_df = self._calculate_prediction(clean_voting_info)
        except ZeroDivisionError:
            return
        prediction = {
            "lula": prediction_df.loc["Lula", "percentage"],
            "bolsonaro": prediction_df.loc["Jair Bolsonaro", "percentage"],
            "time_": vote_obj["request_time"],
        }
        self._save_prediction(prediction)

    def get_last_prediction(self) -> Optional[Dict[str, Any]]:
        """Fetch the last prediction from database.

        Returns:
            Optional[Dict[str, Any]]: The last prediction object
        """
        last_prediction = (
            self.db["predictions"].find().sort("time_", pymongo.DESCENDING).limit(1).next()
        )
        return last_prediction

    def get_all_predictions(self) -> Optional[list[Dict[str, Any]]]:
        """Fetches all predictions from database.

        Returns:
            Optional[list[Dict[str, Any]]]: A list of all predictions in the database.
        """
        all_predictions = list(self.db["predictions"].find().limit(36))
        return all_predictions

    def _get_all_states_voting_info(
        self, voting_info: list[Dict[str, Any]]
    ) -> list[StateVotingInfo]:
        """Gathers relevant information from all states.

        Args:
            voting_info (list[Dict[str, Any]]): The information returned in the voting request json.

        Returns:
            list[StateVotingInfo]: A list of relevant state voting information.
        """
        return [self._get_state_voting_info(state_voting_info) for state_voting_info in voting_info]

    def _get_state_voting_info(self, state_voting_info: Dict[str, Any]) -> StateVotingInfo:
        """Gets relevant voting information from one state.

        Args:
            state_voting_info (Dict[str, Any]): Voting information of one single state.

        Returns:
            StateVotingInfo: The relevand information of one state.
        """
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

    def _get_all_candidates_information(self, state_voting_info: Dict[str, Any]) -> list[Candidate]:
        """Gathers relevant information about all candidates.

        Args:
            state_voting_info (_type_): voting information of one single state

        Returns:
            list[Candidate]: Relevant information about all candidates.
        """
        candidates_info = state_voting_info["cand"]
        return [self._get_candidate_info(candidate_info) for candidate_info in candidates_info]

    def _get_candidate_info(self, candidate_info: Dict[str, Any]) -> Candidate:
        """Gets relevant information about one single candidate.

        Args:
            candidate_info (Dict[str, Any]): Relevant information about one candidate.

        Returns:
            Candidate: Object with relevant information about one candidate.
        """
        name = candidate_info["nm"].title()
        votes = int(candidate_info["vap"])
        percentage = float(candidate_info["pvap"].replace(",", "."))
        return Candidate(name=name, votes=votes, percentage_of_votes=percentage)

    def _clean_voting_info(self, voting_info: list[Dict[str, Any]]) -> list[StateVotingInfo]:
        """Wrapper function that cleans data (only keeps relevant data).

        Args:
            voting_info (list[Dict[str, Any]]): The information returned in the voting request json.

        Returns:
            list[StateVotingInfo]: A list of relevant state voting information.
        """
        return self._get_all_states_voting_info(voting_info)

    def _calculate_prediction(self, clean_voting_info: list[StateVotingInfo]) -> pd.DataFrame:
        """Calculates the final standings if each state's proportion of votes remained the same until the end of vote counting.

        Args:
            clean_voting_info (list[StateVotingInfo]): Only relevant information of the vote request.

        Returns:
            pd.Dataframe: A dataframe with the projected election results.
        """
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

    def _save_prediction(self, prediction: Dict[str, Any]) -> bool:
        """Saves a prediction to the database.

        Args:
            prediction (Dict[str, Any]): A dictionary with the prediction information.

        Returns:
            bool: True if successful.
        """
        self.db["predictions"].insert_one(prediction)
        return True
