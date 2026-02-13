from flask import Flask, render_template, jsonify
from maze_generator import generate_maze

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/new-game')
def new_game():
    # On génère un labyrinthe de 21x21 (doit être impair)
    maze = generate_maze(21, 21)
    return jsonify({
        "maze": maze,
        "width": 21,
        "height": 21,
        "start": [1, 1],
        "end": [19, 19]
    })

if __name__ == '__main__':
    app.run(debug=True)