# 🎮 Labyrun - Jeu d'Évasion Procédurale

```text
██╗      █████╗ ██████╗ ██╗   ██╗██████╗ ██╗   ██╗███╗   ██╗
██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██║   ██║████╗  ██║
██║     ███████║██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██╔██╗ ██║
██║     ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██╗██║   ██║██║╚██╗██║
███████╗██║  ██║██████╔╝   ██║   ██║  ██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask%203.x-green.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/tests-pytest%20passing-brightgreen.svg)](https://pytest.org/)
[![Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://peps.python.org/pep-0008/)

---

## 🎯 Pitch & Démonstration

**Labyrun** (anciennement *DevRun*) est un jeu d'arcade hybride combinant la navigation réactive dans des labyrinthes générés de façon procédurale et la résolution de défis de programmation pour pirater des pare-feux de sécurité.

Le joueur incarne un **orbe radioactif lumineux** propulsé dans une matrice cybernétique. À chaque fois qu'il atteint la sortie du secteur, un pare-feu se déclenche : il doit répondre correctement à une question technique (JavaScript, Python ou C/Embarqué) pour valider l'accès au niveau suivant. 
En cas de série victorieuse (Combo x3), le mode **🔥 OVERDRIVE** s'active, accordant au joueur la capacité de briser les murs de la matrice !

### Visualisation du Gameplay (ASCII Art)

```text
+-------------------------------------------------------------+
|  NIVEAU 03  [🔥 OVERDRIVE ACTIF]          SPÉCIALITÉ : PYTHON |
+-------------------------------------------------------------+
|  #########################################################  |
|  #   S ..........                                        #  |
|  #   : [O]======>    #############################   #####  |
|  #   :  (Orbe en     #                           #   #   #  |
|  #   :   glissade)   #   #########   #########   #   #   #  |
|  #   :               #   #       #   #   #   #   #   #   #  |
|  #   #   #########   #   #   #   #   #   #   #   #   #   #  |
|  #   #   #       #   #   #   #   #   #   #   #   #       #  |
|  #   #   #   #   #   #   #####   #####   #   #   #####   #  |
|  #   #   #   #   #   #                   #   #       #   #  |
|  #   #   #####   #####   #############   #####   #####   #  |
|  #   #                   #           #           # (E)   #  |
|  #   #####################   #####   #############  [X]  #  |
|  #                           #                   (Sortie)#  |
|  #########################################################  |
+-------------------------------------------------------------+
|  LÉGENDE :                                                  |
|  [O] = Joueur (Orbe lumineux avec particules & glissade)    |
|  [X] = Portail de sortie (Déclencheur du Quiz Pare-feu)     |
|  ### = Murs épais (ou brisables en mode OVERDRIVE)          |
|  ... = Trajectoire fluide calculée en temps réel            |
+-------------------------------------------------------------+
```

---

## 🏛️ Architecture & Conception

Le projet suit une **architecture modulaire en couches**, découplant rigoureusement la logique métier, la persistance en mémoire, l'API REST et le client web :

```text
D:\projets_dev\PYTHON\Projets\Labyrun
├── src/labyrun/
│   ├── config.py           # Configuration centrale, seuils DoS et paramètres serveur
│   ├── core/               # Moteur algorithmique de labyrinthes
│   │   ├── maze.py         # Modèle Maze, DFS Backtracker itératif, Point
│   │   └── solver.py       # Algorithmes de pathfinding (A* Manhattan, BFS)
│   ├── quiz/               # Gestion des défis de code et vérification
│   │   ├── models.py       # Dataclasses immuables (Question, QuizSubmission)
│   │   └── questions.py    # Dépôt de questions et validation serveur
│   └── web/                # Couche HTTP Flask
│       ├── app.py          # Application Factory (create_app)
│       └── routes.py       # Blueprints (Web & API JSON)
├── static/                 # Frontend client (Canvas 2D, animations, particules)
├── templates/              # Gabarits HTML Jinja2 (index.html)
├── tests/                  # Suite de tests unitaires et d'intégration (pytest)
├── main.py                 # Point d'entrée exécutable en ligne de commande
├── pyproject.toml          # Métadonnées du package Python (PEP 621)
└── requirements.txt        # Dépendances versionnées
```

### Algorithmes Utilisés

1. **Génération de Labyrinthe (Randomized DFS Backtracker itératif)** :
   - Génère un labyrinthe parfait (arbre couvrant sans cycle ni boucle fermée).
   - Utilise une pile explicite stockée sur le tas (Heap) plutôt qu'une récursion native, évitant tout débordement de pile `RecursionError`.
   - Garantit des dimensions impaires normalisées et bornées pour préserver l'intégrité de la grille.

2. **Algorithme A\* (A-Star Pathfinding)** :
   - Recherche le chemin optimal entre deux points à l'aide d'une file de priorité (`heapq`).
   - Utilise l'heuristique de Manhattan adaptée aux grilles orthogonales :
     $$h(p_1, p_2) = |x_1 - x_2| + |y_1 - y_2|$$
   - Fournit une résolution instantanée pour le calcul de distance et la vérification de solvabilité.

3. **Parcours en Largeur (BFS - Breadth-First Search)** :
   - Vérifie la connexité complète de la grille.
   - Garantit le nombre minimal absolu d'étapes entre la case de départ et la case d'arrivée.

---

## 🛠️ Stack Technique

- **Langage** : Python 3.10+ (développé et testé sous Python 3.14).
- **Backend Web** : [Flask 3.1+](https://flask.palletsprojects.com/) avec Blueprints et Application Factory.
- **Moteur de Templates** : [Jinja2](https://jinja.palletsprojects.com/).
- **Frontend / Rendu** : HTML5 Canvas 2D accéléré, JavaScript moderne (ES6+), boucle d'animation `requestAnimationFrame`.
- **Design & Styles** : [Tailwind CSS v4](https://tailwindcss.com/) via CDN et compilation PostCSS.
- **Tests & Assurance Qualité** : [pytest](https://pytest.org/), `pytest-cov`, typage statique [typing / mypy].

---

## 🚀 Installation & Démarrage

### 1. Prérequis
Assurez-vous d'avoir Python 3.10 ou supérieur installé :
```bash
python --version
```

### 2. Cloner ou naviguer dans le répertoire local
```bash
cd D:\projets_dev\PYTHON\Projets\Labyrun
```

### 3. Création et activation de l'environnement virtuel (venv)
- **Sous Windows (PowerShell)** :
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Sous Windows (CMD)** :
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Sous Linux / macOS** :
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 5. Lancement de l'application
Exécutez le point d'entrée principal :
```bash
python main.py
```
*Options disponibles :*
```bash
python main.py --host 127.0.0.1 --port 5000 --debug
```
Ouvrez votre navigateur web sur **[http://127.0.0.1:5000](http://127.0.0.1:5000)** pour jouer !

---

## 🧪 Tests Automatisés

Le projet dispose d'une suite complète de tests unitaires et d'intégration validant le cœur algorithmique, la banque de quiz et les endpoints d'API :

```bash
# Exécution simple de tous les tests
pytest

# Exécution verbeuse avec détails
pytest -v

# Exécution avec rapport de couverture de code
pytest --cov=src -v
```

### Couverture des tests
- `tests/test_maze.py` : Dimensions impaires, bornage défensif, connectivité, bordures extérieures.
- `tests/test_solver.py` : Chemins optimaux A*, BFS, détection des impasses et labyrinthes non résolubles.
- `tests/test_quiz.py` : Filtrage insensible à la casse par langage, validation des réponses, fallback sécurisé.
- `tests/test_api.py` : Statut 200/400/404, contrainte des niveaux `level` hors limites (anti-DoS), endpoints `/api/new-game`, `/api/question`, `/api/verify-answer`, `/api/solve-maze`.

---

## 📡 Spécification de l'API REST

| Méthode | Route | Description | Exemple de Requête |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Interface de jeu web principale | `GET /` |
| `GET` | `/api/health` | Vérification de la disponibilité du serveur | `GET /api/health` |
| `GET` | `/api/new-game` | Génération d'une grille pour un niveau donné | `GET /api/new-game?level=2` |
| `GET` | `/api/question` | Récupération d'un défi pour un langage | `GET /api/question?lang=Python` |
| `POST` | `/api/verify-answer` | Validation sécurisée d'une réponse côté serveur | `{"question_id": "py-01", "selected_index": 1}` |
| `POST` | `/api/solve-maze` | Résolution automatique du chemin par A* ou BFS | `{"maze": [...], "start": [1,1], "end": [15,15]}` |

---

## 📄 Licence & Contribution

Projet éducatif et d'ingénierie logicielle sous licence **ISC**. Contributions bienvenues via merge request locale.
