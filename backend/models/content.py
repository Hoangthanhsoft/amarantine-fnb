from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ContentRequest(BaseModel):
    venue_id: str = Field(..., example="my-venue")
    promo_input: str = Field(
        ...,
        min_length=10,
        max_length=500,
        example="Half-price oysters every Friday 5-7pm"
    )
    content_types: List[str] = Field(
        default=["social_bundle"],
        description="Types of content to generate"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "venue_id": "my-venue",
                "promo_input": "Half-price oysters every Friday 5-7pm, dine-in only",
                "content_types": ["social_bundle"]
            }
        }


class ContentOutput(BaseModel):
    facebook_posts: Optional[List[str]] = None
    instagram_caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    email_subject_lines: Optional[List[str]] = None
    email_body: Optional[str] = None
    video_script_15s: Optional[str] = None
    video_script_30s: Optional[str] = None
    signage_headline: Optional[str] = None
    signage_subline: Optional[str] = None
    menu_description: Optional[str] = None
    midjourney_prompt: Optional[str] = None
    web_copy: Optional[str] = None


class ContentResponse(BaseModel):
    task_id: str
    venue_id: str
    status: str          # pending | completed | failed
    output: Optional[ContentOutput] = None
    processing_time_seconds: Optional[float] = None
    generated_at: Optional[datetime] = None
    drive_folder_url: Optional[str] = None
    error: Optional[str] = None
