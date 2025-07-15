from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.paper_router import router as paper_router

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    description="API for Paper Glimpse - Research Paper Summarization Tool"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(paper_router)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Paper Glimpse API",
        "version": settings.version,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}