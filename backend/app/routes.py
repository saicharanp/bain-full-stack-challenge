from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import QueryHistory
from .schemas import DistanceRequest, DistanceResponse, QueryHistoryResponse
from .utils import geocode, haversine
from .database import get_db

router = APIRouter()

@router.post("/distance", response_model=DistanceResponse)
async def get_distance(data: DistanceRequest, db: AsyncSession = Depends(get_db)):
    try:
        src_coords = await geocode(data.source)
        if not src_coords:
            raise HTTPException(status_code=400, detail="Invalid source address")
        dest_coords = await geocode(data.destination)
        if not dest_coords:
            raise HTTPException(status_code=400, detail="Invalid destination address")
        dist = haversine(src_coords[0], src_coords[1], dest_coords[0], dest_coords[1])
        new_query = QueryHistory(
            source_address=data.source,
            destination_address=data.destination,
            distance_km=dist
        )
        db.add(new_query)
        await db.commit()
        return {"distance_km": dist}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[QueryHistoryResponse])
async def get_history(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(limit))
    records = result.scalars().all()
    return records
