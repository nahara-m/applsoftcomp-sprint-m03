"""Sentence practice for verb conjugation."""

from typing import Dict, List, Optional, Tuple

from les_verbs.engine import ConjugationEngine
from les_verbs.tracker import PerformanceTracker


class SentencePractice:
    """Sentence practice/quiz mode."""

    def __init__(self, engine: ConjugationEngine, tracker: PerformanceTracker):
        """
        Initialize sentence practice.

        Args:
            engine: Conjugation engine instance
            tracker: Performance tracker instance
        """
        self.engine = engine
        self.tracker = tracker

    def prompt_sentence(self, infinitive: str) -> Tuple[bool, Optional[str]]:
        """
        Prompt user to write a sentence with a verb.

        Args:
            infinitive: The verb to use in a sentence

        Returns:
            Tuple of (skipped, sentence written)
        """
        infinitive = infinitive.lower().strip()

        print(f"\n{'=' * 60}")
        print(f"  Sentence Practice: {infinitive.upper()}")
        print(f"{'=' * 60}\n")
        print(f"  Write a sentence using '{infinitive}' in French.")
        print(f"  (Type 'skip' to skip sentence practice)\n")

        sentence = input("  Your sentence: ").strip()

        if sentence.lower() == "skip":
            self.tracker.record_sentence(infinitive, used=False)
            return True, None

        self.tracker.record_sentence(infinitive, used=True)
        return False, sentence

    def evaluate_sentence(self, infinitive: str, sentence: str) -> Dict[str, any]:
        """
        Evaluate a sentence (basic evaluation).

        Args:
            infinitive: The verb that should be used
            sentence: The user's sentence

        Returns:
            Dict with evaluation results
        """
        infinitive = infinitive.lower().strip()
        sentence_lower = sentence.lower()

        # Check if verb is in sentence (basic check)
        verb_forms = self._get_common_forms(infinitive)
        verb_used = any(form in sentence_lower for form in verb_forms)

        # Basic grammar checks
        has_capital = sentence[0].isupper() if sentence else False
        has_punctuation = sentence.endswith((".", "!", "?")) if sentence else False

        return {
            "verb_used": verb_used,
            "has_capital": has_capital,
            "has_punctuation": has_punctuation,
            "sentence": sentence,
            "verb": infinitive,
        }

    def _get_common_forms(self, infinitive: str) -> List[str]:
        """Get common conjugated forms of a verb."""
        forms = [infinitive]  # infinitive itself

        # Add common conjugated forms
        for tense in ["présent", "passé_composé", "imparfait", "futur"]:
            for pronoun in self.engine.PRONOUNS:
                form = self.engine.conjugate(infinitive, tense, pronoun)
                if form:
                    forms.append(form.lower())

        return forms

    def provide_feedback(self, evaluation: Dict) -> str:
        """
        Provide feedback on a sentence.

        Args:
            evaluation: Evaluation dict from evaluate_sentence

        Returns:
            Feedback string
        """
        feedback = "\n  Feedback:\n"
        feedback += f"  {'-' * 40}\n"

        if evaluation["verb_used"]:
            feedback += "  ✅ You used the verb correctly!\n"
        else:
            feedback += f"  ⚠️  The verb '{evaluation['verb']}' doesn't appear to be in your sentence.\n"

        if evaluation["has_capital"]:
            feedback += "  ✅ Sentence starts with a capital letter.\n"
        else:
            feedback += "  ⚠️  Sentences should start with a capital letter.\n"

        if evaluation["has_punctuation"]:
            feedback += "  ✅ Sentence has proper ending punctuation.\n"
        else:
            feedback += "  ⚠️  Sentences should end with punctuation (.!?)\n"

        feedback += (
            "\n  Keep practicing! Writing sentences helps reinforce verb usage.\n"
        )

        return feedback

    def run_sentence_quiz(self, verbs: List[str]) -> Tuple[List[Dict], int]:
        """
        Run sentence quiz for multiple verbs.

        Args:
            verbs: List of verbs to practice

        Returns:
            Tuple of (results list, skip count)
        """
        results = []
        skip_count = 0

        print(f"\n{'=' * 60}")
        print("  Sentence Quiz")
        print(f"{'=' * 60}")
        print(f"\n  Write a sentence for each of the {len(verbs)} verbs practiced.")
        print("  Type 'skip' to skip any sentence.\n")

        for verb in verbs:
            skipped, sentence = self.prompt_sentence(verb)

            if skipped:
                skip_count += 1
                results.append(
                    {
                        "verb": verb,
                        "sentence": None,
                        "skipped": True,
                    }
                )
            elif sentence:
                evaluation = self.evaluate_sentence(verb, sentence)
                feedback = self.provide_feedback(evaluation)
                print(feedback)

                results.append(
                    {
                        "verb": verb,
                        "sentence": sentence,
                        "skipped": False,
                        "evaluation": evaluation,
                    }
                )

        return results, skip_count

    def run_sentence_quiz_with_input(
        self, verbs: List[str], user_sentences: Dict[str, str]
    ) -> Tuple[List[Dict], int]:
        """
        Run sentence quiz with pre-provided sentences (for testing).

        Args:
            verbs: List of verbs to practice
            user_sentences: Dict of verb -> sentence

        Returns:
            Tuple of (results list, skip count)
        """
        results = []
        skip_count = 0

        for verb in verbs:
            sentence = user_sentences.get(verb, "").strip()

            if sentence.lower() == "skip" or not sentence:
                if not sentence:
                    skip_count += 1
                    self.tracker.record_sentence(verb, used=False)
                else:
                    skip_count += 1
                    self.tracker.record_sentence(verb, used=False)

                results.append(
                    {
                        "verb": verb,
                        "sentence": None,
                        "skipped": True,
                    }
                )
            else:
                self.tracker.record_sentence(verb, used=True)
                evaluation = self.evaluate_sentence(verb, sentence)
                results.append(
                    {
                        "verb": verb,
                        "sentence": sentence,
                        "skipped": False,
                        "evaluation": evaluation,
                    }
                )

        return results, skip_count
