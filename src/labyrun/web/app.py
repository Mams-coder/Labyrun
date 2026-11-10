"""Factory d'application Flask pour Labyrun.

Met en œuvre le pattern Application Factory permettant d'instancier
des contextes d'application isolés pour les tests et la production.
"""

import os
from flask import Flask, jsonify
from src.labyrun.config import ServerConfig
from src.labyrun.web.routes import api_bp, web_bp


def create_app(test_config=None) -> Flask:
    """Crée et configure une instance de l'application Flask Labyrun."""
    app = Flask(
        __name__,
        template_folder=ServerConfig.TEMPLATES_DIR,
        static_folder=ServerConfig.STATIC_DIR,
    )

    app.config["SECRET_KEY"] = ServerConfig.SECRET_KEY

    if test_config:
        app.config.update(test_config)

    # Enregistrement des Blueprints
    app.register_blueprint(web_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix="/api")

    # Gestionnaires d'erreurs centralisés
    @app.errorhandler(404)
    def handle_not_found(err):
        return (
            jsonify({"error": "Ressource introuvable", "code": 404, "message": str(err)}),
            404,
        )

    @app.errorhandler(500)
    def handle_server_error(err):
        return (
            jsonify(
                {
                    "error": "Erreur interne du serveur",
                    "code": 500,
                    "message": "Une erreur inattendue s'est produite.",
                }
            ),
            500,
        )

    return app
