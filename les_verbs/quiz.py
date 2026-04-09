"""Quiz mode for verb conjugation."""

import random
from typing import Dict, List, Optional, Tuple

from les_verbs.engine import ConjugationEngine


class QuizMode:
    """Quiz mode with 5 questions and end scoring."""

    PRONOUNS = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]

    def __init__(self, engine: ConjugationEngine):
        """
        Initialize quiz mode.

        Args:
            engine: Conjugation engine instance
        """
        self.engine = engine

    def generate_questions(self, count: int = 5) -> List[Dict]:
        """
        Generate quiz questions.

        Args:
            count: Number of questions to generate

        Returns:
            List of question dicts
        """
        questions = []
        verbs = list(self.engine.verbs.keys())
        tenses = self.engine.TENSES

        if not verbs:
            return []

        for _ in range(count):
            verb = random.choice(verbs)
            tense = random.choice(tenses)
            pronoun = random.choice(self.PRONOUNS)

            correct_answer = self.engine.conjugate(verb, tense, pronoun)

            if correct_answer is None:
                # Try again with different parameters
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

            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1

            results.append(
                {
                    "question": question,
                    "user_answer": user_answer,
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
