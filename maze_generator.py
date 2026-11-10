"""Module de compatibilité racine pour maze_generator.

Redirige vers la nouvelle implémentation modulaire et défensive
située dans `src.labyrun.core.maze`.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.labyrun.core.maze import generate_maze, Maze

__all__ = ["generate_maze", "Maze"]
