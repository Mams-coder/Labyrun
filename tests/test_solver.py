"""Tests unitaires pour les algorithmes de résolution de labyrinthe (A* et BFS)."""

import pytest
from src.labyrun.core.maze import Maze, Point
from src.labyrun.core.solver import AStarSolver, BFSSolver


def test_solvers_on_open_corridor():
    """Vérifie que A* et BFS trouvent le même plus court chemin dans un couloir simple."""
    # Grille 5x5 avec un chemin en ligne droite de (1, 1) à (3, 1)
    grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    start = Point(1, 1)
    end = Point(3, 1)

    bfs = BFSSolver(grid)
    astar = AStarSolver(grid)

    bfs_path = bfs.solve(start, end)
    astar_path = astar.solve(start, end)

    assert bfs_path is not None
    assert astar_path is not None
    assert len(bfs_path) == 3
    assert len(astar_path) == 3
    assert [(p.x, p.y) for p in bfs_path] == [(1, 1), (2, 1), (3, 1)]
    assert [(p.x, p.y) for p in astar_path] == [(1, 1), (2, 1), (3, 1)]


def test_solvers_on_generated_maze(sample_maze):
    """Vérifie que tout labyrinthe parfait généré est résoluble entre départ et arrivée."""
    astar = AStarSolver(sample_maze.grid)
    bfs = BFSSolver(sample_maze.grid)

    path_astar = astar.solve(sample_maze.start, sample_maze.end)
    path_bfs = bfs.solve(sample_maze.start, sample_maze.end)

    assert path_astar is not None
    assert path_bfs is not None
    # Dans un labyrinthe parfait, le chemin unique sans boucle a la même longueur
    assert len(path_astar) == len(path_bfs)
    assert path_astar[0] == sample_maze.start
    assert path_astar[-1] == sample_maze.end


def test_unsolvable_maze():
    """Vérifie le comportement si la sortie est totalement murée."""
    grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    start = Point(1, 1)
    end = Point(3, 1)

    bfs = BFSSolver(grid)
    astar = AStarSolver(grid)

    assert bfs.solve(start, end) is None
    assert astar.solve(start, end) is None
