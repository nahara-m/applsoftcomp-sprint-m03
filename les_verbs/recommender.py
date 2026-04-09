"""Verb recommendation algorithm."""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from les_verbs.tracker import PerformanceTracker


class VerbRecommender:
    """Recommends verbs based on performance and randomness."""

    def __init__(
        self, tracker: PerformanceTracker, verbs_file: str = "data/french_verbs.json"
    ):
        """
        Initialize the recommender.

        Args:
            tracker: Performance tracker instance
            verbs_file: Path to verbs JSON file
        """
        self.tracker = tracker
        self.verbs = self._load_verbs(verbs_file)

    def _load_verbs(self, verbs_file: str) -> Dict:
        """Load verbs from JSON file."""
        import json
        import os

        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(script_dir, verbs_file)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {v["infinitive"]: v for v in data["verbs"]}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def recommend(
        self, session_type: str = "short", count: Optional[int] = None
    ) -> List[Tuple[str, str]]:
        """
        Recommend verbs for practice.

        Args:
            session_type: "short" (1 verb) or "long" (3 verbs)
            count: Override number of verbs to recommend

        Returns:
            List of (verb, suggested_tense) tuples
        """
        if count is None:
            count = 1 if session_type == "short" else 3

        recommendations = []
        available_verbs = list(self.verbs.keys())

        if not available_verbs:
            return []

        # Score each verb
        scored_verbs = []
        for verb in available_verbs:
            score, tense = self._score_verb(verb)
            scored_verbs.append((verb, score, tense))

        # Sort by score (higher = more in need of practice)
        scored_verbs.sort(key=lambda x: x[1], reverse=True)

        # Take top candidates
        top_candidates = scored_verbs[: max(count * 3, 10)]

        # Add randomness: pick from top candidates
        if len(top_candidates) > count:
            # Weighted random selection based on score
            selected = self._weighted_random_select(top_candidates, count)
        else:
            selected = top_candidates[:count]

        for verb, score, tense in selected:
            recommendations.append((verb, tense))

        return recommendations

    def _score_verb(self, infinitive: str) -> Tuple[float, str]:
        """
        Score a verb based on performance metrics.

        Args:
            infinitive: The verb infinitive

        Returns:
            Tuple of (score, suggested_tense)
        """
        stats = self.tracker.get_verb_stats(infinitive)
        verb_data = self.verbs.get(infinitive, {})

        base_score = 50.0
        suggested_tense = "présent"

        if stats is None:
            # New verb: high priority, default to présent
            return base_score + 30, suggested_tense

        # Factor 1: Error rate (higher error = higher score)
        error_rate = stats["error_rate"]
        base_score += error_rate * 40

        # Factor 2: Time since last practice (older = higher score)
        tenses = stats.get("tenses_practiced", [])
        if tenses:
            # Find the tense with oldest practice
            oldest_tense = None
            oldest_date = None

            for tense in tenses:
                last_date = self.tracker.get_last_practiced(infinitive, tense)
                if last_date:
                    try:
                        date = datetime.fromisoformat(last_date)
                        if oldest_date is None or date < oldest_date:
                            oldest_date = date
                            oldest_tense = tense
                    except ValueError:
                        continue

            if oldest_date:
                days_since = (datetime.now() - oldest_date).days
                # Cap at 30 days
                days_since = min(days_since, 30)
                base_score += (days_since / 30) * 20
                suggested_tense = oldest_tense if oldest_tense else "présent"
        else:
            # Never practiced: default to présent
            suggested_tense = "présent"

        # Factor 3: Total practice count (less practice = higher score)
        total_practice = stats["total_correct"] + stats["total_incorrect"]
        if total_practice < 10:
            base_score += 15
        elif total_practice < 30:
            base_score += 5

        # Factor 4: Randomness component (0-10 points)
        randomness = random.uniform(0, 10)
        base_score += randomness

        return base_score, suggested_tense

    def _weighted_random_select(
        self, candidates: List[Tuple[str, float, str]], count: int
    ) -> List[Tuple[str, float, str]]:
        """
        Select items using weighted random selection.

        Args:
            candidates: List of (verb, score, tense) tuples
            count: Number to select

        Returns:
            Selected items
        """
        if not candidates:
            return []

        selected = []
        remaining = candidates.copy()

        for _ in range(min(count, len(candidates))):
            if not remaining:
                break

            # Calculate weights
            total_score = sum(c[1] for c in remaining)
            if total_score == 0:
                # If all scores are 0, use equal weights
                weights = [1.0] * len(remaining)
            else:
                weights = [c[1] / total_score for c in remaining]

            # Weighted random selection
            chosen = random.choices(remaining, weights=weights, k=1)[0]
            selected.append(chosen)
            remaining.remove(chosen)

        return selected

    def recommend_specific_tense(
        self, infinitive: str, tense: str
    ) -> Optional[Tuple[str, str]]:
        """
        Recommend a specific verb-tense combination.

        Args:
            infinitive: The verb infinitive
            tense: The tense to practice

        Returns:
            (verb, tense) tuple or None if verb doesn't exist
        """
        if infinitive not in self.verbs:
            return None

        return (infinitive, tense)

    def get_new_verbs(self, count: int = 3) -> List[Tuple[str, str]]:
        """
        Get verbs that haven't been practiced yet.

        Args:
            count: Number of verbs to return

        Returns:
            List of (verb, "présent") tuples
        """
        new_verbs = []

        for verb in self.verbs.keys():
            stats = self.tracker.get_verb_stats(verb)
            if stats is None:
                new_verbs.append(verb)
                if len(new_verbs) >= count:
                    break

        return [(v, "présent") for v in new_verbs]
