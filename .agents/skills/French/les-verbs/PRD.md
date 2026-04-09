# les-verbs - French Verb Learning Assistant

## Overview
A personalized AI assistant that helps users learn and practice French verb conjugation through adaptive lesson retrieval, progress tracking, and feedback collection.

## Activation
User types: `les-verbs, show me a new French lesson today`

## Core Features

### 1. Lesson Retrieval
- Fetch French lessons from reputable HTTPS websites
- Extract all verbs from lesson content
- Display source link + extracted verbs marked as new/known

### 2. Progress Tracking
- Track verb status: `new` → `learning` → `known`
- Status updates based on separate CLI quiz app results
- Store in `data/user_progress.json`

### 3. Adaptive Learning
- Prioritize verbs with low accuracy
- Spaced repetition (verbs not practiced recently)
- Cross-session memory via progress files

### 4. Feedback Collection
- Ask user for feedback after each lesson
- Store in `data/preferences.md`
- Track: verb feedback, preferred tenses, lesson sources, learning style, source quality

## Data Files

### data/french_verbs.json
Master list of French verbs (provided)

### data/user_progress.json
```json
{
  "être": {"status": "known", "times_practiced": 10, "last_practiced": "2026-04-09"},
  "avoir": {"status": "learning", "times_practiced": 3, "last_practiced": "2026-04-08"},
  "aller": {"status": "new", "times_practiced": 0, "last_practiced": null}
}
```

### data/preferences.md
User feedback and preferences history

## Output Format
```
📚 Lesson: [Title]
🔗 Source: [URL]

Verbs found:
- être [KNOWN] ✓
- avoir [LEARNING] 
- aller [NEW] ⭐

Progress: 15/50 verbs mastered

[Ask for user feedback]
```

## Edge Cases
- Verb not in french_verbs.json → Add it to progress tracking
- user_progress.json doesn't exist → Create with empty object, add verbs as encountered
- Only use HTTPS reputable websites for lessons

---

## Tasks

## Task 1: Create data folder structure and initialize data files
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 2: Build lesson fetcher module (Python, HTTPS only)
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 3: Build verb extractor from HTML content
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 4: Build progress tracker (read/write user_progress.json)
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 5: Build verb status classifier (new/learning/known)
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 6: Build feedback collector and preferences.md writer
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 7: Build main les-verbs command handler
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 8: Build output formatter (lesson + verbs + progress display)
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 9: Handle edge case - verb not in french_verbs.json
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 10: Handle edge case - user_progress.json doesn't exist
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled

## Task 11: Integration test - full flow from command to output
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Edge cases handled
