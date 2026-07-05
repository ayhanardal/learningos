import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import dashboard, plan, db_routes
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="LearningOS KPSS Dashboard",
    description="KPSS Çalışma Takip Dashboard",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(dashboard.router, prefix="/api")
app.include_router(plan.router, prefix="/api")
app.include_router(db_routes.router, prefix="/api", tags=["Database"])


@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "learningos-dashboard"}
