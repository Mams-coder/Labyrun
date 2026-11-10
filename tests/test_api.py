"""Tests d'intégration des endpoints HTTP de l'API Flask de Labyrun."""

import pytest
import json


def test_home_page(client):
    """Vérifie que la page d'accueil HTML se charge correctement."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"DevRun" in response.data or b"Labyrun" in response.data


def test_api_health(client):
    """Vérifie le statut du endpoint de santé."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["app"] == "Labyrun"


def test_api_new_game_default(client):
    """Vérifie la génération d'un labyrinthe avec les paramètres par défaut."""
    response = client.get("/api/new-game")
    assert response.status_code == 200
    data = response.get_json()

    assert "maze" in data
    assert "width" in data
    assert "height" in data
    assert "start" in data
    assert "end" in data
    assert data["level"] == 1
    assert data["width"] == len(data["maze"][0])
    assert data["height"] == len(data["maze"])


def test_api_new_game_level_bounds(client):
    """Vérifie que les niveaux hors limites sont correctement contraints (bornage défensif)."""
    # Niveau négatif -> clampé à 1
    resp_low = client.get("/api/new-game?level=-5")
    assert resp_low.status_code == 200
    assert resp_low.get_json()["level"] == 1

    # Niveau excessif -> clampé à MAX_LEVEL (20)
    resp_high = client.get("/api/new-game?level=999999")
    assert resp_high.status_code == 200
    assert resp_high.get_json()["level"] == 20

    # Paramètre non numérique -> fallback niveau 1
    resp_invalid = client.get("/api/new-game?level=invalid_string")
    assert resp_invalid.status_code == 200
    assert resp_invalid.get_json()["level"] == 1


def test_api_question_success(client):
    """Vérifie la récupération d'une question pour un langage valide."""
    response = client.get("/api/question?lang=Python")
    assert response.status_code == 200
    data = response.get_json()

    assert data["lang"] == "Python"
    assert "q" in data
    assert len(data["options"]) >= 2
    assert "answer" in data


def test_api_question_not_found(client):
    """Vérifie la réponse en cas de langage non supporté."""
    response = client.get("/api/question?lang=RustInconnu")
    assert response.status_code == 404
    data = response.get_json()
    assert data["lang"] == "Erreur"


def test_api_verify_answer(client):
    """Vérifie la route POST de validation de réponse."""
    # Requête valide
    payload = {"question_id": "py-01", "selected_index": 1}
    response = client.post(
        "/api/verify-answer",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["is_correct"] is True

    # Payload manquant
    bad_resp = client.post("/api/verify-answer", data="{}", content_type="application/json")
    assert bad_resp.status_code == 400


def test_api_solve_maze(client):
    """Vérifie l'endpoint de résolution automatique de labyrinthe."""
    maze_resp = client.get("/api/new-game?level=1")
    maze_data = maze_resp.get_json()

    solve_payload = {
        "maze": maze_data["maze"],
        "start": maze_data["start"],
        "end": maze_data["end"],
    }
    response = client.post(
        "/api/solve-maze?algo=astar",
        data=json.dumps(solve_payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["solvable"] is True
    assert res_data["length"] > 0
    assert len(res_data["path"]) == res_data["length"]
