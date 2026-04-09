"""Practice mode for verb conjugation."""

from typing import Dict, List, Optional, Tuple

from les_verbs.engine import ConjugationEngine
from les_verbs.tracker import PerformanceTracker


class PracticeMode:
    """Interactive practice mode with immediate feedback."""

    PRONOUNS = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]

    def __init__(self, engine: ConjugationEngine, tracker: PerformanceTracker):
        """
        Initialize practice mode.

        Args:
            engine: Conjugation engine instance
            tracker: Performance tracker instance
        """
        self.engine = engine
        self.tracker = tracker

    def practice_verb(
        self, infinitive: str, tense: str
    ) -> Tuple[bool, Dict[str, bool]]:
        """
        Practice a verb in a specific tense through all pronouns.

        Args:
            infinitive: The verb to practice
            tense: The tense to practice

        Returns:
            Tuple of (completed, results dict)
        """
        infinitive = infinitive.lower().strip()
        tense = tense.lower().strip()

        if not self.engine.verb_exists(infinitive):
            return False, {}

        print(f"\n{'=' * 60}")
        print(f"  Practicing: {infinitive.upper()} - {tense}")
        print(f"{'=' * 60}\n")

        results = {}
        completed = True

        for pronoun in self.PRONOUNS:
            correct_form = self.engine.conjugate(infinitive, tense, pronoun)

            if correct_form is None:
                print(f"  ⚠️  No conjugation available for {pronoun}")
                continue

            print(f"  {pronoun}: ", end="")
            user_answer = input().strip().lower()

            if user_answer == "quit":
                completed = False
                print("\n  Session cancelled.")
                break

            if user_answer == correct_form.lower():
                print("  ✅ Correct!")
                results[pronoun] = True
                self.tracker.record_answer(infinitive, tense, pronoun, correct=True)
            else:
                print(f"  ❌ Incorrect. Correct answer: {correct_form}")
                results[pronoun] = False
                self.tracker.record_answer(infinitive, tense, pronoun, correct=False)

        if completed:
            self._show_summary(infinitive, tense, results)
            self.tracker.save_verb_complete(infinitive)

        return completed, results

    def _show_summary(
        self, infinitive: str, tense: str, results: Dict[str, bool]
    ) -> None:
        """Show practice summary."""
        correct_count = sum(1 for v in results.values() if v)
        total = len(results)

        print(f"\n  Summary for {infinitive} ({tense}):")
        print(f"  Score: {correct_count}/{total}")

        if correct_count == total:
            print("  🌟 Perfect! Excellent work!")
        elif correct_count >= total * 0.8:
            print("  👍 Great job! Keep practicing!")
        elif correct_count >= total * 0.5:
            print("  📚 Good effort! More practice needed!")
        else:
            print("  💪 Don't give up! Practice makes perfect!")

    def practice_with_input(
        self,
        infinitive: str,
        tense: str,
        user_answers: Dict[str, str],
    ) -> Tuple[Dict[str, bool], Dict[str, str]]:
        """
        Practice a verb with pre-provided answers (for testing).

        Args:
            infinitive: The verb to practice
            tense: The tense to practice
            user_answers: Dict of pronoun -> user answer

        Returns:
            Tuple of (results dict, corrections dict)
        """
        infinitive = infinitive.lower().strip()
        tense = tense.lower().strip()

        if not self.engine.verb_exists(infinitive):
            return {}, {}

        results = {}
        corrections = {}

        for pronoun in self.PRONOUNS:
            correct_form = self.engine.conjugate(infinitive, tense, pronoun)

            if correct_form is None:
                continue

            user_answer = user_answers.get(pronoun, "").strip().lower()

            if user_answer == correct_form.lower():
                results[pronoun] = True
                self.tracker.record_answer(infinitive, tense, pronoun, correct=True)
            else:
                results[pronoun] = False
                corrections[pronoun] = correct_form
                self.tracker.record_answer(infinitive, tense, pronoun, correct=False)

        self.tracker.save_verb_complete(infinitive)
        return results, corrections

    def get_available_tenses(self, infinitive: str) -> List[str]:
        """
        Get available tenses for a verb.

        Args:
            infinitive: The verb infinitive

        Returns:
            List of available tenses
        """
        conjugations = self.engine.get_full_conjugation(infinitive)
        if conjugations:
            return list(conjugations.keys())
        return self.engine.TENSES
