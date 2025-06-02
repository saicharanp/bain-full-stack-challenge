from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class QueryHistory(Base):
    __tablename__ = 'query_history'

    id = Column(Integer, primary_key=True, index=True)
    source_address = Column(String)
    destination_address = Column(String)
    distance_km = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
