#!/usr/bin/env python3
"""
Generate plain-language summaries for legislative projects using Gemini.
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import google.generativeai as genai
from db.client import get_client

# Configure Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    print("Get your key at: https://makersuite.google.com/app/apikey")
    print("Then run: export GEMINI_API_KEY='your-key-here'")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

client = get_client()

PROMPT_TEMPLATE = """Jesteś ekspertem od prawa polskiego. Napisz krótkie, zrozumiałe podsumowanie projektu ustawy dla zwykłego obywatela.

Tytuł projektu: {title}
Inicjator: {initiator}
Obecny etap: {phase}

Napisz 2-3 zdania wyjaśniające:
1. Co ta ustawa zmienia lub wprowadza
2. Kogo dotyczy i jak wpłynie na ich życie
3. Konkretne liczby/progi jeśli są znane z tytułu

Zasady:
- Pisz prostym językiem, bez żargonu prawniczego
- Bądź konkretny i rzeczowy
- Nie zaczynaj od "Ta ustawa..." ani "Projekt..."
- Nie pisz o procesie legislacyjnym
- Max 300 znaków

Podsumowanie:"""

PHASE_LABELS = {
    'rcl': 'Konsultacje rządowe',
    'sejm': 'Prace w Sejmie',
    'senate': 'Prace w Senacie',
    'president': 'U Prezydenta',
    'published': 'Weszła w życie',
    'rejected': 'Odrzucona',
}


def generate_summary(title: str, initiator: str, phase: str) -> str:
    """Generate a summary using Gemini."""
    prompt = PROMPT_TEMPLATE.format(
        title=title,
        initiator=initiator or 'Nieznany',
        phase=PHASE_LABELS.get(phase, phase),
    )

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()

        # Clean up common issues
        summary = summary.replace('**', '')
        summary = summary.replace('*', '')

        # Ensure reasonable length
        if len(summary) > 500:
            summary = summary[:497] + '...'

        return summary
    except Exception as e:
        print(f"  Error generating summary: {e}")
        return None


def main():
    print("=" * 60)
    print("GENERATING SUMMARIES WITH GEMINI")
    print("=" * 60)

    # Get all projects
    projects = client.table('projects').select('id, title, initiator, phase, summary').execute().data

    print(f"\nFound {len(projects)} projects")
    print()

    updated = 0
    errors = 0

    for i, p in enumerate(projects):
        title = p['title']
        print(f"[{i+1}/{len(projects)}] {title[:50]}...")

        # Generate new summary
        summary = generate_summary(title, p.get('initiator'), p['phase'])

        if summary:
            # Update database
            client.table('projects').update({
                'summary': summary
            }).eq('id', p['id']).execute()

            print(f"  -> {summary[:80]}...")
            updated += 1
        else:
            errors += 1

        # Rate limiting - Gemini has limits
        time.sleep(0.5)

    print()
    print("=" * 60)
    print(f"DONE: {updated} updated, {errors} errors")
    print("=" * 60)


if __name__ == '__main__':
    main()
