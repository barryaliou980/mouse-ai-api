# Moteur d'intelligence artificielle pour la navigation de souris dans un labyrinthe

> **Projet d’étude** – développement d’une API FastAPI pour simuler et contrôler le mouvement de souris dans un labyrinthe.  
> Objectif pédagogique : apprendre à structurer une application modulable, intégrable à des modèles de Machine Learning (PyTorch), et consommable par un frontend Next.js.

## 📋 Description

Cette API fournit un moteur d’intelligence pour contrôler le mouvement des souris dans un environnement de labyrinthe.  
L’architecture est conçue pour être **modulaire, extensible et prête pour l’intégration de modèles ML**.

### Fonctionnalités principales

- **API REST stateless** avec FastAPI
- **Algorithme de mouvement greedy** (axe X puis Y vers l’objectif)
- **Architecture modulaire** prête pour l’IA avancée
- **Validation robuste** avec Pydantic v2
- **Tests unitaires** complets
- **Configuration centralisée**


## 📋 Structure de dossier

- **app/**
  - **api/** : Routes et endpoints
  - **core/** : Configuration et utilitaires
    - `config.py` : Configuration globale
  - **services/** : Logique métier
  - **models/** : Modèles Pydantic
  - `main.py` : Point d'entrée FastAPI
- **tests/** : Tests unitaires
- `requirements.txt` : Dépendances


## 🚀 Installation et lancement

### Prérequis
- Python 3.8+
- pip ou poetry

### 🚀 Installation

```bash
# Cloner le projet
git clone <repository_url>
cd mouse_ai

# Créer un environnement virtuel (Python 3.10+ recommandé)
python3 -m venv .venv

# Activer l'environnement virtuel
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Lancer en mode développement
uvicorn app.main:app --reload --port 8000

# Lancer en mode production
uvicorn app.main:app --host 0.0.0.0 --port 8000
