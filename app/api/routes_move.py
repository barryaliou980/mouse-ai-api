"""
Movement endpoints for Mouse AI API.
"""
from fastapi import APIRouter, HTTPException

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
            goal_position=request.goal
        )
        
        return MoveResponse(next_position=next_position)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
