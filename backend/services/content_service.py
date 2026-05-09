"""
Content Service — MIT Core Version.

Orchestrates AI content generation.
Full Version adds: Google Drive upload, Canva export, Facebook auto-post,
AI image generation, video rendering, n8n automation.

Flow (MIT):
  1. Get venue config from DB
  2. Generate 11 content types via GPT-4o (+ Claude fallback)
  3. Save task to DB
  4. Log basic ROI metrics
  5. Return ContentResponse
"""
import uuid
import json
import time
import logging
from datetime import datetime

from models.content import ContentRequest, ContentResponse, ContentOutput
from services.ai_service import ai_service
from services.prompt_service import build_system_prompt, build_content_prompt
import database

logger = logging.getLogger(__name__)


class ContentService:

    async def generate_content(self, request: ContentRequest) -> ContentResponse:
        task_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            # 1. Get venue config
            venue = await database.get_venue(request.venue_id)
            if not venue:
                raise ValueError(f"Venue not found: {request.venue_id}")

            # 2. Generate content via AI
            logger.info(f"[{task_id}] Generating: {request.promo_input[:50]}")
            system_prompt = build_system_prompt(venue)
            user_prompt = build_content_prompt(request.promo_input)

            raw_output, model_used = await ai_service.generate(
                system_prompt, user_prompt, max_tokens=2500
            )
            output_dict = self._parse_ai_output(raw_output)
            content_output = ContentOutput(**output_dict)
            processing_time = time.time() - start_time

            # 3. Save to DB
            items = self._count_items(content_output)
            await database.save_content_task(
                task_id=task_id,
                venue_id=request.venue_id,
                promo_input=request.promo_input,
                content_types=request.content_types,
                output_json=output_dict,
                status="completed",
                processing_time_ms=int(processing_time * 1000),
                drive_folder_url=None,
                error_message=None
            )

            # 4. Log ROI
            await database.save_task_log(
                task_id=task_id,
                venue_id=request.venue_id,
                task_type="content_bundle",
                items_produced=items,
                manual_time_minutes=float(items * 30),
                ai_time_seconds=processing_time,
                cost_avoided_aud=(items * 30 / 60) * 85.0,
                tools_used=[model_used],
                status="completed"
            )

            logger.info(f"[{task_id}] ✅ {items} items in {processing_time:.1f}s")

            return ContentResponse(
                task_id=task_id,
                venue_id=request.venue_id,
                status="completed",
                output=content_output,
                processing_time_seconds=round(processing_time, 2),
                generated_at=datetime.utcnow()
            )

        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"[{task_id}] ❌ Failed: {e}", exc_info=True)

            try:
                await database.save_content_task(
                    task_id=task_id,
                    venue_id=request.venue_id,
                    promo_input=request.promo_input,
                    content_types=request.content_types,
                    output_json=None,
                    status="failed",
                    processing_time_ms=int(elapsed * 1000),
                    drive_folder_url=None,
                    error_message=str(e)
                )
            except Exception:
                pass

            return ContentResponse(
                task_id=task_id,
                venue_id=request.venue_id,
                status="failed",
                processing_time_seconds=round(elapsed, 2),
                generated_at=datetime.utcnow(),
                error=str(e)
            )

    def _parse_ai_output(self, raw: str) -> dict:
        cleaned = (
            raw.strip()
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        return json.loads(cleaned)

    def _count_items(self, output: ContentOutput) -> int:
        count = 0
        if output.facebook_posts:    count += len(output.facebook_posts)
        if output.instagram_caption: count += 1
        if output.email_body:        count += 1
        if output.video_script_15s:  count += 1
        if output.video_script_30s:  count += 1
        if output.signage_headline:  count += 1
        if output.menu_description:  count += 1
        if output.web_copy:          count += 1
        if output.midjourney_prompt: count += 1
        return count


content_service = ContentService()
