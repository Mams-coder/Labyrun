from flask import Flask, render_template, jsonify, request
from maze_generator import generate_maze
import random # NOUVEAU : Nécessaire pour l'aléatoire

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/new-game')
def new_game():
    level = request.args.get('level', 1, type=int)
    
    base_size = 17
    size = base_size + (level * 4) 
    
    w, h = size, size
    maze = generate_maze(w, h)
    
    empty_cells = []
    for y in range(h):
        for x in range(w):
            if maze[y][x] == 0:
                empty_cells.append([x, y])
                
    start_cell = random.choice(empty_cells)
    
    end_cell = random.choice(empty_cells)
    min_distance = (w // 2) 
    
    while abs(start_cell[0] - end_cell[0]) + abs(start_cell[1] - end_cell[1]) < min_distance:
        end_cell = random.choice(empty_cells)
    
    return jsonify({
        "maze": maze,
        "width": w,
        "height": h,
        "start": start_cell,
        "end": end_cell,
        "level": level
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)