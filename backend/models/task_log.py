from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskLog(BaseModel):
    id: Optional[int] = None
    task_id: str
    venue_id: str
    task_type: str
    items_produced: int
    manual_time_minutes: float
    ai_time_seconds: float
    cost_avoided_aud: float
    tools_used: List[str]
    status: str
    created_at: Optional[datetime] = None
