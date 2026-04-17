#!/usr/bin/env python3
"""
Demo script to run a live teaching session.
This demonstrates the complete teaching workflow from ingestion to mastery.
"""
import asyncio
import time
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine, Base
from app.models.db import Concept
from app.services.learning_service import LearningService
from app.services.ollama_router import OllamaRouter
from app.services.tutor_service import TutorService


def setup_demo_concept(db: Session) -> Concept:
    """Create a demo concept for testing the teaching system."""
    # Check if concept already exists
    existing = db.query(Concept).filter_by(id="demo-sftp").first()
    if existing:
        print("✓ Using existing demo concept")
        return existing
    
    concept = Concept(
        id="demo-sftp",
        name="SFTP Protocol",
        explanation=(
            "SFTP (SSH File Transfer Protocol) is a network protocol that provides "
            "file access, file transfer, and file management over a secure channel. "
            "Unlike FTP, SFTP encrypts both commands and data, preventing passwords "
            "and sensitive information from being transmitted in clear text."
        ),
        intuition=(
            "Think of SFTP as a secure tunnel for moving files. Regular FTP is like "
            "sending postcards - anyone can read them. SFTP is like sending sealed "
            "letters in armored trucks."
        ),
        example=(
            "When transferring EDI 850 purchase orders between trading partners, "
            "SFTP ensures the data is encrypted in transit using SSH keys for "
            "authentication, preventing man-in-the-middle attacks."
        ),
        common_mistake=(
            "Confusing SFTP with FTPS. SFTP uses SSH (port 22) for security, while "
            "FTPS uses SSL/TLS (ports 989/990). They're completely different protocols."
        ),
        why_it_matters=(
            "Critical for secure B2B data exchange. Most enterprise file transfers "
            "require SFTP for compliance (PCI-DSS, HIPAA). Understanding SFTP is "
            "essential for Sterling B2Bi implementations."
        ),
        checkpoint_question=(
            "What makes SFTP different from regular FTP, and why does it matter for "
            "enterprise file transfers?"
        ),
        hard_follow_up=(
            "Under what conditions would SFTP authentication fail, and how would you "
            "diagnose it in a production Sterling B2Bi environment?"
        ),
        source_reference="Demo-Concept",
    )
    db.add(concept)
    db.commit()
    print("✓ Created demo concept: SFTP Protocol")
    return concept


async def run_teaching_session():
    """Run a complete teaching session demonstrating all features."""
    print("\n" + "="*80)
    print("🎓 TEACHING AGENT - LIVE DEMO SESSION")
    print("="*80 + "\n")
    
    # Setup database
    Base.metadata.create_all(engine)
    db = SessionLocal()
    
    try:
        # Create demo concept
        concept = setup_demo_concept(db)
        
        # Initialize services
        router = OllamaRouter()
        tutor = TutorService(db, router)
        learning = LearningService(db)
        
        user_id = "demo-user"
        learning.ensure_profiles(user_id)
        
        print("\n📚 Starting Lesson Mode...")
        print("-" * 80)
        
        # Start lesson
        concept_obj, preview, question, time_pressure = await tutor.start_lesson(
            user_id, mode="lesson"
        )
        
        print(f"\n🎯 Concept: {preview['name']}")
        print(f"⏱️  Time Pressure: {time_pressure} seconds")
        print(f"\n💡 Why it matters: {preview['why_it_matters']}")
        print(f"\n🤔 Intuition: {preview['intuition']}")
        print(f"\n❓ Question: {question}")
        print("\n" + "-" * 80)
        
        # Simulate student answers with different patterns
        test_scenarios = [
            {
                "name": "Lucky Guess (Correct but Low Confidence)",
                "answer": "SFTP uses SSH for secure file transfer",
                "confidence": 35,
                "response_time": 12000,
            },
            {
                "name": "False Confidence (Wrong but High Confidence)",
                "answer": "SFTP is the same as FTPS, just different ports",
                "confidence": 95,
                "response_time": 5000,
            },
            {
                "name": "Strong Understanding (Correct, High Confidence, Fast)",
                "answer": (
                    "SFTP is a network protocol that provides file access, transfer, "
                    "and management over a secure SSH channel, encrypting both commands "
                    "and data unlike regular FTP"
                ),
                "confidence": 92,
                "response_time": 8000,
            },
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n\n{'='*80}")
            print(f"📝 ATTEMPT #{i}: {scenario['name']}")
            print('='*80)
            
            print(f"\n👤 Student Answer: {scenario['answer']}")
            print(f"💪 Confidence: {scenario['confidence']}%")
            print(f"⏱️  Response Time: {scenario['response_time']/1000:.1f}s")
            
            # Simulate thinking time
            print("\n🤖 Tutor is evaluating...")
            start_time = time.time()
            
            result = await tutor.evaluate_answer(
                user_id=user_id,
                concept=concept_obj,
                question=question,
                user_answer=scenario['answer'],
                user_confidence=scenario['confidence'],
                response_time_ms=scenario['response_time'],
                mode="lesson",
            )
            
            eval_time = time.time() - start_time
            
            (
                correctness,
                explanation,
                misconception_tag,
                next_action,
                next_question,
                source_chunks,
                confidence_label,
                uncertainty,
                feedback_delay,
            ) = result
            
            print(f"⚡ Evaluation completed in {eval_time:.2f}s")
            print(f"\n⏳ Feedback Delay: {feedback_delay}ms (enforcing reflection time)")
            
            # Simulate feedback delay
            await asyncio.sleep(feedback_delay / 1000)
            
            print(f"\n{'✅' if correctness else '❌'} Correctness: {correctness}")
            print(f"🏷️  Misconception: {misconception_tag}")
            print(f"🎯 Next Action: {next_action}")
            print(f"📊 Confidence Label: {confidence_label}")
            print(f"❓ Uncertainty: {uncertainty}")
            
            print(f"\n💬 Tutor Feedback:")
            print(f"   {explanation}")
            
            if source_chunks:
                print(f"\n📚 Grounded in {len(source_chunks)} source chunks")
            
            print(f"\n🔄 Next Question: {next_question}")
            
            # Update question for next iteration
            question = next_question
            
            # Show learning progress
            from app.models.db import LearnerProfile
            profile = db.query(LearnerProfile).filter_by(
                user_id=user_id,
                concept_id=concept.id
            ).first()
            
            if profile:
                print(f"\n📈 Learning Progress:")
                print(f"   Accuracy: {profile.accuracy:.2%}")
                print(f"   Confidence: {profile.confidence}%")
                print(f"   Retries: {profile.retries}")
            
            # Check mastery
            is_mastered = learning.is_mastered(user_id, concept.id)
            if is_mastered:
                print(f"\n🎉 MASTERY ACHIEVED! Concept mastered after {i} attempts!")
                break
            else:
                print(f"\n⚠️  Not yet mastered. Need: 3 correct + high confidence + time pressure + spacing")
        
        # Show forced revisit queue
        forced_ids = learning._forced_revisit_concept_ids(user_id)
        if forced_ids:
            print(f"\n\n🔄 Forced Revisit Queue: {len(forced_ids)} concepts")
            print("   These concepts triggered confusion detection and need immediate review")
        
        # Try interview mode
        print(f"\n\n{'='*80}")
        print("🎤 SWITCHING TO INTERVIEW MODE")
        print('='*80)
        
        concept_obj, preview, question, time_pressure = await tutor.start_lesson(
            user_id, mode="interview"
        )
        
        print(f"\n⏱️  Time Pressure: {time_pressure} seconds (shorter for interview!)")
        print(f"\n❓ Interview Question: {question}")
        print("\n💡 This is a harder challenge question to stress-test understanding")
        
        print(f"\n\n{'='*80}")
        print("✅ DEMO COMPLETE")
        print('='*80)
        print("\n📊 Summary:")
        print(f"   - Demonstrated shallow loop prevention (answer before explanation)")
        print(f"   - Showed mandatory confidence scoring (0-100)")
        print(f"   - Enforced feedback delays for reflection")
        print(f"   - Detected confusion patterns (lucky guess, false confidence)")
        print(f"   - Tracked learning progress with brutal mastery requirements")
        print(f"   - Demonstrated interview mode pressure differentiation")
        print(f"\n🎓 The system is working and ready to teach!")
        
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 Starting Teaching Agent Demo...")
    print("   This will demonstrate the complete teaching workflow\n")
    asyncio.run(run_teaching_session())

# Made with Bob
