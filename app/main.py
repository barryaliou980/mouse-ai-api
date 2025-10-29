"""
FastAPI application entry point for Mouse AI Engine.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_health, routes_move, routes_mouse, routes_logs
from app.core.config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        description="Intelligence engine for mice navigation in maze environments"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(routes_health.router, prefix="/api")
    # app.include_router(routes_move.router, prefix="/api")  # Désactivé - utilise routes_mouse
    app.include_router(routes_mouse.router, prefix="/api")
    app.include_router(routes_logs.router, prefix="/api")
    
    return app


app = create_app()
