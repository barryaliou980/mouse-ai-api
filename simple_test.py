#!/usr/bin/env python3
"""
Test simple pour vérifier l'API Mouse AI.
"""
import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test que tous les modules peuvent être importés."""
    try:
        from app.main import app
        print(" Import app.main successful")
        
        from app.api.routes_mouse import router
        print(" Import routes_mouse successful")
        
        from app.services.mouse_ai_service import MouseAIService
        print(" Import MouseAIService successful")
        
        from app.core.utils import is_valid_position
        print(" Import utils successful")
        
        return True
    except Exception as e:
        print(f" Import failed: {e}")
        return False

def test_service():
    """Test le service MouseAIService."""
    try:
        from app.services.mouse_ai_service import MouseAIService
        
        service = MouseAIService()
        
        # Test avec un labyrinthe simple
        labyrinth = [
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1]
        ]
        
        current_pos = [1, 1]
        goal_pos = [2, 2]
        
        next_pos = service.calculate_next_position(labyrinth, current_pos, goal_pos)
        print(f" Service test successful: {current_pos} -> {next_pos}")
        
        return True
    except Exception as e:
        print(f" Service test failed: {e}")
        return False

def main():
    """Lancer tous les tests."""
    print("🧪 Testing Mouse AI API...")
    print("=" * 40)
    
    # Test des imports
    print("\n1. Testing imports...")
    import_ok = test_imports()
    
    # Test du service
    print("\n2. Testing service...")
    service_ok = test_service()
    
    # Résumé
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"Imports: {'' if import_ok else ''}")
    print(f"Service: {'' if service_ok else ''}")
    
    if import_ok and service_ok:
        print("\n🎉 All tests passed! API is ready to use.")
        print("\nTo start the server, run:")
        print("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
