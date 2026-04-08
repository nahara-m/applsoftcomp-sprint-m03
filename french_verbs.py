#!/usr/bin/env python3
"""
🇫🇷 French Verb Conjugation App
A fun interactive tool to learn French verb conjugations!
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class VerbConjugation:
    """Represents a conjugated verb."""

    infinitive: str
    pronoun: str
    tense: str
    conjugation: str


class FrenchVerbApp:
    """Interactive French verb conjugation application."""

    PRONOUNS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
    TENSES = ["présent", "passé composé", "imparfait", "futur simple", "conditionnel"]

    VERBS = {
        "être": {
            "présent": ["suis", "es", "est", "sommes", "êtes", "sont"],
            "passé composé": [
                "ai été",
                "as été",
                "a été",
                "avons été",
                "avez été",
                "ont été",
            ],
            "imparfait": ["étais", "étais", "était", "étions", "étiez", "étaient"],
            "futur simple": ["serai", "seras", "sera", "serons", "serez", "seront"],
            "conditionnel": [
                "serais",
                "serais",
                "serait",
                "serions",
                "seriez",
                "seraient",
            ],
        },
        "avoir": {
            "présent": ["ai", "as", "a", "avons", "avez", "ont"],
            "passé composé": [
                "ai eu",
                "as eu",
                "a eu",
                "avons eu",
                "avez eu",
                "ont eu",
            ],
            "imparfait": ["avais", "avais", "avait", "avions", "aviez", "avaient"],
            "futur simple": ["aurai", "auras", "aura", "aurons", "aurez", "auront"],
            "conditionnel": [
                "aurais",
                "aurais",
                "aurait",
                "aurions",
                "auriez",
                "auraient",
            ],
        },
        "aller": {
            "présent": ["vais", "vas", "va", "allons", "allez", "vont"],
            "passé composé": [
                "suis allé(e)",
                "es allé(e)",
                "est allé(e)",
                "sommes allé(e)s",
                "êtes allé(e)s",
                "sont allé(e)s",
            ],
            "imparfait": [
                "allais",
                "allais",
                "allait",
                "allions",
                "alliez",
                "allaient",
            ],
            "futur simple": ["irai", "iras", "ira", "irons", "irez", "iront"],
            "conditionnel": ["irais", "irais", "irait", "irions", "iriez", "iraient"],
        },
        "faire": {
            "présent": ["fais", "fais", "fait", "faisons", "faites", "font"],
            "passé composé": [
                "ai fait",
                "as fait",
                "a fait",
                "avons fait",
                "avez fait",
                "ont fait",
            ],
            "imparfait": [
                "faisais",
                "faisais",
                "faisait",
                "faisions",
                "faisiez",
                "faisaient",
            ],
            "futur simple": ["ferai", "feras", "fera", "ferons", "ferez", "feront"],
            "conditionnel": [
                "ferais",
                "ferais",
                "ferait",
                "ferions",
                "feriez",
                "feraient",
            ],
        },
        "prendre": {
            "présent": ["prends", "prends", "prend", "prenons", "prenez", "prennent"],
            "passé composé": [
                "ai pris",
                "as pris",
                "a pris",
                "avons pris",
                "avez pris",
                "ont pris",
            ],
            "imparfait": [
                "prenais",
                "prenais",
                "prenait",
                "prenions",
                "preniez",
                "prenaient",
            ],
            "futur simple": [
                "prendrai",
                "prendras",
                "prendra",
                "prendrons",
                "prendrez",
                "prendront",
            ],
            "conditionnel": [
                "prendrais",
                "prendrais",
                "prendrait",
                "prendrions",
                "prendriez",
                "prendraient",
            ],
        },
        "venir": {
            "présent": ["viens", "viens", "vient", "venons", "venez", "viennent"],
            "passé composé": [
                "suis venu(e)",
                "es venu(e)",
                "est venu(e)",
                "sommes venu(e)s",
                "êtes venu(e)s",
                "sont venu(e)s",
            ],
            "imparfait": [
                "venais",
                "venais",
                "venait",
                "venions",
                "veniez",
                "venaient",
            ],
            "futur simple": [
                "viendrai",
                "viendras",
                "viendra",
                "viendrons",
                "viendrez",
                "viendront",
            ],
            "conditionnel": [
                "viendrais",
                "viendrais",
                "viendrait",
                "viendrions",
                "viendriez",
                "viendraient",
            ],
        },
        "pouvoir": {
            "présent": ["peux", "peux", "peut", "pouvons", "pouvez", "peuvent"],
            "passé composé": [
                "ai pu",
                "as pu",
                "a pu",
                "avons pu",
                "avez pu",
                "ont pu",
            ],
            "imparfait": [
                "pouvais",
                "pouvais",
                "pouvait",
                "pouvions",
                "pouviez",
                "pouvaient",
            ],
            "futur simple": [
                "pourrai",
                "pourras",
                "pourra",
                "pourrons",
                "pourrez",
                "pourront",
            ],
            "conditionnel": [
                "pourrais",
                "pourrais",
                "pourrait",
                "pourrions",
                "pourriez",
                "pourraient",
            ],
        },
        "vouloir": {
            "présent": ["veux", "veux", "veut", "voulons", "voulez", "veulent"],
            "passé composé": [
                "ai voulu",
                "as voulu",
                "a voulu",
                "avons voulu",
                "avez voulu",
                "ont voulu",
            ],
            "imparfait": [
                "voulais",
                "voulais",
                "voulait",
                "voulions",
                "vouliez",
                "voulaient",
            ],
            "futur simple": [
                "voudrai",
                "voudras",
                "voudra",
                "voudrons",
                "voudrez",
                "voudront",
            ],
            "conditionnel": [
                "voudrais",
                "voudrais",
                "voudrait",
                "voudrions",
                "voudriez",
                "voudraient",
            ],
        },
        "devoir": {
            "présent": ["dois", "dois", "doit", "devons", "devez", "doivent"],
            "passé composé": [
                "ai dû",
                "as dû",
                "a dû",
                "avons dû",
                "avez dû",
                "ont dû",
            ],
            "imparfait": [
                "devais",
                "devais",
                "devait",
                "devions",
                "deviez",
                "devaient",
            ],
            "futur simple": [
                "devrai",
                "devras",
                "devra",
                "devrons",
                "devrez",
                "devront",
            ],
            "conditionnel": [
                "devrais",
                "devrais",
                "devrait",
                "devrions",
                "devriez",
                "devraient",
            ],
        },
        "parler": {
            "présent": ["parle", "parles", "parle", "parlons", "parlez", "parlent"],
            "passé composé": [
                "ai parlé",
                "as parlé",
                "a parlé",
                "avons parlé",
                "avez parlé",
                "ont parlé",
            ],
            "imparfait": [
                "parlais",
                "parlais",
                "parlait",
                "parlions",
                "parliez",
                "parlaient",
            ],
            "futur simple": [
                "parlerai",
                "parleras",
                "parlera",
                "parlerons",
                "parlerez",
                "parleront",
            ],
            "conditionnel": [
                "parlerais",
                "parlerais",
                "parlerait",
                "parlerions",
                "parleriez",
                "parleraient",
            ],
        },
        "finir": {
            "présent": [
                "finis",
                "finis",
                "finit",
                "finissons",
                "finissez",
                "finissent",
            ],
            "passé composé": [
                "ai fini",
                "as fini",
                "a fini",
                "avons fini",
                "avez fini",
                "ont fini",
            ],
            "imparfait": [
                "finissais",
                "finissais",
                "finissait",
                "finissions",
                "finissiez",
                "finissaient",
            ],
            "futur simple": [
                "finirai",
                "finiras",
                "finira",
                "finirons",
                "finirez",
                "finiront",
            ],
            "conditionnel": [
                "finirais",
                "finirais",
                "finirait",
                "finirions",
                "finiriez",
                "finiraient",
            ],
        },
        "choisir": {
            "présent": [
                "choisis",
                "choisis",
                "choisit",
                "choisissons",
                "choisissez",
                "choisissent",
            ],
            "passé composé": [
                "ai choisi",
                "as choisi",
                "a choisi",
                "avons choisi",
                "avez choisi",
                "ont choisi",
            ],
            "imparfait": [
                "choisissais",
                "choisissais",
                "choisissait",
                "choisissions",
                "choisissiez",
                "choisissaient",
            ],
            "futur simple": [
                "choisirai",
                "choisiras",
                "choisira",
                "choisirons",
                "choisirez",
                "choisiront",
            ],
            "conditionnel": [
                "choisirais",
                "choisirais",
                "choisirait",
                "choisirions",
                "choisiriez",
                "choisiraient",
            ],
        },
        "manger": {
            "présent": ["mange", "manges", "mange", "mangeons", "mangez", "mangent"],
            "passé composé": [
                "ai mangé",
                "as mangé",
                "a mangé",
                "avons mangé",
                "avez mangé",
                "ont mangé",
            ],
            "imparfait": [
                "mangeais",
                "mangeais",
                "mangeait",
                "mangions",
                "mangiez",
                "mangeaient",
            ],
            "futur simple": [
                "mangerai",
                "mangeras",
                "mangera",
                "mangerons",
                "mangerez",
                "mangeront",
            ],
            "conditionnel": [
                "mangerais",
                "mangerais",
                "mangerait",
                "mangerions",
                "mangeriez",
                "mangeraient",
            ],
        },
        "aimer": {
            "présent": ["aime", "aimes", "aime", "aimons", "aimez", "aiment"],
            "passé composé": [
                "ai aimé",
                "as aimé",
                "a aimé",
                "avons aimé",
                "avez aimé",
                "ont aimé",
            ],
            "imparfait": [
                "aimais",
                "aimais",
                "aimait",
                "aimions",
                "aimiez",
                "aimaient",
            ],
            "futur simple": [
                "aimerai",
                "aimeras",
                "aimera",
                "aimerons",
                "aimerez",
                "aimeront",
            ],
            "conditionnel": [
                "aimerais",
                "aimerais",
                "aimerait",
                "aimerions",
                "aimeriez",
                "aimeraient",
            ],
        },
    }

    def __init__(self):
        self.score = 0
        self.total_questions = 0

    def display_header(self, title: str) -> None:
        """Display a formatted header."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def display_conjugation_table(self, verb: str) -> None:
        """Display full conjugation table for a verb."""
        if verb not in self.VERBS:
            print(f"❌ Verb '{verb}' not found!")
            return

        self.display_header(f"📚 {verb.upper()}")

        for tense in self.TENSES:
            print(f"\n  {tense}:")
            print("  " + "-" * 40)
            conjugations = self.VERBS[verb][tense]
            for i, pronoun in enumerate(self.PRONOUNS):
                print(f"    {pronoun:12} → {conjugations[i]}")

    def list_verbs(self) -> None:
        """List all available verbs."""
        self.display_header("📖 Available Verbs")
        for i, verb in enumerate(self.VERBS.keys(), 1):
            print(f"  {i:2}. {verb}")
        print(f"\n  Total: {len(self.VERBS)} verbs")

    def quiz_mode(self) -> None:
        """Interactive quiz mode."""
        self.display_header("🎯 Quiz Mode")
        print("\n  Type the correct conjugation or 'quit' to exit")
        print("  Press Enter to skip a question\n")

        self.score = 0
        self.total_questions = 0

        while True:
            verb = random.choice(list(self.VERBS.keys()))
            tense = random.choice(self.TENSES)
            pronoun_idx = random.randint(0, 5)
            pronoun = self.PRONOUNS[pronoun_idx]
            correct_answer = self.VERBS[verb][tense][pronoun_idx]

            self.total_questions += 1
            print(f"\n  Question {self.total_questions}:")
            print(f"  Verb: {verb} | Tense: {tense} | Pronoun: {pronoun}")

            user_answer = input("  Your answer: ").strip().lower()

            if user_answer == "quit":
                break

            if user_answer == correct_answer.lower():
                print("  ✅ Correct! Bravo!")
                self.score += 1
            elif user_answer == "":
                print(f"  ⏭️  Skipped! Answer: {correct_answer}")
            else:
                print(f"  ❌ Incorrect! Correct answer: {correct_answer}")

            print(
                f"  Score: {self.score}/{self.total_questions} ({self.get_percentage()}%)"
            )

        self.display_quiz_results()

    def get_percentage(self) -> int:
        """Calculate score percentage."""
        if self.total_questions == 0:
            return 0
        return int((self.score / self.total_questions) * 100)

    def display_quiz_results(self) -> None:
        """Display quiz results."""
        self.display_header("🏆 Quiz Results")
        print(f"\n  Final Score: {self.score}/{self.total_questions}")
        print(f"  Percentage: {self.get_percentage()}%")

        if self.get_percentage() >= 90:
            print("  🌟 Excellent! You're a French master!")
        elif self.get_percentage() >= 70:
            print("  👍 Great job! Keep practicing!")
        elif self.get_percentage() >= 50:
            print("  📚 Good effort! More practice needed!")
        else:
            print("  💪 Don't give up! Practice makes perfect!")

    def practice_mode(self) -> None:
        """Practice specific verb conjugations."""
        self.display_header("📝 Practice Mode")

        print("\n  Available verbs:")
        self.list_verbs()

        verb = input("\n  Enter verb to practice (or 'quit'): ").strip().lower()

        if verb == "quit" or verb not in self.VERBS:
            return

        print("\n  Choose tense (or 'all' for all tenses):")
        for i, tense in enumerate(self.TENSES, 1):
            print(f"    {i}. {tense}")
        print("    0. All tenses")

        choice = input("\n  Your choice: ").strip()

        if choice == "0":
            self.display_conjugation_table(verb)
        elif choice.isdigit() and 1 <= int(choice) <= len(self.TENSES):
            tense = self.TENSES[int(choice) - 1]
            self.display_header(f"📚 {verb.upper()} - {tense}")
            conjugations = self.VERBS[verb][tense]
            for i, pronoun in enumerate(self.PRONOUNS):
                print(f"  {pronoun:12} → {conjugations[i]}")
        else:
            print("  Invalid choice!")

    def main_menu(self) -> None:
        """Display main menu and handle user input."""
        self.display_header("🇫🇷 French Verb Conjugation App")

        while True:
            print("\n  Main Menu:")
            print("  1. 📖 List all verbs")
            print("  2. 📚 View conjugation table")
            print("  3. 🎯 Quiz mode")
            print("  4. 📝 Practice mode")
            print("  5. ❌ Quit")

            choice = input("\n  Your choice (1-5): ").strip()

            if choice == "1":
                self.list_verbs()
            elif choice == "2":
                verb = input("\n  Enter verb name: ").strip().lower()
                self.display_conjugation_table(verb)
            elif choice == "3":
                self.quiz_mode()
            elif choice == "4":
                self.practice_mode()
            elif choice == "5":
                print("\n  Au revoir! 👋")
                break
            else:
                print("  Invalid choice! Please enter 1-5.")


def main():
    """Main entry point."""
    app = FrenchVerbApp()
    app.main_menu()


if __name__ == "__main__":
    main()
