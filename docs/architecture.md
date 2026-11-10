# Architecture Technique & Modèle de Conception — Labyrun

## 1. Vue d'Ensemble du Système

**Labyrun** est une application web combinant un moteur de génération procédurale de labyrinthes et un système de mini-défis de programmation sous forme de pare-feu interactif.

L'application repose sur une séparation stricte entre :
1. **La couche Métier (Core & Quiz)** : Génération algorithmique, graphes et résolution (A*, BFS), banque de questions et vérification.
2. **La couche Web (API REST & Contrôleur Flask)** : Application Factory, sérialisation JSON, gestion d'erreurs et points de terminaison.
3. **La couche Présentation (Frontend Canvas & Tailwind)** : Rendu 60 FPS, physique de glissade (sliding collision), système de particules et modales de hack.

---

## 2. Arborescence du Projet

```text
D:\projets_dev\PYTHON\Projets\Labyrun
│
├── assets/                          # Ressources statiques (audio, icônes, polices)
│   └── README.md
│
├── docs/                            # Documentation technique et schémas
│   └── architecture.md
│
├── src/
│   └── labyrun/                     # Code source modulaire Python
│       ├── __init__.py              # Métadonnées du package
│       ├── config.py                # Constantes et seuils défensifs
│       ├── core/                    # Moteur algorithmique de labyrinthes
│       │   ├── __init__.py
│       │   ├── maze.py              # DFS Backtracker itératif, Point, validation
│       │   └── solver.py            # Résolveurs A* et BFS
│       ├── quiz/                    # Moteur de défis et pare-feu
│       │   ├── __init__.py
│       │   ├── models.py            # Modèles typés (Question, VerificationResult)
│       │   └── questions.py         # Référentiel et validation côté serveur
│       └── web/                     # Application web Flask
│           ├── __init__.py
│           ├── app.py               # Pattern Application Factory (create_app)
│           └── routes.py            # Blueprints (Web & API REST)
│
├── static/                          # Fichiers statiques servis au client
│   ├── css/
│   ├── js/
│   │   └── game.js                  # Boucle de jeu, canvas, contrôles tactiles
│   └── src/
│       └── input.css
│
├── templates/                       # Gabarits HTML Jinja2
│   ├── home.html
│   └── index.html                   # Vue principale du jeu
│
├── tests/                           # Suite de tests automatisés (pytest)
│   ├── __init__.py
│   ├── conftest.py                  # Fixtures et configuration de test
│   ├── test_api.py                  # Tests d'intégration des endpoints HTTP
│   ├── test_maze.py                 # Tests unitaires de génération
│   ├── test_quiz.py                 # Tests du système de questions
│   └── test_solver.py               # Tests des algorithmes A* et BFS
│
├── .gitignore                       # Règles d'exclusion Git (venv, node_modules)
├── app.py                           # Fichier de compatibilité racine
├── main.py                          # Point d'entrée principal en ligne de commande
├── maze_generator.py                # Fichier de compatibilité racine
├── package.json                     # Gestion des dépendances CSS Tailwind
├── pyproject.toml                   # Configuration moderne du package Python
└── requirements.txt                 # Dépendances Python versionnées
```

---

## 3. Schéma Fonctionnel & Flux de Données

```text
+------------------------------------------------------------------------+
|                          CLIENT (Navigateur)                           |
|  - HTML5 Canvas (rendu 60 FPS, orbe radioactif, halo de particules)    |
|  - game.js (physique de glissade, gestion des carrefours)              |
|  - Interface Tailwind CSS & Clavier / D-Pad tactile                    |
+------------------------------------------------------------------------+
                       ▲                                 │
                       │ JSON (Matrice, Start, End)      │ GET /api/new-game
                       │                                 │ GET /api/question
                       │                                 ▼
+------------------------------------------------------------------------+
|                    COUCHE APPLICATION WEB (Flask)                      |
|  - Blueprints : web_bp (HTML), api_bp (JSON REST)                      |
|  - Validation et contraintes des requêtes (anti-déni de service)       |
|  - Centralisation des gestionnaires d'erreurs (400, 404, 500)          |
+------------------------------------------------------------------------+
                       │                                 ▲
                       ▼                                 │
+-----------------------------------+   +--------------------------------+
|       MODULE CORE (Labyrinthe)    |   |      MODULE QUIZ (Pare-feu)    |
|  - Maze (Backtracking DFS itératif)|   |  - QuestionRepository (Banque) |
|  - Solver (A* Manhattan / BFS)    |   |  - Verification côté serveur   |
|  - Placement borné des entrées    |   |  - Modèles typés (dataclasses) |
+-----------------------------------+   +--------------------------------+
```

---

## 4. Spécifications Algorithmiques

### 4.1. Génération de Labyrinthe (DFS Backtracker Itératif)
- **Garantie d'arbre couvrant parfait** : Le labyrinthe est sans boucle et connexe (un chemin unique relie chaque paire de cases libres).
- **Implémentation sur pile explicite** : Aucune récursion native Python, éliminant tout risque de dépassement de pile `RecursionError` sur de grandes grilles.
- **Bornage défensif des dimensions** : Dimensions impaires contraintes dans l'intervalle `[5, 81]`.

### 4.2. Résolution et Pathfinding
- **A\* (A-Star)** : Utilise une file de priorité `heapq` et l'heuristique de Manhattan (`h(p1, p2) = |x1 - x2| + |y1 - y2|`). Optimal pour les grilles carrées à coût unitaire.
- **BFS (Breadth-First Search)** : Explore en largeur pour garantir le plus court chemin minimal en nombre d'étapes.

---

## 5. Matrice des Points d'Accès de l'API REST

| Endpoint | Méthode | Paramètres | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Aucun | Affiche l'écran d'accueil et le jeu HTML5 Canvas |
| `/api/health` | `GET` | Aucun | Vérifie l'état opérationnel du serveur Flask |
| `/api/new-game` | `GET` | `level` (int, 1-20) | Génère une nouvelle grille, coordonnées de départ et arrivée |
| `/api/question` | `GET` | `lang` (str) | Retourne un défi aléatoire (JS, Python, C) |
| `/api/verify-answer` | `POST` | `{question_id, selected_index}` | Validation sécurisée côté serveur d'une réponse |
| `/api/solve-maze` | `POST` | `{maze, start, end}`, `algo` | Calcule le chemin optimal via A* ou BFS |
