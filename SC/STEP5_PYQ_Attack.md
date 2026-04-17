# 🎯 STEP 5: PYQ ATTACK MODE - Grouped Questions with Perfect Answers

## 📊 QUESTION PATTERN ANALYSIS

Based on May 2024, June 2023, and previous papers analysis.

## ✅ NEW COMPLETION UPDATE (SC FULL)

To keep this file focused on pattern attack, the fully detailed solved content is now split as:

- [STEP8_Module4_CrashGuide.md](STEP8_Module4_CrashGuide.md)
- [STEP9_Module5_CrashGuide.md](STEP9_Module5_CrashGuide.md)
- [PYQ_Solved_Master_SC.md](PYQ_Solved_Master_SC.md) (all modules, solved, with step-by-step numericals and diagram-ready answers)

---

## 🔥 MODULE 1: MOST REPEATED QUESTIONS

### **Q1. Soft Computing vs Hard Computing (100% frequency)**

**Appears in:** May 2024, June 2023, Dec 2021, Every paper

**Perfect Answer (3 marks - 6 points):**

1. Soft computing handles imprecision and uncertainty
2. Hard computing requires precise formulation
3. Soft computing targets robustness and low solution cost
4. Hard computing gives precise guaranteed output
5. Soft computing is adaptive and human-mind inspired
6. ANN, fuzzy logic, GA are soft-computing techniques

**Keywords to include:** Lotfi Zadeh, tolerance, tractability, human mind

---

### **Q2. Biological vs Artificial Neuron (100% frequency)**

**Appears in:** May 2024, June 2023, Every paper

**Perfect Answer (3 marks - 6 points):**

1. Biological neuron has soma, dendrites, axon, synapse
2. ANN neuron is a simplified processing unit
3. Dendritic reception maps to ANN input stage
4. Synaptic behavior maps to ANN weighted connections
5. Biological firing is threshold dependent
6. ANN output is activation-function dependent

**Diagram to draw:**
```
Biological: Dendrites → Soma → Axon → Synapse
Artificial: Inputs → Weights → Σ → Activation → Output
```

---

### **Q3. Activation Functions (100% frequency)**

**Appears in:** May 2024, June 2023, Dec 2021

**Perfect Answer (3 marks - 6 points):**

1. Activation is applied over net input to produce output
2. It decides whether neuron response should be active
3. Linear activation has limited expressive ability
4. Nonlinear functions support complex mapping
5. Binary sigmoid outputs lie between 0 and 1
6. Bipolar sigmoid outputs lie between -1 and 1

**Must mention:** Binary sigmoid [0,1], Bipolar sigmoid [-1,1]

---

### **Q4. Draw Artificial Neuron & Net Input (80% frequency)**

**Appears in:** June 2023, Model papers

**Perfect Answer (3 marks - 6 points):**

1. Inputs are connected through weighted links
2. Yin is treated as net input
3. Output Y is obtained after activation operation
4. Weights represent signal strength
5. Bias affects Yin magnitude and direction
6. Net-input calculation is central to ANN response

**Diagram:**
```
x₁ ──w₁──┐
         ├──→ [Σ] → [f] → y
x₂ ──w₂──┘    ↑
             bias
Formula: Yin = Σ(wi×xi) + bias
```

---

### **Q5. MP Neuron - AND/ANDNOT Implementation (80% frequency)**

**Appears in:** May 2024 (ANDNOT), June 2023 (ANDNOT), Model papers (AND)

**Perfect Answer for ANDNOT (8 marks - 14 points):**

1. MP neuron uses binary input and threshold output
2. Links can be excitatory or inhibitory
3. Build two-input binary ANDNOT truth table
4. Compute summed input per row
5. Compare each sum with fixed threshold
6. If threshold is satisfied, neuron fires
7. Otherwise output remains zero
8. Input-1 supports the AND term (weight = +1)
9. Input-2 supports NOT behavior via inhibition (weight = -1)
10. Verify four input cases one by one
11. Exactly one case (1,0) should produce output 1
12. Remaining three cases produce output 0
13. This matches ANDNOT functional definition
14. Conclusion: MP threshold architecture realizes ANDNOT directly

**Truth Table & Design:**
```
x₁  x₂  | Output
0   0   |   0
0   1   |   0
1   0   |   1  ← Only this
1   1   |   0

Weights: w₁=1, w₂=-1, θ=1
```

---

### **Q6. Hebb Rule & Pattern Classification (70% frequency)**

**Appears in:** May 2024 (I vs O), June 2023 (I vs O)

**Perfect Answer (8 marks - 14 points):**

1. Convert symbols to bipolar values (+ as 1, blank as -1)
2. Assign targets: I as +1 and O as -1
3. Initialize all weights and bias to zero
4. Present first pattern and apply Hebb update: Δw = x × t
5. Carry updated weights into next pattern
6. Continue until all patterns are presented
7. Maintain bipolar consistency through entire process
8. Use final learned weights for testing stage
9. Test pattern I: Yin = Σ(wi×xi) + b
10. Check if Yin > 0 → Class +1 (correct for I)
11. Test pattern O: Yin = Σ(wi×xi) + b
12. Check if Yin < 0 → Class -1 (correct for O)
13. Report classification correctness
14. Conclusion: Hebb network performs class separation for I/O patterns

**Pattern representation:**
```
I: + + +     →  [1, 1, 1, -1, 1, -1, 1, 1, 1]  Target: +1
     +
   + + +

O: + + +     →  [1, 1, 1, 1, -1, 1, 1, 1, 1]  Target: -1
   +   +
   + + +
```

---

### **Q7. Linear Separability & XOR (60% frequency)**

**Appears in:** May 2024, June 2023

**Perfect Answer (6 marks - 14 points for full question):**

1. Linear separability means one line separates two classes in 2D
2. Class points occupy opposite half-spaces
3. Single-layer classifier depends on such separability
4. AND-like class setting is separable in standard 2D view
5. Hebb logic examples work for separable cases
6. XOR is classic non-separable pattern
7. XOR class points are diagonally distributed
8. No single line can split XOR classes correctly
9. Therefore single linear boundary is insufficient for XOR
10. XOR cannot be separated by one line (key phrase!)
11. This explains failure of simple linear classification
12. More complex partitioning is required for XOR
13. Multi-layer networks (BPN) can solve XOR
14. Conclusion: separability criterion explains both AND success and XOR failure

**XOR Plot:**
```
x₂
1 |  1    0
  |
0 |  0    1
  |_______
    0     1  x₁
    
Opposite diagonals - no single line works!
```

---

### **Q8. Activation Function Numerical (60% frequency)**

**Appears in:** May 2024, June 2023

**Perfect Answer (6 marks):**

**Given:** Network with inputs, weights, bias

**Solution Steps:**
1. Calculate net input: Yin = Σ(wi×xi) + bias
2. For binary sigmoid: y = 1/(1+e^(-Yin)), range [0,1]
3. For bipolar sigmoid: y = (e^Yin - e^(-Yin))/(e^Yin + e^(-Yin)), range [-1,1]
4. Substitute Yin value
5. Calculate both outputs
6. Compare ranges and behavior

**Example:**
```
Given: x₁=0.7, x₂=0.8, w₁=0.2, w₂=0.3, bias=0.9

Yin = (0.7×0.2) + (0.8×0.3) + 0.9
    = 0.14 + 0.24 + 0.9
    = 1.28

Binary sigmoid: y ≈ 0.78
Bipolar sigmoid: y ≈ 0.86
```

---

## 🔥 MODULE 2: MOST REPEATED QUESTIONS

### **Q9. Perceptron Training Algorithm (100% frequency)**

**Appears in:** May 2024, June 2023, Every paper

**Perfect Answer (3 marks - 6 points):**

1. Initialize weights, bias, and learning rate
2. Present one training pattern at a time
3. Compute net input and output using activation rule
4. Compare calculated output with target output
5. If error occurs, adjust trainable weights: w = w + η(t-y)x
6. Repeat pattern loop across epochs until stop condition

**Keywords:** epoch, learning rate, error correction, convergence

---

### **Q10. Perceptron Testing Algorithm (80% frequency)**

**Appears in:** June 2023, Model papers

**Perfect Answer (3 marks - 6 points):**

1. Testing evaluates trained network performance
2. Use weights obtained from training phase
3. Apply each test input to the network
4. Compute net input and corresponding output class
5. Compare predicted class with expected class
6. Report classification result or accuracy

**Key point:** No weight updates during testing!

---

### **Q11. BPN Architecture & Stages (100% frequency)**

**Appears in:** May 2024, June 2023, Every paper

**Perfect Answer (3 marks - 6 points for stages):**

1. Feed-forward of training input
2. Calculation of output error
3. Back-propagation of error to hidden layer
4. Weight updation based on propagated error
5. Repeat for all patterns
6. Continue epochs until stopping criterion

**For full architecture (8 marks - 14 points):**

1. BPN is a multilayer feedforward network
2. It contains input, hidden, and output layers
3. Hidden and output layers include bias terms
4. Training objective is reducing target-output mismatch
5. Output-layer error is directly computed: δ = (t-y)×f'(y)
6. Hidden-layer error is inferred by backward propagation
7. This is required for hidden-layer weight tuning
8. Stage 1 is feed-forward computation
9. Stage 2 is error calculation and backpropagation
10. Stage 3 is weight updation
11. This process repeats for all training patterns
12. Repeated epochs reduce overall output error
13. Differentiable activation is required in BPN
14. Conclusion: error terms guide all layer-wise weight corrections

**Diagram:**
```
Input → Hidden → Output
  ↓       ↓       ↓
Forward propagation
  ↑       ↑       ↑
Backward error flow
```

---

### **Q12. Adaline Architecture & Delta Rule (70% frequency)**

**Appears in:** May 2024, June 2023

**Perfect Answer (3 marks - 6 points):**

1. Adaline is a single linear output unit model
2. Inputs and one bias connection feed the output unit
3. Weights are trainable and can be positive/negative
4. Error is measured against target output
5. Delta rule adjusts weights to reduce error: Δw = η(t-Yin)x
6. Goal is minimization of mean squared error

**Key difference from Perceptron:** Uses Yin (not y) for error calculation

---

### **Q13. Perceptron OR Implementation (80% frequency)**

**Appears in:** May 2024, June 2023, Model papers

**Perfect Answer (6-8 marks with table):**

**Setup:**
```
Binary inputs: {0,1}
Bipolar targets: {-1,+1}
Initial: w₁=0, w₂=0, b=0, η=1
```

**Epoch 1 Table:**

| Pattern | x₁ | x₂ | t | Yin | y | Error | w₁ | w₂ | b |
|---------|----|----|---|-----|---|-------|----|----|---|
| (0,0) | 0 | 0 | -1 | 0 | +1 | -2 | 0 | 0 | -2 |
| (0,1) | 0 | 1 | +1 | -2 | -1 | +2 | 0 | 2 | 0 |
| (1,0) | 1 | 0 | +1 | 0 | +1 | 0 | 0 | 2 | 0 |
| (1,1) | 1 | 1 | +1 | 2 | +1 | 0 | 0 | 2 | 0 |

**Epoch 2:** Test all - if correct, STOP!

**Conclusion:** OR converges due to linear separability

---

### **Q14. Adaline AND Implementation (70% frequency)**

**Appears in:** May 2024, Model papers

**Perfect Answer (8 marks with table):**

**Setup:**
```
Binary inputs: {0,1}
Bipolar targets: {-1,+1}
Initial: w₁=0.2, w₂=0.1, b=0, η=0.2
```

**Epoch 1 Table:**

| Pattern | x₁ | x₂ | t | Yin | δ=(t-Yin) | w₁ | w₂ | b |
|---------|----|----|---|-----|-----------|----|----|---|
| (0,0) | 0 | 0 | -1 | 0 | -1 | 0.2 | 0.1 | -0.2 |
| (0,1) | 0 | 1 | -1 | -0.1 | -0.9 | 0.2 | -0.08 | -0.38 |
| (1,0) | 1 | 0 | -1 | -0.18 | -0.82 | 0.036 | -0.08 | -0.544 |
| (1,1) | 1 | 1 | +1 | -0.624 | 1.624 | 0.361 | 0.245 | -0.219 |

**Continue until convergence...**

**Key:** Show all calculations clearly!

---

## 🔥 MODULE 3: MOST REPEATED QUESTIONS

### **Q15. Plot Fuzzy Membership - Age of People (100% frequency)**

**Appears in:** May 2024, June 2023, Every paper

**Perfect Answer (3 marks - 6 points):**

1. Define universe, for example U=[0,80] years
2. Choose five overlapping fuzzy labels
3. Use triangular/trapezoidal shapes for smooth transition
4. Ensure neighboring sets overlap to model gradual change
5. Peak points represent strongest membership for each label
6. Final plot must cover whole universe without large gaps

**Diagram:**
```
μ(x)
1.0 |  /\    /\    /\    /\    /\
    | /  \  /  \  /  \  /  \  /  \
0.5 |/    \/    \/    \/    \/    \
0.0 |__________________________________
    0   20  35  55  75  100 (years)
    VY   Y   M   O   VO
```

---

### **Q16. Core, Support, Boundary (60% frequency)**

**Appears in:** June 2023, Dec 2020

**Perfect Answer (3 marks - 6 points):**

1. Core(A) = {x | μA(x) = 1}
2. Support(A) = {x | μA(x) > 0}
3. Boundary(A) = {x | 0 < μA(x) < 1}
4. Core may be empty for some fuzzy sets
5. Support can be finite or continuous interval
6. Boundary region is most important for soft transitions

**Memory:** Core=1, Support>0, Boundary=between

---

### **Q17. Fuzzy Set Operations (70% frequency)**

**Appears in:** May 2024, June 2023, Model papers

**Perfect Answer (6 marks with calculations):**

**Given:** A and B fuzzy sets

**Operations to compute:**
1. Algebraic Sum: a+b-ab
2. Algebraic Product: ab
3. Bounded Sum: min(1, a+b)
4. Bounded Difference: max(0, a-b)

**Example:**
```
A = 1/1 + 0.5/2 + 0.3/3 + 0.2/4
B = 0.5/1 + 0.7/2 + 0.2/3 + 0.4/4

For element 2:
Alg Sum: 0.5+0.7-(0.5×0.7) = 1.2-0.35 = 0.85
Alg Prod: 0.5×0.7 = 0.35
Bound Sum: min(1, 0.5+0.7) = 1.0
Bound Diff: max(0, 0.5-0.7) = 0.0
```

**Present as table for full marks!**

---

### **Q18. Defuzzification Methods (100% frequency)**

**Appears in:** May 2024, June 2023, Every paper

**Perfect Answer (8 marks - explain 4 methods):**

**1. Max-Membership:**
- Select value with highest membership
- Fast but ignores other values
- Example: {0.3/20, 0.8/40, 0.5/60} → Output = 40

**2. Centroid (Center of Area):**
- Formula: z* = Σ(zi×μi) / Σμi
- Most commonly used
- Balanced approach
- Example: z* = (20×0.3 + 40×0.8 + 60×0.5)/(0.3+0.8+0.5) = 42.5

**3. Weighted Average:**
- For singleton outputs
- Formula: z* = Σ(μi×zi) / Σμi
- Similar to centroid
- Example: Same as centroid for discrete sets

**4. Center of Sums:**
- For multiple overlapping sets
- Formula: z* = Σ(Ai×ci) / ΣAi
- Considers area and centroid of each set
- More complex but comprehensive

**Conclusion:** Centroid is most popular for general use

---

### **Q19. Fuzzy Relations & Composition (60% frequency)**

**Appears in:** June 2023, Model papers

**Perfect Answer (9 marks with matrices):**

**Given:** R(X×Y) and S(Y×Z)

**Max-Min Composition:**
```
T(x,z) = max[min(R(x,y), S(y,z))]
         y

Example calculation for T₁₁:
y₁: min(0.6, 1.0) = 0.6
y₂: min(0.3, 0.8) = 0.3
T₁₁ = max(0.6, 0.3) = 0.6
```

**Max-Product Composition:**
```
T(x,z) = max[R(x,y) × S(y,z)]
         y

Example calculation for T₁₁:
y₁: 0.6 × 1.0 = 0.6
y₂: 0.3 × 0.8 = 0.24
T₁₁ = max(0.6, 0.24) = 0.6
```

**Show complete matrices for full marks!**

---

### **Q20. α-Cuts (50% frequency)**

**Appears in:** May 2024, June 2023

**Perfect Answer (5 marks):**

**Given:** A = 1/a + 0.9/b + 0.6/c + 0.3/d + 0.1/e

**Find cuts:**
```
α = 1:    A₁ = {a}
α = 0.9:  A₀.₉ = {a, b}
α = 0.6:  A₀.₆ = {a, b, c}
α = 0⁺:   A₀₊ = {a, b, c, d, e}
α = 0:    A₀ = {a, b, c, d, e}
```

**Rule:** Include all elements where μ ≥ α

---

## 🎯 EXAM PAPER PATTERN

### **Part A (30 marks)**
- 10 questions × 3 marks
- Answer ALL questions
- Time: 30-40 minutes

**Module-wise distribution:**
- Module 1: 3-4 questions
- Module 2: 2-3 questions
- Module 3: 2-3 questions
- Module 4: 1-2 questions
- Module 5: 1-2 questions

### **Part B (70 marks)**
- 5 modules × 2 questions each
- Choose 1 from each module
- Each question: 14 marks (usually 6+8 or 8+6)
- Time: 2 hours

---

## 🏆 HIGH-SCORING QUESTION COMBINATIONS

### **Module 1 (Choose 1):**
- **Option A:** MP Neuron (8) + Linear Separability (6) ← Easier
- **Option B:** Hebb Pattern (8) + Activation Numerical (6) ← More scoring

### **Module 2 (Choose 1):**
- **Option A:** BPN Architecture (8) + Perceptron OR (6) ← Balanced
- **Option B:** Adaline Training (6) + Adaline Numerical (8) ← If good at numericals

### **Module 3 (Choose 1):**
- **Option A:** Operations (6) + Defuzzification (8) ← Most common
- **Option B:** Composition (9) + α-cuts (5) ← If good at matrices

---

## 📝 ANSWER WRITING STRATEGY

### **For 3-mark questions:**
- Write 6 points (0.5 marks each)
- Use bullet points
- Be concise
- Time: 3 minutes max

### **For 6-mark questions:**
- Write 8-10 points
- Include diagram if asked
- Show formulas
- Time: 8 minutes

### **For 8-mark questions:**
- Write 12-14 points
- Include complete calculations
- Show tables for numericals
- Time: 12 minutes

### **For 14-mark questions:**
- Part A (6-8 marks) + Part B (6-8 marks)
- Total 14-16 points minimum
- Include diagrams, tables, formulas
- Time: 20 minutes

---

## ⚡ QUICK SCORING TIPS

1. **Always write formulas first** (even if you forget steps)
2. **Draw diagrams** (even rough ones get marks)
3. **Show calculations step-by-step** (method marks!)
4. **Use tables for numericals** (organized = more marks)
5. **Underline keywords** (helps examiner spot key points)
6. **Number your points** (easier to count marks)
7. **Write conclusions** (shows complete understanding)
8. **If stuck, write related points** (partial marks!)

---

**✅ PYQ ATTACK COMPLETE! Now go to STEP 6 → Memory Hacks** 🚀