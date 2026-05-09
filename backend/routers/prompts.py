from fastapi import APIRouter

router = APIRouter()


@router.get("/prompts/types")
async def list_prompt_types():
    """List available prompt template types."""
    return {
        "types": [
            {
                "id": "social_bundle",
                "description": "Full social + email + video + signage + web copy bundle",
                "outputs": [
                    "facebook_posts (x3)",
                    "instagram_caption",
                    "hashtags",
                    "email_subject_lines (x3)",
                    "email_body",
                    "video_script_15s",
                    "video_script_30s",
                    "signage_headline",
                    "signage_subline",
                    "menu_description",
                    "midjourney_prompt",
                    "web_copy"
                ]
            }
        ]
    }
