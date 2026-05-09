from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Venue(BaseModel):
    id: str
    name: str
    brand_voice: Optional[str] = None
    tone_keywords: Optional[List[str]] = None
    avoid_words: Optional[List[str]] = None
    primary_color: Optional[str] = None
    drive_folder_id: Optional[str] = None
    created_at: Optional[datetime] = None


class VenueCreate(BaseModel):
    id: str
    name: str
    brand_voice: Optional[str] = "Premium quality, authentic experience"
    tone_keywords: Optional[List[str]] = ["premium", "fresh", "authentic"]
    avoid_words: Optional[List[str]] = ["cheap", "budget"]
    primary_color: Optional[str] = None
