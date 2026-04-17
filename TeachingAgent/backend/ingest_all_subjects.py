#!/usr/bin/env python3
"""
Comprehensive ingestion script for all study materials.
Ingests PDFs, markdown files, and text files from SC, BCT, DC, DM folders.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings
from app.models.db import Base, Subject, Concept, ContentChunk, IngestionJob, SourceFile
from app.services.concept_extraction_service import ConceptExtractionService
import asyncio
import fitz  # PyMuPDF
from docx import Document as DocxDocument

# Study material paths
STUDY_ROOT = Path("/Users/eric/Documents/StudyCollege")
SUBJECTS = {
    "Soft Computing": {
        "code": "SC",
        "path": STUDY_ROOT / "SC",
        "files": [
            "SC - M1 -Ktunotes.in.pdf",
            "SC - M2 -Ktunotes.in.pdf", 
            "SC - M3 -Ktunotes.in.pdf",
            "SC - M4 -Ktunotes.in.pdf",
            "SC - M5 -Ktunotes.in.pdf",
            "module 1.md",
            "module 2.md",
            "module 3.md",
            "STEP1_Priority_Topics.md",
            "STEP2_Module1_CrashGuide.md",
            "STEP3_Module2_CrashGuide.md",
            "STEP4_Module3_CrashGuide.md",
            "STEP5_PYQ_Attack.md",
            "STEP6_Memory_Hacks.md",
            "STEP7_30Min_Plan.md",
            "build/M1_pdf_source.txt",
            "build/M2_pdf_source.txt",
            "build/M3_pdf_source.txt",
            "build/M4_pdf_source.txt",
            "build/M5_pdf_source.txt",
        ]
    },
    "Blockchain Technology": {
        "code": "BCT",
        "path": STUDY_ROOT / "BCT",
        "files": [
            "CST428-M1-Ktunotes.in.pdf",
            "Module 1.pdf",
            "Module II-1.pdf",
            "Module IV - Part I.pdf",
            "Module IV - Part II (1).pdf",
        ]
    },
    "Distributed Computing": {
        "code": "DC",
        "path": STUDY_ROOT / "DC",
        "files": [
            "Dcmod2.pdf",
            "DCmod3.pdf",
            "dcMod4.pdf",
            "DCSeries1.pdf",
            "DCSeries2.pdf",
            "Model QP Solved.pdf",
        ]
    },
    "Data Mining": {
        "code": "DM",
        "path": STUDY_ROOT / "DM",
        "files": [
            "Data-Mining-Module-1-Important-Topics-PYQs.pdf",
            "Data-Mining-Module-2-Important-Topics-PYQs.pdf",
            "mod3.pdf",
            "series1.pdf",
        ]
    }
}


def create_db_session() -> Session:
    """Create database session."""
    db_url = f"sqlite:///{settings.db_path}"
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def extract_text_from_file(file_path: Path) -> Optional[str]:
    """Extract text from PDF, markdown, or text file."""
    try:
        if file_path.suffix.lower() == '.pdf':
            # Extract PDF text using PyMuPDF
            doc = fitz.open(str(file_path))
            pages = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    pages.append(f"[Page {page_num + 1}]\n{text}")
            doc.close()
            return "\n\n".join(pages)
        elif file_path.suffix.lower() == '.docx':
            # Extract DOCX text
            doc = DocxDocument(str(file_path))
            lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            return "\n".join(lines)
        elif file_path.suffix.lower() in ['.md', '.txt']:
            return file_path.read_text(encoding='utf-8')
        else:
            print(f"⚠️  Unsupported file type: {file_path.suffix}")
            return None
    except Exception as e:
        print(f"❌ Error extracting text from {file_path.name}: {e}")
        return None


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Simple text chunking with overlap."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks


def ingest_subject(db: Session, subject_name: str, subject_info: dict) -> tuple[Subject, str]:
    """Ingest all files for a subject."""
    print(f"\n{'='*60}")
    print(f"📚 Ingesting: {subject_name} ({subject_info['code']})")
    print(f"{'='*60}")
    
    # Create or get subject
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        subject = Subject(
            name=subject_name,
            description=f"Study materials for {subject_name}",
            status="processing"
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)
        print(f"✅ Created subject: {subject.id}")
    else:
        print(f"♻️  Using existing subject: {subject.id}")
    
    # Process each file
    total_chunks = 0
    processed_files = 0
    all_text_parts = []
    
    for file_name in subject_info['files']:
        file_path = subject_info['path'] / file_name
        
        if not file_path.exists():
            print(f"⚠️  File not found: {file_name}")
            continue
        
        print(f"\n📄 Processing: {file_name}")
        
        # Extract text
        text = extract_text_from_file(file_path)
        if not text:
            continue
        
        print(f"   Extracted {len(text)} characters")
        all_text_parts.append(text)
        
        # Chunk text
        chunks = chunk_text(text)
        print(f"   Created {len(chunks)} chunks")
        total_chunks += len(chunks)
        
        processed_files += 1
    
    # Combine all text
    all_text = "\n\n".join(all_text_parts)
    
    print(f"\n✅ Processed {processed_files} files, {total_chunks} chunks, {len(all_text)} total chars")
    
    # Update subject status
    subject.status = "ready"
    db.commit()
    
    return subject, all_text


async def extract_concepts_for_subject(db: Session, subject: Subject, all_text: str):
    """Extract concepts from subject's text content."""
    print(f"\n🧠 Extracting concepts for: {subject.name}")
    
    if not all_text or len(all_text) < 100:
        print("⚠️  Not enough text for concept extraction")
        return
    
    # Split text into chunks for extraction
    text_chunks = chunk_text(all_text, chunk_size=1000, overlap=100)
    print(f"   Using {len(text_chunks)} text chunks ({len(all_text)} chars total)")
    
    # Extract concepts using Ollama
    extractor = ConceptExtractionService()
    try:
        concepts_data = await extractor.extract_concepts(
            subject_name=subject.name,
            content_chunks=text_chunks[:10]  # Use first 10 chunks
        )
        
        print(f"   Extracted {len(concepts_data)} concepts")
        
        # Store concepts in database
        for concept_data in concepts_data:
            concept = Concept(
                subject_id=subject.id,
                name=concept_data.get('name', 'Unknown'),
                plain_name=concept_data.get('plain_name', concept_data.get('name', 'Unknown')),
                difficulty=concept_data.get('difficulty', 'intermediate'),
                explanation=concept_data.get('explanation', '')
            )
            db.add(concept)
            db.flush()  # Get the concept ID
            
            # Create prerequisite edges if any
            prereqs = concept_data.get('prerequisites', [])
            if prereqs:
                # Store as JSON in source_reference for now
                # TODO: Create ConceptEdge entries when we have concept name -> ID mapping
                concept.source_reference = json.dumps({'prerequisites': prereqs})
        
        db.commit()
        print(f"✅ Stored concepts in database")
        
    except Exception as e:
        print(f"❌ Error extracting concepts: {e}")


async def main():
    """Main ingestion process."""
    print("🚀 Starting comprehensive ingestion of all study materials")
    print(f"📂 Study root: {STUDY_ROOT}")
    
    db = create_db_session()
    
    try:
        for subject_name, subject_info in SUBJECTS.items():
            # Ingest subject files
            subject, all_text = ingest_subject(db, subject_name, subject_info)
            
            # Extract concepts
            await extract_concepts_for_subject(db, subject, all_text)
        
        print("\n" + "="*60)
        print("✅ INGESTION COMPLETE!")
        print("="*60)
        
        # Print summary
        total_subjects = db.query(Subject).count()
        total_concepts = db.query(Concept).count()
        
        print(f"\n📊 Summary:")
        print(f"   Subjects: {total_subjects}")
        print(f"   Concepts: {total_concepts}")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
