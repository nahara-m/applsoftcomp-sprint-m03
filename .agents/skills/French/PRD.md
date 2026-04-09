# les-verbs - French Verb Conjugation AI Assistant

## Overview
CLI chatbot for practicing French verb conjugation (C2 level). Practices 1-3 verbs at a time, one tense at a time, with performance tracking and adaptive recommendations.

## Features
- **Practice Mode**: Conjugate with immediate feedback through all pronouns
- **Quiz Mode**: 5 fill-in-the-blank questions, scored at end
- **Status**: View metrics (total verbs, times practiced, verbs practiced)
- **Sentence Quiz**: Create sentences using practiced verbs

## Data & Tracking
- Local JSON: times practiced, errors, last practiced date, sentence usage, skips
- ~500-1000 C2 verbs fetched once, saved locally
- Fresh recommendations each session (errors/performance + random)
- User confirms verbs before session; progress saved after full verb only

---

## Task 1: Curated French Verbs Data File
- **Implemented**: false | **Test Passed**: false
- **Goal**: Build `data/french_verbs.json` with ~500-1000 C2 verbs
- **Inputs**: Wiktionary and standard C2 verb lists
- **Outputs**: JSON with infinitive, group (-er/-ir/-re), irregularity flag
- **Specifications**: Full conjugation tables for ~150 irregular verbs; rules for regular verbs; stem changes for semi-irregulars
- **Test Case**: Load file, verify 500+ verbs with required fields
- **Evaluation Criteria**: All 3 groups present, irregulars have full tables

## Task 2: Conjugation Engine
- **Implemented**: false | **Test Passed**: false
- **Goal**: Lightweight conjugation generator (no external dependencies)
- **Inputs**: Verb infinitive, tense/mood, pronoun
- **Outputs**: Correct conjugated form
- **Specifications**: Rule-based for regular verbs; stored tables for irregulars; all tenses (présent, imparfait, futur, passé composé, conditionnel, subjonctif, plus-que-parfait, futur antérieur, passé simple, subjonctif imparfait, impératif)
- **Test Case**: Conjugate être(présent-je), finir(présent-nous), manger(présent-nous)
- **Evaluation Criteria**: Returns "suis", "finissons", "mangeons"

## Task 3: Performance Tracking System
- **Implemented**: false | **Test Passed**: false
- **Goal**: Track user progress in `data/user_progress.json`
- **Inputs**: Correct/incorrect answers, sentence completion, skips
- **Outputs**: Updated JSON with counts and timestamps
- **Specifications**: Track per verb-tense-pronoun; save only after full verb completed; handle corrupted/missing files gracefully
- **Test Case**: Record 3 correct conjugations, verify counts update
- **Evaluation Criteria**: Accurate counts, no data loss on interrupted session

## Task 4: Verb Recommendation Algorithm
- **Implemented**: false | **Test Passed**: false
- **Goal**: Recommend verbs based on performance + randomness
- **Inputs**: User progress, session type (short=1 verb, long=3 verbs)
- **Outputs**: Recommended verbs with suggested tense
- **Specifications**: Prioritize high error rates and older practice dates; include randomness; default to présent for new verbs; user confirms before starting
- **Test Case**: Request 3 recommendations with mock data
- **Evaluation Criteria**: Returns prioritized verbs with random component

## Task 5: Practice Mode
- **Implemented**: false | **Test Passed**: false
- **Goal**: Interactive practice with immediate feedback
- **Inputs**: User conjugation attempts per pronoun
- **Outputs**: Correct/incorrect feedback, progression
- **Specifications**: One verb at a time; 6 pronouns (je, tu, il/elle/on, nous, vous, ils/elles); immediate correction; prompt for next verb or add tense after completion; save only after full verb
- **Test Case**: Complete 1 verb, 1 tense, all 6 pronouns
- **Evaluation Criteria**: All pronouns covered, feedback given, progress saved

## Task 6: Quiz Mode
- **Implemented**: false | **Test Passed**: false
- **Goal**: 5-question quiz with end scoring
- **Inputs**: User answers to fill-in-the-blank
- **Outputs**: Score /5, corrections at end
- **Specifications**: Mix of pronoun conjugation and sentence completion; no feedback during quiz; offer practice on wrong answers; not saved to progress
- **Test Case**: Complete 5-question quiz, verify score
- **Evaluation Criteria**: Accurate score, corrections shown, practice offered

## Task 7: Status Display
- **Implemented**: false | **Test Passed**: false
- **Goal**: Show user progress metrics
- **Inputs**: User progress data
- **Outputs**: Formatted status display
- **Specifications**: Total verbs, times practiced, verbs practiced (unique count)
- **Test Case**: Display status with mock data
- **Evaluation Criteria**: Accurate counts, clear formatting

## Task 8: Sentence Practice/Quiz
- **Implemented**: false | **Test Passed**: false
- **Goal**: User creates sentences with practiced verbs
- **Inputs**: User-written sentences (one per verb)
- **Outputs**: Correction/feedback, skip tracking
- **Specifications**: Prompt after all 3 verbs completed; correct grammar and verb usage; track usage/skip counts; allow "skip sentence practice"
- **Test Case**: User writes sentence with être, receives correction
- **Evaluation Criteria**: Sentence evaluated, skip option works

## Task 9: CLI Chatbot Interface
- **Implemented**: false | **Test Passed**: false
- **Goal**: Interactive command-line interface
- **Inputs**: User commands via terminal
- **Outputs**: Menus, prompts, responses
- **Specifications**: `les-verbs` command starts chatbot; menu with Practice/Quiz/Status/Sentence Quiz; accept text commands; support "quiz on [verb]"; short(1 verb)/long(3 verbs) selection; confirm verbs before session
- **Test Case**: Launch chatbot, navigate all menu options
- **Evaluation Criteria**: All options accessible, commands parsed correctly

## Task 10: Edge Cases & Error Recovery
- **Implemented**: false | **Test Passed**: false
- **Goal**: Robust error handling
- **Inputs**: Corrupted files, missing data, interrupted sessions
- **Outputs**: Graceful recovery, user prompts
- **Specifications**: Prompt to confirm verbs if tracking file missing; discard incomplete verb on quit; fuzzy matching for typos; clear error messages
- **Test Case**: Delete progress file, verify confirmation prompt
- **Evaluation Criteria**: No crashes, appropriate prompts

## Task 11: Entry Point & Installation
- **Implemented**: false | **Test Passed**: false
- **Goal**: Installable Python package
- **Inputs**: N/A
- **Outputs**: `python -m les_verbs` or `les-verbs` command
- **Specifications**: Package at `.agents/skills/French/les_verbs/`; `__main__.py` for execution; pyproject.toml; no external dependencies
- **Test Case**: Install and run `les-verbs`
- **Evaluation Criteria**: Command launches chatbot without errors
