"""Tests unitaires pour la gestion et la vérification des questions de quiz."""

import pytest
from src.labyrun.quiz.questions import QuestionRepository


def test_question_repository_loading(question_repo):
    """Vérifie que les questions par défaut sont correctement chargées."""
    all_q = question_repo.all()
    assert len(all_q) >= 6

    langs = {q.lang for q in all_q}
    assert "JavaScript" in langs
    assert "Python" in langs
    assert "C" in langs


def test_get_random_by_language(question_repo):
    """Vérifie le filtrage insensible à la casse par langage."""
    q_py = question_repo.get_random_by_language("python")
    assert q_py is not None
    assert q_py.lang == "Python"

    q_c = question_repo.get_random_by_language("C")
    assert q_c is not None
    assert q_c.lang == "C"

    # Langage inexistant
    q_unknown = question_repo.get_random_by_language("Brainfuck")
    assert q_unknown is None


def test_answer_verification(question_repo):
    """Vérifie la logique de validation des réponses."""
    all_q = question_repo.all()
    target_q = all_q[0]

    # Bonne réponse
    res_correct = question_repo.verify(target_q.id, target_q.answer_index)
    assert res_correct is not None
    assert res_correct.is_correct is True

    # Mauvaise réponse
    wrong_index = (target_q.answer_index + 1) % len(target_q.options)
    res_wrong = question_repo.verify(target_q.id, wrong_index)
    assert res_wrong is not None
    assert res_wrong.is_correct is False

    # ID de question invalide
    assert question_repo.verify("non-existent-id", 0) is None
