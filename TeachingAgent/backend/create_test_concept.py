#!/usr/bin/env python3
"""Create a test concept for testing streaming endpoints"""

from app.core.database import SessionLocal
from app.models.db import Subject, Concept

def create_test_data():
    db = SessionLocal()
    try:
        # Create test subject
        subject = Subject(
            id="test-subject-1",
            name="Machine Learning Basics",
            description="Introduction to ML concepts",
            status="ready"
        )
        db.add(subject)
        db.flush()
        
        # Create test concept
        concept = Concept(
            id="test-concept-1",
            subject_id=subject.id,
            name="supervised_learning",
            plain_name="Supervised Learning",
            difficulty="beginner",
            why_it_matters="Foundation of most ML applications",
            intuition="Learning from labeled examples, like a teacher showing you the answers",
            explanation="Supervised learning is when you train a model using data that already has the correct answers (labels). The model learns patterns from these examples.",
            example="Email spam detection: You show the model thousands of emails labeled as 'spam' or 'not spam', and it learns to classify new emails.",
            common_mistake="Thinking the model 'understands' the data like humans do. It only finds statistical patterns.",
            checkpoint_question="What's the key difference between supervised and unsupervised learning?",
            hard_follow_up="How would you handle imbalanced datasets in supervised learning?",
            source_reference="test_data"
        )
        db.add(concept)
        db.commit()
        
        print(f"✅ Created test subject: {subject.id}")
        print(f"✅ Created test concept: {concept.id}")
        print(f"   Plain name: {concept.plain_name}")
        print(f"   Difficulty: {concept.difficulty}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()

# Made with Bob
