"""Conjugation engine for French verbs."""

import json
import os
from typing import Dict, List, Optional


class ConjugationEngine:
    """Engine for conjugating French verbs."""

    PRONOUNS = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]
    TENSES = [
        "présent",
        "imparfait",
        "futur",
        "passé_composé",
        "conditionnel",
        "subjonctif",
        "plus_que_parfait",
        "futur_antérieur",
        "passé_simple",
        "subjonctif_imparfait",
        "impératif",
    ]

    def __init__(self, verbs_file: str = "data/french_verbs.json"):
        """Initialize the engine with verb data."""
        self.verbs_file = verbs_file
        self.verbs: Dict = {}
        self._load_verbs()

    def _load_verbs(self) -> None:
        """Load verbs from JSON file."""
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(script_dir, self.verbs_file)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for verb in data["verbs"]:
                    self.verbs[verb["infinitive"]] = verb
        except FileNotFoundError:
            self.verbs = {}
        except json.JSONDecodeError:
            self.verbs = {}

    def conjugate(self, infinitive: str, tense: str, pronoun: str) -> Optional[str]:
        """
        Conjugate a verb for a given tense and pronoun.

        Args:
            infinitive: The verb infinitive (e.g., "être", "parler")
            tense: The tense (e.g., "présent", "imparfait")
            pronoun: The pronoun (e.g., "je", "tu", "nous")

        Returns:
            The conjugated form or None if not found
        """
        infinitive = infinitive.lower().strip()
        tense = tense.lower().strip()
        pronoun = pronoun.lower().strip()

        if infinitive not in self.verbs:
            return None

        verb_data = self.verbs[infinitive]

        # If verb has stored conjugations, use them
        if "conjugations" in verb_data:
            if tense in verb_data["conjugations"]:
                if pronoun in verb_data["conjugations"][tense]:
                    return verb_data["conjugations"][tense][pronoun]

        # Otherwise, generate using rules
        return self._generate_conjugation(verb_data, tense, pronoun)

    def _generate_conjugation(
        self, verb_data: Dict, tense: str, pronoun: str
    ) -> Optional[str]:
        """Generate conjugation using rules for regular verbs."""
        infinitive = verb_data["infinitive"]
        group = verb_data["group"]
        stem_changes = verb_data.get("stem_changes", "")

        if group == "-er":
            return self._conjugate_er(infinitive, tense, pronoun, stem_changes)
        elif group == "-ir":
            return self._conjugate_ir(infinitive, tense, pronoun)
        elif group == "-re":
            return self._conjugate_re(infinitive, tense, pronoun)

        return None

    def _get_pronoun_index(self, pronoun: str) -> int:
        """Get pronoun index for array-based conjugations."""
        pronoun_map = {
            "je": 0,
            "tu": 1,
            "il/elle/on": 2,
            "il": 2,
            "elle": 2,
            "on": 2,
            "nous": 3,
            "vous": 4,
            "ils/elles": 5,
            "ils": 5,
            "elles": 5,
        }
        return pronoun_map.get(pronoun.lower(), -1)

    def _conjugate_er(
        self, infinitive: str, tense: str, pronoun: str, stem_changes: str = ""
    ) -> Optional[str]:
        """Conjugate regular -er verbs."""
        stem = infinitive[:-2]
        idx = self._get_pronoun_index(pronoun)

        if idx == -1:
            return None

        # Handle manger-type stem changes (nous form needs 'e')
        if stem_changes == "nous_form_e" and idx == 3:
            stem = stem + "e"

        endings = {
            "présent": ["e", "es", "e", "ons", "ez", "ent"],
            "imparfait": ["ais", "ais", "ait", "ions", "iez", "aient"],
            "futur": ["ai", "as", "a", "ons", "ez", "ont"],
            "conditionnel": ["ais", "ais", "ait", "ions", "iez", "aient"],
            "subjonctif": ["e", "es", "e", "ions", "iez", "ent"],
            "passé_simple": ["ai", "as", "a", "âmes", "âtes", "èrent"],
            "subjonctif_imparfait": [
                "asse",
                "asses",
                "ât",
                "assions",
                "assiez",
                "assent",
            ],
        }

        if tense in endings:
            return stem + endings[tense][idx]

        # Compound tenses
        if tense == "passé_composé":
            return (
                f"ai {stem}é"
                if idx in [0]
                else f"as {stem}é"
                if idx in [1]
                else f"a {stem}é"
                if idx in [2]
                else f"avons {stem}é"
                if idx in [3]
                else f"avez {stem}é"
                if idx in [4]
                else f"ont {stem}é"
            )
        elif tense == "plus_que_parfait":
            return (
                f"avais {stem}é"
                if idx in [0, 1]
                else f"avait {stem}é"
                if idx in [2]
                else f"avions {stem}é"
                if idx in [3]
                else f"aviez {stem}é"
                if idx in [4]
                else f"avaient {stem}é"
            )
        elif tense == "futur_antérieur":
            return (
                f"aurai {stem}é"
                if idx in [0]
                else f"auras {stem}é"
                if idx in [1]
                else f"aura {stem}é"
                if idx in [2]
                else f"aurons {stem}é"
                if idx in [3]
                else f"aurez {stem}é"
                if idx in [4]
                else f"auront {stem}é"
            )

        # Impératif (only tu, nous, vous)
        if tense == "impératif":
            if idx == 1:
                return stem + "e"
            elif idx == 3:
                return stem + "ons"
            elif idx == 4:
                return stem + "ez"
            return None

        return None

    def _conjugate_ir(self, infinitive: str, tense: str, pronoun: str) -> Optional[str]:
        """Conjugate regular -ir verbs."""
        stem = infinitive[:-2]
        idx = self._get_pronoun_index(pronoun)

        if idx == -1:
            return None

        endings = {
            "présent": ["is", "is", "it", "issons", "issez", "issent"],
            "imparfait": [
                "issais",
                "issais",
                "issait",
                "issions",
                "issiez",
                "issaient",
            ],
            "futur": ["irai", "iras", "ira", "irons", "irez", "iront"],
            "conditionnel": ["irais", "irais", "irait", "irions", "iriez", "iraient"],
            "subjonctif": ["isse", "isses", "isse", "issions", "issiez", "issent"],
            "passé_simple": ["is", "is", "it", "îmes", "îtes", "irent"],
            "subjonctif_imparfait": [
                "isse",
                "isses",
                "ît",
                "issions",
                "issiez",
                "issent",
            ],
        }

        if tense in endings:
            return stem + endings[tense][idx]

        # Compound tenses
        if tense == "passé_composé":
            return (
                f"ai {stem}i"
                if idx in [0]
                else f"as {stem}i"
                if idx in [1]
                else f"a {stem}i"
                if idx in [2]
                else f"avons {stem}i"
                if idx in [3]
                else f"avez {stem}i"
                if idx in [4]
                else f"ont {stem}i"
            )
        elif tense == "plus_que_parfait":
            return (
                f"avais {stem}i"
                if idx in [0, 1]
                else f"avait {stem}i"
                if idx in [2]
                else f"avions {stem}i"
                if idx in [3]
                else f"aviez {stem}i"
                if idx in [4]
                else f"avaient {stem}i"
            )
        elif tense == "futur_antérieur":
            return (
                f"aurai {stem}i"
                if idx in [0]
                else f"auras {stem}i"
                if idx in [1]
                else f"aura {stem}i"
                if idx in [2]
                else f"aurons {stem}i"
                if idx in [3]
                else f"aurez {stem}i"
                if idx in [4]
                else f"auront {stem}i"
            )

        # Impératif
        if tense == "impératif":
            if idx == 1:
                return stem + "is"
            elif idx == 3:
                return stem + "issons"
            elif idx == 4:
                return stem + "issez"
            return None

        return None

    def _conjugate_re(self, infinitive: str, tense: str, pronoun: str) -> Optional[str]:
        """Conjugate regular -re verbs."""
        stem = infinitive[:-2]
        idx = self._get_pronoun_index(pronoun)

        if idx == -1:
            return None

        endings = {
            "présent": ["s", "s", "", "ons", "ez", "ent"],
            "imparfait": ["ais", "ais", "ait", "ions", "iez", "aient"],
            "futur": ["rai", "ras", "ra", "rons", "rez", "ront"],
            "conditionnel": ["rais", "rais", "rait", "rions", "riez", "raient"],
            "subjonctif": ["e", "es", "e", "ions", "iez", "ent"],
            "passé_simple": ["is", "is", "it", "îmes", "îtes", "irent"],
            "subjonctif_imparfait": [
                "isse",
                "isses",
                "ît",
                "issions",
                "issiez",
                "issent",
            ],
        }

        if tense in endings:
            return stem + endings[tense][idx]

        # Compound tenses
        if tense == "passé_composé":
            return (
                f"ai {stem}u"
                if idx in [0]
                else f"as {stem}u"
                if idx in [1]
                else f"a {stem}u"
                if idx in [2]
                else f"avons {stem}u"
                if idx in [3]
                else f"avez {stem}u"
                if idx in [4]
                else f"ont {stem}u"
            )
        elif tense == "plus_que_parfait":
            return (
                f"avais {stem}u"
                if idx in [0, 1]
                else f"avait {stem}u"
                if idx in [2]
                else f"avions {stem}u"
                if idx in [3]
                else f"aviez {stem}u"
                if idx in [4]
                else f"avaient {stem}u"
            )
        elif tense == "futur_antérieur":
            return (
                f"aurai {stem}u"
                if idx in [0]
                else f"auras {stem}u"
                if idx in [1]
                else f"aura {stem}u"
                if idx in [2]
                else f"aurons {stem}u"
                if idx in [3]
                else f"aurez {stem}u"
                if idx in [4]
                else f"auront {stem}u"
            )

        # Impératif
        if tense == "impératif":
            if idx == 1:
                return stem
            elif idx == 3:
                return stem + "ons"
            elif idx == 4:
                return stem + "ez"
            return None

        return None

    def get_full_conjugation(self, infinitive: str) -> Optional[Dict]:
        """Get all conjugations for a verb."""
        infinitive = infinitive.lower().strip()

        if infinitive not in self.verbs:
            return None

        verb_data = self.verbs[infinitive]

        # If verb has stored conjugations, return them
        if "conjugations" in verb_data:
            return verb_data["conjugations"]

        # Otherwise, generate all forms
        result = {}
        for tense in self.TENSES:
            result[tense] = {}
            for pronoun in self.PRONOUNS:
                form = self._generate_conjugation(verb_data, tense, pronoun)
                if form:
                    result[tense][pronoun] = form

        return result

    def verb_exists(self, infinitive: str) -> bool:
        """Check if a verb exists in the database."""
        return infinitive.lower().strip() in self.verbs

    def get_verb_info(self, infinitive: str) -> Optional[Dict]:
        """Get basic info about a verb."""
        infinitive = infinitive.lower().strip()

        if infinitive not in self.verbs:
            return None

        verb_data = self.verbs[infinitive]
        return {
            "infinitive": verb_data["infinitive"],
            "group": verb_data["group"],
            "irregularity": verb_data["irregularity"],
        }
