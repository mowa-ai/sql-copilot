import datetime
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd


class MessageType(Enum):
    AI = "AI"
    USER = "User"


@dataclass
class MessagePayload:
    text: str | None = None
    code: str | None = None
    df: pd.DataFrame | None = None
    active: bool | None = None


@dataclass
class Message:
    message_type: MessageType
    payload: MessagePayload
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
