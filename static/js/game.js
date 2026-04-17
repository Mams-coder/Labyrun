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
// function draw() {
//     // Effacer tout
//     ctx.clearRect(0, 0, canvas.width, canvas.height);

//     // Dessiner le labyrinthe
//     for (let y = 0; y < mazeGrid.length; y++) {
//         for (let x = 0; x < mazeGrid[y].length; x++) {
//             if (mazeGrid[y][x] === 1) {
//                 ctx.fillStyle = "#34495e"; // Couleur Mur
//                 ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
//             }
//         }
//     }

//     // Dessiner la sortie (Rouge)
//     ctx.fillStyle = "#e74c3c";
//     ctx.fillRect(goal.x * CELL_SIZE, goal.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

//     // Dessiner le joueur (Bleu)
//     ctx.fillStyle = "#3498db";
//     // On ajoute un petit padding pour faire joli
//     ctx.fillRect(player.x * CELL_SIZE + 2, player.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
// }

function draw() {
    // 1. Fond du labyrinthe (Le chemin en jaune/doré clair)
    ctx.fillStyle = "#fada5e"; // Couleur "Royal Yellow"
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Dessin des MURS avec un effet 3D (Ombre portée)
    ctx.shadowColor = "rgba(0, 0, 0, 0.35)"; // Ombre noire semi-transparente
    ctx.shadowBlur = 4;                      // Flou de l'ombre
    ctx.shadowOffsetX = 2;                   // Décalage vers la droite
    ctx.shadowOffsetY = 4;                   // Décalage vers le bas
    ctx.fillStyle = "#d4ac0d";               // Couleur des murs (Doré sombre)

    for (let y = 0; y < mazeGrid.length; y++) {
        for (let x = 0; x < mazeGrid[y].length; x++) {
            if (mazeGrid[y][x] === 1) {
                // On dessine le mur un tout petit peu plus grand pour éviter les lignes de démarcation
                ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE + 0.5, CELL_SIZE + 0.5);
            }
        }
    }

    // --- On réinitialise l'ombre pour ne pas l'appliquer partout ---
    ctx.shadowColor = "transparent";
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    // Utilitaires pour trouver le centre exact d'une case
    const centerX = (x) => x * CELL_SIZE + CELL_SIZE / 2;
    const centerY = (y) => y * CELL_SIZE + CELL_SIZE / 2;
    const radius = CELL_SIZE / 3; // Taille des orbes

    // 3. Dessin de la SORTIE (Orbe scintillant)
    ctx.beginPath();
    ctx.arc(centerX(goal.x), centerY(goal.y), radius, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = "#f1c40f"; // Lueur dorée éclatante
    ctx.shadowBlur = 25;         // Lueur très large
    ctx.fill();
    ctx.closePath();

    // 4. Dessin du JOUEUR (L'Orbe de Lumière)
    ctx.beginPath();
    ctx.arc(centerX(player.x), centerY(player.y), radius, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";   // Coeur blanc pur
    ctx.shadowColor = "#ffffff"; // Lueur blanche
    ctx.shadowBlur = 30;         // Effet d'éblouissement fort
    ctx.fill();
    ctx.closePath();

    // Reset complet du blur pour la prochaine frame (très important)
    ctx.shadowBlur = 0;
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

function movePlayer(dx, dy) {
    const newX = player.x + dx;
    const newY = player.y + dy;

    // Vérification : Est-ce qu'on reste dans la grille ?
    if (mazeGrid[newY] && mazeGrid[newY][newX] !== undefined) {
        // Vérification : Est-ce un chemin (0) ?
        if (mazeGrid[newY][newX] === 0) {
            player.x = newX;
            player.y = newY;
            draw();
            checkWin();
        }
    }
}

// 2. Écouteurs pour le CLAVIER
document.addEventListener('keydown', (e) => {
    if (e.key === "ArrowUp") movePlayer(0, -1);
    if (e.key === "ArrowDown") movePlayer(0, 1);
    if (e.key === "ArrowLeft") movePlayer(-1, 0);
    if (e.key === "ArrowRight") movePlayer(1, 0);
});

// 3. Écouteurs pour les BOUTONS (Souris / Tactile)
document.getElementById('btnUp').addEventListener('click', () => movePlayer(0, -1));
document.getElementById('btnDown').addEventListener('click', () => movePlayer(0, 1));
document.getElementById('btnLeft').addEventListener('click', () => movePlayer(-1, 0));
document.getElementById('btnRight').addEventListener('click', () => movePlayer(1, 0));
// Lancer le jeu au chargement de la page
initGame();