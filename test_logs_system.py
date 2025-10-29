#!/usr/bin/env python3
"""
Script de test pour vérifier le système de logs SSE.
"""
import requests
import json
import time
import threading
from datetime import datetime

def test_logs_history():
    """Test l'endpoint d'historique des logs."""
    print(" Test de l'endpoint d'historique des logs...")
    try:
        response = requests.get("http://localhost:8000/api/logs/history")
        if response.status_code == 200:
            data = response.json()
            print(f" Historique des logs: {data['count']} logs trouvés")
            return True
        else:
            print(f" Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f" Erreur de connexion: {e}")
        return False

def test_sse_stream():
    """Test le stream SSE."""
    print(" Test du stream SSE...")
    try:
        response = requests.get("http://localhost:8000/api/logs/stream", stream=True)
        if response.status_code == 200:
            print(" Connexion SSE établie")
            
            # Lire quelques événements
            count = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Enlever 'data: '
                        try:
                            data = json.loads(data_str)
                            print(f" Log reçu: {data.get('message', 'N/A')}")
                            count += 1
                            if count >= 5:  # Arrêter après 5 logs
                                break
                        except json.JSONDecodeError:
                            print(f"⚠️ Données JSON invalides: {data_str}")
            
            print(" Test SSE terminé")
            return True
        else:
            print(f" Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f" Erreur de connexion SSE: {e}")
        return False

def test_health_endpoint():
    """Test l'endpoint de santé."""
    print(" Test de l'endpoint de santé...")
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f" Serveur en bonne santé: {data.get('status', 'N/A')}")
            return True
        else:
            print(f" Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f" Erreur de connexion: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Démarrage des tests du système de logs SSE")
    print("=" * 50)
    
    # Attendre que le serveur soit prêt
    print("⏳ Attente du démarrage du serveur...")
    time.sleep(3)
    
    # Tests
    tests = [
        test_health_endpoint,
        test_logs_history,
        test_sse_stream
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f" Erreur dans le test: {e}")
            results.append(False)
            print()
    
    # Résumé
    print("=" * 50)
    print(" Résumé des tests:")
    passed = sum(results)
    total = len(results)
    print(f" Tests réussis: {passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Le système de logs SSE fonctionne correctement.")
    else:
        print(" Certains tests ont échoué. Vérifiez les logs ci-dessus.")

if __name__ == "__main__":
    main()
