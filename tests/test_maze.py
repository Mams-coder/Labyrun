"""Tests unitaires pour la génération de labyrinthes et le modèle Maze."""

import pytest
from src.labyrun.core.maze import Maze, Point, generate_maze
from src.labyrun.config import MazeConfig


def test_dimension_normalization():
    """Vérifie que les dimensions sont toujours impaires et bornées."""
    # Pair -> Impair
    maze_even = Maze(10, 12)
    assert maze_even.width % 2 == 1
    assert maze_even.height % 2 == 1

    # Trop petit -> Min dimension
    maze_small = Maze(2, 2)
    assert maze_small.width >= MazeConfig.MIN_DIMENSION
    assert maze_small.height >= MazeConfig.MIN_DIMENSION

    # Trop grand -> Max dimension
    maze_large = Maze(200, 300)
    assert maze_large.width <= MazeConfig.MAX_DIMENSION
    assert maze_large.height <= MazeConfig.MAX_DIMENSION


def test_maze_generation():
    """Vérifie la structure interne après génération."""
    maze = Maze(15, 15)
    maze.generate()

    # Les dimensions de la matrice correspondent
    assert len(maze.grid) == maze.height
    assert len(maze.grid[0]) == maze.width

    # Les cellules de départ conventionnelle et de sortie sont des chemins (0)
    assert maze.grid[1][1] == MazeConfig.PATH_CELL
    assert maze.grid[maze.height - 2][maze.width - 2] == MazeConfig.PATH_CELL

    # Les bordures extérieures restent des murs (1)
    for x in range(maze.width):
        assert maze.grid[0][x] == MazeConfig.WALL_CELL
        assert maze.grid[maze.height - 1][x] == MazeConfig.WALL_CELL
    for y in range(maze.height):
        assert maze.grid[y][0] == MazeConfig.WALL_CELL
        assert maze.grid[y][maze.width - 1] == MazeConfig.WALL_CELL


def test_endpoints_placement():
    """Vérifie que le départ et l'arrivée sont positionnés sur des chemins avec distance."""
    maze = Maze(17, 17)
    maze.generate()
    start, end = maze.place_endpoints()

    assert isinstance(start, Point)
    assert isinstance(end, Point)
    assert maze.grid[start.y][start.x] == MazeConfig.PATH_CELL
    assert maze.grid[end.y][end.x] == MazeConfig.PATH_CELL
    assert start.manhattan_distance(end) > 0


def test_legacy_generate_maze():
    """Vérifie la fonction rétro-compatible generate_maze()."""
    grid = generate_maze(15, 15)
    assert isinstance(grid, list)
    assert len(grid) == 15
    assert len(grid[0]) == 15
