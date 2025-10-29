#!/usr/bin/env python3
"""
Script de test pour simuler des mouvements de souris et voir les logs en temps réel.
"""
import requests
import json
import time
import threading
from datetime import datetime

def test_mouse_movement():
    """Test des mouvements de souris pour générer des logs."""
    print("🐭 Test des mouvements de souris...")
    
    # Configuration de test
    mouse_id = "souris1"
    position = {"x": 1, "y": 1}
    
    # Grille de test simple
    grid = [
        ["wall", "path", "path", "wall"],
        ["path", "path", "path", "path"],
        ["path", "wall", "path", "path"],
        ["wall", "path", "path", "wall"]
    ]
    
    environment = {
        "grid": grid,
        "width": 4,
        "height": 4,
        "cheesePositions": [{"x": 2, "y": 3}],
        "otherMice": [],
        "walls": [],
        "paths": []
    }
    
    mouse_state = {
        "health": 100,
        "happiness": 50,
        "energy": 80,
        "cheeseFound": 0,
        "tag": 1
    }
    
    available_moves = ["north", "south", "east", "west"]
    
    request_data = {
        "mouseId": mouse_id,
        "position": position,
        "environment": environment,
        "mouseState": mouse_state,
        "availableMoves": available_moves
    }
    
    try:
        print(f"📤 Envoi de la requête de mouvement pour {mouse_id}...")
        response = requests.post("http://localhost:8000/api/move", json=request_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Mouvement calculé: {result['move']}")
            print(f"💭 Raisonnement: {result['reasoning']}")
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_multiple_movements():
    """Test de plusieurs mouvements pour générer plus de logs."""
    print("🔄 Test de plusieurs mouvements...")
    
    movements = [
        {"mouseId": "souris1", "position": {"x": 1, "y": 1}, "tag": 1},
        {"mouseId": "souris2", "position": {"x": 2, "y": 1}, "tag": 2},
        {"mouseId": "souris3", "position": {"x": 1, "y": 2}, "tag": 3},
    ]
    
    grid = [
        ["wall", "path", "path", "wall"],
        ["path", "path", "path", "path"],
        ["path", "wall", "path", "path"],
        ["wall", "path", "path", "wall"]
    ]
    
    environment = {
        "grid": grid,
        "width": 4,
        "height": 4,
        "cheesePositions": [{"x": 2, "y": 3}],
        "otherMice": [],
        "walls": [],
        "paths": []
    }
    
    for i, mouse in enumerate(movements):
        print(f"\n🐭 Test mouvement {i+1}/3 pour {mouse['mouseId']}")
        
        request_data = {
            "mouseId": mouse["mouseId"],
            "position": mouse["position"],
            "environment": environment,
            "mouseState": {
                "health": 100,
                "happiness": 50,
                "energy": 80,
                "cheeseFound": 0,
                "tag": mouse["tag"]
            },
            "availableMoves": ["north", "south", "east", "west"]
        }
        
        try:
            response = requests.post("http://localhost:8000/api/move", json=request_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {mouse['mouseId']}: {result['move']} - {result['reasoning']}")
            else:
                print(f"❌ Erreur pour {mouse['mouseId']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur pour {mouse['mouseId']}: {e}")
        
        time.sleep(1)  # Pause entre les mouvements

def monitor_logs():
    """Surveille les logs en temps réel."""
    print("📡 Surveillance des logs en temps réel...")
    try:
        response = requests.get("http://localhost:8000/api/logs/stream", stream=True)
        if response.status_code == 200:
            print("✅ Connexion au stream de logs établie")
            
            count = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        try:
                            data = json.loads(data_str)
                            if data.get('type') != 'heartbeat':
                                print(f"📝 [{data.get('timestamp', 'N/A')}] {data.get('message', 'N/A')}")
                                count += 1
                                if count >= 20:  # Arrêter après 20 logs
                                    break
                        except json.JSONDecodeError:
                            pass
        else:
            print(f"❌ Erreur de connexion au stream: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de surveillance: {e}")

def main():
    """Fonction principale de test."""
    print("🚀 Test du système de logs des mouvements de souris")
    print("=" * 60)
    
    # Attendre que le serveur soit prêt
    print("⏳ Attente du démarrage du serveur...")
    time.sleep(3)
    
    # Test de santé
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("✅ Serveur en bonne santé")
        else:
            print("❌ Serveur non disponible")
            return
    except Exception as e:
        print(f"❌ Impossible de se connecter au serveur: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎯 Phase 1: Test de mouvements simples")
    test_mouse_movement()
    
    print("\n" + "=" * 60)
    print("🎯 Phase 2: Test de plusieurs mouvements")
    test_multiple_movements()
    
    print("\n" + "=" * 60)
    print("🎯 Phase 3: Surveillance des logs")
    print("Les logs suivants devraient apparaître dans le frontend...")
    
    # Surveiller les logs pendant 10 secondes
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\n⏹️ Surveillance interrompue")
    
    print("\n✅ Test terminé!")
    print("💡 Vérifiez maintenant le frontend pour voir les logs des mouvements de souris")

if __name__ == "__main__":
    main()
