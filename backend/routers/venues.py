from fastapi import APIRouter, HTTPException
from models.venue import Venue
from database import get_venue, list_venues

router = APIRouter()


@router.get("/venues", response_model=list[Venue])
async def get_venues():
    """List all configured venues."""
    return await list_venues()


@router.get("/venues/{venue_id}", response_model=Venue)
async def get_venue_by_id(venue_id: str):
    """Get a single venue by ID."""
    venue = await get_venue(venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
