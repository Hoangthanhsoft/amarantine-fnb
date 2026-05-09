from fastapi import APIRouter, HTTPException
from models.content import ContentRequest, ContentResponse
from services.content_service import content_service

router = APIRouter()


@router.post("/content/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate a full content bundle from a promotional brief."""
    result = await content_service.generate_content(request)
    if result.status == "failed":
        raise HTTPException(status_code=500, detail=result.error)
    return result


@router.get("/content/{task_id}", response_model=ContentResponse)
async def get_content_task(task_id: str):
    """Retrieve a previously generated content task by ID."""
    from database import get_content_task
    task = await get_content_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
