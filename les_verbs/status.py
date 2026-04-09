"""Status display for user progress."""

from typing import Dict, Optional

from les_verbs.tracker import PerformanceTracker


class StatusDisplay:
    """Display user progress statistics."""

    def __init__(self, tracker: PerformanceTracker):
        """
        Initialize status display.

        Args:
            tracker: Performance tracker instance
        """
        self.tracker = tracker

    def get_status(self) -> Dict:
        """
        Get current status metrics.

        Returns:
            Dict with status metrics
        """
        all_stats = self.tracker.get_all_stats()

        return {
            "total_verbs": all_stats["total_verbs"],
            "times_practiced": all_stats["times_practiced"],
            "verbs_practiced": all_stats["verbs_practiced"],
        }

    def display_status(self) -> str:
        """
        Format status for display.

        Returns:
            Formatted status string
        """
        stats = self.get_status()

        output = f"\n{'=' * 60}\n"
        output += f"  Your Progress\n"
        output += f"{'=' * 60}\n\n"
        output += f"  Total verbs in database: {stats['total_verbs']}\n"
        output += f"  Times practiced: {stats['times_practiced']}\n"
        output += f"  Unique verbs practiced: {stats['verbs_practiced']}\n"

        if stats["verbs_practiced"] > 0:
            percentage = int(
                (stats["verbs_practiced"] / max(stats["total_verbs"], 1)) * 100
            )
            output += f"\n  Progress: {percentage}% of verbs practiced\n"

            if percentage >= 80:
                output += "  🌟 Outstanding dedication!\n"
            elif percentage >= 50:
                output += "  👍 Great progress! Keep going!\n"
            elif percentage >= 20:
                output += "  📚 Good start! More practice ahead!\n"
            else:
                output += "  💪 Ready to begin your journey?\n"
        else:
            output += f"\n  Start practicing to track your progress!\n"

        output += f"\n{'=' * 60}\n"

        return output

    def get_verb_status(self, infinitive: str) -> Optional[str]:
        """
        Get status for a specific verb.

        Args:
            infinitive: The verb infinitive

        Returns:
            Formatted verb status or None if not found
        """
        stats = self.tracker.get_verb_stats(infinitive)

        if stats is None:
            return None

        output = f"\n  {stats['infinitive'].upper()}\n"
        output += f"  {'-' * 40}\n"
        output += f"  Correct answers: {stats['total_correct']}\n"
        output += f"  Incorrect answers: {stats['total_incorrect']}\n"

        error_rate = stats["error_rate"] * 100
        output += f"  Error rate: {error_rate:.1f}%\n"
        output += f"  Tenses practiced: {', '.join(stats['tenses_practiced']) if stats['tenses_practiced'] else 'None'}\n"
        output += f"  Sentences written: {stats['sentence_usage']}\n"
        output += f"  Sentences skipped: {stats['sentence_skip']}\n"

        return output
