"""Modèles de données typés pour le système de questions et de défis de Labyrun."""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class Question:
    """Représente une question à choix multiples pour un langage donné."""

    id: str
    lang: str
    question: str
    options: List[str]
    answer_index: int
    explanation: str = ""

    def to_client_dict(self, include_answer: bool = True) -> Dict[str, Any]:
        """Convertit en dictionnaire pour le client web.

        Par défaut, conserve la rétro-compatibilité avec le frontend actuel ('q', 'options', 'answer').
        Le paramètre include_answer permet de masquer l'indice de la réponse correcte
        pour une vérification strictement côté serveur.
        """
        payload: Dict[str, Any] = {
            "id": self.id,
            "lang": self.lang,
            "q": self.question,
            "options": list(self.options),
        }
        if include_answer:
            payload["answer"] = self.answer_index
        return payload


@dataclass(frozen=True)
class QuizSubmission:
    """Représente la soumission d'une réponse par un joueur."""

    question_id: str
    selected_index: int


@dataclass(frozen=True)
class VerificationResult:
    """Résultat de vérification d'une réponse."""

    is_correct: bool
    correct_index: int
    explanation: str
