"""CLI chatbot interface for les-verbs."""

import sys
from typing import List, Optional

from les_verbs.engine import ConjugationEngine
from les_verbs.tracker import PerformanceTracker
from les_verbs.recommender import VerbRecommender
from les_verbs.practice import PracticeMode
from les_verbs.quiz import QuizMode
from les_verbs.status import StatusDisplay
from les_verbs.sentence import SentencePractice


class CLI:
    """Interactive CLI chatbot for les-verbs."""

    def __init__(self):
        """Initialize the CLI."""
        self.engine = ConjugationEngine()
        self.tracker = PerformanceTracker()
        self.recommender = VerbRecommender(self.tracker)
        self.practice = PracticeMode(self.engine, self.tracker)
        self.quiz = QuizMode(self.engine)
        self.status = StatusDisplay(self.tracker)
        self.sentence = SentencePractice(self.engine, self.tracker)
        self.running = True

        # Handle missing/corrupted tracking file
        if not self.tracker.has_data():
            print("\n  ℹ️  No progress file found. Starting fresh!")
            print("  Your progress will be saved automatically.")

    def _fuzzy_match(self, verb: str) -> Optional[str]:
        """
        Find a verb with fuzzy matching for typos.

        Args:
            verb: The verb to match

        Returns:
            Matching verb or None
        """
        verb = verb.lower().strip()
        available = list(self.engine.verbs.keys())

        # Exact match
        if verb in available:
            return verb

        # Check if verb starts with the input
        matches = [v for v in available if v.startswith(verb)]
        if len(matches) == 1:
            return matches[0]

        # Check for common typos (missing accents)
        accent_map = {
            "etre": "être",
            "avoir": "avoir",
            "aller": "aller",
            "etre": "être",
            "etre": "être",
        }
        if verb in accent_map:
            corrected = accent_map[verb]
            if corrected in available:
                return corrected

        return None

    def run(self) -> None:
        """Run the main CLI loop."""
        self._show_welcome()

        while self.running:
            self._show_menu()
            command = input("\n  Your choice: ").strip().lower()

            if command in ["quit", "exit", "q"]:
                self._quit()
            elif command == "1" or command == "practice":
                self._run_practice()
            elif command == "2" or command == "quiz":
                self._run_quiz()
            elif command == "3" or command == "status":
                self._show_status()
            elif command == "4" or command == "sentence":
                self._run_sentence_quiz()
            elif command.startswith("quiz on"):
                self._quiz_on_verb(command)
            else:
                print("\n  ⚠️  Invalid command. Choose 1-4 or type 'quit'.")

    def _show_welcome(self) -> None:
        """Show welcome message."""
        print("\n" + "=" * 60)
        print("  🇫🇷  LES VERBS - French Verb Conjugation")
        print("=" * 60)
        print("\n  Welcome! Practice French verb conjugations with")
        print("  intelligent recommendations and progress tracking.")
        print("\n  Type 'help' for commands or 'quit' to exit.")

    def _show_menu(self) -> None:
        """Show main menu."""
        print(f"\n{'=' * 60}")
        print("  Main Menu")
        print(f"{'=' * 60}")
        print("  1. Practice     - Practice recommended verbs")
        print("  2. Quiz         - Take a 5-question quiz")
        print("  3. Status       - View your progress")
        print("  4. Sentence     - Write sentences with verbs")
        print("\n  Or type: 'quiz on [verb]', 'help', 'quit'")

    def _run_practice(self) -> None:
        """Run practice mode."""
        print(f"\n{'=' * 60}")
        print("  Practice Mode")
        print(f"{'=' * 60}")
        print("\n  Choose session type:")
        print("  1. Short (1 verb)")
        print("  2. Long (3 verbs)")

        choice = input("\n  Your choice (1-2): ").strip()
        session_type = "short" if choice == "1" else "long"

        # Get recommendations
        recommendations = self.recommender.recommend(session_type)

        if not recommendations:
            print("\n  ⚠️  No verbs available for practice!")
            return

        # Show recommendations and confirm
        print(f"\n  Recommended verbs:")
        for verb, tense in recommendations:
            print(f"    - {verb} ({tense})")

        confirm = input("\n  Start with these verbs? (y/n): ").strip().lower()
        if confirm != "y":
            print("\n  Getting new recommendations...")
            recommendations = self.recommender.recommend(session_type)
            if not recommendations:
                print("  ⚠️  No verbs available!")
                return
            print(f"\n  New recommendations:")
            for verb, tense in recommendations:
                print(f"    - {verb} ({tense})")
            confirm = input("\n  Start with these? (y/n): ").strip().lower()
            if confirm != "y":
                print("\n  Returning to menu.")
                return

        # Practice each verb
        verbs_to_practice = [v for v, t in recommendations]
        completed_verbs = []

        for verb, tense in recommendations:
            print(f"\n  Starting practice: {verb} ({tense})")
            completed, results = self.practice.practice_verb(verb, tense)

            if completed:
                completed_verbs.append(verb)

            # Ask if user wants to continue
            if verb != verbs_to_practice[-1]:
                cont = input("\n  Continue to next verb? (y/n): ").strip().lower()
                if cont != "y":
                    break

        # Offer sentence practice after long session
        if len(completed_verbs) >= 3:
            self._offer_sentence_practice(completed_verbs)

    def _run_quiz(self) -> None:
        """Run quiz mode."""
        self.quiz.run_quiz_interactive()

    def _show_status(self) -> None:
        """Show user status."""
        print(self.status.display_status())

    def _run_sentence_quiz(self) -> None:
        """Run sentence quiz."""
        # Get recently practiced verbs
        all_stats = self.tracker.get_all_stats()

        if all_stats["verbs_practiced"] == 0:
            print("\n  ⚠️  Practice some verbs first before sentence quiz!")
            return

        # Get verbs from tracker
        practiced_verbs = list(self.tracker.progress["verbs"].keys())[:3]

        if not practiced_verbs:
            print("\n  ⚠️  No verbs to practice sentences with!")
            return

        results, skip_count = self.sentence.run_sentence_quiz(practiced_verbs)

        print(f"\n  Sentence quiz complete!")
        print(f"  Sentences written: {len(results) - skip_count}")
        print(f"  Sentences skipped: {skip_count}")

    def _quiz_on_verb(self, command: str) -> None:
        """Run quiz on a specific verb."""
        parts = command.split("quiz on")
        if len(parts) < 2 or not parts[1].strip():
            print("\n  ⚠️  Usage: quiz on [verb]")
            return

        verb = parts[1].strip().lower()

        # Try fuzzy matching if exact match fails
        if not self.engine.verb_exists(verb):
            matched = self._fuzzy_match(verb)
            if matched:
                print(f"\n  ℹ️  Did you mean '{matched}'?")
                verb = matched
            else:
                print(f"\n  ⚠️  Verb '{verb}' not found!")
                print("  Try: quiz on être")
                return

        print(f"\n  Quiz on: {verb.upper()}")

        # Generate questions for this verb
        questions = []
        tenses = self.engine.TENSES
        pronouns = self.engine.PRONOUNS

        import random

        for _ in range(5):
            tense = random.choice(tenses)
            pronoun = random.choice(pronouns)
            answer = self.engine.conjugate(verb, tense, pronoun)
            if answer:
                questions.append(
                    {
                        "verb": verb,
                        "tense": tense,
                        "pronoun": pronoun,
                        "correct_answer": answer,
                    }
                )

        if len(questions) < 5:
            print(f"\n  ⚠️  Not enough conjugations available for {verb}")
            return

        # Run quiz
        print(f"\n  5 questions on {verb}:")
        score = 0

        for i, q in enumerate(questions, 1):
            print(f"\n  Question {i}: {q['tense']} - {q['pronoun']}")
            user_answer = input("  Your answer: ").strip()

            if user_answer.lower() == q["correct_answer"].lower():
                score += 1
                print("  ✅ Correct!")
            else:
                print(f"  ❌ Correct answer: {q['correct_answer']}")

        print(f"\n  Score: {score}/5")

    def _offer_sentence_practice(self, verbs: List[str]) -> None:
        """Offer sentence practice after completing verbs."""
        print(f"\n{'=' * 60}")
        print("  Great job completing the verbs!")
        print(f"{'=' * 60}")

        choice = input("\n  Write sentences with these verbs? (y/n): ").strip().lower()

        if choice == "y":
            self.sentence.run_sentence_quiz(verbs)

    def _quit(self) -> None:
        """Quit the application."""
        print("\n  Saving progress...")
        # Save any pending progress
        self.tracker._save_progress()
        print("  Progress saved!")
        print("\n  Au revoir! 👋")
        self.running = False


def main():
    """Main entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
