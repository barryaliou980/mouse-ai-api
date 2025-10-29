"""
Log service for managing server logs and streaming them to clients.
"""
import asyncio
import logging
from typing import List, Dict, Any, AsyncGenerator
from datetime import datetime
from collections import deque
import threading

logger = logging.getLogger(__name__)


class LogService:
    """Service for managing and streaming server logs."""
    
    def __init__(self, max_logs: int = 1000):
        """
        Initialize the log service.
        
        Args:
            max_logs: Maximum number of logs to keep in memory
        """
        self.max_logs = max_logs
        self.logs = deque(maxlen=max_logs)
        self.subscribers: List[asyncio.Queue] = []
        self.lock = threading.Lock()
        
        # Configurer le logger pour capturer les logs
        self._setup_log_capture()
        
        logger.info("LogService initialized")
    
    def _setup_log_capture(self):
        """Setup log capture to intercept all logging messages."""
        # Créer un handler personnalisé pour capturer les logs
        class LogCaptureHandler(logging.Handler):
            def __init__(self, log_service):
                super().__init__()
                self.log_service = log_service
            
            def emit(self, record):
                try:
                    log_entry = {
                        'type': 'log',
                        'level': record.levelname,
                        'message': record.getMessage(),
                        'module': record.module,
                        'function': record.funcName,
                        'line': record.lineno,
                        'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                        'thread_id': record.thread
                    }
                    self.log_service.add_log(log_entry)
                except Exception:
                    pass  # Éviter les erreurs infinies
        
        # Ajouter le handler au logger racine
        root_logger = logging.getLogger()
        handler = LogCaptureHandler(self)
        handler.setLevel(logging.INFO)
        root_logger.addHandler(handler)
    
    def add_log(self, log_entry: Dict[str, Any]):
        """
        Add a new log entry.
        
        Args:
            log_entry: Log entry dictionary
        """
        with self.lock:
            self.logs.append(log_entry)
            
            # Notifier tous les abonnés
            for queue in self.subscribers[:]:  # Copie pour éviter les modifications pendant l'itération
                try:
                    queue.put_nowait(log_entry)
                except asyncio.QueueFull:
                    # Retirer les abonnés avec des queues pleines
                    self.subscribers.remove(queue)
                except Exception:
                    # Retirer les abonnés avec des erreurs
                    self.subscribers.remove(queue)
    
    def add_custom_log(self, message: str, level: str = "INFO", **kwargs):
        """
        Add a custom log entry.
        
        Args:
            message: Log message
            level: Log level (INFO, DEBUG, WARNING, ERROR)
            **kwargs: Additional log data
        """
        log_entry = {
            'type': 'custom',
            'level': level,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'thread_id': threading.get_ident(),
            **kwargs
        }
        self.add_log(log_entry)
    
    def get_recent_logs(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent logs.
        
        Args:
            count: Number of recent logs to return
            
        Returns:
            List of recent log entries
        """
        with self.lock:
            return list(self.logs)[-count:]
    
    async def get_logs_stream(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream logs as they are added.
        
        Yields:
            Log entries as they are created
        """
        # Créer une queue pour ce client
        queue = asyncio.Queue(maxsize=100)
        self.subscribers.append(queue)
        
        try:
            # Envoyer les logs récents d'abord
            recent_logs = self.get_recent_logs(50)
            for log_entry in recent_logs:
                yield log_entry
            
            # Ensuite, streamer les nouveaux logs
            while True:
                try:
                    log_entry = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield log_entry
                except asyncio.TimeoutError:
                    # Envoyer un heartbeat pour maintenir la connexion
                    yield {
                        'type': 'heartbeat',
                        'timestamp': datetime.now().isoformat()
                    }
                    
        except asyncio.CancelledError:
            logger.info("Log stream cancelled")
        finally:
            # Nettoyer l'abonnement
            if queue in self.subscribers:
                self.subscribers.remove(queue)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get log service statistics.
        
        Returns:
            Statistics about the log service
        """
        with self.lock:
            return {
                'total_logs': len(self.logs),
                'max_logs': self.max_logs,
                'active_subscribers': len(self.subscribers),
                'oldest_log': self.logs[0]['timestamp'] if self.logs else None,
                'newest_log': self.logs[-1]['timestamp'] if self.logs else None
            }


# Instance globale du service de logs
log_service = LogService()
