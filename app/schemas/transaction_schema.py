from typing import Any

from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    id: str
    trn_hash: str
    uid: str
    type: str
    amount: str

    timestamp: datetime

    class Config:
        from_orm = True
