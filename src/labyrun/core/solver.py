"""Algorithmes de résolution et de pathfinding pour Labyrun.

Fournit les implémentations de :
- BFS (Breadth-First Search) : garantie du plus court chemin en nombre de pas
- A* (A-Star) : heuristique de Manhattan pour une résolution guidée et optimale
"""

import heapq
from typing import List, Tuple, Optional, Set, Dict
from src.labyrun.core.maze import Point
from src.labyrun.config import MazeConfig


class BFSSolver:
    """Résolution par parcours en largeur (Breadth-First Search)."""

    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def _is_valid(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and 0 <= y < self.height
            and self.grid[y][x] == MazeConfig.PATH_CELL
        )

    def solve(self, start: Point, end: Point) -> Optional[List[Point]]:
        """Trouve le plus court chemin entre start et end en utilisant BFS."""
        if not self._is_valid(start.x, start.y) or not self._is_valid(end.x, end.y):
            return None

        queue: List[Point] = [start]
        visited: Set[Tuple[int, int]] = {(start.x, start.y)}
        parent: Dict[Tuple[int, int], Point] = {}

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while queue:
            current = queue.pop(0)

            if current.x == end.x and current.y == end.y:
                # Reconstruire le chemin
                path: List[Point] = []
                curr_key = (end.x, end.y)
                while curr_key in parent:
                    path.append(Point(curr_key[0], curr_key[1]))
                    prev = parent[curr_key]
                    curr_key = (prev.x, prev.y)
                path.append(start)
                path.reverse()
                return path

            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy
                if self._is_valid(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
                    queue.append(Point(nx, ny))

        return None


class AStarSolver:
    """Résolution par algorithme A* avec heuristique de Manhattan."""

    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def _is_valid(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and 0 <= y < self.height
            and self.grid[y][x] == MazeConfig.PATH_CELL
        )

    @staticmethod
    def _heuristic(p1: Point, p2: Point) -> int:
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def solve(self, start: Point, end: Point) -> Optional[List[Point]]:
        """Calcule le chemin optimal entre start et end via l'algorithme A*."""
        if not self._is_valid(start.x, start.y) or not self._is_valid(end.x, end.y):
            return None

        # Priority queue stocke (f_score, counter, Point)
        open_set: List[Tuple[int, int, Point]] = []
        counter = 0
        heapq.heappush(open_set, (self._heuristic(start, end), counter, start))

        came_from: Dict[Tuple[int, int], Point] = {}
        g_score: Dict[Tuple[int, int], int] = {(start.x, start.y): 0}

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current.x == end.x and current.y == end.y:
                # Reconstruction du chemin optimal
                path: List[Point] = []
                curr_key = (end.x, end.y)
                while curr_key in came_from:
                    path.append(Point(curr_key[0], curr_key[1]))
                    prev = came_from[curr_key]
                    curr_key = (prev.x, prev.y)
                path.append(start)
                path.reverse()
                return path

            curr_key = (current.x, current.y)
            current_g = g_score.get(curr_key, float("inf"))

            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy
                neighbor = Point(nx, ny)

                if not self._is_valid(nx, ny):
                    continue

                tentative_g = current_g + 1
                neighbor_key = (nx, ny)

                if tentative_g < g_score.get(neighbor_key, float("inf")):
                    came_from[neighbor_key] = current
                    g_score[neighbor_key] = tentative_g
                    f_score = tentative_g + self._heuristic(neighbor, end)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, neighbor))

        return None
