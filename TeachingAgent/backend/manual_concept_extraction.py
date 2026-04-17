#!/usr/bin/env python3
"""
Manual concept extraction script to fix failed ingestion.
Uses heuristic approach to extract concepts from chunks without Ollama timeout.
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
    print("Starting manual concept extraction (heuristic mode)...")
    
    with SessionLocal() as db:
        router = OllamaRouter()
        graph = KnowledgeGraphService(db, router)
        quiz = QuizService(db, router)
        learning = LearningService(db)
        
        try:
            # Get chunks
            chunks = list(db.scalars(select(ContentChunk)).all())
            print(f"Found {len(chunks)} chunks to analyze")
            
            if not chunks:
                print("❌ No chunks found. Run ingestion first.")
                return
            
            # Use heuristic extraction (no Ollama timeout)
            print("Extracting concepts using heuristic analysis...")
            concept_specs = graph._heuristic_concepts(chunks)
            print(f"Identified {len(concept_specs)} potential concepts")
            
            # Create concepts
            concept_by_name = {}
            for spec in concept_specs:
                name = spec["name"].strip()
                if not name or name.lower() in concept_by_name:
                    continue
                
                concept = Concept(
                    name=name,
                    why_it_matters=spec.get("why_it_matters", ""),
                    intuition=spec.get("intuition", ""),
                    explanation=spec.get("explanation", ""),
                    example=spec.get("example", ""),
                    common_mistake=spec.get("common_mistake", ""),
                    checkpoint_question=spec.get("checkpoint_question", ""),
                    hard_follow_up=spec.get("hard_follow_up", ""),
                    source_reference=spec.get("source_reference", ""),
                )
                db.add(concept)
                db.flush()
                concept_by_name[name.lower()] = concept
                print(f"  ✓ Created concept: {name}")
            
            db.commit()
            
            # Build edges
            concept_list = list(db.scalars(select(Concept)).all())
            edge_count = graph._build_edges(concept_list)
            print(f"✅ Created {len(concept_list)} concepts and {edge_count} edges")
            
            print("Generating quiz questions...")
            quiz_count = await quiz.ensure_questions()
            print(f"✅ Generated {quiz_count} quiz questions")
            
            print("Ensuring learner profiles...")
            learning.ensure_profiles(user_id="demo-user")
            print("✅ Learner profiles ready")
            
            print("\n🎉 Concept extraction complete!")
            print(f"   - {len(concept_list)} concepts")
            print(f"   - {edge_count} prerequisite edges")
            print(f"   - {quiz_count} quiz questions")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
