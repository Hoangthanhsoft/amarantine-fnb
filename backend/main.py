from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from routers import content, venues, prompts, tracking, health

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — %(name)s — %(levelname)s — %(message)s'
)

app = FastAPI(
    title="Amarantine AI — F&B Ops System",
    description="AI-powered content production engine for F&B venues",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.time() - start:.3f}s"
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# Register routers
app.include_router(health.router, tags=["health"])
app.include_router(content.router, prefix="/api/v1", tags=["content"])
app.include_router(venues.router, prefix="/api/v1", tags=["venues"])
app.include_router(prompts.router, prefix="/api/v1", tags=["prompts"])
app.include_router(tracking.router, prefix="/api/v1", tags=["tracking"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
