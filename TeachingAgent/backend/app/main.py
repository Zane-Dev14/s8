from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.streaming_routes import router as streaming_router
from app.core.database import Base, engine
from app.core.settings import ensure_data_dirs, settings
# Import models so SQLAlchemy knows about them
from app.models import db  # noqa: F401


def create_app() -> FastAPI:
    ensure_data_dirs()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.app_name,
        description="Teaching Agent - Personalized Learning with Goku",
        version="2.0.0",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    app.include_router(streaming_router)
    
    return app


app = create_app()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "features": [
            "streaming_teaching",
            "goku_voice",
            "sm2_flashcards",
            "rag_quiz",
            "multi_subject",
        ],
    }
