---
name: french
description: Build a French verb conjugation AI assistant with practice, quiz, and tracking features.
---

1. Read PRD: `cat .agents/skills/French/PRD.md`. Review all 11 tasks.

2. Create project structure:
   - `data/french_verbs.json` - verb database
   - `data/user_progress.json` - tracking
   - `les_verbs/` package with `__init__.py`, `__main__.py`, `engine.py`, `tracker.py`, `recommender.py`, `cli.py`

3. Build verb database (Task 1):
   - Create `data/french_verbs.json` with 500+ C2 verbs
   - Include: infinitive, group (-er/-ir/-re), irregularity flag
   - Full conjugation tables for ~150 irregular verbs
   - Rules for regular verbs, stem changes for semi-irregulars
   - Test: `uv run python3 -c "import json; d=json.load(open('data/french_verbs.json')); assert len(d)>=500"`

4. Implement conjugation engine (Task 2):
   - Rule-based for regular verbs
   - Stored tables for irregulars
   - Support all tenses: présent, imparfait, futur, passé composé, conditionnel, subjonctif, plus-que-parfait, futur antérieur, passé simple, subjonctif imparfait, impératif
   - Test: `être(présent-je)→suis`, `finir(présent-nous)→finissons`, `manger(présent-nous)→mangeons`

5. Implement performance tracker (Task 3):
   - Track per verb-tense-pronoun: correct/incorrect counts, last practiced, sentence usage, skips
   - Save only after full verb completed
   - Handle corrupted/missing files gracefully
   - Test: Record 3 correct answers, verify counts update

6. Implement recommendation algorithm (Task 4):
   - Prioritize high error rates and older practice dates
   - Include randomness component
   - Default to présent for new verbs
   - Support short (1 verb) and long (3 verbs) sessions
   - Test: Request 3 recommendations with mock data

7. Implement practice mode (Task 5):
   - One verb at a time, one tense
   - Cycle through 6 pronouns: je, tu, il/elle/on, nous, vous, ils/elles
   - Immediate feedback after each attempt
   - Prompt for next verb or add tense after completion
   - Test: Complete 1 verb, 1 tense, all 6 pronouns

8. Implement quiz mode (Task 6):
   - 5 fill-in-the-blank questions
   - No feedback during quiz
   - Show score and corrections at end
   - Offer practice on wrong answers
   - Test: Complete 5-question quiz, verify score

9. Implement status display (Task 7):
   - Show: total verbs, times practiced, unique verbs practiced
   - Test: Display status with mock data

10. Implement sentence practice (Task 8):
    - Prompt after completing all 3 verbs (long session)
    - User writes sentence per verb
    - Track usage/skip counts
    - Support "skip sentence practice"
    - Test: Write sentence with être, receive correction

11. Implement CLI interface (Task 9):
    - `les-verbs` command starts chatbot
    - Menu: Practice, Quiz, Status, Sentence Quiz
    - Support `quiz on [verb]` command
    - Short/long session selection
    - Confirm verbs before session
    - Test: Navigate all menu options

12. Add error handling (Task 10):
    - Prompt to confirm verbs if tracking file missing
    - Discard incomplete verb on quit
    - Fuzzy matching for typos
    - Clear error messages
    - Test: Delete progress file, verify confirmation prompt

13. Set up entry point (Task 11):
    - Update `pyproject.toml` with `[project.scripts]`
    - `les-verbs = les_verbs.cli:main`
    - Test: `uv run les-verbs` launches chatbot

14. Run full test: `uv run python3 -m les_verbs`, verify all features work
