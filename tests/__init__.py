"""Tests package."""

"""
Unit tests for Mouse AI API endpoints and services.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.movement_service import MovementService

client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for health endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint returns correct status."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestMoveEndpoint:
    """Test cases for move endpoint."""
    
    def test_valid_move_request(self):
        """Test valid move request returns next position."""
        payload = {
            "labyrinth": [
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0]
            ],
            "position": [0, 0],
            "goal": [2, 2]
        }
        
        response = client.post("/api/move", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "next_position" in data
        assert len(data["next_position"]) == 2
    
    def test_invalid_labyrinth(self):
        """Test invalid labyrinth structure returns error."""
        payload = {
            "labyrinth": [],
            "position": [0, 0],
            "goal": [1, 1]
        }
        
        response = client.post("/api/move", json=payload)
        assert response.status_code == 422
    
    def test_invalid_position_format(self):
        """Test invalid position format returns error."""
        payload = {
            "labyrinth": [[0, 0], [0, 0]],
            "position": [0],  # Missing Y coordinate
            "goal": [1, 1]
        }
        
        response = client.post("/api/move", json=payload)
        assert response.status_code == 422
    
    def test_blocked_current_position(self):
        """Test blocked current position returns error."""
        payload = {
            "labyrinth": [
                [1, 0],  # Current position is blocked
                [0, 0]
            ],
            "position": [0, 0],
            "goal": [1, 1]
        }
        
        response = client.post("/api/move", json=payload)
        assert response.status_code == 400
    
    def test_already_at_goal(self):
        """Test mouse already at goal returns same position."""
        payload = {
            "labyrinth": [
                [0, 0],
                [0, 0]
            ],
            "position": [1, 1],
            "goal": [1, 1]
        }
        
        response = client.post("/api/move", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["next_position"] == [1, 1]


class TestMovementService:
    """Test cases for movement service logic."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = MovementService()
    
    def test_greedy_movement_towards_goal(self):
        """Test greedy algorithm moves towards goal."""
        labyrinth = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        
        next_pos = self.service.calculate_next_position(
            labyrinth=labyrinth,
            current_position=[0, 0],
            goal_position=[2, 2]
        )
        
        # Should move right first (X axis priority)
        assert next_pos == [1, 0]
    
    def test_movement_with_obstacles(self):
        """Test movement navigation around obstacles."""
        labyrinth = [
            [0, 1, 0],  # Wall blocks direct path
            [0, 0, 0],
            [0, 0, 0]
        ]
        
        next_pos = self.service.calculate_next_position(
            labyrinth=labyrinth,
            current_position=[0, 0],
            goal_position=[2, 0]
        )
        
        # Should move down to avoid wall
        assert next_pos == [0, 1]
    
    def test_no_valid_moves(self):
        """Test behavior when no valid moves are available."""
        labyrinth = [
            [1, 1, 1],
            [1, 0, 1],  # Mouse trapped in center
            [1, 1, 1]
        ]
        
        next_pos = self.service.calculate_next_position(
            labyrinth=labyrinth,
            current_position=[1, 1],
            goal_position=[0, 0]
        )
        
        # Should stay in place when trapped
        assert next_pos == [1, 1]


if __name__ == "__main__":
    pytest.main([__file__])