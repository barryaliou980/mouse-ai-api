"""
Server-Sent Events endpoint for server logs streaming.
"""
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import asyncio
import json
import logging
from typing import AsyncGenerator
from datetime import datetime

from app.services.log_service import log_service

logger = logging.getLogger(__name__)
router = APIRouter(tags=["logs"])

# Utilise l'instance globale du service de logs partagée avec le thread


@router.get("/logs/stream")
async def stream_logs():
    """
    Stream server logs using Server-Sent Events (SSE).
    
    Returns:
        StreamingResponse: SSE stream of server logs
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events for server logs."""
        try:
            # Envoyer un événement de connexion
            yield f"data: {json.dumps({'type': 'connection', 'message': 'Connected to server logs stream', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # S'abonner aux logs du service
            async for log_entry in log_service.get_logs_stream():
                yield f"data: {json.dumps(log_entry)}\n\n"
                
        except asyncio.CancelledError:
            logger.info("Client disconnected from logs stream")
            yield f"data: {json.dumps({'type': 'disconnection', 'message': 'Disconnected from server logs stream', 'timestamp': datetime.now().isoformat()})}\n\n"
        except Exception as e:
            logger.error(f"Error in logs stream: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': f'Stream error: {str(e)}', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )


@router.get("/logs/history")
async def get_logs_history():
    """
    Get recent logs history.
    
    Returns:
        dict: Recent logs with metadata
    """
    try:
        logs = log_service.get_recent_logs()
        return {
            "success": True,
            "logs": logs,
            "count": len(logs),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting logs history: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
