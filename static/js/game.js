// const canvas = document.getElementById('gameCanvas');
// const ctx = canvas.getContext('2d');
// const CELL_SIZE = 20; // Taille d'une case en pixels

// let mazeGrid = [];
// let player = { x: 1, y: 1 };
// let goal = { x: 1, y: 1 };

// // Fonction principale pour lancer le jeu
// async function initGame() {
//     // 1. Appeler le backend Python
//     const response = await fetch('/api/new-game');
//     const data = await response.json();

//     mazeGrid = data.maze;
//     player.x = data.start[0];
//     player.y = data.start[1];
//     goal.x = data.end[0];
//     goal.y = data.end[1];

//     // Redimensionner le canvas selon la taille du labyrinthe
//     canvas.width = data.width * CELL_SIZE;
//     canvas.height = data.height * CELL_SIZE;

//     draw();
// }

// // Fonction de dessin
// // function draw() {
// //     // Effacer tout
// //     ctx.clearRect(0, 0, canvas.width, canvas.height);

// //     // Dessiner le labyrinthe
// //     for (let y = 0; y < mazeGrid.length; y++) {
// //         for (let x = 0; x < mazeGrid[y].length; x++) {
// //             if (mazeGrid[y][x] === 1) {
// //                 ctx.fillStyle = "#34495e"; // Couleur Mur
// //                 ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
// //             }
// //         }
// //     }

// //     // Dessiner la sortie (Rouge)
// //     ctx.fillStyle = "#e74c3c";
// //     ctx.fillRect(goal.x * CELL_SIZE, goal.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

// //     // Dessiner le joueur (Bleu)
// //     ctx.fillStyle = "#3498db";
// //     // On ajoute un petit padding pour faire joli
// //     ctx.fillRect(player.x * CELL_SIZE + 2, player.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
// // }

// function draw() {
//     // 1. Fond du labyrinthe (Le chemin en jaune/doré clair)
//     ctx.fillStyle = "#fada5e"; // Couleur "Royal Yellow"
//     ctx.fillRect(0, 0, canvas.width, canvas.height);

//     // 2. Dessin des MURS avec un effet 3D (Ombre portée)
//     ctx.shadowColor = "rgba(0, 0, 0, 0.35)"; // Ombre noire semi-transparente
//     ctx.shadowBlur = 4;                      // Flou de l'ombre
//     ctx.shadowOffsetX = 2;                   // Décalage vers la droite
//     ctx.shadowOffsetY = 4;                   // Décalage vers le bas
//     ctx.fillStyle = "#d4ac0d";               // Couleur des murs (Doré sombre)

//     for (let y = 0; y < mazeGrid.length; y++) {
//         for (let x = 0; x < mazeGrid[y].length; x++) {
//             if (mazeGrid[y][x] === 1) {
//                 // On dessine le mur un tout petit peu plus grand pour éviter les lignes de démarcation
//                 ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE + 0.5, CELL_SIZE + 0.5);
//             }
//         }
//     }

//     // --- On réinitialise l'ombre pour ne pas l'appliquer partout ---
//     ctx.shadowColor = "transparent";
//     ctx.shadowOffsetX = 0;
//     ctx.shadowOffsetY = 0;

//     // Utilitaires pour trouver le centre exact d'une case
//     const centerX = (x) => x * CELL_SIZE + CELL_SIZE / 2;
//     const centerY = (y) => y * CELL_SIZE + CELL_SIZE / 2;
//     const radius = CELL_SIZE / 3; // Taille des orbes

//     // 3. Dessin de la SORTIE (Orbe scintillant)
//     ctx.beginPath();
//     ctx.arc(centerX(goal.x), centerY(goal.y), radius, 0, Math.PI * 2);
//     ctx.fillStyle = "#ffffff";
//     ctx.shadowColor = "#f1c40f"; // Lueur dorée éclatante
//     ctx.shadowBlur = 25;         // Lueur très large
//     ctx.fill();
//     ctx.closePath();

//     // 4. Dessin du JOUEUR (L'Orbe de Lumière)
//     ctx.beginPath();
//     ctx.arc(centerX(player.x), centerY(player.y), radius, 0, Math.PI * 2);
//     ctx.fillStyle = "#ffffff";   // Coeur blanc pur
//     ctx.shadowColor = "#ffffff"; // Lueur blanche
//     ctx.shadowBlur = 30;         // Effet d'éblouissement fort
//     ctx.fill();
//     ctx.closePath();

//     // Reset complet du blur pour la prochaine frame (très important)
//     ctx.shadowBlur = 0;
// }

// // Gestion des mouvements
// document.addEventListener('keydown', (e) => {
//     let dx = 0;
//     let dy = 0;

//     if (e.key === "ArrowUp") dy = -1;
//     if (e.key === "ArrowDown") dy = 1;
//     if (e.key === "ArrowLeft") dx = -1;
//     if (e.key === "ArrowRight") dx = 1;

//     // Calcul de la future position
//     const newX = player.x + dx;
//     const newY = player.y + dy;

//     // Vérification de collision (si ce n'est pas un mur '1')
//     if (mazeGrid[newY] && mazeGrid[newY][newX] === 0) {
//         player.x = newX;
//         player.y = newY;
//         draw();
//         checkWin();
//     }
// });

// function checkWin() {
//     if (player.x === goal.x && player.y === goal.y) {
//         // Petit délai pour laisser le temps au dessin de se faire
//         setTimeout(() => alert("Gagné ! 🎉"), 10);
//     }
// }

// function movePlayer(dx, dy) {
//     const newX = player.x + dx;
//     const newY = player.y + dy;

//     // Vérification : Est-ce qu'on reste dans la grille ?
//     if (mazeGrid[newY] && mazeGrid[newY][newX] !== undefined) {
//         // Vérification : Est-ce un chemin (0) ?
//         if (mazeGrid[newY][newX] === 0) {
//             player.x = newX;
//             player.y = newY;
//             draw();
//             checkWin();
//         }
//     }
// }

// // 2. Écouteurs pour le CLAVIER
// document.addEventListener('keydown', (e) => {
//     if (e.key === "ArrowUp") movePlayer(0, -1);
//     if (e.key === "ArrowDown") movePlayer(0, 1);
//     if (e.key === "ArrowLeft") movePlayer(-1, 0);
//     if (e.key === "ArrowRight") movePlayer(1, 0);
// });

// // 3. Écouteurs pour les BOUTONS (Souris / Tactile)
// document.getElementById('btnUp').addEventListener('click', () => movePlayer(0, -1));
// document.getElementById('btnDown').addEventListener('click', () => movePlayer(0, 1));
// document.getElementById('btnLeft').addEventListener('click', () => movePlayer(-1, 0));
// document.getElementById('btnRight').addEventListener('click', () => movePlayer(1, 0));
// // Lancer le jeu au chargement de la page
// initGame();

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');

let CELL_SIZE = 20; 
let mazeGrid = [];
let player = { x: 1, y: 1 };
let goal = { x: 1, y: 1 };
let currentMazeColor = colorPicker ? colorPicker.value : "#059669"; 

if (colorPicker) {
    colorPicker.addEventListener('input', (e) => {
        currentMazeColor = e.target.value;
    });
}

// --- NOUVEAU : SYSTÈME DE GLISSADE ---
let realX = 1; // Position visuelle X exacte
let realY = 1; // Position visuelle Y exacte
let isMoving = false; // L'orbe est-il en train de glisser ?
let moveDx = 0; // Direction X actuelle
let moveDy = 0; // Direction Y actuelle
const SPEED = 0.2; // Vitesse de la glissade (plus c'est élevé, plus ça va vite)

// --- PARTICULES RADIOACTIVES ---
let particles = [];
const MAX_PARTICLES = 35; 

class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 1.2;
        this.vy = (Math.random() - 0.5) * 1.2;
        this.life = Math.random() * 30 + 20;
        this.maxLife = this.life;
        this.size = Math.random() * 2 + 1;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life--;
    }
    draw(ctx) {
        const alpha = Math.max(0, this.life / this.maxLife);
        ctx.fillStyle = `rgba(173, 255, 47, ${alpha})`; 
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

async function initGame() {
    try {
        const response = await fetch('/api/new-game');
        const data = await response.json();
        
        mazeGrid = data.maze;
        player = { x: data.start[0], y: data.start[1] };
        goal = { x: data.end[0], y: data.end[1] };
        
        // Réinitialiser la glissade
        realX = player.x;
        realY = player.y;
        isMoving = false;
        particles = []; 

        CELL_SIZE = 420 / data.width; 
        canvas.width = data.width * CELL_SIZE;
        canvas.height = data.height * CELL_SIZE;
    } catch (e) {
        console.error("Erreur serveur :", e);
    }
}

let currentLevel = 1;

async function initGame(resetToLevel1 = false) {
    // Si on a cliqué sur le bouton recommencer, on remet le niveau à 1
    if (resetToLevel1) {
        currentLevel = 1;
    }

    try {
        const response = await fetch(`/api/new-game?level=${currentLevel}`);
        const data = await response.json();
        
        mazeGrid = data.maze;
        player = { x: data.start[0], y: data.start[1] };
        goal = { x: data.end[0], y: data.end[1] };
        particles = []; 

        const levelDisplay = document.getElementById('levelDisplay');
        if (levelDisplay) levelDisplay.innerText = `NIVEAU ${currentLevel}`;

        realX = player.x;
        realY = player.y;
        isMoving = false;
        moveDx = 0;
        moveDy = 0;

        CELL_SIZE = 420 / data.width; 
        canvas.width = data.width * CELL_SIZE;
        canvas.height = data.height * CELL_SIZE;
    } catch (e) {
        console.error("Erreur serveur :", e);
    }
}

function updatePlayer() {
    if (!isMoving) return;

    realX += moveDx * SPEED;
    realY += moveDy * SPEED;

    if ((moveDx > 0 && realX >= player.x + 1) ||
        (moveDx < 0 && realX <= player.x - 1) ||
        (moveDy > 0 && realY >= player.y + 1) ||
        (moveDy < 0 && realY <= player.y - 1)) {
        
        player.x += moveDx;
        player.y += moveDy;
        
        realX = player.x;
        realY = player.y;

        checkWin();
        if (player.x === goal.x && player.y === goal.y) {
            isMoving = false;
            return;
        }

        const canGoStraight = mazeGrid[player.y + moveDy] && mazeGrid[player.y + moveDy][player.x + moveDx] === 0;
        
        let canTurn = false;
        if (moveDx !== 0) { // Si on bouge horizontalement, on vérifie haut/bas
            canTurn = (mazeGrid[player.y - 1] && mazeGrid[player.y - 1][player.x] === 0) || 
                      (mazeGrid[player.y + 1] && mazeGrid[player.y + 1][player.x] === 0);
        } else { // Si on bouge verticalement, on vérifie gauche/droite
            canTurn = (mazeGrid[player.y] && mazeGrid[player.y][player.x - 1] === 0) || 
                      (mazeGrid[player.y] && mazeGrid[player.y][player.x + 1] === 0);
        }

        // Si c'est un mur tout droit OU si c'est un carrefour, on s'arrête !
        if (!canGoStraight || canTurn) {
            isMoving = false; 
        }
    }
}


function gameLoop() {
    updatePlayer(); // On met à jour la position en glissade
    draw(); 
    requestAnimationFrame(gameLoop);
}

function draw() {
    if (mazeGrid.length === 0) return;

    // 1. Fond
    ctx.fillStyle = "#0f172a"; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. MURS FINS 3D
    ctx.fillStyle = currentMazeColor; 
    ctx.shadowColor = "rgba(0, 0, 0, 0.85)"; 
    ctx.shadowBlur = 0;    
    ctx.shadowOffsetX = 0; 
    ctx.shadowOffsetY = 8; 

    const thicknessScale = 0.25; 
    const wallThick = CELL_SIZE * thicknessScale; 
    const offset = (CELL_SIZE - wallThick) / 2;

    ctx.beginPath(); 
    for (let y = 0; y < mazeGrid.length; y++) {
        for (let x = 0; x < mazeGrid[y].length; x++) {
            if (mazeGrid[y][x] === 1) {
                ctx.rect(x * CELL_SIZE + offset, y * CELL_SIZE + offset, wallThick, wallThick);

                if (x < mazeGrid[y].length - 1 && mazeGrid[y][x+1] === 1) {
                    ctx.rect(x * CELL_SIZE + offset + wallThick, y * CELL_SIZE + offset, CELL_SIZE - wallThick, wallThick);
                }
                
                if (y < mazeGrid.length - 1 && mazeGrid[y+1][x] === 1) {
                    ctx.rect(x * CELL_SIZE + offset, y * CELL_SIZE + offset + wallThick, wallThick, CELL_SIZE - wallThick);
                }
            }
        }
    }
    ctx.fill(); 

    ctx.shadowColor = "transparent";
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    const centerX = (x) => x * CELL_SIZE + CELL_SIZE / 2;
    const centerY = (y) => y * CELL_SIZE + CELL_SIZE / 2;
    const radius = CELL_SIZE / 3;

    // 3. LA SORTIE
    ctx.beginPath();
    ctx.arc(centerX(goal.x), centerY(goal.y), radius, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = "#38bdf8"; 
    ctx.shadowBlur = 20;         
    ctx.fill();
    ctx.closePath();

    // 4. LE JOUEUR (Orbe Radioactif & Particules)
    // On utilise realX et realY pour que le dessin soit fluide !
    const px = centerX(realX);
    const py = centerY(realY);

    if (particles.length < MAX_PARTICLES && Math.random() < 0.7) {
        particles.push(new Particle(px + (Math.random()-0.5)*12, py + (Math.random()-0.5)*12));
    }
    for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        particles[i].draw(ctx);
        if (particles[i].life <= 0) particles.splice(i, 1);
    }

    const time = Date.now() / 150; 
    const pulse = Math.sin(time) * 3; 
    const haloRadius = radius + 6 + pulse;

    const gradient = ctx.createRadialGradient(px, py, radius / 2, px, py, haloRadius);
    gradient.addColorStop(0, "rgba(173, 255, 47, 0.9)"); 
    gradient.addColorStop(0.5, "rgba(34, 197, 94, 0.5)"); 
    gradient.addColorStop(1, "rgba(0, 255, 0, 0)");       

    ctx.beginPath();
    ctx.arc(px, py, Math.max(0, haloRadius), 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.arc(px, py, radius - 2, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";   
    ctx.shadowColor = "#adff2f"; 
    ctx.shadowBlur = 25;         
    ctx.fill();
    ctx.closePath();

    ctx.shadowBlur = 0; 
}

// --- CONTRÔLES MODIFIÉS ---
function movePlayer(dx, dy) {
    if (isMoving) return; // Si l'orbe glisse déjà, on ignore les touches

    const newX = player.x + dx;
    const newY = player.y + dy;

    // Si le chemin direct est libre, on lance la glissade !
    if (mazeGrid[newY] && mazeGrid[newY][newX] === 0) { 
        isMoving = true;
        moveDx = dx;
        moveDy = dy;
    }
}

function checkWin() {
    if (player.x === goal.x && player.y === goal.y) {
        setTimeout(() => {
            currentLevel++; 
            alert(`☢️ Niveau terminé ! Préparation du NIVEAU ${currentLevel}...`);
            initGame(false); // false = on ne reset pas le niveau
        }, 100);
    }
}

document.addEventListener('keydown', (e) => {
    if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault(); 
    }
    if (e.key === "ArrowUp") movePlayer(0, -1);
    if (e.key === "ArrowDown") movePlayer(0, 1);
    if (e.key === "ArrowLeft") movePlayer(-1, 0);
    if (e.key === "ArrowRight") movePlayer(1, 0);
});

const directions = {
    'btnUp': [0, -1], 'btnDown': [0, 1], 'btnLeft': [-1, 0], 'btnRight': [1, 0]
};

for (const [id, dir] of Object.entries(directions)) {
    const btn = document.getElementById(id);
    if (btn) {
        btn.addEventListener('click', () => movePlayer(dir[0], dir[1]));
        btn.addEventListener('touchstart', (e) => {
            e.preventDefault(); 
            movePlayer(dir[0], dir[1]);
        });
    }
}

initGame().then(() => {
    requestAnimationFrame(gameLoop); 
});