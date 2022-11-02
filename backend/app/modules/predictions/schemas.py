from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prediction:
    bolsonaro: str
    lula: str
    time_: datetime
