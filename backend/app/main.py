import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.indexes import create_indexes
from app.routers import auth, employees, attendance, leave, payroll, dashboard, reports, recruitment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dayflow.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Dayflow HRMS Backend...")
    await connect_to_mongo()
    await create_indexes()
    yield
    logger.info("Shutting down Dayflow HRMS Backend...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Dayflow Human Resource Management System API Engine",
    lifespan=lifespan
)

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://day-flow-hr-management-system.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ] + settings.CORS_ORIGINS,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "*"],
)

@app.options("/{full_path:path}")
async def preflight_options_handler(full_path: str):
    return {"status": "ok"}

# Register routers
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(recruitment.router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.PROJECT_NAME,
        "docs": "/docs"
    }

@app.get("/health")
async def health_root():
    return {"status": "ok"}

# Unified SPA deployment support
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist) and os.path.exists(os.path.join(frontend_dist, "index.html")):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "status": "online",
            "app": settings.PROJECT_NAME,
            "docs": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
