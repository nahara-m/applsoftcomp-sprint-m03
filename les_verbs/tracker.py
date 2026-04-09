"""Performance tracking for user progress."""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PerformanceTracker:
    """Tracks user progress for verb conjugation practice."""

    def __init__(self, progress_file: str = "data/user_progress.json"):
        """Initialize the tracker."""
        self.progress_file = progress_file
        self.progress: Dict = {}
        self._load_progress()

    def _load_progress(self) -> None:
        """Load progress from JSON file."""
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(script_dir, self.progress_file)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                self.progress = json.load(f)
        except FileNotFoundError:
            self.progress = {"verbs": {}}
        except json.JSONDecodeError:
            self.progress = {"verbs": {}}

    def _save_progress(self) -> None:
        """Save progress to JSON file."""
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(script_dir, self.progress_file)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def record_answer(
        self,
        infinitive: str,
        tense: str,
        pronoun: str,
        correct: bool,
        sentence: Optional[str] = None,
    ) -> None:
        """
        Record a conjugation attempt.

        Args:
            infinitive: The verb infinitive
            tense: The tense practiced
            pronoun: The pronoun used
            correct: Whether the answer was correct
            sentence: Optional sentence using the verb
        """
        infinitive = infinitive.lower().strip()
        tense = tense.lower().strip()
        pronoun = pronoun.lower().strip()

        if infinitive not in self.progress["verbs"]:
            self.progress["verbs"][infinitive] = {
                "tenses": {},
                "sentence_usage": 0,
                "sentence_skip": 0,
                "first_practiced": datetime.now().isoformat(),
            }

        verb_data = self.progress["verbs"][infinitive]

        if tense not in verb_data["tenses"]:
            verb_data["tenses"][tense] = {"pronouns": {}}

        if pronoun not in verb_data["tenses"][tense]["pronouns"]:
            verb_data["tenses"][tense]["pronouns"][pronoun] = {
                "correct": 0,
                "incorrect": 0,
                "last_practiced": None,
            }

        pronoun_data = verb_data["tenses"][tense]["pronouns"][pronoun]
        if correct:
            pronoun_data["correct"] += 1
        else:
            pronoun_data["incorrect"] += 1
        pronoun_data["last_practiced"] = datetime.now().isoformat()

    def record_sentence(self, infinitive: str, used: bool) -> None:
        """
        Record sentence practice for a verb.

        Args:
            infinitive: The verb infinitive
            used: Whether user wrote a sentence or skipped
        """
        infinitive = infinitive.lower().strip()

        if infinitive not in self.progress["verbs"]:
            self.progress["verbs"][infinitive] = {
                "tenses": {},
                "sentence_usage": 0,
                "sentence_skip": 0,
                "first_practiced": datetime.now().isoformat(),
            }

        if used:
            self.progress["verbs"][infinitive]["sentence_usage"] += 1
        else:
            self.progress["verbs"][infinitive]["sentence_skip"] += 1

    def save_verb_complete(self, infinitive: str) -> None:
        """
        Save progress after completing a full verb.

        Args:
            infinitive: The verb infinitive
        """
        self._save_progress()

    def get_verb_stats(self, infinitive: str) -> Optional[Dict]:
        """
        Get statistics for a specific verb.

        Args:
            infinitive: The verb infinitive

        Returns:
            Dict with stats or None if not found
        """
        infinitive = infinitive.lower().strip()

        if infinitive not in self.progress["verbs"]:
            return None

        verb_data = self.progress["verbs"][infinitive]

        total_correct = 0
        total_incorrect = 0
        tenses_practiced = set()

        for tense, tense_data in verb_data["tenses"].items():
            tenses_practiced.add(tense)
            for pronoun_data in tense_data["pronouns"].values():
                total_correct += pronoun_data["correct"]
                total_incorrect += pronoun_data["incorrect"]

        return {
            "infinitive": infinitive,
            "total_correct": total_correct,
            "total_incorrect": total_incorrect,
            "error_rate": total_incorrect / (total_correct + total_incorrect)
            if (total_correct + total_incorrect) > 0
            else 0,
            "tenses_practiced": list(tenses_practiced),
            "sentence_usage": verb_data["sentence_usage"],
            "sentence_skip": verb_data["sentence_skip"],
            "first_practiced": verb_data["first_practiced"],
        }

    def get_all_stats(self) -> Dict:
        """
        Get overall statistics.

        Returns:
            Dict with overall stats
        """
        total_verbs = len(self.progress["verbs"])
        total_practice_sessions = 0
        verbs_practiced = 0

        for verb_data in self.progress["verbs"].values():
            tenses_count = sum(len(t["pronouns"]) for t in verb_data["tenses"].values())
            if tenses_count > 0:
                verbs_practiced += 1
            total_practice_sessions += tenses_count

        return {
            "total_verbs": total_verbs,
            "times_practiced": total_practice_sessions,
            "verbs_practiced": verbs_practiced,
        }

    def get_error_rate(self, infinitive: str, tense: str) -> float:
        """
        Get error rate for a verb-tense combination.

        Args:
            infinitive: The verb infinitive
            tense: The tense

        Returns:
            Error rate (0.0 to 1.0)
        """
        infinitive = infinitive.lower().strip()
        tense = tense.lower().strip()

        if infinitive not in self.progress["verbs"]:
            return 0.0

        verb_data = self.progress["verbs"][infinitive]
        if tense not in verb_data["tenses"]:
            return 0.0

        total_correct = 0
        total_incorrect = 0

        for pronoun_data in verb_data["tenses"][tense]["pronouns"].values():
            total_correct += pronoun_data["correct"]
            total_incorrect += pronoun_data["incorrect"]

        total = total_correct + total_incorrect
        return total_incorrect / total if total > 0 else 0.0

    def get_last_practiced(self, infinitive: str, tense: str) -> Optional[str]:
        """
        Get last practiced date for a verb-tense combination.

        Args:
            infinitive: The verb infinitive
            tense: The tense

        Returns:
            ISO format date string or None
        """
        infinitive = infinitive.lower().strip()
        tense = tense.lower().strip()

        if infinitive not in self.progress["verbs"]:
            return None

        verb_data = self.progress["verbs"][infinitive]
        if tense not in verb_data["tenses"]:
            return None

        last_date = None
        for pronoun_data in verb_data["tenses"][tense]["pronouns"].values():
            if pronoun_data["last_practiced"]:
                if last_date is None or pronoun_data["last_practiced"] > last_date:
                    last_date = pronoun_data["last_practiced"]

        return last_date

    def reset_progress(self) -> None:
        """Reset all progress."""
        self.progress = {"verbs": {}}
        self._save_progress()

    def has_data(self) -> bool:
        """Check if tracker has any data."""
        return len(self.progress["verbs"]) > 0
