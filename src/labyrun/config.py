"""Configuration centralisée pour l'application Labyrun.

Ce module définit les constantes globales, les limites défensives
pour éviter les attaques par déni de service (DoS) et la surcharge mémoire,
ainsi que les paramètres par défaut du serveur et du jeu.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class MazeConfig:
    """Paramètres et contraintes pour la génération de labyrinthes."""

    BASE_SIZE: int = 17
    INCREMENT_PER_LEVEL: int = 4
    MIN_DIMENSION: int = 5
    MAX_DIMENSION: int = 81  # Empêche l'allocation excessive de mémoire
    MAX_LEVEL: int = 20  # Niveau maximum autorisé via l'API
    DEFAULT_LEVEL: int = 1
    WALL_CELL: int = 1
    PATH_CELL: int = 0
    MAX_DISTANCE_ATTEMPTS: int = 150  # Limite d'itérations pour placer l'arrivée


@dataclass(frozen=True)
class ServerConfig:
    """Paramètres d'exécution du serveur web Flask."""

    HOST: str = os.getenv("LABYRUN_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("LABYRUN_PORT", "5000"))
    DEBUG: bool = os.getenv("LABYRUN_DEBUG", "false").lower() in ("true", "1", "yes")
    SECRET_KEY: str = os.getenv("LABYRUN_SECRET_KEY", "labyrun-secret-dev-key-change-in-prod")
    TEMPLATES_DIR: str = os.getenv(
        "LABYRUN_TEMPLATES_DIR",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates")),
    )
    STATIC_DIR: str = os.getenv(
        "LABYRUN_STATIC_DIR",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static")),
    )


@dataclass(frozen=True)
class QuizConfig:
    """Paramètres du système de quiz."""

    DEFAULT_LANGUAGE: str = "JavaScript"
    ALLOWED_LANGUAGES: tuple = ("JavaScript", "Python", "C")
