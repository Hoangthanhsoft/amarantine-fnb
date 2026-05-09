from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/tracking/roi-summary")
async def get_roi_summary(venue_id: str = None, days: int = 30):
    """Get ROI summary — time saved, cost avoided, content produced."""
    from database import get_tracking_summary
    since = datetime.utcnow() - timedelta(days=days)
    data = await get_tracking_summary(venue_id=venue_id, since=since)

    manual_hours = data["total_manual_minutes"] / 60
    ai_hours = data["total_ai_seconds"] / 3600
    cost_avoided = manual_hours * 85.0
    ai_cost = data["estimated_api_cost"]

    return {
        "period_days": days,
        "venue_id": venue_id or "all",
        "summary": {
            "total_content_items": data["total_items_produced"],
            "total_tasks": data["total_tasks"],
            "success_rate_pct": data["success_rate"]
        },
        "time_metrics": {
            "manual_hours_saved": round(manual_hours - ai_hours, 1),
            "speed_multiplier": round(manual_hours / ai_hours, 0) if ai_hours > 0 else 0
        },
        "financial_metrics": {
            "cost_avoided_aud": round(cost_avoided, 2),
            "ai_tool_cost_aud": round(ai_cost, 2),
            "net_roi_aud": round(cost_avoided - ai_cost, 2),
            "roi_ratio": round(cost_avoided / ai_cost, 1) if ai_cost > 0 else 0
        }
    }
