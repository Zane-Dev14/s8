#!/usr/bin/env python3
"""
Extract concepts using Ollama with improved prompts and longer timeout.
This leverages your M4 chip to intelligently extract concepts from bootcamp content.
"""
import asyncio
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.db import Concept, ConceptEdge, ContentChunk
from app.services.knowledge_graph_service import KnowledgeGraphService
from app.services.ollama_router import OllamaRouter
from app.services.quiz_service import QuizService
from app.services.learning_service import LearningService

async def main():
    print("=" * 70)
    print("INTELLIGENT CONCEPT EXTRACTION USING OLLAMA")
    print("=" * 70)
    print("\nThis will use your M4 chip to analyze bootcamp content and extract")
    print("meaningful learning concepts using AI.\n")
    
    with SessionLocal() as db:
        router = OllamaRouter()
        graph = KnowledgeGraphService(db, router)
        quiz = QuizService(db, router)
        learning = LearningService(db)
        
        try:
            # Get all chunks
            chunks = list(db.scalars(select(ContentChunk)).all())
            print(f"📊 Found {len(chunks)} content chunks to analyze")
            
            if not chunks:
                print("❌ No chunks found. Please run ingestion first.")
                return
            
            # Show chunk sources
            sources = set(c.source_reference for c in chunks if c.source_reference)
            print(f"📁 Content from {len(sources)} source files")
            print("\nTop sources:")
            for i, src in enumerate(list(sources)[:10], 1):
                print(f"  {i}. {src}")
            
            # Delete existing bad concepts (keep demo-sftp if you want)
            print("\n🧹 Cleaning up existing concepts...")
            existing = db.scalars(select(Concept)).all()
            for concept in existing:
                if concept.id != "demo-sftp":  # Keep demo if desired
                    print(f"  Removing: {concept.name}")
                    db.delete(concept)
            db.commit()
            
            # Use Ollama to extract concepts
            print("\n🤖 Analyzing content with Ollama (this may take 2-5 minutes)...")
            print("   Using improved prompts and 5-minute timeout for M4 chip")
            print("   Extracting key topics from bootcamp materials...\n")
            
            concept_count, edge_count = await graph.build_graph()
            
            if concept_count == 0:
                print("❌ No concepts extracted. Check Ollama logs.")
                return
            
            print(f"\n✅ Successfully extracted {concept_count} concepts!")
            
            # Show extracted concepts
            concepts = list(db.scalars(select(Concept)).all())
            print("\n📚 Extracted Concepts:")
            for i, concept in enumerate(concepts, 1):
                print(f"\n{i}. {concept.name}")
                print(f"   Source: {concept.source_reference}")
                print(f"   Why it matters: {concept.why_it_matters[:100]}...")
            
            print(f"\n🔗 Created {edge_count} prerequisite edges")
            
            # Generate quiz questions
            print("\n📝 Generating quiz questions...")
            quiz_count = await quiz.ensure_questions()
            print(f"✅ Generated {quiz_count} quiz questions")
            
            # Ensure learner profiles
            print("\n👤 Ensuring learner profiles...")
            learning.ensure_profiles(user_id="demo-user")
            print("✅ Learner profiles ready")
            
            print("\n" + "=" * 70)
            print("🎉 CONCEPT EXTRACTION COMPLETE!")
            print("=" * 70)
            print(f"\nResults:")
            print(f"  • {concept_count} meaningful concepts extracted")
            print(f"  • {edge_count} prerequisite relationships")
            print(f"  • {quiz_count} quiz questions generated")
            print(f"\nThe system is ready for learning!")
            print("Refresh your browser to see the new concepts.\n")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print("\nIf Ollama timed out, try:")
            print("  1. Check Ollama is running: curl http://localhost:11434/api/tags")
            print("  2. Increase timeout in knowledge_graph_service.py")
            print("  3. Use a smaller/faster model in settings")

if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
