#!/usr/bin/env python3
"""
🇫🇷 French Verb Conjugation Demo
Shows the app features without requiring interactive input
"""

from french_verbs import FrenchVerbApp

app = FrenchVerbApp()

print("\n" + "=" * 60)
print("  🇫🇷 FRENCH VERB CONJUGATION APP - DEMO")
print("=" * 60)

print("\n✨ Features:")
print("  1. View full conjugation tables for 15 common verbs")
print("  2. Interactive quiz mode with scoring")
print("  3. Practice mode for specific verbs/tenses")
print("  4. Support for 5 tenses: présent, passé composé,")
print("     imparfait, futur simple, conditionnel")

print("\n" + "=" * 60)
print("  📚 SAMPLE CONJUGATION: ÊTRE (to be)")
print("=" * 60)

app.display_conjugation_table("être")

print("\n" + "=" * 60)
print("  📚 SAMPLE CONJUGATION: AVOIR (to have)")
print("=" * 60)

app.display_conjugation_table("avoir")

print("\n" + "=" * 60)
print("  📚 SAMPLE CONJUGATION: ALLER (to go)")
print("=" * 60)

app.display_conjugation_table("aller")

print("\n" + "=" * 60)
print("  📖 AVAILABLE VERBS")
print("=" * 60)
app.list_verbs()

print("\n" + "=" * 60)
print("  🎯 TO RUN THE APP INTERACTIVELY:")
print("=" * 60)
print("\n  python french_verbs.py\n")
print("  Then choose from the menu:")
print("    1. List all verbs")
print("    2. View conjugation table")
print("    3. Quiz mode (test yourself!)")
print("    4. Practice mode")
print("    5. Quit")

print("\n" + "=" * 60)
print("  BONNE CHANCE! 🍀")
print("=" * 60 + "\n")
