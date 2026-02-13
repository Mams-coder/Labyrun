import random

def generate_maze(width, height):
    # 1. Créer une grille remplie de murs (1 = mur, 0 = chemin)
    # On force des dimensions impaires pour que l'algo fonctionne bien
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1
    
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # 2. Point de départ (1, 1)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    
    # Pile pour le backtracking [(x, y)]
    stack = [(start_x, start_y)]
    
    while stack:
        x, y = stack[-1]
        
        # Trouver les voisins valides (distance de 2 cases pour sauter le mur)
        neighbors = []
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)] # Haut, Bas, Gauche, Droite
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Vérifier si on est dans la grille et si c'est un mur
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny, dx // 2, dy // 2))
        
        if neighbors:
            # Choisir un voisin au hasard
            nx, ny, wx, wy = random.choice(neighbors)
            
            # Casser le mur entre la case actuelle et la voisine
            maze[y + wy][x + wx] = 0 
            # Marquer la voisine comme chemin
            maze[ny][nx] = 0
            
            stack.append((nx, ny))
        else:
            # Cul-de-sac, on revient en arrière
            stack.pop()
            
    # Ajouter une sortie en bas à droite
    maze[height-2][width-2] = 0
    
    return maze