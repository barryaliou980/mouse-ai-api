"""
Mouse movement endpoints compatible with the frontend.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import logging

from app.services.mouse_ai_service import MouseAIService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["mouse"])

# Initialize service
mouse_ai_service = MouseAIService()


@router.post("/move")
async def get_mouse_move(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get next move for a mouse based on the frontend request format.
    
    Expected request format:
    {
        "mouseId": "string",
        "position": {"x": int, "y": int},
        "environment": {
            "grid": [["wall", "path", ...], ...],
            "width": int,
            "height": int,
            "cheesePositions": [{"x": int, "y": int}, ...],
            "otherMice": [...],
            "walls": [...],
            "paths": [...]
        },
        "mouseState": {
            "health": int,
            "happiness": int,
            "energy": int,
            "cheeseFound": int
        },
        "availableMoves": ["north", "south", "east", "west"]
    }
    
    Returns:
    {
        "mouseId": "string",
        "move": "north|south|east|west",
        "reasoning": "string"
    }
    """
    try:
        # Extract data from request
        mouse_id = request.get("mouseId", "unknown")
        position = request.get("position", {"x": 0, "y": 0})
        environment = request.get("environment", {})
        mouse_state = request.get("mouseState", {})
        available_moves = request.get("availableMoves", ["north", "south", "east", "west"])
        
        # Convert frontend grid format to Python format
        grid = environment.get("grid", [])
        python_grid = []
        for row in grid:
            python_row = []
            for cell in row:
                if cell == "wall":
                    python_row.append(1)  # 1 = wall (impassable)
                else:  # path, cheese, start = 0 (passable)
                    python_row.append(0)
            python_grid.append(python_row)
        
        # Debug: Log the grid conversion
        print(f"Frontend grid: {grid}")
        print(f"Python grid: {python_grid}")
        print(f"Mouse position: {position}")
        
        # Find the nearest cheese as goal
        cheese_positions = environment.get("cheesePositions", [])
        if not cheese_positions:
            # No cheese, use random movement
            import random
            move = random.choice(available_moves)
            return {
                "mouseId": mouse_id,
                "move": move,
                "reasoning": "No cheese found, random movement"
            }
        
        # Find closest cheese
        current_pos = [position["x"], position["y"]]
        
        # Check if mouse is already on a cheese
        for cheese in cheese_positions:
            if current_pos[0] == cheese["x"] and current_pos[1] == cheese["y"]:
                return {
                    "mouseId": mouse_id,
                    "move": "north",  # Use a valid direction but the frontend should handle this
                    "reasoning": f"Mouse is already on cheese at ({cheese['x']}, {cheese['y']}) - staying in place"
                }
        
        closest_cheese = cheese_positions[0]
        min_distance = abs(current_pos[0] - closest_cheese["x"]) + abs(current_pos[1] - closest_cheese["y"])
        
        for cheese in cheese_positions[1:]:
            distance = abs(current_pos[0] - cheese["x"]) + abs(current_pos[1] - cheese["y"])
            if distance < min_distance:
                min_distance = distance
                closest_cheese = cheese
        
        goal_position = [closest_cheese["x"], closest_cheese["y"]]
        
        # Get next move using the AI service
        next_position = mouse_ai_service.calculate_next_position(
            labyrinth=python_grid,
            current_position=current_pos,
            goal_position=goal_position,
            mouse_id=mouse_id
        )
        
        # Convert position change to direction
        move = _position_to_direction(current_pos, next_position)
        
        # Generate intelligent reasoning
        distance_to_cheese = abs(current_pos[0] - closest_cheese['x']) + abs(current_pos[1] - closest_cheese['y'])
        
        if next_position == current_pos:
            reasoning = f"Staying in place - no valid moves available"
        elif move == "north":
            reasoning = f"Moving north towards cheese at ({closest_cheese['x']}, {closest_cheese['y']}) - distance: {distance_to_cheese}"
        elif move == "south":
            reasoning = f"Moving south towards cheese at ({closest_cheese['x']}, {closest_cheese['y']}) - distance: {distance_to_cheese}"
        elif move == "east":
            reasoning = f"Moving east towards cheese at ({closest_cheese['x']}, {closest_cheese['y']}) - distance: {distance_to_cheese}"
        elif move == "west":
            reasoning = f"Moving west towards cheese at ({closest_cheese['x']}, {closest_cheese['y']}) - distance: {distance_to_cheese}"
        else:
            reasoning = f"Moving {move} towards cheese at ({closest_cheese['x']}, {closest_cheese['y']})"
        
        return {
            "mouseId": mouse_id,
            "move": move,
            "reasoning": reasoning
        }
        
    except Exception as e:
        logger.error(f"Error processing mouse move request: {str(e)}")
        # Fallback to random movement
        import random
        available_moves = request.get("availableMoves", ["north", "south", "east", "west"])
        move = random.choice(available_moves)
        return {
            "mouseId": request.get("mouseId", "unknown"),
            "move": move,
            "reasoning": f"Error occurred, using random movement: {str(e)}"
        }


def _position_to_direction(current_pos: List[int], next_pos: List[int]) -> str:
    """Convert position change to direction string."""
    dx = next_pos[0] - current_pos[0]
    dy = next_pos[1] - current_pos[1]
    
    if dx > 0:
        return "east"
    elif dx < 0:
        return "west"
    elif dy > 0:
        return "south"
    elif dy < 0:
        return "north"
    else:
        return "north"  # Default fallback


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Mouse AI service is running"
    }
