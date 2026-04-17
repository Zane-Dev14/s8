#!/usr/bin/env python3
"""
Soft Computing Subject Ingestion Script
Extracts module-wise concepts from SC crash guides with exam focus
"""
import asyncio
import sys
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.db import Subject, Concept, SourceFile
from app.services.concept_extraction_service import ConceptExtractionService


# Module-wise concept definitions based on SC crash guides
SC_MODULES = {
    "Module 1: Neural Networks Basics": {
        "concepts": [
            {
                "name": "Soft Computing vs Hard Computing",
                "plain_name": "Soft vs Hard Computing",
                "difficulty": "beginner",
                "explanation": "Two different approaches to problem-solving. Hard computing requires precise input and gives exact results using binary logic. Soft computing tolerates imprecision and uncertainty, using techniques like ANN, Fuzzy Logic, and GA.",
                "example": "Hard: Calculator (exact math). Soft: Human reasoning (approximate but flexible).",
                "common_mistake": "Thinking soft computing is 'easier' - it's actually more sophisticated for handling real-world uncertainty.",
                "prerequisites": [],
                "module": "Module 1",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part A - 3 marks",
                "time_to_learn": "3 min"
            },
            {
                "name": "Biological vs Artificial Neuron",
                "plain_name": "Brain Cells vs Math Neurons",
                "difficulty": "beginner",
                "explanation": "Biological neurons have dendrites (input), soma (processing), axon (output), and synapses (connections). Artificial neurons mimic this with inputs, weights, summation, activation function, and output.",
                "example": "Brain neuron fires when enough signals arrive. ANN neuron outputs 1 when weighted sum crosses threshold.",
                "common_mistake": "Forgetting that synaptic strength maps to weights in ANN.",
                "prerequisites": [],
                "module": "Module 1",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part A - 3 marks",
                "time_to_learn": "4 min"
            },
            {
                "name": "Activation Functions",
                "plain_name": "How Neurons Decide to Fire",
                "difficulty": "beginner",
                "explanation": "Mathematical functions that decide if a neuron should activate. Common types: Binary Sigmoid [0,1], Bipolar Sigmoid [-1,1], Step {0,1}, Linear (all values). They introduce non-linearity for complex pattern learning.",
                "example": "Binary sigmoid: f(x) = 1/(1+e^(-x)). Used for binary classification.",
                "common_mistake": "Using linear activation for complex problems - it can't learn non-linear patterns.",
                "prerequisites": [],
                "module": "Module 1",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part A - 3 marks + numericals",
                "time_to_learn": "5 min"
            },
            {
                "name": "McCulloch-Pitts Neuron",
                "plain_name": "MP Neuron for Logic Gates",
                "difficulty": "intermediate",
                "explanation": "First mathematical neuron model (1943). Uses binary inputs, threshold logic. Can implement AND, OR, NOT gates. Formula: y=1 if Σ(xi)≥θ, else 0. Weights can be excitatory (+) or inhibitory (-).",
                "example": "AND gate: w1=1, w2=1, θ=2. Only (1,1) gives sum≥2, output=1.",
                "common_mistake": "Wrong threshold selection. For AND, θ must equal number of inputs.",
                "prerequisites": ["Activation Functions"],
                "module": "Module 1",
                "exam_importance": 4,
                "pyq_frequency": "80%",
                "marks_pattern": "Part B - 8 marks",
                "time_to_learn": "6 min"
            },
            {
                "name": "Hebb Learning Rule",
                "plain_name": "Neurons That Fire Together Wire Together",
                "difficulty": "intermediate",
                "explanation": "Learning rule: Δw = η × x × t. Strengthens connections between simultaneously active neurons. Works best with bipolar data [-1,+1]. Algorithm: Initialize weights to 0, update for each pattern, test with final weights.",
                "example": "Pattern I (target=+1): w_new = w_old + (x × 1). Pattern O (target=-1): w_new = w_old + (x × -1).",
                "common_mistake": "Using binary [0,1] instead of bipolar [-1,+1] - gives poor learning.",
                "prerequisites": ["Biological vs Artificial Neuron"],
                "module": "Module 1",
                "exam_importance": 4,
                "pyq_frequency": "70%",
                "marks_pattern": "Part B - 8 marks",
                "time_to_learn": "7 min"
            },
            {
                "name": "Linear Separability and XOR Problem",
                "plain_name": "Why Single Layer Can't Solve XOR",
                "difficulty": "intermediate",
                "explanation": "Linear separability: Can you draw ONE line to separate two classes? Simple networks only solve linearly separable problems. XOR is NOT linearly separable - points are on opposite diagonals, no single line works.",
                "example": "AND is separable (line works). XOR isn't - (0,0) and (1,1) need same side as do (0,1) and (1,0), but they're on opposite corners.",
                "common_mistake": "Trying to solve XOR with single-layer perceptron - mathematically impossible.",
                "prerequisites": ["McCulloch-Pitts Neuron"],
                "module": "Module 1",
                "exam_importance": 3,
                "pyq_frequency": "60%",
                "marks_pattern": "Part B - 6 marks",
                "time_to_learn": "5 min"
            }
        ]
    },
    "Module 2: Perceptron and Backpropagation": {
        "concepts": [
            {
                "name": "Perceptron Training Algorithm",
                "plain_name": "How Perceptron Learns",
                "difficulty": "intermediate",
                "explanation": "Supervised learning algorithm for binary classification. Updates weights when prediction is wrong: w_new = w_old + α(t-y)x. Continues until all patterns classified correctly or max epochs reached.",
                "example": "If target=1 but output=0, increase weights. If target=0 but output=1, decrease weights.",
                "common_mistake": "Not checking convergence - perceptron only converges for linearly separable data.",
                "prerequisites": ["Activation Functions", "Linear Separability and XOR Problem"],
                "module": "Module 2",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part B - 14 marks",
                "time_to_learn": "8 min"
            },
            {
                "name": "Adaline and Delta Rule",
                "plain_name": "Adaptive Linear Neuron",
                "difficulty": "intermediate",
                "explanation": "Uses continuous activation (linear) and minimizes mean squared error. Delta rule: Δw = α(t-y)x where y is continuous. More stable than perceptron. Learns optimal weights through gradient descent.",
                "example": "For regression: predict continuous values. Updates based on error magnitude, not just sign.",
                "common_mistake": "Confusing with perceptron - Adaline uses continuous output, perceptron uses binary.",
                "prerequisites": ["Perceptron Training Algorithm"],
                "module": "Module 2",
                "exam_importance": 4,
                "pyq_frequency": "70%",
                "marks_pattern": "Part B - 8 marks",
                "time_to_learn": "8 min"
            },
            {
                "name": "Backpropagation Network Architecture",
                "plain_name": "Multi-Layer Neural Network",
                "difficulty": "advanced",
                "explanation": "Multi-layer network with input, hidden, and output layers. Uses sigmoid activation. Learns through backpropagation: forward pass computes output, backward pass updates weights using gradient descent. Can solve non-linear problems like XOR.",
                "example": "XOR solution: 2 inputs → 2 hidden neurons → 1 output. Hidden layer creates non-linear decision boundary.",
                "common_mistake": "Not normalizing inputs [0,1] for sigmoid - causes slow learning.",
                "prerequisites": ["Perceptron Training Algorithm", "Linear Separability and XOR Problem"],
                "module": "Module 2",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part B - 14 marks",
                "time_to_learn": "8 min"
            },
            {
                "name": "BPN Training Stages",
                "plain_name": "Forward and Backward Pass",
                "difficulty": "advanced",
                "explanation": "Two stages: (1) Forward: Input → Hidden → Output, compute error. (2) Backward: Output error → Hidden error → Update weights. Uses chain rule for gradient calculation. Learning rate α controls update size.",
                "example": "Forward: x → h=σ(w1x) → y=σ(w2h). Backward: δ_out=(t-y)y(1-y), δ_hid=δ_out·w2·h(1-h).",
                "common_mistake": "Forgetting derivative term y(1-y) in sigmoid gradient - causes wrong updates.",
                "prerequisites": ["Backpropagation Network Architecture"],
                "module": "Module 2",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part B - 14 marks",
                "time_to_learn": "10 min"
            }
        ]
    },
    "Module 3: Fuzzy Logic": {
        "concepts": [
            {
                "name": "Fuzzy Sets and Membership Functions",
                "plain_name": "Partial Truth Values",
                "difficulty": "beginner",
                "explanation": "Unlike crisp sets (0 or 1), fuzzy sets allow partial membership [0,1]. Membership function μ(x) gives degree of belonging. Common shapes: triangular, trapezoidal, Gaussian. Handles uncertainty and vagueness.",
                "example": "Temperature: Cold (0-20°C), Warm (15-30°C), Hot (25-40°C). 22°C is 0.3 Cold, 0.7 Warm.",
                "common_mistake": "Thinking membership must sum to 1 - it doesn't! Each set is independent.",
                "prerequisites": [],
                "module": "Module 3",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part A - 3 marks + plotting",
                "time_to_learn": "6 min"
            },
            {
                "name": "Fuzzy Set Operations",
                "plain_name": "AND, OR, NOT for Fuzzy Sets",
                "difficulty": "intermediate",
                "explanation": "Union (OR): max(μA, μB). Intersection (AND): min(μA, μB). Complement (NOT): 1-μA. Also algebraic: AND=μA×μB, OR=μA+μB-μA×μB. Bounded: AND=max(0,μA+μB-1), OR=min(1,μA+μB).",
                "example": "A={0.7}, B={0.4}. Union=max(0.7,0.4)=0.7. Intersection=min(0.7,0.4)=0.4. Complement of A=1-0.7=0.3.",
                "common_mistake": "Using wrong operation - standard uses min/max, algebraic uses multiply/add.",
                "prerequisites": ["Fuzzy Sets and Membership Functions"],
                "module": "Module 3",
                "exam_importance": 4,
                "pyq_frequency": "70%",
                "marks_pattern": "Part B - 6 marks",
                "time_to_learn": "6 min"
            },
            {
                "name": "Defuzzification Methods",
                "plain_name": "Converting Fuzzy to Crisp Output",
                "difficulty": "intermediate",
                "explanation": "Converts fuzzy output to single crisp value. Methods: (1) Centroid: weighted average of area. (2) Bisector: divides area in half. (3) MOM: mean of maximum. (4) LOM/SOM: leftmost/smallest of maximum.",
                "example": "Centroid: x* = Σ(x·μ(x)) / Σμ(x). Most common method, gives balanced output.",
                "common_mistake": "Not calculating area correctly - must integrate membership function.",
                "prerequisites": ["Fuzzy Sets and Membership Functions"],
                "module": "Module 3",
                "exam_importance": 5,
                "pyq_frequency": "100%",
                "marks_pattern": "Part B - 8 marks",
                "time_to_learn": "7 min"
            },
            {
                "name": "Fuzzy Relations and Composition",
                "plain_name": "Relationships Between Fuzzy Sets",
                "difficulty": "advanced",
                "explanation": "Fuzzy relation R: A×B → [0,1]. Composition combines relations: R∘S. Max-min: μ(x,z)=max_y[min(μR(x,y), μS(y,z))]. Max-product: μ(x,z)=max_y[μR(x,y)×μS(y,z)].",
                "example": "If 'tall' relates to 'heavy' and 'heavy' relates to 'strong', compose to get 'tall' relates to 'strong'.",
                "common_mistake": "Confusing max-min with max-product - check which composition rule to use.",
                "prerequisites": ["Fuzzy Set Operations"],
                "module": "Module 3",
                "exam_importance": 3,
                "pyq_frequency": "60%",
                "marks_pattern": "Part B - 8 marks",
                "time_to_learn": "8 min"
            }
        ]
    },
    "Module 4: Genetic Algorithms and FIS": {
        "concepts": [
            {
                "name": "Fuzzy Inference System (Mamdani)",
                "plain_name": "Fuzzy If-Then Rules",
                "difficulty": "intermediate",
                "explanation": "Rule-based system: IF (condition) THEN (action). Steps: (1) Fuzzification: crisp→fuzzy. (2) Rule evaluation: apply AND/OR. (3) Aggregation: combine rules. (4) Defuzzification: fuzzy→crisp.",
                "example": "IF temp is Hot AND humidity is High THEN fan speed is Fast. Evaluate membership, apply rules, defuzzify to get actual speed.",
                "common_mistake": "Skipping aggregation step - must combine all fired rules before defuzzification.",
                "prerequisites": ["Fuzzy Sets and Membership Functions", "Defuzzification Methods"],
                "module": "Module 4",
                "exam_importance": 3,
                "pyq_frequency": "60%",
                "marks_pattern": "Part B - 8 marks",
                "time_to_learn": "5 min"
            },
            {
                "name": "Genetic Algorithm Basics",
                "plain_name": "Evolution-Based Optimization",
                "difficulty": "intermediate",
                "explanation": "Mimics natural selection. Population of solutions evolves through: (1) Selection: choose fittest. (2) Crossover: combine parents. (3) Mutation: random changes. Fitness function guides evolution. Encoding: binary, real-valued, permutation.",
                "example": "Optimize f(x)=x². Population: [2,5,7,3]. Fitness: [4,25,49,9]. Select 5,7. Crossover→[5.5,6.5]. Mutate→[5.3,6.7].",
                "common_mistake": "Too high mutation rate destroys good solutions. Keep it low (1-5%).",
                "prerequisites": [],
                "module": "Module 4",
                "exam_importance": 2,
                "pyq_frequency": "50%",
                "marks_pattern": "Part B - 6 marks",
                "time_to_learn": "4 min"
            }
        ]
    },
    "Module 5: Hybrid Systems": {
        "concepts": [
            {
                "name": "Neuro-Fuzzy Hybrid Systems",
                "plain_name": "Combining Neural Networks and Fuzzy Logic",
                "difficulty": "advanced",
                "explanation": "Combines learning ability of ANN with interpretability of fuzzy logic. ANFIS (Adaptive Neuro-Fuzzy Inference System): neural network structure implements fuzzy inference. Learns membership functions and rules from data.",
                "example": "Fuzzy rules define structure, backpropagation tunes membership parameters. Best of both worlds.",
                "common_mistake": "Thinking it's just ANN or just fuzzy - it's a true hybrid with both capabilities.",
                "prerequisites": ["Backpropagation Network Architecture", "Fuzzy Inference System (Mamdani)"],
                "module": "Module 5",
                "exam_importance": 2,
                "pyq_frequency": "50%",
                "marks_pattern": "Part B - 6 marks",
                "time_to_learn": "4 min"
            },
            {
                "name": "Multi-Objective Optimization",
                "plain_name": "Optimizing Multiple Goals",
                "difficulty": "advanced",
                "explanation": "Optimize multiple conflicting objectives simultaneously. Pareto optimal: can't improve one objective without worsening another. MOOP finds Pareto front - set of non-dominated solutions. Trade-off between objectives.",
                "example": "Car design: maximize speed, minimize cost. Pareto front shows speed-cost trade-offs.",
                "common_mistake": "Looking for single 'best' solution - MOOP gives set of optimal trade-offs.",
                "prerequisites": ["Genetic Algorithm Basics"],
                "module": "Module 5",
                "exam_importance": 2,
                "pyq_frequency": "40%",
                "marks_pattern": "Part B - 4 marks",
                "time_to_learn": "3 min"
            }
        ]
    }
}


async def ingest_soft_computing(db: Session):
    """Ingest Soft Computing subject with module-wise concepts"""
    
    print("🚀 Starting Soft Computing ingestion...")
    
    # Create or get subject
    subject = db.query(Subject).filter(Subject.name == "Soft Computing").first()
    if not subject:
        subject = Subject(
            name="Soft Computing",
            description="Neural Networks, Fuzzy Logic, and Genetic Algorithms for VTU exam preparation"
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)
        print(f"✅ Created subject: {subject.name}")
    else:
        print(f"📚 Subject exists: {subject.name}")
    
    # Extract and create concepts module-wise
    total_concepts = 0
    for module_name, module_data in SC_MODULES.items():
        print(f"\n📖 Processing {module_name}...")
        
        for concept_data in module_data["concepts"]:
            # Check if concept exists
            existing = db.query(Concept).filter(
                Concept.subject_id == subject.id,
                Concept.name == concept_data["name"]
            ).first()
            
            if existing:
                print(f"  ⏭️  Skipping existing: {concept_data['plain_name']}")
                continue
            
            # Create concept
            concept = Concept(
                subject_id=subject.id,
                name=concept_data["name"],
                plain_name=concept_data["plain_name"],
                difficulty=concept_data["difficulty"],
                explanation=concept_data["explanation"],
                example=concept_data["example"],
                common_mistake=concept_data["common_mistake"],
                prerequisites=concept_data["prerequisites"],
                metadata={
                    "module": concept_data["module"],
                    "exam_importance": concept_data["exam_importance"],
                    "pyq_frequency": concept_data["pyq_frequency"],
                    "marks_pattern": concept_data["marks_pattern"],
                    "time_to_learn": concept_data["time_to_learn"]
                }
            )
            db.add(concept)
            total_concepts += 1
            print(f"  ✅ Created: {concept_data['plain_name']} ({concept_data['difficulty']})")
        
        db.commit()
    
    print(f"\n🎉 Ingestion complete! Created {total_concepts} concepts across 5 modules")
    print(f"📊 Subject: {subject.name} (ID: {subject.id})")
    
    return subject


async def main():
    """Main ingestion function"""
    db = SessionLocal()
    try:
        subject = await ingest_soft_computing(db)
        
        # Print summary
        concept_count = db.query(Concept).filter(Concept.subject_id == subject.id).count()
        print(f"\n📈 Final Stats:")
        print(f"   Subject: {subject.name}")
        print(f"   Total Concepts: {concept_count}")
        print(f"   Modules: 5 (M1-M5)")
        print(f"\n✨ Ready for teaching! Start the frontend to explore concepts.")
        
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
