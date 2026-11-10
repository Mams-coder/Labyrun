"""Dépôt de questions et logique de vérification pour Labyrun."""

import random
from typing import List, Optional
from src.labyrun.quiz.models import Question, VerificationResult


class QuestionRepository:
    """Gestionnaire de questions en mémoire avec méthodes de recherche et validation."""

    def __init__(self, questions: Optional[List[Question]] = None) -> None:
        """Initialise le dépôt avec les questions par défaut ou fournies."""
        if questions is not None:
            self._questions = list(questions)
        else:
            self._questions = self._load_default_questions()

    @staticmethod
    def _load_default_questions() -> List[Question]:
        """Charge le catalogue par défaut des questions de programmation."""
        return [
            # JavaScript
            Question(
                id="js-01",
                lang="JavaScript",
                question="Quel mot-clé permet de déclarer une variable dont la valeur ne changera jamais en ES6 ?",
                options=["var", "let", "const", "static"],
                answer_index=2,
                explanation="'const' crée une référence immuable vers une valeur en JavaScript moderne.",
            ),
            Question(
                id="js-02",
                lang="JavaScript",
                question="Quelle méthode permet d'ajouter un élément à la fin d'un tableau ?",
                options=["push()", "pop()", "append()", "add()"],
                answer_index=0,
                explanation="'push()' ajoute un ou plusieurs éléments à la fin d'un Array.",
            ),
            Question(
                id="js-03",
                lang="JavaScript",
                question="Quelle est la valeur de typeof null en JavaScript ?",
                options=["'null'", "'undefined'", "'object'", "'boolean'"],
                answer_index=2,
                explanation="C'est un bug historique d'implémentation de JS : typeof null retourne 'object'.",
            ),
            # Python
            Question(
                id="py-01",
                lang="Python",
                question="Comment obtenir la longueur d'une liste nommée 'tab' ?",
                options=["tab.length()", "len(tab)", "size(tab)", "tab.size"],
                answer_index=1,
                explanation="La fonction built-in 'len()' renvoie le nombre d'éléments d'une séquence.",
            ),
            Question(
                id="py-02",
                lang="Python",
                question="Quel mot-clé est utilisé pour définir une fonction ?",
                options=["function", "def", "func", "define"],
                answer_index=1,
                explanation="'def' introduit une définition de fonction en syntaxe Python.",
            ),
            Question(
                id="py-03",
                lang="Python",
                question="Quelle structure de données garantit l'unicité de ses éléments en Python ?",
                options=["list", "tuple", "dict", "set"],
                answer_index=3,
                explanation="'set' est une collection non ordonnée d'éléments uniques.",
            ),
            # C / Embarqué
            Question(
                id="c-01",
                lang="C",
                question="Que signifie l'acronyme GPIO sur un microcontrôleur ?",
                options=[
                    "Global Processor Input Output",
                    "General Purpose Input/Output",
                    "Graphic Processing Interface Object",
                    "Grid Pin In Out",
                ],
                answer_index=1,
                explanation="GPIO signifie General Purpose Input/Output (broches d'E/S à usage général).",
            ),
            Question(
                id="c-02",
                lang="C",
                question="Comment déclare-t-on un pointeur vers un entier nommé 'ptr' ?",
                options=["int ptr*;", "int &ptr;", "int *ptr;", "pointer int ptr;"],
                answer_index=2,
                explanation="En langage C, 'int *ptr;' déclare un pointeur vers une valeur entière.",
            ),
            Question(
                id="c-03",
                lang="C",
                question="Quelle fonction standard de stdlib.h permet d'allouer de la mémoire sur le tas ?",
                options=["alloc()", "malloc()", "new()", "memget()"],
                answer_index=1,
                explanation="'malloc()' (memory allocation) alloue un bloc d'octets sur le tas (heap).",
            ),
        ]

    def get_by_id(self, question_id: str) -> Optional[Question]:
        """Recherche une question par son identifiant unique."""
        for q in self._questions:
            if q.id == question_id:
                return q
        return None

    def get_random_by_language(self, language: str) -> Optional[Question]:
        """Retourne une question aléatoire pour un langage donné."""
        matching = [
            q for q in self._questions if q.lang.lower() == language.strip().lower()
        ]
        if not matching:
            return None
        return random.choice(matching)

    def verify(self, question_id: str, selected_index: int) -> Optional[VerificationResult]:
        """Vérifie la réponse d'un utilisateur de manière sécurisée côté serveur."""
        q = self.get_by_id(question_id)
        if q is None:
            return None
        is_correct = q.answer_index == selected_index
        return VerificationResult(
            is_correct=is_correct,
            correct_index=q.answer_index,
            explanation=q.explanation,
        )

    def all(self) -> List[Question]:
        """Retourne toutes les questions enregistrées."""
        return list(self._questions)
