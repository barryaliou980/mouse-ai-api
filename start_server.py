#!/usr/bin/env python3
"""
Script de démarrage du serveur Mouse AI API avec support des variables d'environnement.
"""
import os
import sys
import uvicorn
from app.core.config import settings

def main():
    """Démarre le serveur avec la configuration des variables d'environnement."""
    
    print("🚀 Démarrage du serveur Mouse AI API")
    print("=" * 50)
    print(f"📡 Host: {settings.HOST}")
    print(f"🔌 Port: {settings.PORT}")
    print(f"🐛 Debug: {settings.DEBUG}")
    print(f"🌐 CORS Origins: {settings.CORS_ORIGINS}")
    print(f"📊 Log Level: {settings.LOG_LEVEL}")
    print(f"📝 Max Logs: {settings.MAX_LOGS}")
    print("=" * 50)
    
    # Démarrer le serveur
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )

if __name__ == "__main__":
    main()
