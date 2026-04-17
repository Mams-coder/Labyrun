from flask import Flask, render_template, jsonify, request
from maze_generator import generate_maze

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
    
    return jsonify({
        "maze": maze,
        "width": w,
        "height": h,
        "start": [1, 1],
        "end": [w-2, h-2],
        "level": level
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)