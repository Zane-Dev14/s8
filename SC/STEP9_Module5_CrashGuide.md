# STEP 9: MODULE 5 CRASH GUIDE (From Zero to Exam-Ready)

## Module 5 Topics: Multi Objective Optimization + Hybrid Systems

This guide is mapped to:
- SC source-note OCR: SC/build/M5_pdf_source.txt
- PYQ OCR: SC/QP/ocr_output/CST444_SOFT_COMPUTING,_JUNE_2023.txt and SC/QP/ocr_output/CST444_SOFT_COMPUTING,_MAY_2024.txt

---

## TOPIC 1: MULTI OBJECTIVE OPTIMIZATION PROBLEM (MOOP)

### What is it? (1 line)
MOOP optimizes two or more objective functions at the same time.

### Why is it used?
Real systems usually have conflicting goals, e.g., minimize cost and maximize quality.

### Key Idea (Intuition)
There is often no single best solution for all objectives together.
You look for good trade-off solutions.

### Standard Mathematical Form

Minimize/Maximize:
- f1(x), f2(x), ..., fm(x)

Subject to:
- gj(x) <= 0 for inequality constraints
- hk(x) = 0 for equality constraints

Where:
- x = decision vector
- feasible set = all x satisfying constraints

### Core Terms (MEMORIZE)
1. Decision vector x
2. Objective vector f(x)
3. Decision space X
4. Objective space Y
5. Feasible region

### Perfect Exam Answer (3 marks - 6 points)
1. MOOP contains multiple objective functions
2. Objectives may conflict with one another
3. So a single global best point is usually unavailable
4. Solutions are evaluated in objective space as vectors
5. Constraints define feasible search region
6. Final output is typically a set of trade-off optimal solutions

### Memory Trick
MOOP = Many Objectives, One Pareto set

---

## TOPIC 2: LINEAR/NONLINEAR + CONVEX/NON-CONVEX MOOP

### A) Linear vs Nonlinear MOOP

- Linear MOOP: all objective and constraint functions linear
- Nonlinear MOOP: at least one objective or constraint nonlinear

### B) Convex vs Non-convex MOOP

- Convex MOOP: objective functions and feasible region are convex
- Non-convex MOOP: convexity conditions fail in some region

### Convexity Condition (Write this)
For 0 < lambda < 1:

f(lambda*x + (1-lambda)*y) <= lambda*f(x) + (1-lambda)*f(y)

If strict inequality (<) holds, function is strictly convex.

### Important Property
For convex objective, local minimum is also global minimum.

### Perfect Exam Answer (6-7 marks)
1. MOOP may be linear or nonlinear by model expressions
2. If all terms are linear, it is linear MOOP
3. If any objective/constraint is nonlinear, it is nonlinear MOOP
4. Convex MOOP satisfies convexity inequality conditions
5. In convex cases, local optimum equals global optimum
6. Non-convex MOOP may have many local minima
7. Non-convex search is generally harder computationally
8. Most practical problems are nonlinear and frequently non-convex

### Memory Trick
L-N = Line shape of equations
C-NC = Curve shape of optimization landscape

---

## TOPIC 3: DOMINANCE RELATION

### What is dominance? (1 line)
Solution A dominates B if A is no worse in all objectives and better in at least one.

### Dominance Test
A dominates B if:
1. For every objective i, fi(A) <= fi(B) (for minimization case)
2. For at least one objective j, fj(A) < fj(B)

(Reverse inequalities for maximization objectives.)

### Properties of Dominance Relation (Source-aligned)
1. Not reflexive
2. Not symmetric
3. Not antisymmetric (in strict dominance sense used in notes)
4. Transitive

### Perfect Exam Answer (3-7 marks)
1. Dominance compares quality of multi-objective solutions
2. One solution must be no worse in every objective
3. It must be strictly better in at least one objective
4. Dominance forms basis of Pareto ranking
5. Strict dominance relation is not reflexive
6. It is not symmetric
7. It is transitive and useful for front construction

### Memory Trick
N-N-N-T = Not reflexive, Not symmetric, Not antisymmetric, Transitive

---

## TOPIC 4: PARETO OPTIMALITY + NON-DOMINATED SET

### What is Pareto-optimality? (1 line)
A solution is Pareto-optimal if no other feasible solution dominates it.

### Core Definitions (Must write)
- Non-dominated set in P: solutions not dominated by any member of P
- Pareto-optimal set: non-dominated set of full feasible space
- Pareto front: image of Pareto-optimal set in objective space

### Visual Intuition
On Pareto front:
- improving one objective worsens at least one other objective.

### Diagram to Draw

```text
f2 (min)
^
|     x  dominated points
|   x
| x
|-------------------  <- Pareto front (non-dominated)
|         o   o   o
+-------------------------> f1 (min)
```

### Perfect Exam Answer (6 marks)
1. Pareto-optimal solutions are non-dominated feasible solutions
2. No single solution is best in all conflicting objectives
3. Non-dominated set is defined within selected candidate set P
4. Pareto-optimal set is obtained when P is full feasible space
5. Pareto front is the boundary in objective space
6. Movement along front is trade-off movement
7. Dominated points lie behind the front
8. Good algorithms move solutions toward front and maintain diversity

### Memory Trick
Pareto front = Best compromise boundary

---

## TOPIC 5: PROCEDURE TO FIND NON-DOMINATED SET (WORKED STEP-BY-STEP)

### Generic Algorithm (Exam method)
1. List all candidate solutions with objective values
2. Pick one solution A
3. Compare A with every other solution using dominance test
4. Mark solutions dominated by others
5. Repeat for all solutions
6. Remove all dominated solutions
7. Remaining set is non-dominated set

### Worked Example (Air-ticket style from source-note OCR)
Assume objective: minimize time and minimize cost

Given:
- A(2,7.5), B(3,6), C(3,7.5), D(4,5), E(4,6.5), F(5,4.5), G(5,6), H(5,7), I(6,6.5)

Step 1: Compare A with others
- A dominates C (better or equal in both, strict in one)
- A does not dominate B, D, F due to trade-off

Step 2: Compare B
- B dominates C, E, G, H, I

Step 3: Compare D
- D dominates E, G, H, I

Step 4: Compare F
- F dominates G, H, I

Step 5: Remove dominated solutions
Dominated: C, E, G, H, I

Step 6: Non-dominated set
- {A, B, D, F}

Step 7: Conclusion
- {A, B, D, F} forms Pareto-optimal / non-dominated front for this candidate set.

### Perfect Exam Answer (6 marks - 10 points)
1. Construct objective-value table first
2. Apply pairwise dominance test systematically
3. Mark dominated solutions clearly
4. Keep solutions that no one dominates
5. Report non-dominated set explicitly
6. Draw front in objective plane if asked
7. Mention trade-off among front points
8. Distinguish candidate non-dominated vs global Pareto-optimal
9. State whether objectives are minimization/maximization
10. Conclude with final set and front statement

---

## TOPIC 6: GENETIC-NEURO HYBRID SYSTEM

### What is it? (1 line)
A hybrid where GA optimizes ANN parameters like weights, topology, and learning settings.

### Why is it used?
ANN can model complex patterns; GA can perform global search of good ANN configurations.

### Block Diagram to Draw

```text
Initial Population -> Selection/Crossover/Mutation -> New Child Population -> ANN Evaluation
                      ^                                                     |
                      |                                                     v
                      +--------------------- Fitness Calculation <-----------+
```

### Working Flow (Exam order)
1. Initialize GA population of candidate ANN parameters
2. Evaluate candidates through ANN performance
3. Select good parent candidates
4. Perform crossover and mutation
5. Send new candidate set to ANN
6. Compute fitness (e.g., inverse MSE)
7. Repeat until target performance or stop criterion

### Advantages (Source-aligned)
1. Optimizes ANN topology
2. Optimizes connection weights
3. Tunes learning-rate and momentum parameters
4. Helps avoid poor local search behavior
5. Useful in complex pattern tasks

### Disadvantages
1. High computational complexity
2. Strong dependence on initial population quality
3. Higher maintenance/tuning cost

### Perfect Exam Answer (8 marks - 14 points)
1. Genetic-neuro system combines GA and neural network strengths
2. GA provides search and optimization capability
3. ANN provides learning and nonlinear mapping capability
4. Candidate ANN settings are encoded as chromosomes
5. Selection chooses better parameter candidates
6. Crossover recombines ANN parameter structures
7. Mutation preserves diversity in parameter search
8. ANN evaluates each candidate and returns performance metric
9. Fitness metric guides next GA generation
10. Process iterates to improve ANN design quality
11. GA can tune hidden layers, nodes, and interconnections
12. GA can tune learning hyperparameters
13. Hybrid improves solution quality in complex search spaces
14. Conclusion: GA-guided ANN training/design gives robust optimization-driven intelligence

---

## TOPIC 7: NEURO-FUZZY HYBRID SYSTEM

### What is it? (1 line)
A fuzzy system trained/adapted using neural learning principles.

### Why is it used?
To combine fuzzy interpretability with neural adaptability.

### Structure (Source-aligned)
1. Input layer
2. Fuzzification layer
3. Rule/hidden layer
4. Output aggregation/defuzzification layer

### Working Flow
1. Crisp input enters system
2. Fuzzification neurons compute membership grades
3. Rule layer evaluates fuzzy rules
4. Output neuron aggregates rule outputs (often union/aggregation)
5. Defuzzification produces crisp output
6. Learning updates local parameters in fuzzy structure

### Characteristics (PYQ keywords)
1. Handles numeric + linguistic information
2. Manages imprecise/partial/vague information
3. Supports self-learning and self-tuning
4. Supports conflict resolution by aggregation
5. Mimics human-like reasoning behavior

### Classifications (exam-safe mention)
- Cooperative neuro-fuzzy
- Concurrent neuro-fuzzy
- Fully fused/integrated neuro-fuzzy

### Perfect Exam Answer (8 marks - 14 points)
1. Neuro-fuzzy combines fuzzy logic with neural adaptation
2. It is often modeled as layered feedforward architecture
3. Input layer passes crisp external values
4. Fuzzification maps inputs to membership values
5. Rule layer encodes fuzzy IF-THEN logic
6. Aggregation and defuzzification produce final output
7. Learning modifies local fuzzy parameters
8. This preserves interpretability while improving adaptability
9. It handles uncertain and imprecise data efficiently
10. It supports numeric and linguistic reasoning together
11. Cooperative, concurrent, and fused forms are common classifications
12. It is widely used in control and prediction tasks
13. Limitations include model-design complexity and parameter tuning difficulty
14. Conclusion: neuro-fuzzy gives explainable + trainable intelligent decision systems

---

## TOPIC 8: OPTIMALITY CONDITIONS (SHORT NOTE FOR SAFETY)

If asked in brief:
- Mention Fritz-John necessary condition
- Mention KKT sufficient condition for Pareto-optimality context
- Keep answer concise unless explicitly asked mathematically

Quick point format:
1. Optimality conditions provide mathematical checks for Pareto candidates
2. FJ gives necessary condition
3. KKT provides sufficient condition under suitable regularity assumptions
4. Used in analytical treatment of constrained MOOPs

---

## NUMERICAL/WORKED TEMPLATES (MODULE 5)

### Template 1: Dominance Check
1. Write objective direction (min/min or max/max)
2. Compare candidate pair objective-wise
3. Check no-worse-all + better-one condition
4. Record dominates/dominated/non-comparable

### Template 2: Non-dominated Set
1. Build pairwise dominance table
2. Mark all dominated points
3. Remaining points = non-dominated set
4. Draw approximate Pareto front

### Template 3: Convexity Statement
1. Write convex inequality
2. Substitute symbolic points x,y and lambda
3. State whether condition holds globally

---

## QUICK REVISION CHECKLIST

Can you answer these in 30 seconds?
- What is MOOP?
- Difference between linear and nonlinear MOOP?
- Convexity condition statement?
- Define dominance.
- Define Pareto-optimal set and Pareto front.
- Name two hybrid systems.

Can you solve in 3 minutes?
- Find dominance relation for a given pair
- Build non-dominated set from 6-8 points
- Explain one hybrid system with block flow

Can you draw in 1 minute?
- Pareto front sketch
- Genetic-neuro block diagram
- Neuro-fuzzy layered structure

---

## EXAM STRATEGY FOR MODULE 5

Part A (3 marks):
- Write 6 keyword points, not long paragraphs
- Always include one definition line first

Part B (14 marks):
- Use 14-point structure for 14 marks
- For dominance/non-dominated questions: show explicit pairwise logic
- For hybrid questions: add block diagram + flow + pros/cons

Scoring Tips:
1. Always state objective direction before dominance checks
2. Use words non-dominated, Pareto front, trade-off explicitly
3. In hybrid answers, mention both structure and working flow
4. End with one conclusion line connected to application value

---

## PYQ MAP FOR MODULE 5 (OCR VERIFIED)

From June 2023 and May 2024 OCR:
- Convex vs non-convex MOOP
- Non-dominated set procedure
- Dominance and properties of dominance
- Pareto optimality
- Genetic-neuro hybrid systems (detail + block diagram)
- Neuro-fuzzy hybrid classification/characteristics

This crash guide is tuned exactly for those asks.

---

MODULE 5 COMPLETE. Next: Full SC PYQ solved master file.
