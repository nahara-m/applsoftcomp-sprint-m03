---
name: les-verbs
description: Build a French verb learning assistant with lesson retrieval, progress tracking, and adaptive learning.
---

1. Read PRD: `cat .agents/skills/French/les-verbs/PRD.md`. Review all 11 tasks.

2. Create project structure:
   - `data/french_verbs.json` - master verb list
   - `data/user_progress.json` - verb status tracking
   - `data/preferences.md` - user feedback history
   - `les_verbs/` package with `__init__.py`, `__main__.py`, `lesson_fetcher.py`, `verb_extractor.py`, `progress_tracker.py`, `feedback_collector.py`, `cli.py`

3. Initialize data files (Task 1):
   - Create `data/french_verbs.json` with French verbs list
   - Create empty `data/user_progress.json` with `{}`
   - Create `data/preferences.md` with header
   - Test: Verify all files exist and are valid JSON/Markdown

4. Build lesson fetcher module (Task 2):
   - Fetch lessons from HTTPS URLs only
   - Use requests or urllib for HTTPS requests
   - Validate SSL certificates
   - Handle connection errors gracefully
   - Test: Fetch from a reputable French learning site, verify HTML content retrieved

5. Build verb extractor (Task 3):
   - Parse HTML content for French verbs
   - Use BeautifulSoup or regex for extraction
   - Match against french_verbs.json master list
   - Handle variations in verb forms
   - Test: Extract verbs from sample HTML, verify matches

6. Build progress tracker (Task 4):
   - Read/write user_progress.json
   - Track: status, times_practiced, last_practiced
   - Create file if doesn't exist
   - Handle corrupted JSON gracefully
   - Test: Update verb status, verify JSON updates correctly

7. Build verb status classifier (Task 5):
   - Classify verbs as: new, learning, known
   - new: times_practiced = 0
   - learning: 0 < times_practiced < threshold
   - known: times_practiced >= threshold OR accuracy high
   - Test: Classify verbs with different practice counts

8. Build feedback collector (Task 6):
   - Prompt user for feedback after each lesson
   - Collect: verb feedback, preferred tenses, source quality
   - Append to data/preferences.md with timestamp
   - Parse existing preferences for context
   - Test: Submit feedback, verify it's saved to preferences.md

9. Build main command handler (Task 7):
   - Handle `les-verbs` command
   - Parse user input for lesson requests
   - Coordinate between fetcher, extractor, tracker
   - Support "show me a new lesson today" activation
   - Test: Run command, verify full flow executes

10. Build output formatter (Task 8):
    - Format lesson display with title, source URL
    - Show verbs with status markers: [KNOWN] ✓, [LEARNING], [NEW] ⭐
    - Display progress summary (e.g., "15/50 verbs mastered")
    - Include feedback prompt
    - Test: Format sample output, verify all elements present

11. Handle edge case - unknown verb (Task 9):
    - Detect verbs not in french_verbs.json
    - Add to progress tracking automatically
    - Optionally add to master list
    - Test: Process lesson with unknown verb, verify it's tracked

12. Handle edge case - missing progress file (Task 10):
    - Detect when user_progress.json doesn't exist
    - Create with empty object `{}`
    - Add encountered verbs as "new" status
    - Test: Delete progress file, run command, verify recreation

13. Integration test (Task 11):
    - Full flow: command → fetch lesson → extract verbs → classify → display → collect feedback
    - Verify progress updates correctly
    - Test preferences are saved
    - Test: Run complete session, verify all data files updated

14. Run full test: `uv run python3 -m les_verbs`, verify lesson retrieval and tracking work
