# STEP 8: MODULE 4 CRASH GUIDE (From Zero to Exam-Ready)

## Module 4 Topics: Fuzzy Inference System + Genetic Algorithms

This guide is mapped to:
- SC source-note OCR: SC/build/M4_pdf_source.txt
- PYQ OCR: SC/QP/ocr_output/CST444_SOFT_COMPUTING,_JUNE_2023.txt and SC/QP/ocr_output/CST444_SOFT_COMPUTING,_MAY_2024.txt

---

## TOPIC 1: FUZZY INFERENCE SYSTEM (FIS)

### What is it? (1 line)
A Fuzzy Inference System is a rule-based system that converts inputs into decisions using fuzzy IF-THEN logic.

### Why is it used?
Real inputs are often vague (hot, medium, low). FIS converts such linguistic information into actionable output.

### Key Idea (Intuition)
Think of a teacher using rules:
- IF attendance is low AND test score is low THEN risk is high.

That is exactly FIS logic.

### Core FIS Blocks (MEMORIZE)
1. Fuzzifier
2. Rule base
3. Database/knowledge base
4. Inference engine (decision-making unit)
5. Defuzzifier

### Block Diagram to Draw in Exam

```text
Crisp Input -> Fuzzifier -> Inference Engine + Rule Base -> Defuzzifier -> Crisp Output
```

Expanded:

```text
Input x ----> [Fuzzifier] ----> [Rule Evaluation + Inference] ----> [Defuzzifier] ----> y
                    ^                      ^
                    |                      |
               Membership DB          IF-THEN Rule Base
```

### FIS Working Steps (Write in order)
1. Convert crisp input to fuzzy values (fuzzification)
2. Compute rule strengths
3. Apply AND/OR operators as required
4. Obtain each rule consequent
5. Aggregate all rule outputs
6. Defuzzify to a single crisp output

### Perfect Exam Answer (3 marks - 6 points)
1. FIS is a fuzzy rule-based input-output mapping framework
2. It uses linguistic variables and IF-THEN rules
3. Fuzzifier maps crisp inputs to fuzzy membership values
4. Inference engine evaluates and combines active rules
5. Rule base stores expert knowledge
6. Defuzzifier converts final fuzzy output to crisp value

### Memory Trick
F-R-I-D = Fuzzify, Rules, Infer, Defuzzify

---

## TOPIC 2: MAMDANI VS SUGENO FIS

### What is it? (1 line)
Two popular FIS models that differ mainly in rule consequent and output computation.

### Why is it asked often?
This is a direct PYQ long-answer favorite in Module 4.

### Key Difference (Core)
- Mamdani: consequent is a fuzzy set
- Sugeno: consequent is a function/constant

### Comparison Table (Draw This)

| Feature | Mamdani | Sugeno |
|---|---|---|
| Rule consequent | Fuzzy set | Linear/constant function |
| Output type before final step | Fuzzy | Crisp from rule equation |
| Defuzzification | Mandatory | Often weighted average style |
| Interpretability | Very intuitive | More mathematical |
| Computational cost | Higher | Lower |
| Optimization/tuning | Harder | Easier |

### Mamdani Procedure (Exam Flow)
1. Fuzzify input variables
2. Find rule firing strengths
3. Clip/scale output membership functions
4. Aggregate all rule outputs
5. Defuzzify final fuzzy output

### Sugeno Procedure (Exam Flow)
1. Fuzzify inputs
2. Compute rule firing strengths
3. Compute each rule output by function/constant
4. Take weighted average of rule outputs

### Example Rule Pair
- Mamdani: IF temperature is high THEN fan speed is fast
- Sugeno: IF temperature is high THEN fan_speed = 0.5*temperature + 10

### Perfect Exam Answer (8 marks - 14 points)
1. Mamdani and Sugeno are two major FIS models
2. Both use fuzzy antecedents in IF-THEN rules
3. Mamdani uses fuzzy membership functions in consequents
4. Sugeno uses linear/constant consequent equations
5. Mamdani requires output aggregation over fuzzy sets
6. Mamdani then performs explicit defuzzification
7. Sugeno computes weighted crisp output from firing strengths
8. Mamdani is preferred for interpretability and expert-rule clarity
9. Sugeno is preferred for computational efficiency
10. Sugeno is suitable for adaptive optimization tasks
11. Mamdani has strong human-expert acceptance
12. Both models share fuzzification and rule evaluation front-end
13. Difference lies in consequent representation and output stage
14. Conclusion: model choice depends on interpretability vs efficiency needs

### Memory Trick
Mamdani = More intuitive, Sugeno = Speed + simple output math

---

## TOPIC 3: FLC DESIGN STEPS (VERY IMPORTANT)

### What is it? (1 line)
Structured method to build a fuzzy logic controller from variables, rules, and defuzzification.

### 9 Design Steps (Source-Aligned)
1. Identify input, output, and state variables
2. Partition universe of discourse into fuzzy subsets
3. Define membership functions for subsets
4. Build fuzzy input-output rule base
5. Set normalization/scaling factors
6. Perform fuzzification
7. Perform inference to get rule outputs
8. Combine fuzzy outputs (aggregation)
9. Perform defuzzification for crisp output

### Perfect Exam Answer (5 marks - 10 points)
1. FLC design starts with variable identification
2. Universe is divided into linguistic subsets
3. Membership functions are assigned to each subset
4. Rule base captures expert control knowledge
5. Scaling factors normalize variables
6. Fuzzifier converts crisp to fuzzy
7. Inference engine applies fuzzy reasoning
8. Aggregation combines all fired rule outputs
9. Defuzzifier generates final crisp control signal
10. Final controller quality depends on rule and MF quality

### Common Mistakes to Avoid
- Writing blocks but not the sequence
- Forgetting scaling/normalization
- Skipping aggregation before defuzzification

---

## TOPIC 4: GENETIC ALGORITHM (GA) FLOW

### What is it? (1 line)
A population-based optimization method inspired by natural evolution.

### Why is it used?
To search large solution spaces where exact methods are difficult.

### Key Idea (Intuition)
- Better solutions survive
- Good traits combine (crossover)
- Random variation (mutation) avoids stagnation

### GA Flowchart (Draw This)

```text
Initialize Population -> Fitness Evaluation -> Selection -> Crossover -> Mutation -> New Population -> Stop?
                                                                                           |
                                                                                           No
                                                                                           v
                                                                                     Repeat cycle
```

### Standard GA Steps (Answer-ready)
1. Encode candidate solutions as chromosomes
2. Generate initial population
3. Evaluate fitness of each chromosome
4. Select parent chromosomes
5. Apply crossover to create offspring
6. Apply mutation to offspring
7. Form next generation
8. Check stopping condition

### Perfect Exam Answer (3 marks - 6 points)
1. GA starts with encoded random population
2. Fitness function scores each chromosome
3. Selection picks fitter parents for reproduction
4. Crossover combines parent genes into offspring
5. Mutation introduces random diversity
6. Process repeats until stopping criterion is satisfied

### Memory Trick
I-F-S-C-M-N-S = Initialize, Fitness, Selection, Crossover, Mutation, New-gen, Stop

---

## TOPIC 5: SELECTION TECHNIQUES IN GA

### Most Asked Selection Operators
1. Roulette Wheel Selection
2. Rank Selection
3. Tournament Selection
4. Boltzmann Selection
5. Stochastic Universal Sampling (SUS)

### Quick Intuition
- Roulette: probability proportional to fitness
- Rank: uses position/rank instead of raw fitness
- Tournament: best among random mini-group wins

### Exam-ready 3 Techniques (for 6 marks)

#### 1. Roulette Wheel Selection
- Probability of selection proportional to fitness
- Better individuals get larger wheel segment
- Easy but can over-favor very high fitness individuals

#### 2. Rank Selection
- Individuals sorted by fitness rank
- Selection based on rank, not raw fitness
- Prevents domination by one extreme individual

#### 3. Tournament Selection
- Randomly pick k individuals
- Select the best among k
- Good balance of simplicity and control

### Worked Mini Numerical (Roulette)
Given fitness values: [2, 6, 3, 1]

Step 1: Total fitness = 2 + 6 + 3 + 1 = 12

Step 2: Probability of each chromosome:
- P1 = 2/12 = 0.1667
- P2 = 6/12 = 0.5000
- P3 = 3/12 = 0.2500
- P4 = 1/12 = 0.0833

Step 3: Convert to percentage:
- 16.67%, 50%, 25%, 8.33%

### Perfect Exam Answer (6 marks - 10 points)
1. Selection chooses parents for the next generation
2. Roulette-wheel uses fitness-proportional chance
3. Rank selection assigns chance by sorted rank
4. Tournament picks best from random subgroup
5. Selection pressure affects convergence speed
6. Very strong pressure may reduce diversity
7. Very weak pressure slows convergence
8. Selection itself does not create new genes
9. Crossover and mutation generate diversity
10. Proper selection improves GA performance stability

---

## TOPIC 6: CROSSOVER TECHNIQUES (MODULE 4 HOTSPOT)

### What is crossover?
Combining parent chromosomes to produce child chromosomes.

### PYQ-Focused Methods
1. Single-point crossover
2. Two-point crossover
3. Uniform crossover
4. Three-parent crossover
5. Shuffle crossover
6. Precedence preservative crossover (PPX)

### ASCII Mini Examples

#### Uniform crossover
Parent A: 1 1 0 0 1 0 1 0
Parent B: 0 0 1 1 0 1 0 1
Mask    : 1 0 1 0 1 0 1 0
Child   : 1 0 0 1 1 1 1 1

#### Three-parent crossover (idea)
- Start with Parent1 and Parent2
- Use Parent3 as tie-break/reference for disputed bits

#### Shuffle crossover
1. Shuffle bit positions randomly
2. Perform crossover
3. Unshuffle back to original order

#### PPX (for schedules/permutations)
- Preserves precedence/order constraints
- Used in scheduling and sequencing problems

### Perfect Exam Answer (8 marks - 14 points)
1. Crossover is a recombination operator in GA
2. It exchanges genetic material among selected parents
3. Single-point uses one split location
4. Two-point uses two split locations and exchanges middle block
5. Uniform chooses gene source independently per position
6. Three-parent crossover uses three sources for offspring construction
7. Shuffle crossover removes positional bias before recombination
8. PPX preserves ordering constraints in permutation problems
9. Crossover type depends on chromosome representation
10. Binary/value encoding can use standard point-based methods
11. Permutation problems require order-preserving crossovers
12. Crossover increases exploration in search space
13. Mutation complements crossover to avoid premature convergence
14. Conclusion: choose crossover based on encoding + feasibility constraints

---

## TOPIC 7: ENCODING SCHEMES IN GA

### Encoding Types (Must memorize)
1. Binary encoding
2. Real/value encoding
3. Permutation encoding
4. Tree encoding

### Simple Explanation
- Binary: bits (0/1)
- Real/value: floating values directly
- Permutation: ordered sequence (e.g., city order)
- Tree: expression/program structures

### Quick Example Table

| Type | Example chromosome | Typical use |
|---|---|---|
| Binary | 10110100 | combinational search |
| Real/Value | [2.3, -0.7, 5.1] | continuous optimization |
| Permutation | [3,1,4,2,5] | routing/scheduling |
| Tree | (+ x (* y 2)) | symbolic/program search |

### Perfect Exam Answer (6 marks - 10 points)
1. Encoding maps candidate solution to chromosome format
2. Binary encoding uses 0/1 gene strings
3. Value encoding stores real/continuous values directly
4. Permutation encoding stores ordered unique symbols
5. Tree encoding stores hierarchical expressions
6. Encoding choice depends on problem nature
7. Wrong encoding can create invalid offspring
8. Operator design must match encoding type
9. Permutation requires order-safe crossover/mutation
10. Conclusion: representation quality strongly affects GA efficiency

---

## TOPIC 8: MUTATION TECHNIQUES + STOPPING CONDITIONS

### Common Mutation Techniques
1. Bit-flip mutation (binary)
2. Swap/interchange mutation
3. Reverse mutation (segment reversal)

### Mutation Example
Parent: 10100110
Bit-flip at position 4 -> 10110110

### GA Stopping Conditions (PYQ)
1. Maximum generations reached
2. Maximum time reached
3. Target fitness reached
4. No improvement for many generations
5. Population diversity collapse/stagnation

### Perfect Exam Answer (3 marks - 6 points)
1. Mutation introduces random genetic change
2. It restores lost gene diversity in population
3. Bit-flip changes selected bits in binary chromosomes
4. Swap mutation exchanges two gene positions
5. Reverse mutation flips sequence in selected segment
6. GA stops on generation/time/fitness/stagnation criteria

---

## NUMERICAL/WORKED TEMPLATES (MODULE 4)

### Template 1: Roulette Selection
1. Write fitness list
2. Compute total fitness
3. Compute Pi = fi/sum(fi)
4. Build cumulative range table
5. Map random numbers to selected parents

### Template 2: Single/Two-point Crossover
1. Write parent chromosomes
2. Mark cut point(s)
3. Exchange required segment(s)
4. Write children clearly

### Template 3: Mutation
1. Write parent chromosome
2. Mark mutation position/segment
3. Apply rule (flip/swap/reverse)
4. Write final chromosome

---

## QUICK REVISION CHECKLIST

Can you answer in 30 seconds?
- What are 5 FIS blocks?
- Main difference between Mamdani and Sugeno?
- Why selection is needed in GA?
- Difference between uniform and two-point crossover?
- One use-case each for binary and permutation encoding?
- Name 3 stopping criteria.

Can you draw in 1 minute?
- FIS block diagram
- GA flowchart
- Single-point crossover sketch

---

## EXAM STRATEGY FOR MODULE 4

Part A (3 marks):
- Write 6 short points
- Use keyword-heavy definitions
- For GA: mention operator order (selection -> crossover -> mutation)

Part B (14 marks):
- 8-mark part: give definition + diagram + 10+ points
- 6-mark part: give 3 techniques with short examples
- Always add one concluding line

Scoring Tips:
1. In FIS answers, write block names in exact sequence
2. In crossover answers, add one mini chromosome example
3. In encoding answers, include use-case per encoding
4. In GA stopping answer, include both convergence and practical limits

---

## PYQ MAP FOR MODULE 4 (OCR VERIFIED)

From June 2023 and May 2024 OCR:
- FIS definition and Mamdani/Sugeno explanation
- Crossover methods (uniform, three-parent, shuffle, PPX)
- Selection techniques
- Encoding schemes
- Mutation techniques
- GA flow and stopping conditions

This crash guide is optimized exactly for those asks.

---

MODULE 4 COMPLETE. Next: STEP 9 Module 5 Crash Guide.
