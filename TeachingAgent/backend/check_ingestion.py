#!/usr/bin/env python3
"""Check what was ingested into the database"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.db import Subject, Concept

db = SessionLocal()
subjects = db.query(Subject).all()

print('\n📊 Ingestion Summary:')
print('='*60)

for subject in subjects:
    concept_count = db.query(Concept).filter(Concept.subject_id == subject.id).count()
    print(f'\n✅ {subject.name}')
    print(f'   ID: {subject.id}')
    print(f'   Status: {subject.status}')
    print(f'   Concepts: {concept_count}')
    
    if concept_count > 0:
        concepts = db.query(Concept).filter(Concept.subject_id == subject.id).limit(5).all()
        print(f'   Sample concepts:')
        for c in concepts:
            print(f'      - {c.name} ({c.difficulty})')

print('\n' + '='*60)
print(f'Total Subjects: {len(subjects)}')
print(f'Total Concepts: {db.query(Concept).count()}')
print('='*60)

db.close()

# Made with Bob
