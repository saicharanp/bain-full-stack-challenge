from pydantic import BaseModel
from datetime import datetime
from typing import List

class DistanceRequest(BaseModel):
    source: str
    destination: str

class DistanceResponse(BaseModel):
    distance_km: float

class QueryHistoryResponse(BaseModel):
    source: str
    destination: str
    distance_km: float
    timestamp: datetime

    class Config:
        orm_mode = True
