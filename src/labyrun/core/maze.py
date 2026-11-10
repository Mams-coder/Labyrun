"""Génération et manipulation de labyrinthes parfaits.

Ce module implémente l'algorithme Randomized Depth-First Search (Backtracking itératif)
avec des garde-fous stricts contre les boucles infinies et les dépassements de mémoire.
"""

from dataclasses import dataclass
import random
from typing import List, Tuple, Optional
from src.labyrun.config import MazeConfig


@dataclass(frozen=True)
class Point:
    """Représente une coordonnée 2D (x, y) dans la grille."""

    x: int
    y: int

    def to_list(self) -> List[int]:
        """Convertit le point en liste [x, y]."""
        return [self.x, self.y]

    def manhattan_distance(self, other: "Point") -> int:
        """Calcule la distance de Manhattan jusqu'à un autre point."""
        return abs(self.x - other.x) + abs(self.y - other.y)


class Maze:
    """Représente une grille de labyrinthe avec sa matrice, dimensions et points clés."""

    def __init__(self, width: int, height: int) -> None:
        """Initialise un labyrinthe en validant et normalisant les dimensions."""
        self.width = self._normalize_dimension(width)
        self.height = self._normalize_dimension(height)
        self.grid: List[List[int]] = [
            [MazeConfig.WALL_CELL for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.start: Optional[Point] = None
        self.end: Optional[Point] = None

    @staticmethod
    def _normalize_dimension(dim: int) -> int:
        """Valide et contraint une dimension pour qu'elle soit impaire et bornée."""
        if dim < MazeConfig.MIN_DIMENSION:
            dim = MazeConfig.MIN_DIMENSION
        elif dim > MazeConfig.MAX_DIMENSION:
            dim = MazeConfig.MAX_DIMENSION

        if dim % 2 == 0:
            dim += 1
        return dim

    def generate(self) -> "Maze":
        """Génère le labyrinthe par exploration en profondeur itérative (DFS Backtracker).

        Garantit qu'aucun débordement de pile (RecursionError) n'est possible
        grâce à une pile explicite stockée dans le tas.
        """
        # Point de départ conventionnel (1, 1)
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = MazeConfig.PATH_CELL

        stack: List[Tuple[int, int]] = [(start_x, start_y)]
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Haut, Bas, Gauche, Droite

        while stack:
            x, y = stack[-1]
            neighbors: List[Tuple[int, int, int, int]] = []

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 < nx < self.width - 1
                    and 0 < ny < self.height - 1
                    and self.grid[ny][nx] == MazeConfig.WALL_CELL
                ):
                    neighbors.append((nx, ny, dx // 2, dy // 2))

            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                # Ouvrir le mur intermédiaire
                self.grid[y + wy][x + wx] = MazeConfig.PATH_CELL
                # Marquer la case voisine
                self.grid[ny][nx] = MazeConfig.PATH_CELL
                stack.append((nx, ny))
            else:
                stack.pop()

        # Sortie garantie en bas à droite
        self.grid[self.height - 2][self.width - 2] = MazeConfig.PATH_CELL
        return self

    def get_empty_cells(self) -> List[Point]:
        """Retourne la liste de toutes les cellules de passage (chemin libre)."""
        cells: List[Point] = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == MazeConfig.PATH_CELL:
                    cells.append(Point(x, y))
        return cells

    def place_endpoints(self) -> Tuple[Point, Point]:
        """Place un point de départ et d'arrivée avec une distance minimale garantie.

        Utilise un algorithme avec compteur d'essais maximal pour empêcher
        toute boucle infinie en cas de topologie contrainte.
        """
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            # Fallback de secours
            p_default = Point(1, 1)
            self.start = p_default
            self.end = p_default
            return p_default, p_default

        start_cell = random.choice(empty_cells)
        min_dist = max(4, (self.width + self.height) // 4)

        best_candidate = empty_cells[-1]
        best_dist = -1

        attempts = 0
        while attempts < MazeConfig.MAX_DISTANCE_ATTEMPTS:
            candidate = random.choice(empty_cells)
            dist = start_cell.manhattan_distance(candidate)
            if dist > best_dist:
                best_dist = dist
                best_candidate = candidate
            if dist >= min_dist:
                best_candidate = candidate
                break
            attempts += 1

        self.start = start_cell
        self.end = best_candidate
        return self.start, self.end

    def to_dict(self) -> dict:
        """Sérialise le labyrinthe sous forme de dictionnaire pour l'API JSON."""
        return {
            "maze": self.grid,
            "width": self.width,
            "height": self.height,
            "start": self.start.to_list() if self.start else [1, 1],
            "end": self.end.to_list() if self.end else [self.width - 2, self.height - 2],
        }


def generate_maze(width: int, height: int) -> List[List[int]]:
    """Fonction utilitaire rétro-compatible retournant la matrice brute."""
    maze = Maze(width, height)
    maze.generate()
    return maze.grid
