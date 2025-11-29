from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path
from .api.routes import router
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Prompt Optimizer SaaS API",
    description="AI-powered prompt optimization using multi-stage pipeline (Smart Queue → PCV → D/S Cycle)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["Optimization"])

# Serve frontend static files if they exist
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")
    app.mount("/components", StaticFiles(directory=str(frontend_path / "components")), name="components")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend HTML"""
        return FileResponse(str(frontend_path / "index.html"))
else:
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Prompt Optimizer SaaS API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health"
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG
    )
