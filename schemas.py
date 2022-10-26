from dataclasses import dataclass


@dataclass
class Candidate:
    name: str
    votes: int
    percentage_of_votes: float


@dataclass
class StateVotingInfo:
    state: str
    last_update_time: str
    percentage_of_votes_counted: float
    candidates: list[Candidate]
