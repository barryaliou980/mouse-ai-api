"""
Background thread for generating server logs.
"""
import threading
import time
import random
import logging
from datetime import datetime
from typing import Optional

from app.services.log_service import log_service

logger = logging.getLogger(__name__)


class ServerLogThread:
    """Background thread that generates server logs periodically."""
    
    def __init__(self, interval: float = 2.0):
        """
        Initialize the log thread.
        
        Args:
            interval: Interval between log generations in seconds
        """
        self.interval = interval
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.stop_event = threading.Event()
        
        # Messages de log prédéfinis
        self.log_messages = [
            "- Thread 1 - Mouse AI service initialized",
            "- Thread 2 - Processing mouse movement request",
            "- Thread 1 - Calculating optimal path",
            "- Thread 3 - Mouse reached cheese position",
            "- Thread 2 - Updating mouse state",
            "- Thread 1 - Checking for obstacles",
            "- Thread 3 - Mouse energy level updated",
            "- Thread 2 - Pathfinding algorithm completed",
            "- Thread 1 - Mouse position updated",
            "- Thread 3 - Simulation step completed",
            "- Thread 2 - Mouse AI decision made",
            "- Thread 1 - Environment analysis finished",
            "- Thread 3 - Mouse health status checked",
            "- Thread 2 - Movement validation passed",
            "- Thread 1 - Next move calculated",
            "- Thread 3 - Mouse happiness increased",
            "- Thread 2 - Cheese detection successful",
            "- Thread 1 - Collision avoidance active",
            "- Thread 3 - Mouse performance metrics updated",
            "- Thread 2 - AI learning algorithm running"
        ]
        
        logger.info("ServerLogThread initialized")
    
    def start(self):
        """Start the log generation thread."""
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            logger.info("ServerLogThread started")
    
    def stop(self):
        """Stop the log generation thread."""
        self.running = False
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5.0)
        logger.info("ServerLogThread stopped")
    
    def _run(self):
        """Main thread loop."""
        logger.info("ServerLogThread running")
        
        while self.running and not self.stop_event.is_set():
            try:
                # Générer un log aléatoire
                message = random.choice(self.log_messages)
                
                # Ajouter des informations contextuelles
                log_data = {
                    'message': message,
                    'level': random.choice(['INFO', 'DEBUG', 'WARNING']),
                    'simulation_id': f"sim_{random.randint(1000, 9999)}",
                    'mouse_id': f"mouse_{random.randint(1, 3)}",
                    'turn': random.randint(1, 100),
                    'performance': {
                        'cpu_usage': round(random.uniform(10, 80), 1),
                        'memory_usage': round(random.uniform(20, 90), 1),
                        'response_time': round(random.uniform(50, 200), 1)
                    }
                }
                
                # Ajouter le log au service
                log_service.add_custom_log(**log_data)
                
                # Attendre l'intervalle suivant
                time.sleep(self.interval)
                
            except Exception as e:
                logger.error(f"Error in ServerLogThread: {e}")
                time.sleep(self.interval)
    
    def is_running(self) -> bool:
        """Check if the thread is running."""
        return self.running and self.thread is not None and self.thread.is_alive()


# Instance globale du thread de logs
server_log_thread = ServerLogThread(interval=3.0)  # Log toutes les 3 secondes
