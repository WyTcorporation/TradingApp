from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str