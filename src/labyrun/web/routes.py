"""Définition des routes web et des API JSON pour Labyrun."""

from flask import Blueprint, render_template, jsonify, request
from src.labyrun.config import MazeConfig, QuizConfig
from src.labyrun.core.maze import Maze, Point
from src.labyrun.core.solver import AStarSolver, BFSSolver
from src.labyrun.quiz.questions import QuestionRepository

api_bp = Blueprint("api", __name__)
web_bp = Blueprint("web", __name__)

# Instance partagée de la banque de questions
_question_repo = QuestionRepository()


@web_bp.route("/")
def home():
    """Point d'entrée principal : sert l'interface de jeu Labyrun."""
    return render_template("index.html")


@api_bp.route("/health")
def health():
    """Vérification de l'état de santé du service."""
    return jsonify({"status": "ok", "app": "Labyrun", "version": "1.0.0"})


@api_bp.route("/question")
def get_question():
    """Fournit une question aléatoire pour le langage demandé."""
    requested_lang = request.args.get("lang", QuizConfig.DEFAULT_LANGUAGE).strip()

    question = _question_repo.get_random_by_language(requested_lang)
    if not question:
        # Réponse défensive si le langage est introuvable
        return (
            jsonify(
                {
                    "id": "err-not-found",
                    "lang": "Erreur",
                    "q": f"Pas de question trouvée pour le langage : {requested_lang}",
                    "options": ["Retour", "Annuler"],
                    "answer": 0,
                    "explanation": "Langage non répertorié.",
                }
            ),
            404,
        )

    # Conserve 'answer' pour rétro-compatibilité totale avec game.js
    return jsonify(question.to_client_dict(include_answer=True))


@api_bp.route("/verify-answer", methods=["POST"])
def verify_answer():
    """Vérifie la réponse d'un utilisateur côté serveur de manière sécurisée."""
    data = request.get_json(silent=True)
    if not data or "question_id" not in data or "selected_index" not in data:
        return (
            jsonify(
                {
                    "error": "Payload invalide. 'question_id' et 'selected_index' sont requis."
                }
            ),
            400,
        )

    question_id = str(data["question_id"])
    try:
        selected_index = int(data["selected_index"])
    except (ValueError, TypeError):
        return jsonify({"error": "'selected_index' doit être un entier."}), 400

    result = _question_repo.verify(question_id, selected_index)
    if not result:
        return jsonify({"error": f"Question non trouvée : {question_id}"}), 404

    return jsonify(
        {
            "is_correct": result.is_correct,
            "correct_index": result.correct_index,
            "explanation": result.explanation,
        }
    )


@api_bp.route("/new-game")
def new_game():
    """Génère un nouveau labyrinthe avec des dimensions sécurisées basées sur le niveau."""
    # Validation défensive du niveau
    raw_level = request.args.get("level", str(MazeConfig.DEFAULT_LEVEL))
    try:
        level = int(raw_level)
    except (ValueError, TypeError):
        level = MazeConfig.DEFAULT_LEVEL

    # Bornage strict contre DoS et allocations excessives
    if level < 1:
        level = 1
    elif level > MazeConfig.MAX_LEVEL:
        level = MazeConfig.MAX_LEVEL

    # Calcul de dimension impaire
    size = MazeConfig.BASE_SIZE + (level * MazeConfig.INCREMENT_PER_LEVEL)
    if size % 2 == 0:
        size += 1

    maze = Maze(size, size)
    maze.generate()
    start_pt, end_pt = maze.place_endpoints()

    payload = maze.to_dict()
    payload["level"] = level
    return jsonify(payload)


@api_bp.route("/solve-maze", methods=["POST"])
def solve_maze():
    """Résout un labyrinthe donné via l'algorithme A* ou BFS."""
    data = request.get_json(silent=True)
    if not data or "maze" not in data or "start" not in data or "end" not in data:
        return (
            jsonify({"error": "Champs requis : 'maze', 'start' et 'end'."}),
            400,
        )

    grid = data["maze"]
    try:
        start_pt = Point(int(data["start"][0]), int(data["start"][1]))
        end_pt = Point(int(data["end"][0]), int(data["end"][1]))
    except (ValueError, TypeError, IndexError):
        return jsonify({"error": "Format des coordonnées invalide."}), 400

    algorithm = request.args.get("algo", "astar").lower()
    if algorithm == "bfs":
        solver = BFSSolver(grid)
    else:
        solver = AStarSolver(grid)

    path = solver.solve(start_pt, end_pt)
    if path is None:
        return jsonify({"solvable": False, "path": [], "length": 0})

    return jsonify(
        {
            "solvable": True,
            "length": len(path),
            "path": [p.to_list() for p in path],
            "algorithm": algorithm,
        }
    )
