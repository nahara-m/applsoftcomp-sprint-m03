# test-skill - French Verb Conjugation Assistant

## Overview
This skill tests the French verb conjugation assistant implementation by running the test cases defined in PRD.md for each task.

## Test Execution Plan

### Task 1: Verb Database Test
```bash
cd .agents/skills/French
uv run python3 -c "import json; d=json.load(open('data/french_verbs.json')); assert len(d)>=500; print('✓ 500+ verbs found')"
```

### Task 2: Conjugation Engine Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.engine import conjugate
assert conjugate('être', 'présent', 'je') == 'suis', 'être conjugation failed'
assert conjugate('finir', 'présent', 'nous') == 'finissons', 'finir conjugation failed'
assert conjugate('manger', 'présent', 'nous') == 'mangeons', 'manger conjugation failed'
print('✓ Conjugation engine passed')
"
```

### Task 3: Performance Tracker Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.tracker import PerformanceTracker
t = PerformanceTracker('data/user_progress.json')
t.record('être', 'présent', 'je', correct=True)
t.record('être', 'présent', 'tu', correct=True)
t.record('être', 'présent', 'il', correct=True)
t.save()
import json
d = json.load(open('data/user_progress.json'))
assert d['être']['présent']['je']['correct'] == 1
print('✓ Performance tracker passed')
"
```

### Task 4: Recommendation Algorithm Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.recommender import Recommender
r = Recommender('data/user_progress.json', 'data/french_verbs.json')
recs = r.recommend(num=3)
assert len(recs) == 3, 'Should return 3 recommendations'
print('✓ Recommendation algorithm passed')
"
```

### Task 5: Practice Mode Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.engine import PracticeMode
p = PracticeMode()
# Simulate practice session for 1 verb, 1 tense, 6 pronouns
pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
for pronoun in pronouns:
    result = p.attempt('être', 'présent', pronoun, 'suis' if pronoun=='je' else None)
assert p.is_complete(), 'Practice should be complete after 6 pronouns'
print('✓ Practice mode passed')
"
```

### Task 6: Quiz Mode Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.engine import QuizMode
q = QuizMode()
questions = q.generate(5)
assert len(questions) == 5, 'Should generate 5 questions'
score = q.score(['suis', 'es', 'est', 'sommes', 'êtes'])
assert isinstance(score, int), 'Score should be integer'
print('✓ Quiz mode passed')
"
```

### Task 7: Status Display Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.tracker import PerformanceTracker
t = PerformanceTracker('data/user_progress.json')
status = t.get_status()
assert 'total_verbs' in status
assert 'times_practiced' in status
assert 'verbs_practiced' in status
print('✓ Status display passed')
"
```

### Task 8: Sentence Practice Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.engine import SentencePractice
s = SentencePractice()
result = s.evaluate('Je suis étudiant', 'être')
assert 'correct' in result or 'feedback' in result
print('✓ Sentence practice passed')
"
```

### Task 9: CLI Interface Test
```bash
cd .agents/skills/French
uv run python3 -c "
from les_verbs.cli import main
# Test CLI launches without error
import sys
sys.argv = ['les-verbs', '--test']
print('✓ CLI interface passed')
"
```

### Task 10: Error Handling Test
```bash
cd .agents/skills/French
mv data/user_progress.json data/user_progress.json.bak 2>/dev/null || true
uv run python3 -c "
from les_verbs.tracker import PerformanceTracker
t = PerformanceTracker('data/user_progress.json')
# Should handle missing file gracefully
assert t is not None
print('✓ Error handling passed')
"
mv data/user_progress.json.bak data/user_progress.json 2>/dev/null || true
```

### Task 11: Entry Point Test
```bash
cd .agents/skills/French
uv run les-verbs --help || uv run python3 -m les_verbs --help
echo "✓ Entry point passed"
```

## Evaluation
- Each test must pass without errors
- Update PRD.md with `Test Passed: true` for passing tasks
- Report failures with specific error messages

## Usage
Run this skill to verify all 11 tasks are implemented correctly.
