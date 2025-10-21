"""
Movement service implementing mouse navigation algorithms.
"""
from typing import List

from app.core.utils import is_valid_position, get_adjacent_positions
from app.services.ai_agent import MouseAgent


class MovementService:
    """Service for handling mouse movement logic."""
    
    def __init__(self):
        """Initialize movement service with AI agent."""
        self.ai_agent = MouseAgent()
    
    def calculate_next_position(
        self, 
        labyrinth: List[List[int]], 
        current_position: List[int], 
        goal_position: List[int],
        available_cheeses: List[List[int]] = None
    ) -> List[int]:
        """
        Calculate the next position for the mouse using intelligent algorithm.
        
        Args:
            labyrinth: 2D maze representation
            current_position: Current mouse position [x, y]
            goal_position: Target goal position [x, y]
            available_cheeses: List of available cheese positions [[x, y], ...]
            
        Returns:
            List[int]: Next position [x, y]
            
        Raises:
            ValueError: If positions are invalid or no valid move exists
        """
        # Validate current position
        if not is_valid_position(current_position, labyrinth):
            raise ValueError("Current position is invalid or blocked")
        
        # Validate goal position
        if not is_valid_position(goal_position, labyrinth):
            raise ValueError("Goal position is invalid or blocked")
        
        # If already at goal, stay in place
        if current_position == goal_position:
            return current_position
        
        # Use AI agent to determine next move
        return self.ai_agent.get_next_move(
            labyrinth=labyrinth,
            current_position=current_position,
            goal_position=goal_position,
            available_cheeses=available_cheeses
        )
    
    def _greedy_algorithm(
        self, 
        labyrinth: List[List[int]], 
        current_position: List[int], 
        goal_position: List[int]
    ) -> List[int]:
        """
        Simple greedy algorithm: move towards goal prioritizing X then Y axis.
        
        Args:
            labyrinth: 2D maze representation
            current_position: Current position [x, y]
            goal_position: Goal position [x, y]
            
        Returns:
            List[int]: Next position using greedy approach
        """
        x, y = current_position
        gx, gy = goal_position
        
        # Priority: adjust X axis first, then Y axis
        candidate_moves = []
        
        # X axis movement
        if x < gx:  # Move right
            candidate_moves.append([x + 1, y])
        elif x > gx:  # Move left
            candidate_moves.append([x - 1, y])
        
        # Y axis movement
        if y < gy:  # Move down
            candidate_moves.append([x, y + 1])
        elif y > gy:  # Move up
            candidate_moves.append([x, y - 1])
        
        # Find first valid move
        for move in candidate_moves:
            if is_valid_position(move, labyrinth):
                return move
        
        # If no direct move towards goal is possible, try any valid adjacent position
        for adjacent_pos in get_adjacent_positions(current_position):
            if is_valid_position(adjacent_pos, labyrinth):
                return adjacent_pos
        
        # If no move is possible, stay in place
        return current_position
