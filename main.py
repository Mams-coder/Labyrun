"""Point d'entrée principal pour exécuter l'application Labyrun."""

import argparse
import sys
import os
import subprocess

# S'assurer que le répertoire racine est dans le sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Détection et bascule automatique sur le venv local si Flask n'est pas dans le Python global
try:
    import flask  # noqa: F401
except ImportError:
    venv_python_win = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
    venv_python_posix = os.path.join(BASE_DIR, "venv", "bin", "python")
    venv_python = (
        venv_python_win
        if os.path.isfile(venv_python_win)
        else (venv_python_posix if os.path.isfile(venv_python_posix) else None)
    )

    if (
        venv_python
        and os.path.abspath(sys.executable).lower() != os.path.abspath(venv_python).lower()
    ):
        print(f"[Labyrun] 🔄 Bascule automatique sur l'interpréteur venv : {venv_python}")
        try:
            completed = subprocess.run([venv_python] + sys.argv, cwd=BASE_DIR)
            sys.exit(completed.returncode)
        except KeyboardInterrupt:
            print("\n[Labyrun] Arrêt du serveur.")
            sys.exit(0)
    else:
        print("=" * 65)
        print("❌ [ERREUR] Dépendances manquantes : le module 'flask' n'est pas installé.")
        print()
        print("👉 Veuillez activer l'environnement virtuel local du projet :")
        print("   - Sous PowerShell : .\\venv\\Scripts\\Activate.ps1")
        print("   - Sous CMD        : venv\\Scripts\\activate.bat")
        print("   - Ou directement  : .\\venv\\Scripts\\python.exe main.py")
        print()
        print("👉 Ou installez les dépendances :")
        print("   pip install -r requirements.txt")
        print("=" * 65)
        sys.exit(1)

from src.labyrun.config import ServerConfig
from src.labyrun.web.app import create_app


def main():
    """Parse les arguments de ligne de commande et démarre le serveur web Flask."""
    parser = argparse.ArgumentParser(
        description="Labyrun - Jeu d'évasion et de code dans un labyrinthe procédural."
    )
    parser.add_argument(
        "--host",
        type=str,
        default=ServerConfig.HOST,
        help=f"Hôte d'écoute du serveur (défaut: {ServerConfig.HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=ServerConfig.PORT,
        help=f"Port d'écoute du serveur (défaut: {ServerConfig.PORT})",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=ServerConfig.DEBUG,
        help="Activer le mode debug de Flask",
    )

    args = parser.parse_args()

    app = create_app()

    print("=" * 60)
    print("   🎮 LABYRUN - SERVEUR D'INGÉNIERIE & DE JEU")
    print(f"   🚀 Démarrage sur http://{args.host}:{args.port}")
    print(f"   🛠️ Mode Debug : {args.debug}")
    print("=" * 60)

    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n[Labyrun] Arrêt demandé par l'utilisateur.")


if __name__ == "__main__":
    main()
