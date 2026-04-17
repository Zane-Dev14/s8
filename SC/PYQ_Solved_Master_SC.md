# SOFT COMPUTING PYQ SOLVED MASTER (ALL MODULES, OCR-MAPPED)

This file is the complete solved PYQ master for SC.

Mapped sources used:
- PYQ OCR:
  - SC/QP/ocr_output/CST444_SOFT_COMPUTING,_JUNE_2023.txt
  - SC/QP/ocr_output/CST444_SOFT_COMPUTING,_MAY_2024.txt
  - SC/QP/ocr_output/DC+SC.txt
- Source-note OCR:
  - SC/build/M1_pdf_source.txt
  - SC/build/M2_pdf_source.txt
  - SC/build/M3_pdf_source.txt
  - SC/build/M4_pdf_source.txt
  - SC/build/M5_pdf_source.txt

Goal of this master:
- If question is asked, answer is directly usable in exam
- If diagram is asked, a draw-ready sketch is included
- If numerical is asked, every step is shown

---

## HOW TO USE THIS FILE FAST

1. Part A prep (3 marks): use the 6-point compact answers.
2. Part B prep (14 marks): use the 14-point long answers.
3. Numericals: copy the table format exactly.
4. Before exam: revise only the "High-Frequency Set" in each module.

---

## MODULE 1 SOLVED PYQ SET

### M1-Q1: Role of activation function + any two activation functions (Part A)

Answer (3 marks, 6 points):
1. Activation function converts neuron net input into output response.
2. It controls whether neuron should fire strongly, weakly, or not.
3. Nonlinearity from activation lets ANN learn complex patterns.
4. Binary sigmoid: f(x)=1/(1+e^(-x)), output range [0,1].
5. Bipolar sigmoid: f(x)=(e^x-e^(-x))/(e^x+e^(-x)), output range [-1,1].
6. Linear activation is simple but weak for complex classification.

---

### M1-Q2: Biological neuron vs artificial neuron (Part A)

Answer (3 marks, 6 points):
1. Biological neuron has dendrite, soma, axon, synapse.
2. Artificial neuron has inputs, weights, summation, activation, output.
3. Dendrite corresponds to ANN input reception stage.
4. Synapse strength corresponds to connection weights.
5. Soma processing corresponds to weighted summation.
6. Firing threshold corresponds to activation decision.

Draw this:

```text
Biological:  Dendrites -> Soma -> Axon -> Synapse
Artificial:  Inputs -> [SUM] -> [Activation] -> Output
```

---

### M1-Q3: Draw simple artificial neuron + net input calculation (Part A)

Friendly exam answer:

```text
x1 --w1--\
       > [ SUM ] --> [ f(.) ] --> y
x2 --w2--/
      + b
```

Step-by-step explanation:
1. Read the input values x1 and x2.
2. Multiply each input by its weight:
  - contribution 1 = w1*x1
  - contribution 2 = w2*x2
3. Add both contributions and then add bias b.
4. This gives net input Yin:
  - Yin = w1*x1 + w2*x2 + b
5. Apply activation function f(.) on Yin to get output y:
  - y = f(Yin)

Quick mini-example (for understanding):
- Let x1=1, x2=0, w1=0.5, w2=-0.2, b=0.1
- Yin = (0.5*1) + (-0.2*0) + 0.1 = 0.6
- Output = f(0.6)

Scoring points (write any 6):
1. Inputs carry feature values.
2. Weights control influence of each input.
3. Bias shifts threshold.
4. SUM block computes Yin.
5. Activation block maps Yin to final output.
6. Output y is the neuron response.

---

### M1-Q4: MP neuron implementation of AND/ANDNOT (Part B)

#### (A) AND using MP neuron
Truth table:

```text
x1 x2 | y
0  0  | 0
0  1  | 0
1  0  | 0
1  1  | 1
```

Choose parameters:
- w1=1, w2=1, threshold theta=2

Formula used:
- Yin = w1*x1 + w2*x2
- y = 1 if Yin >= theta, else 0

Row-wise check (do this in exam table):

| x1 | x2 | Yin | Condition vs theta=2 | y |
|---:|---:|---:|---|---:|
| 0 | 0 | 0 | 0 < 2 | 0 |
| 0 | 1 | 1 | 1 < 2 | 0 |
| 1 | 0 | 1 | 1 < 2 | 0 |
| 1 | 1 | 2 | 2 >= 2 | 1 |

So the neuron behaves exactly like AND.

#### (B) ANDNOT: x1 AND NOT x2
Truth table:

```text
x1 x2 | y
0  0  | 0
0  1  | 0
1  0  | 1
1  1  | 0
```

Choose parameters:
- w1=+1 (excitatory), w2=-1 (inhibitory), theta=1

Formula used:
- Yin = (1*x1) + (-1*x2)
- y = 1 if Yin >= 1, else 0

Row-wise check:

| x1 | x2 | Yin | Condition vs theta=1 | y |
|---:|---:|---:|---|---:|
| 0 | 0 | 0 | 0 < 1 | 0 |
| 0 | 1 | -1 | -1 < 1 | 0 |
| 1 | 0 | 1 | 1 >= 1 | 1 |
| 1 | 1 | 0 | 0 < 1 | 0 |

So only (1,0) gives output 1, which matches ANDNOT.

Architecture to draw:

```text
x1 --(+1)--\
            > [SUM] -> [Yin >= 1 ?] -> y
x2 --(-1)--/
```

Easy 14-point long-answer structure:
1. MP neuron uses binary inputs/outputs.
2. It uses threshold firing logic.
3. Weights may be excitatory or inhibitory.
4. Write truth table first.
5. Select candidate weights.
6. Select threshold.
7. Compute Yin for each row.
8. Compare with threshold.
9. Assign output per row.
10. Verify all 4 rows exactly.
11. For ANDNOT use inhibitory second input.
12. Show that only (1,0) fires.
13. Draw architecture and label theta.
14. Conclude correctness against truth table.

---

### M1-Q5: Hebb rule classification of I/O pattern + testing (Part B)

This is the same question many students fear, but it is very mechanical.
Do it in this order and it becomes easy.

Given bipolar patterns:
- I = [1,1,1,-1,1,-1,1,1,1], target t=+1
- O = [1,1,1,1,-1,1,1,1,1], target t=-1

Step 0: Initialize
- w = [0,0,0,0,0,0,0,0,0]
- b = 0

Step 1: Write Hebb update formulas
- Delta wi = xi*t
- wi(new) = wi(old) + Delta wi
- b(new) = b(old) + t

Step 2: Train with pattern I (t=+1)
- Delta w = I * (+1) = [1,1,1,-1,1,-1,1,1,1]
- New w = old w + Delta w = [1,1,1,-1,1,-1,1,1,1]
- New b = 0 + 1 = 1

Step 3: Train with pattern O (t=-1)
- Delta w = O * (-1) = [-1,-1,-1,-1,1,-1,-1,-1,-1]
- Final w = [1,1,1,-1,1,-1,1,1,1] + [-1,-1,-1,-1,1,-1,-1,-1,-1]
- Final w = [0,0,0,-2,2,-2,0,0,0]
- Final b = 1 + (-1) = 0

Step 4: Test pattern I
- Formula: Yin = sum(wi*xi) + b
- Only non-zero weights are at positions 4,5,6
- Yin = (-2*-1) + (2*1) + (-2*-1) + 0
- Yin = 2 + 2 + 2 = 6
- Since Yin > 0, predicted class = +1, so I is correctly classified

Step 5: Test pattern O
- Yin = (-2*1) + (2*-1) + (-2*1) + 0
- Yin = -2 -2 -2 = -6
- Since Yin < 0, predicted class = -1, so O is correctly classified

Final conclusion:
- Hebb learning successfully separates I and O for this dataset.

---

### M1-Q6: Activation numerical (binary + bipolar sigmoid)

Given:
- x1=0.7, x2=0.8
- w1=0.2, w2=0.3
- bias b=0.9

Step 1: Compute net input Yin
- Formula: Yin = (w1*x1) + (w2*x2) + b
- Substitute: Yin = (0.2*0.7) + (0.3*0.8) + 0.9
- Compute products: 0.14 and 0.24
- Add all: Yin = 0.14 + 0.24 + 0.9 = 1.28

Step 2: Binary sigmoid output
- Formula: y = 1 / (1 + e^(-Yin))
- Substitute Yin=1.28:
  y = 1 / (1 + e^(-1.28))
- Use approximation e^(-1.28) approximately 0.278
- y = 1 / (1 + 0.278) = 1 / 1.278 approximately 0.782

Step 3: Bipolar sigmoid output
- Formula: y = (e^(Yin)-e^(-Yin)) / (e^(Yin)+e^(-Yin))
- Substitute Yin=1.28:
  y = (e^(1.28)-e^(-1.28)) / (e^(1.28)+e^(-1.28))
- Final numeric value approximately 0.856

Final answers:
- Binary sigmoid output approximately 0.782
- Bipolar sigmoid output approximately 0.856

Exam tip:
- Always show Yin first. Without Yin step, you lose method marks.

---

### M1-Q7: Linear separability + XOR non-separability

Answer points:
1. Linearly separable means one line separates two classes in 2D.
2. Perceptron/single-layer linear models need separability.
3. AND is linearly separable.
4. XOR points lie on opposite diagonals.
5. No single line separates XOR classes correctly.
6. Hence XOR is non-linearly separable.
7. Single-layer perceptron fails on XOR.
8. Multilayer network (BPN) solves XOR.

Draw this:

```text
XOR plot:
x2
1 |  1    0
0 |  0    1
  +----------- x1
    0    1
```

---

## MODULE 2 SOLVED PYQ SET

### M2-Q1: Perceptron training algorithm (Part A)

Answer (3 marks):
1. Initialize weights, bias, and learning rate.
2. Present one pattern at a time.
3. Compute net input Yin and output y.
4. Compare y with target t.
5. If error exists, update weights and bias.
6. Repeat over epochs until stop condition.

Update rule:
- wi(new)=wi(old)+eta*(t-y)*xi
- b(new)=b(old)+eta*(t-y)

---

### M2-Q2: Perceptron testing algorithm (Part A)

Answer:
1. Use trained weights and bias from training phase.
2. Apply each test input.
3. Compute Yin and output class.
4. Compare with expected class.
5. Count correct predictions.
6. Report accuracy/decision.

Important:
- No weight update during testing.

---

### M2-Q3: BPN architecture and stages (Part A/Part B)

Three stages:
1. Feed-forward computation
2. Error backpropagation
3. Weight and bias updation

Architecture sketch:

```text
Input Layer -> Hidden Layer -> Output Layer
    x_i          h_j            o_k

Forward: x -> h -> o
Backward: error from o -> h
```

Long-answer points:
1. BPN is multilayer feedforward network.
2. Uses differentiable activation.
3. Computes output by forward pass.
4. Output error is computed from target mismatch.
5. Hidden error inferred from output errors.
6. Weight corrections propagate backward.
7. Updates repeated across all training patterns.
8. Epochs continue until stopping criterion.

---

### M2-Q4: Adaline architecture + delta rule

Answer:
1. Adaline is single-layer adaptive linear neuron.
2. Learning uses net input Yin (before hard decision output).
3. Error term is delta = t - Yin.
4. Weight update: wi(new)=wi(old)+eta*delta*xi.
5. Bias update: b(new)=b(old)+eta*delta.
6. Objective is minimizing MSE.

---

### M2-Q5: Perceptron OR implementation (2 epochs style)

Given (one common exam setup):
- Inputs binary, targets bipolar
- OR targets: (0,0)->-1, (0,1)->+1, (1,0)->+1, (1,1)->+1
- eta=1, initial w1=0,w2=0,b=0

Use activation:
- y=+1 if Yin>=0, else -1

Update formulas:
- e = t - y
- w1(new)=w1(old)+eta*e*x1
- w2(new)=w2(old)+eta*e*x2
- b(new)=b(old)+eta*e

Epoch 1:

| Pattern | x1 | x2 | t | Yin | y | e=t-y | w1 | w2 | b |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | -1 | 0 | +1 | -2 | 0 | 0 | -2 |
| 2 | 0 | 1 | +1 | -2 | -1 | +2 | 0 | 2 | 0 |
| 3 | 1 | 0 | +1 | 0 | +1 | 0 | 0 | 2 | 0 |
| 4 | 1 | 1 | +1 | 2 | +1 | 0 | 0 | 2 | 0 |

How the first two updates happened (write this in exam if space permits):
- Pattern 1: e=-2, but x1=x2=0, so weights stay same; only bias changes to -2.
- Pattern 2: e=+2, x2=1, so w2 increases by 2; bias returns to 0.

Epoch 2:
- Re-test with w1=0, w2=2, b=0
- All four patterns now classify correctly for OR under this sign rule
- So training can stop

---

### M2-Q6: Adaline one epoch for AND (given w1=0.2, w2=0.1, eta=0.2)

Targets (bipolar):
- (0,0)->-1
- (0,1)->-1
- (1,0)->-1
- (1,1)->+1

Initial:
- w1=0.2, w2=0.1, b=0

Rule:
- Yin = w1*x1 + w2*x2 + b
- delta = t - Yin
- w1(new) = w1(old) + eta*delta*x1
- w2(new) = w2(old) + eta*delta*x2
- b(new) = b(old) + eta*delta

Epoch 1 step-by-step:

| Pattern | x1 | x2 | t | Yin | delta=t-Yin | w1(new) | w2(new) | b(new) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | -1 | 0.0000 | -1.0000 | 0.2000 | 0.1000 | -0.2000 |
| 2 | 0 | 1 | -1 | -0.1000 | -0.9000 | 0.2000 | -0.0800 | -0.3800 |
| 3 | 1 | 0 | -1 | -0.1800 | -0.8200 | 0.0360 | -0.0800 | -0.5440 |
| 4 | 1 | 1 | +1 | -0.5880 | +1.5880 | 0.3536 | 0.2376 | -0.2264 |

One detailed row calculation (Pattern 4):
- Yin = (0.036*1) + (-0.08*1) + (-0.544) = -0.588
- delta = 1 - (-0.588) = 1.588
- w1(new) = 0.036 + 0.2*1.588*1 = 0.3536
- w2(new) = -0.08 + 0.2*1.588*1 = 0.2376
- b(new) = -0.544 + 0.2*1.588 = -0.2264

End of one epoch:
- w1=0.3536, w2=0.2376, b=-0.2264

---

## MODULE 3 SOLVED PYQ SET

### M3-Q1: Plot fuzzy membership for age of people

Answer points:
1. Define universe U=[0,100] years.
2. Use overlapping labels: very young, young, middle, old, very old.
3. Use triangular/trapezoidal membership functions.
4. Keep smooth overlap between neighboring sets.
5. Label axes clearly: x-axis age, y-axis membership.
6. Peaks are strongest membership points.

Sketch:

```text
mu
1.0 |  /\    /\    /\    /\    /\
    | /  \  /  \  /  \  /  \  /  \
0.0 +----------------------------------> age
      VY   Y    M    O    VO
```

---

### M3-Q2: Core, support, boundary

Answer:
1. Core(A)={x | muA(x)=1}
2. Support(A)={x | muA(x)>0}
3. Boundary(A)={x | 0<muA(x)<1}
4. Core gives full membership region.
5. Support gives all potentially belonging elements.
6. Boundary captures gradual transition zone.

---

### M3-Q3: Union, intersection, complement of fuzzy sets

Given:
- A={(x1,0.5),(x2,0.1),(x3,0.9)}
- B={(x1,0.4),(x2,0.4),(x3,0.5)}

Step 1: Write formulas
- Union: mu(A union B)=max(muA,muB)
- Intersection: mu(A intersection B)=min(muA,muB)
- Complement: mu(A')=1-muA

Step 2: Solve element by element

| Element | muA | muB | Union max(muA,muB) | Intersection min(muA,muB) | A' = 1-muA | B' = 1-muB |
|---|---:|---:|---:|---:|---:|---:|
| x1 | 0.5 | 0.4 | 0.5 | 0.4 | 0.5 | 0.6 |
| x2 | 0.1 | 0.4 | 0.4 | 0.1 | 0.9 | 0.6 |
| x3 | 0.9 | 0.5 | 0.9 | 0.5 | 0.1 | 0.5 |

Step 3: Write final sets
- A union B = {(x1,0.5),(x2,0.4),(x3,0.9)}
- A intersection B = {(x1,0.4),(x2,0.1),(x3,0.5)}
- A' = {(x1,0.5),(x2,0.9),(x3,0.1)}
- B' = {(x1,0.6),(x2,0.6),(x3,0.5)}

---

### M3-Q4: Algebraic sum/product, bounded sum/difference (full worked)

Given:
- A = 1/1 + 0.5/2 + 0.3/3 + 0.2/4
- B = 0.5/1 + 0.7/2 + 0.2/3 + 0.4/4

Formulas:
- Alg Sum = a+b-ab
- Alg Prod = ab
- Bounded Sum = min(1,a+b)
- Bounded Diff = max(0,a-b)

Step-by-step calculations:
- Element 1 (a=1.0, b=0.5):
  - Alg Sum = 1.0+0.5-(1.0*0.5) = 1.0
  - Alg Prod = 1.0*0.5 = 0.5
  - Bounded Sum = min(1,1.5)=1.0
  - Bounded Diff = max(0,1.0-0.5)=0.5

- Element 2 (a=0.5, b=0.7):
  - Alg Sum = 0.5+0.7-(0.5*0.7)=0.85
  - Alg Prod = 0.5*0.7=0.35
  - Bounded Sum = min(1,1.2)=1.0
  - Bounded Diff = max(0,-0.2)=0.0

- Element 3 (a=0.3, b=0.2):
  - Alg Sum = 0.3+0.2-(0.3*0.2)=0.44
  - Alg Prod = 0.3*0.2=0.06
  - Bounded Sum = min(1,0.5)=0.5
  - Bounded Diff = max(0,0.1)=0.1

- Element 4 (a=0.2, b=0.4):
  - Alg Sum = 0.2+0.4-(0.2*0.4)=0.52
  - Alg Prod = 0.2*0.4=0.08
  - Bounded Sum = min(1,0.6)=0.6
  - Bounded Diff = max(0,-0.2)=0.0

Final summary table:

| Element | a | b | Alg Sum | Alg Prod | Bounded Sum | Bounded Diff |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1.0 | 0.5 | 1.00 | 0.50 | 1.0 | 0.5 |
| 2 | 0.5 | 0.7 | 0.85 | 0.35 | 1.0 | 0.0 |
| 3 | 0.3 | 0.2 | 0.44 | 0.06 | 0.5 | 0.1 |
| 4 | 0.2 | 0.4 | 0.52 | 0.08 | 0.6 | 0.0 |

---

### M3-Q5: Defuzzification methods (long-answer)

Define:
- Defuzzification converts fuzzy output into one crisp value.

Methods:
1. Max-membership method
2. Centroid method
3. Weighted average method
4. Center of sums
5. First of maxima

Weighted average example:
- Given points (mu,z): (0.2,40), (0.5,60), (0.3,80)
- Formula: z* = sum(mu_i*z_i) / sum(mu_i)
- Numerator = (0.2*40) + (0.5*60) + (0.3*80)
- Numerator = 8 + 30 + 24 = 62
- Denominator = 0.2 + 0.5 + 0.3 = 1.0
- Final crisp value: z* = 62/1.0 = 62

Center of sums example:
- Given (Ai,ci): (10,20), (15,40), (8,60)
- Formula: z* = sum(Ai*ci) / sum(Ai)
- Numerator = (10*20) + (15*40) + (8*60)
- Numerator = 200 + 600 + 480 = 1280
- Denominator = 10 + 15 + 8 = 33
- Final crisp value: z* = 1280/33 approximately 38.8

Encouragement tip:
- In exam, always write numerator and denominator separately.
- Even if arithmetic slips, method marks are safe.

14-point answer skeleton:
1. Define defuzzification.
2. Explain why fuzzy output needs crisp conversion.
3. Describe max-membership.
4. Describe centroid formula.
5. Describe weighted average formula.
6. Describe center of sums.
7. Mention first-of-maxima for multi-peak cases.
8. Show one worked numeric example.
9. Mention trade-off between accuracy and complexity.
10. State centroid is most common.
11. Mention weighted average for singleton outputs.
12. Mention max-membership is fast but less informative.
13. Mention method choice depends on control need.
14. Conclude with final crisp-value interpretation.

---

### M3-Q6: Alpha-cut operations for a fuzzy relation (A=0.9 and 0+)

Given relation matrix R (from PYQ OCR):

```text
[1.0 0.8 0.0 0.1 0.2]
[0.8 1.0 0.4 0.0 0.9]
[0.0 0.4 1.0 0.0 0.0]
[0.1 0.0 0.0 1.0 0.5]
[0.2 0.9 0.0 0.5 1.0]
```

Rule:
- R_alpha keeps entries >= alpha

Step-by-step method:
1. Pick alpha value.
2. Scan matrix entry by entry.
3. Write 1 where condition is true, else write 0.
4. Build final binary alpha-cut matrix.

For alpha=0.9:
- Keep entries 1.0 and 0.9
- Positions: (1,1),(2,2),(3,3),(4,4),(5,5),(2,5),(5,2)

Binary alpha-cut matrix:

```text
[1 0 0 0 0]
[0 1 0 0 1]
[0 0 1 0 0]
[0 0 0 1 0]
[0 1 0 0 1]
```

For alpha=0+:
- Keep all positive entries (>0)

Binary matrix:

```text
[1 1 0 1 1]
[1 1 1 0 1]
[0 1 1 0 0]
[1 0 0 1 1]
[1 1 0 1 1]
```

Final check:
- Alpha=0.9 gives a stricter (sparser) matrix.
- Alpha=0+ gives a broader matrix because all positive memberships are retained.

---

## MODULE 4 SOLVED PYQ SET

### M4-Q1: What is FIS? Illustrate Mamdani and Sugeno with examples

Answer:
1. FIS is a fuzzy rule-based decision mapping system.
2. Core components: fuzzifier, rule base, knowledge base, inference engine, defuzzifier.
3. Mamdani uses fuzzy set consequents.
4. Sugeno uses constant/linear function consequents.
5. Mamdani output aggregation is fuzzy and needs defuzzification.
6. Sugeno often yields weighted crisp output more directly.
7. Mamdani is more interpretable.
8. Sugeno is more computationally efficient.

Draw:

```text
Crisp input -> Fuzzifier -> Rule Inference -> Defuzzifier -> Crisp output
```

Example rules:
- Mamdani: IF dirt is high THEN wash_time is long
- Sugeno: IF dirt is high THEN wash_time = 10 + 2*dirt

---

### M4-Q2: Explain any three selection techniques in GA

Answer:
1. Roulette-wheel: parent probability proportional to fitness.
2. Rank selection: select based on sorted rank, not raw values.
3. Tournament selection: best from random subset is chosen.
4. Selection pressure controls convergence speed.
5. Too high pressure reduces diversity.
6. Balanced selection improves robustness.

---

### M4-Q3: Explain crossover methods (uniform, 3-parent, shuffle, PPX)

#### Uniform crossover
- Use random mask; each child bit chosen from parent A/B by mask.

#### Three-parent crossover
- Three parents contribute; third parent helps resolve conflicts.

#### Shuffle crossover
1. Randomly shuffle gene order
2. Perform crossover
3. Unshuffle to original order

#### PPX (precedence preservative crossover)
- Used in permutation/scheduling tasks
- Preserves relative precedence constraints

Scoring points:
1. Crossover recombines parent genes.
2. Method depends on encoding type.
3. Uniform is position-wise independent.
4. Three-parent expands search combinations.
5. Shuffle reduces positional bias.
6. PPX preserves feasible order in sequencing problems.

---

### M4-Q4: Explain encoding schemes in GA

Answer:
1. Binary encoding: chromosomes as bit strings.
2. Value/real encoding: chromosomes as real numbers.
3. Permutation encoding: ordered sequences without duplication.
4. Tree encoding: expression/tree structures.
5. Operator selection must match encoding.
6. Wrong encoding may produce invalid offspring.

---

### M4-Q5: Explain mutation techniques + stopping conditions

Mutation techniques:
1. Bit-flip mutation
2. Swap/interchange mutation
3. Reverse mutation

Stopping conditions:
1. Max generations reached
2. Max time reached
3. Target fitness reached
4. No improvement over many generations
5. Diversity collapse/stagnation

---

## MODULE 5 SOLVED PYQ SET

### M5-Q1: Explain convex and non-convex MOOP. How to find non-dominated set?

Part 1 (convex vs non-convex):
1. Convex MOOP satisfies convexity in objectives/feasible region.
2. Convex inequality: f(lambda x + (1-lambda)y) <= lambda f(x) + (1-lambda)f(y).
3. For convex objectives, local minimum is global minimum.
4. Non-convex MOOP does not satisfy convexity globally.
5. Non-convex problems may have many local minima.

Part 2 (non-dominated set procedure):
1. List all candidate points with objective values.
2. Apply pairwise dominance test.
3. Mark dominated points.
4. Remaining points are non-dominated set.
5. In full feasible space this is Pareto-optimal set.

---

### M5-Q2: Explain dominance and properties of dominance relation

Answer:
1. A dominates B if A is no worse in all objectives and better in at least one.
2. Dominance is key for Pareto-based ranking.
3. Strict dominance is not reflexive.
4. Strict dominance is not symmetric.
5. Strict dominance is not antisymmetric (as treated in module notes).
6. Dominance relation is transitive.
7. Dominance supports non-dominated front construction.

---

### M5-Q3: Explain Pareto optimality

Answer:
1. Pareto-optimal solutions are not dominated by any feasible solution.
2. Set of all such solutions is Pareto-optimal set.
3. Curve/surface in objective space is Pareto front.
4. On front, improving one objective worsens another objective.
5. Dominated points are inferior to at least one front point.
6. Goal of MOOP algorithm: reach and spread along Pareto front.

---

### M5-Q4: Explain Genetic-Neuro hybrid system with block diagram

Block:

```text
GA population -> selection/crossover/mutation -> ANN evaluation -> fitness -> next generation
```

Detailed answer:
1. GA encodes ANN parameters into chromosomes.
2. Initial population creates multiple ANN candidate settings.
3. ANN evaluates candidate quality (error/fitness).
4. Selection chooses promising candidates.
5. Crossover recombines candidate settings.
6. Mutation introduces random exploration.
7. New generation is re-evaluated by ANN.
8. Process continues till stopping condition.
9. GA can tune ANN topology, weights, and hyperparameters.
10. Hybrid improves global search quality.
11. Handles complex non-convex optimization better than local search alone.
12. Drawback: computational complexity and setup cost.

---

### M5-Q5: Classifications/characteristics of neuro-fuzzy hybrid systems

Classification (exam-safe):
1. Cooperative neuro-fuzzy
2. Concurrent neuro-fuzzy
3. Fully fused/integrated neuro-fuzzy

Characteristics:
1. Combines fuzzy interpretability + neural adaptability
2. Handles numeric and linguistic information
3. Works with uncertain/imprecise inputs
4. Supports self-learning and self-tuning
5. Provides rule-based explainability with adaptive parameter updates

Typical layered view:

```text
Input -> Fuzzification -> Rule Layer -> Aggregation/Defuzzification -> Output
```

---

## HIGH-FREQUENCY SET (LAST DAY REVISION)

Module 1:
- Biological vs artificial neuron
- Activation role and types
- MP AND/ANDNOT
- Hebb I/O classification
- XOR non-separability

Module 2:
- Perceptron training/testing
- Adaline delta rule
- Adaline epoch numerical
- BPN architecture and 3 stages

Module 3:
- Membership plot (Age/Liquid level)
- Core/support/boundary
- Fuzzy operations numerical
- Defuzzification methods + weighted average
- Alpha-cut relation

Module 4:
- FIS blocks + Mamdani vs Sugeno
- Selection methods
- Crossover methods
- Encoding schemes
- Mutation + stopping criteria

Module 5:
- Linear/nonlinear, convex/non-convex MOOP
- Dominance properties
- Pareto optimality + non-dominated set
- Genetic-neuro hybrid
- Neuro-fuzzy classification/characteristics

---

## EXAM WRITING FORMULA (FOR ALL PART B QUESTIONS)

Use this sequence every time:
1. Definition
2. Formula/rule
3. Diagram
4. Step-by-step method
5. Worked example/table
6. Final conclusion line

If you follow this order, answers look complete and score consistently.
