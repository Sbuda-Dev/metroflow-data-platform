from pydantic import BaseModel
from typing import Any

class EventRequest (BaseModel):

    event_type: str
    source : str
    payload: dict[str, Any]