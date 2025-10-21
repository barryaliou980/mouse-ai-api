"""
Movement endpoints for Mouse AI API.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.models.schemas import MoveRequest, MoveResponse
from app.services.movement_service import MovementService

router = APIRouter(tags=["movement"])

# Initialize service
movement_service = MovementService()


@router.post("/move", response_model=MoveResponse)
async def calculate_next_move(request: MoveRequest) -> MoveResponse:
    """
    Calculate the next optimal move for the mouse in the labyrinth.
    
    Args:
        request: Move request containing labyrinth, current position, and goal
        
    Returns:
        MoveResponse: Next recommended position
        
    Raises:
        HTTPException: If movement calculation fails
    """
    try:
        next_position = movement_service.calculate_next_position(
            labyrinth=request.labyrinth,
            current_position=request.position,
            goal_position=request.goal,
            available_cheeses=getattr(request, 'available_cheeses', None)
        )
        
        return MoveResponse(next_position=next_position)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/move-frontend")
async def calculate_next_move_frontend(request: dict) -> dict:
    """
    Calculate the next optimal move for the mouse using frontend format.
    
    Args:
        request: Frontend move request containing environment, position, etc.
        
    Returns:
        dict: Next recommended position in frontend format
        
    Raises:
        HTTPException: If movement calculation fails
    """
    try:
        # Extract data from frontend format
        position = request.get("position", [0, 0])
        environment = request.get("environment", {})
        grid = environment.get("grid", [])
        cheese_positions = environment.get("cheesePositions", [])
        available_cheeses = request.get("available_cheeses", [])
        
        # Convert grid format (string to int)
        labyrinth = []
        for row in grid:
            int_row = []
            for cell in row:
                if cell == "wall":
                    int_row.append(1)
                else:  # path, cheese, start
                    int_row.append(0)
            labyrinth.append(int_row)
        
        # Convert cheese positions to list format
        available_cheeses_list = []
        if available_cheeses:
            for cheese in available_cheeses:
                available_cheeses_list.append([cheese["x"], cheese["y"]])
        elif cheese_positions:
            for cheese in cheese_positions:
                available_cheeses_list.append([cheese["x"], cheese["y"]])
        
        # Choose the first available cheese as goal (will be optimized by AI)
        goal_position = [0, 0]
        if available_cheeses_list:
            goal_position = available_cheeses_list[0]
        
        # Calculate next position using intelligent AI
        next_position = movement_service.calculate_next_position(
            labyrinth=labyrinth,
            current_position=position,
            goal_position=goal_position,
            available_cheeses=available_cheeses_list
        )
        
        # Convert back to frontend format
        return {
            "mouseId": request.get("mouseId", "default"),
            "move": _position_to_direction(position, next_position),
            "reasoning": f"Intelligent pathfinding to nearest cheese. Next position: {next_position}"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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
        return "north"  # Default if no movement
