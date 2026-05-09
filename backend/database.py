import asyncpg
import json
import logging
from datetime import datetime
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_pool = None


async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=2,
            max_size=10,
            command_timeout=30
        )
    return _pool


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


# ── Venues ──────────────────────────────────────────────────────────────────

async def get_venue(venue_id: str) -> dict | None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM venues WHERE id = $1", venue_id
        )
        return dict(row) if row else None


async def list_venues() -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM venues ORDER BY name")
        return [dict(r) for r in rows]


# ── Content Tasks ────────────────────────────────────────────────────────────

async def save_content_task(
    task_id: str,
    venue_id: str,
    promo_input: str,
    content_types: list[str],
    output_json: dict | None,
    status: str,
    processing_time_ms: int,
    drive_folder_url: str | None,
    error_message: str | None
) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO content_tasks
              (id, venue_id, promo_input, content_types, output_json,
               status, processing_time_ms, drive_folder_url, error_message)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ON CONFLICT (id) DO UPDATE SET
              status = EXCLUDED.status,
              output_json = EXCLUDED.output_json,
              processing_time_ms = EXCLUDED.processing_time_ms,
              drive_folder_url = EXCLUDED.drive_folder_url,
              error_message = EXCLUDED.error_message
            """,
            task_id, venue_id, promo_input,
            content_types,
            json.dumps(output_json) if output_json else None,
            status, processing_time_ms,
            drive_folder_url, error_message
        )


async def get_content_task(task_id: str) -> dict | None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM content_tasks WHERE id = $1", task_id
        )
        if row:
            d = dict(row)
            if d.get("output_json"):
                d["output_json"] = json.loads(d["output_json"])
            return d
        return None


# ── Tracking ─────────────────────────────────────────────────────────────────

async def save_task_log(
    task_id: str,
    venue_id: str,
    task_type: str,
    items_produced: int,
    manual_time_minutes: float,
    ai_time_seconds: float,
    cost_avoided_aud: float,
    tools_used: list[str],
    status: str
) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO task_logs
              (task_id, venue_id, task_type, items_produced,
               manual_time_minutes, ai_time_seconds, cost_avoided_aud,
               tools_used, status)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            """,
            task_id, venue_id, task_type, items_produced,
            manual_time_minutes, ai_time_seconds, cost_avoided_aud,
            tools_used, status
        )


async def get_tracking_summary(
    venue_id: str | None,
    since: datetime
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        base = "WHERE created_at >= $1"
        params: list = [since]
        if venue_id:
            base += " AND venue_id = $2"
            params.append(venue_id)

        row = await conn.fetchrow(
            f"""
            SELECT
              COALESCE(SUM(items_produced), 0)       AS total_items_produced,
              COUNT(*)                                AS total_tasks,
              COALESCE(SUM(manual_time_minutes), 0)  AS total_manual_minutes,
              COALESCE(SUM(ai_time_seconds), 0)      AS total_ai_seconds,
              ROUND(
                100.0 * SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END)
                / NULLIF(COUNT(*), 0), 1
              )                                      AS success_rate
            FROM task_logs {base}
            """,
            *params
        )
        d = dict(row)
        d["estimated_api_cost"] = float(d["total_tasks"]) * 0.01
        return d
