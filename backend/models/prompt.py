from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PromptTemplate(BaseModel):
    id: Optional[int] = None
    name: str
    category: Optional[str] = None
    content_type: Optional[str] = None
    template_text: str
    version: int = 1
    is_active: bool = True
    created_at: Optional[datetime] = None
