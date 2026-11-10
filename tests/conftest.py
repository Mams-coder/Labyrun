"""Fixtures Pytest partagées pour la suite de tests de Labyrun."""

import pytest
from src.labyrun.web.app import create_app
from src.labyrun.quiz.questions import QuestionRepository
from src.labyrun.core.maze import Maze


@pytest.fixture
def app():
    """Crée une instance de l'application Flask configurée en mode test."""
    app_instance = create_app({"TESTING": True, "DEBUG": False})
    return app_instance


@pytest.fixture
def client(app):
    """Client de test HTTP pour interagir avec l'API Flask."""
    return app.test_client()


@pytest.fixture
def question_repo():
    """Instance fraîche du dépôt de questions."""
    return QuestionRepository()


@pytest.fixture
def sample_maze():
    """Génère un labyrinthe 11x11 déterministe pour les tests."""
    maze = Maze(11, 11)
    maze.generate()
    maze.place_endpoints()
    return maze
