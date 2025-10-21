"""
Utility functions for the Mouse AI application.
"""
from typing import List, Tuple


def is_valid_position(position: List[int], labyrinth: List[List[int]]) -> bool:
    """
    Check if a position is valid within the labyrinth bounds.
    
    Args:
        position: [x, y] coordinates
        labyrinth: 2D maze representation
        
    Returns:
        bool: True if position is valid and not a wall
    """
    if not labyrinth or not labyrinth[0]:
        return False
    
    x, y = position
    height = len(labyrinth)
    width = len(labyrinth[0])
    
    # Check bounds
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    
    # Check if it's not a wall (assuming 1 = wall, 0 = free space)
    return labyrinth[y][x] == 0


def calculate_manhattan_distance(pos1: List[int], pos2: List[int]) -> int:
    """
    Calculate Manhattan distance between two positions.
    
    Args:
        pos1: First position [x, y]
        pos2: Second position [x, y]
        
    Returns:
        int: Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_adjacent_positions(position: List[int]) -> List[List[int]]:
    """
    Get all adjacent positions (4-directional movement).
    
    Args:
        position: Current position [x, y]
        
    Returns:
        List of adjacent positions
    """
    x, y = position
    return [
        [x, y - 1],  # North
        [x + 1, y],  # East
        [x, y + 1],  # South
        [x - 1, y]   # West
    ]