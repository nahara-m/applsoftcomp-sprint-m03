"""Quiz mode for verb conjugation."""

import random
from typing import Dict, List, Optional, Tuple

from les_verbs.engine import ConjugationEngine
from les_verbs.tracker import PerformanceTracker


class QuizMode:
    """Quiz mode with 5 questions and end scoring."""

    PRONOUNS = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]

    def __init__(
        self, engine: ConjugationEngine, tracker: Optional[PerformanceTracker] = None
    ):
        """
        Initialize quiz mode.

        Args:
            engine: Conjugation engine instance
            tracker: Optional performance tracker for filtering practiced verbs
        """
        self.engine = engine
        self.tracker = tracker

    def generate_questions(
        self, count: int = 5, verbs_filter: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Generate quiz questions.

        Args:
            count: Number of questions to generate
            verbs_filter: Optional list of verbs to limit questions to

        Returns:
            List of question dicts
        """
        questions = []
        tenses = self.engine.TENSES

        # Determine which verbs to use
        if verbs_filter:
            # Use only the specified verbs
            verbs = [v for v in verbs_filter if v in self.engine.verbs]
        elif self.tracker and self.tracker.has_data():
            # Use only verbs the user has practiced
            verbs = list(self.tracker.progress["verbs"].keys())
            verbs = [v for v in verbs if v in self.engine.verbs]
        else:
            # Fall back to all verbs if no tracker data
            verbs = list(self.engine.verbs.keys())

        if not verbs:
            return []

        # If we have fewer verbs than questions, allow repeats
        allow_repeats = len(verbs) < count

        attempts = 0
        max_attempts = count * 10

        while len(questions) < count and attempts < max_attempts:
            attempts += 1
            verb = random.choice(verbs)
            tense = random.choice(tenses)
            pronoun = random.choice(self.PRONOUNS)

            correct_answer = self.engine.conjugate(verb, tense, pronoun)

            if correct_answer is None:
                continue

            # Avoid duplicate questions
            is_duplicate = any(
                q["verb"] == verb and q["tense"] == tense and q["pronoun"] == pronoun
                for q in questions
            )
            if is_duplicate:
                continue

            questions.append(
                {
                    "verb": verb,
                    "tense": tense,
                    "pronoun": pronoun,
                    "correct_answer": correct_answer,
                }
            )

        return questions[:count]

    def _normalize_answer(self, answer: str) -> str:
        """
        Normalize user answer by removing pronouns.

        Args:
            answer: User's answer string

        Returns:
            Normalized answer (just the verb form)
        """
        answer = answer.strip().lower()

        # List of pronouns to strip from the beginning
        pronouns = [
            "je ",
            "j'",
            "tu ",
            "il ",
            "elle ",
            "on ",
            "nous ",
            "vous ",
            "ils ",
            "elles ",
        ]

        for pronoun in pronouns:
            if answer.startswith(pronoun):
                return answer[len(pronoun) :].strip()

        return answer

    def run_quiz(
        self, questions: List[Dict], user_answers: List[str]
    ) -> Tuple[int, List[Dict]]:
        """
        Run a quiz and score it.

        Args:
            questions: List of question dicts
            user_answers: List of user answers

        Returns:
            Tuple of (score, results with corrections)
        """
        score = 0
        results = []

        for i, question in enumerate(questions):
            if i >= len(user_answers):
                break

            user_answer = user_answers[i].strip().lower()
            correct_answer = question["correct_answer"].lower()

            # Normalize answer to accept "je suis" or just "suis"
            normalized_answer = self._normalize_answer(user_answer)

            is_correct = normalized_answer == correct_answer
            if is_correct:
                score += 1

            results.append(
                {
                    "question": question,
                    "user_answer": user_answer,
                    "normalized_answer": normalized_answer,
                    "is_correct": is_correct,
                }
            )

        return score, results

    def format_question(self, question: Dict, question_num: int) -> str:
        """
        Format a question for display.

        Args:
            question: Question dict
            question_num: Question number

        Returns:
            Formatted question string
        """
        return (
            f"\n  Question {question_num}:\n"
            f"  Verb: {question['verb']} | Tense: {question['tense']} | Pronoun: {question['pronoun']}\n"
        )

    def format_results(self, score: int, total: int, results: List[Dict]) -> str:
        """
        Format quiz results for display.

        Args:
            score: Final score
            total: Total questions
            results: Results list

        Returns:
            Formatted results string
        """
        percentage = int((score / total) * 100) if total > 0 else 0

        output = f"\n{'=' * 60}\n"
        output += f"  Quiz Results\n"
        output += f"{'=' * 60}\n\n"
        output += f"  Score: {score}/{total} ({percentage}%)\n\n"

        if percentage >= 90:
            output += "  🌟 Excellent! You're a French master!\n"
        elif percentage >= 70:
            output += "  👍 Great job! Keep practicing!\n"
        elif percentage >= 50:
            output += "  📚 Good effort! More practice needed!\n"
        else:
            output += "  💪 Don't give up! Practice makes perfect!\n"

        # Show corrections
        incorrect = [r for r in results if not r["is_correct"]]
        if incorrect:
            output += f"\n  Corrections:\n"
            output += f"  {'-' * 40}\n"
            for result in incorrect:
                q = result["question"]
                output += (
                    f"  {q['verb']} ({q['tense']}, {q['pronoun']}): "
                    f"You answered '{result['user_answer']}', "
                    f"correct answer is '{q['correct_answer']}'\n"
                )

        return output

    def run_quiz_interactive(self) -> None:
        """Run an interactive quiz (for CLI use)."""
        print(f"\n{'=' * 60}")
        print("  Quiz Mode")
        print(f"{'=' * 60}")
        print("\n  Type the correct conjugation or 'quit' to exit")
        print("  Press Enter to skip a question\n")

        questions = self.generate_questions(5)
        if not questions:
            print("  ⚠️  No questions available!")
            return

        score = 0
        results = []

        for i, question in enumerate(questions, 1):
            print(self.format_question(question, i))
            user_answer = input("  Your answer: ").strip()

            if user_answer.lower() == "quit":
                print("\n  Quiz cancelled.")
                return

            correct_answer = question["correct_answer"]
            is_correct = user_answer.lower() == correct_answer.lower()

            if is_correct:
                score += 1

            results.append(
                {
                    "question": question,
                    "user_answer": user_answer,
                    "is_correct": is_correct,
                }
            )

        print(self.format_results(score, len(questions), results))
