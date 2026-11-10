"""Module de compatibilité racine pour Labyrun.

Permet d'exécuter `python app.py` ou `flask run` tout en déléguant
la logique à l'architecture modulaire `src.labyrun`.
"""

import sys
import os
import subprocess

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
        print("   - Ou directement  : .\\venv\\Scripts\\python.exe app.py")
        print("=" * 65)
        sys.exit(1)

from src.labyrun.web.app import create_app
from src.labyrun.config import ServerConfig

app = create_app()

if __name__ == "__main__":
    app.run(
        host=ServerConfig.HOST,
        port=ServerConfig.PORT,
        debug=ServerConfig.DEBUG,
    )
