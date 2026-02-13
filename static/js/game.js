const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const CELL_SIZE = 20; // Taille d'une case en pixels

let mazeGrid = [];
let player = { x: 1, y: 1 };
let goal = { x: 1, y: 1 };

// Fonction principale pour lancer le jeu
async function initGame() {
    // 1. Appeler le backend Python
    const response = await fetch('/api/new-game');
    const data = await response.json();
    
    mazeGrid = data.maze;
    player.x = data.start[0];
    player.y = data.start[1];
    goal.x = data.end[0];
    goal.y = data.end[1];

    // Redimensionner le canvas selon la taille du labyrinthe
    canvas.width = data.width * CELL_SIZE;
    canvas.height = data.height * CELL_SIZE;

    draw();
}

// Fonction de dessin
function draw() {
    // Effacer tout
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dessiner le labyrinthe
    for (let y = 0; y < mazeGrid.length; y++) {
        for (let x = 0; x < mazeGrid[y].length; x++) {
            if (mazeGrid[y][x] === 1) {
                ctx.fillStyle = "#34495e"; // Couleur Mur
                ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }
    }

    // Dessiner la sortie (Rouge)
    ctx.fillStyle = "#e74c3c";
    ctx.fillRect(goal.x * CELL_SIZE, goal.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

    // Dessiner le joueur (Bleu)
    ctx.fillStyle = "#3498db";
    // On ajoute un petit padding pour faire joli
    ctx.fillRect(player.x * CELL_SIZE + 2, player.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
}

// Gestion des mouvements
document.addEventListener('keydown', (e) => {
    let dx = 0;
    let dy = 0;

    if (e.key === "ArrowUp") dy = -1;
    if (e.key === "ArrowDown") dy = 1;
    if (e.key === "ArrowLeft") dx = -1;
    if (e.key === "ArrowRight") dx = 1;

    // Calcul de la future position
    const newX = player.x + dx;
    const newY = player.y + dy;

    // Vérification de collision (si ce n'est pas un mur '1')
    if (mazeGrid[newY] && mazeGrid[newY][newX] === 0) {
        player.x = newX;
        player.y = newY;
        draw();
        checkWin();
    }
});

function checkWin() {
    if (player.x === goal.x && player.y === goal.y) {
        // Petit délai pour laisser le temps au dessin de se faire
        setTimeout(() => alert("Gagné ! 🎉"), 10);
    }
}

// Lancer le jeu au chargement de la page
initGame();