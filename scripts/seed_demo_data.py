#!/usr/bin/env python3
"""
Seed demo data for hackathon presentation.

This script:
1. Ensures we have projects at various stages
2. Creates developments/news items for the feed
3. Populates Sejm stages for linked projects
"""

import sys
import os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from db.client import get_client, SejmStagesDB
import requests

client = get_client()
sejm_db = SejmStagesDB()


def get_interesting_sejm_processes():
    """Find Sejm processes at various stages."""

    # Hand-picked interesting process numbers from Sejm term 10
    # These are real projects at various stages
    interesting = [
        # Published laws
        1426,  # Kodeks pracy (already have)
        900,   #
        1000,
        1100,
        1200,
        1300,

        # Various stages
        1500,
        1600,
        1700,
        1800,
        1900,
        2000,
    ]

    results = []
    for num in interesting:
        try:
            url = f'https://api.sejm.gov.pl/sejm/term10/processes/{num}'
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('stages'):
                    results.append(data)
        except Exception as e:
            print(f'  Error fetching {num}: {e}')

    return results


def create_developments_for_project(project_id: str, project_title: str, phase: str):
    """Create realistic development entries for a project."""

    now = datetime.now()
    developments = []

    # Base templates for different phases
    if phase == 'rcl':
        developments = [
            {
                'title': 'Projekt rozpoczal konsultacje publiczne',
                'development_type': 'neutral',
                'occurred_at': (now - timedelta(days=random.randint(5, 30))).isoformat(),
            },
            {
                'title': 'Zakonczono etap uzgodnien miedzyresortowych',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(1, 5))).isoformat(),
            },
        ]
    elif phase == 'sejm':
        developments = [
            {
                'title': 'Projekt skierowan do I czytania w Sejmie',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(10, 30))).isoformat(),
            },
            {
                'title': 'Komisja sejmowa zakonczyla prace nad projektem',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(1, 10))).isoformat(),
            },
        ]
    elif phase == 'senate':
        developments = [
            {
                'title': 'Sejm uchwalil ustawe - przekazano do Senatu',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(5, 15))).isoformat(),
            },
            {
                'title': 'Senat rozpatruje projekt',
                'development_type': 'neutral',
                'occurred_at': (now - timedelta(days=random.randint(1, 5))).isoformat(),
            },
        ]
    elif phase == 'president':
        developments = [
            {
                'title': 'Sejm przyj al stanowisko Senatu',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(5, 15))).isoformat(),
            },
            {
                'title': 'Ustawa przekazana Prezydentowi do podpisu',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(1, 5))).isoformat(),
            },
        ]
    elif phase == 'published':
        developments = [
            {
                'title': 'Prezydent podpisal ustawe',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(10, 30))).isoformat(),
            },
            {
                'title': 'Ustawa opublikowana w Dzienniku Ustaw',
                'development_type': 'positive',
                'occurred_at': (now - timedelta(days=random.randint(1, 10))).isoformat(),
            },
        ]
    elif phase == 'rejected':
        developments = [
            {
                'title': 'Sejm odrzucil projekt ustawy',
                'development_type': 'negative',
                'occurred_at': (now - timedelta(days=random.randint(1, 10))).isoformat(),
            },
        ]

    # Insert developments
    for dev in developments:
        dev['project_id'] = project_id
        dev['description'] = f'Aktualizacja dotyczaca: {project_title[:100]}'

    if developments:
        result = client.table('project_developments').insert(developments).execute()
        return len(result.data)
    return 0


def populate_sejm_stages_for_project(project_id: str, sejm_print: str, term: int = 10):
    """Fetch and populate Sejm stages for a project."""

    try:
        url = f'https://api.sejm.gov.pl/sejm/term{term}/processes/{sejm_print}'
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return 0

        data = resp.json()
        stages = data.get('stages', [])

        if stages:
            result = sejm_db.upsert_stages(project_id, stages)
            return len(result)
    except Exception as e:
        print(f'  Error: {e}')

    return 0


def main():
    print('=' * 60)
    print('SEEDING DEMO DATA')
    print('=' * 60)

    # Get existing projects
    projects = client.table('projects').select('id, title, phase, sejm_print, sejm_term').execute().data

    print(f'\nFound {len(projects)} existing projects')

    # Count by phase
    by_phase = {}
    for p in projects:
        by_phase[p['phase']] = by_phase.get(p['phase'], 0) + 1
    print('By phase:', by_phase)

    # Create developments for each project
    print('\n--- Creating developments ---')
    total_devs = 0
    for p in projects:
        count = create_developments_for_project(p['id'], p['title'], p['phase'])
        if count > 0:
            print(f'  Created {count} developments for: {p["title"][:50]}...')
            total_devs += count

    print(f'\nTotal developments created: {total_devs}')

    # Populate Sejm stages for projects that have sejm_print
    print('\n--- Populating Sejm stages ---')
    for p in projects:
        if p.get('sejm_print'):
            count = populate_sejm_stages_for_project(
                p['id'],
                p['sejm_print'],
                p.get('sejm_term', 10)
            )
            if count > 0:
                print(f'  Added {count} Sejm stages for print {p["sejm_print"]}')

    print('\n' + '=' * 60)
    print('DONE')
    print('=' * 60)


if __name__ == '__main__':
    main()
