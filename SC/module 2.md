# MODULE 2: SOFT COMPUTING CRASH FILE (NO REPETITION)

This file is your single exam sheet for Module 2.
Focus on algorithm order and update equations.

---

## STEP 1: PRIORITY TOPIC MATRIX (PYQ-DRIVEN)

| Topic | Importance | Why It Is Priority |
|---|---|---|
| Perceptron training algorithm | CRITICAL | Asked in Part A 2024. Part B implementations in 2023 and 2024. |
| Perceptron testing algorithm | CRITICAL | Asked in Part A 2023 directly. |
| Adaline model + delta rule | CRITICAL | Part A 2024 and Part B 2023/2024 asked repeatedly. |
| Adaline epoch implementation | CRITICAL | Long numerical style in both years. |
| Backpropagation architecture + stages | CRITICAL | Part A 2023 and Part B 2024 high marks. |
| BPN error terms / backprop concept | HIGH | Appears as 8-mark architecture+error discussion. |
| Perceptron logic implementation (AND/OR) | HIGH | Stable long-answer pattern with epochs. |

---

## STEP 2: ZERO-TO-EXAM TEACHING (CRITICAL + HIGH)

## TOPIC: Perceptron Network (Training + Testing)

### What It Is
Perceptron is a single-layer supervised classifier.
It learns by correcting classification errors.

### Why Exams Love It
It gives fixed algorithm steps with table updates.

### Core Intuition
Model predicts class.
If prediction is wrong, push weights to correct side.
Repeat until no mistakes remain.

### Exam-Critical Definitions
- **PERCEPTRON**: Linear threshold classifier for separable data.
- **EPOCH**: One full pass through all training patterns.
- **TESTING PHASE**: Use trained weights without updates.

### Key Formulas
- Net input: `y_in=sum(w_i x_i)+b`
- Output (bipolar sign): `y=+1 if y_in>=0 else -1`
- Update rule: `w_i(new)=w_i(old)+eta(t-y)x_i`
- Bias update: `b(new)=b(old)+eta(t-y)`

### Algorithm/Steps
1. Initialize `w` and `b`.
2. For each pattern, compute `y_in` and output `y`.
3. Compare with target `t`.
4. If mismatch, update weights and bias.
5. Complete all patterns for one epoch.
6. Stop if no changes in epoch.
7. Testing: run forward only, no updates.

### Diagram Description
- What to draw: two-input perceptron with SUM, step activation, output.
- Labels: x1,x2,w1,w2,b,y_in,y,t.
- Arrows: inputs and bias into SUM, SUM into step block.

ASCII:

```
x1 --w1--\
          > (SUM y_in) --> [STEP f] --> y
x2 --w2--/
        + b
Target t compares with y for update.
```

### Common Exam Question Formats
- Explain perceptron training algorithm.
- State testing algorithm used in perceptron network.
- Implement AND/OR with bipolar targets up to epochs.

### Scoring Keywords
**SUPERVISED**, **ERROR CORRECTION**, **EPOCH**, **WEIGHT UPDATE**, **CONVERGENCE**.

### What NOT to waste time on
Perceptron convergence theorem proof details.

---

## TOPIC: Adaline and Delta Rule

### What It Is
Adaline is adaptive linear neuron using LMS learning.
It minimizes mean squared error continuously.

### Why Exams Love It
It combines architecture sketch and weighted update numerical.

### Core Intuition
Perceptron learns only from class error.
Adaline learns from magnitude of error.
So Adaline adjusts more smoothly.

### Exam-Critical Definitions
- **ADALINE**: Single-output linear adaptive neuron.
- **DELTA RULE (LMS)**: Gradient-style update reducing mean squared error.

### Key Formulas
- `y_in=sum(w_i x_i)+b`
- Error: `delta=t-y_in`
- Update: `w_i(new)=w_i(old)+eta*delta*x_i`
- Bias: `b(new)=b(old)+eta*delta`
- MSE idea: minimize average squared error.

### Algorithm/Steps
1. Initialize small weights and bias.
2. For each pattern, compute `y_in`.
3. Compute `delta=t-y_in`.
4. Update all weights and bias.
5. Complete epoch table.
6. Repeat until tolerance or epoch limit.

### Diagram Description
- What to draw: perceptron-like structure but label linear output and delta update loop.
- Labels: y_in, delta, eta.

ASCII:

```
x1 --w1--\
          > (SUM y_in) ---> [linear/activation] ---> y
x2 --w2--/
        + b

delta = t - y_in  --> update w,b
```

### Common Exam Question Formats
- Explain architecture and delta rule of Adaline.
- Explain Adaline training algorithm for single output class.
- Implement one epoch for AND/OR with given initial weights.

### Scoring Keywords
**WIDROW-HOFF**, **LMS**, **DELTA**, **MSE**, **ADAPTIVE**.

### What NOT to waste time on
Matrix derivation of gradient descent.

---

## TOPIC: Backpropagation Network (BPN)

### What It Is
BPN is a multi-layer feedforward network.
It learns by propagating output error backward.

### Why Exams Love It
Stable long-answer topic with architecture and three stages.

### Core Intuition
Output is wrong.
Error is sent backward.
Each layer shares responsibility.
Weights change to reduce future error.

### Exam-Critical Definitions
- **BPN**: Multi-layer ANN trained with backpropagation.
- **OUTPUT ERROR TERM**: Difference-driven correction at output layer.
- **HIDDEN ERROR TERM**: Backpropagated correction for hidden layer.

### Key Formulas (write conceptually if not asked numerically)
- Output error term depends on `(t-y)` and derivative.
- Hidden error term is weighted sum of next-layer errors.
- Weight updates are proportional to learning rate and error term.

### Algorithm/Steps
1. Initialize all weights small random.
2. Feed-forward to get outputs.
3. Compute output error terms.
4. Backpropagate to hidden layer.
5. Update output-layer weights.
6. Update hidden-layer weights.
7. Repeat per pattern and per epoch.

### Diagram Description
- What to draw: input, hidden, output layers with full connections.
- Labels: x_i, hidden nodes h_j, outputs o_k, v_ij, w_jk.
- Arrows: forward arrows; one backward arrow marked error signal.

ASCII:

```
Input Layer      Hidden Layer       Output Layer
x1 ----\        h1 ----\
x2 ----- >-----> h2 ----- >-----> o1
x3 ----/        h3 ----/          o2

Forward pass: x -> h -> o
Backward pass: error from o -> h
```

### Common Exam Question Formats
- List stages involved in BPN.
- Explain architecture and error portions in BPN.
- Draw architecture and explain training algorithm.

### Scoring Keywords
**FEED-FORWARD**, **BACKPROPAGATION**, **ERROR TERMS**, **WEIGHT UPDATION**, **MULTILAYER**.

### What NOT to waste time on
Deep chain-rule proof derivation.

---

## STEP 3: PYQ PATTERN EXPLOITATION (OFFICIAL PAPERS)

## Official PYQ Stems Collected
- 2023 Part A: State testing algorithm used in perceptron network.
- 2023 Part A: List stages involved in backpropagation network.
- 2023 Module II: Implement AND with binary inputs and bipolar targets using perceptron (8).
- 2023 Module II: Draw BPN architecture and explain training algorithm (6).
- 2023 Module II: What is Adaline? Draw model (4).
- 2023 Module II: Use Adaline to train OR with bipolar inputs/targets for 2 epochs (10).
- 2024 Part A: Explain training algorithm of perceptron network.
- 2024 Part A: Explain architecture and delta rule for Adaline.
- 2024 Module II: Significance of error portions in BPN and architecture (8).
- 2024 Module II: Implement OR with binary inputs and bipolar targets up to two epochs (6).
- 2024 Module II: Explain Adaline training algorithm for single output class (6).
- 2024 Module II: Implement one epoch of Adaline for AND with given initial weights (8).

## Cluster Templates

### Cluster A: Perceptron Training/Testing (3-8 marks)
- Repetition: 2/2 years.
- Template: definition -> algorithm steps -> update rule -> stop/test condition.
- Mark split (8m implementation): 1+2+3+1+1.
- Keywords: **EPOCH**, **ERROR CORRECTION**, **UPDATE ONLY ON MISMATCH**.
- ⚠️ Mistake: updating weights during testing.

### Cluster B: Adaline + Delta Rule (3-10 marks)
- Repetition: 2/2 years.
- Template: model diagram -> delta formula -> epoch update table -> convergence comment.
- Mark split (8m epoch): 1+2+3+1+1.
- Keywords: **LMS**, **DELTA**, **MSE**, **CONTINUOUS ERROR**.
- ⚠️ Mistake: using `t-y` instead of `t-y_in` for Adaline update.

### Cluster C: BPN Architecture + Error Terms (3-8 marks)
- Repetition: 2/2 years.
- Template: architecture drawing -> three stages -> output/hidden error role -> weight update summary.
- Mark split (8m): 2+3+2+1.
- Keywords: **FEED-FORWARD**, **BACKPROPAGATION**, **ERROR PROPAGATION**.
- ⚠️ Mistake: missing hidden-layer error explanation.

---

## STEP 4: MEMORY OPTIMIZATION

| Topic | Mnemonic | Must Memorize | Recall Trigger |
|---|---|---|---|
| Perceptron | INIT-CALC-COMPARE-UPDATE-REPEAT | `w+=eta(t-y)x` | Update only if wrong |
| Testing | FORWARD-ONLY | No update in test | Compute and classify only |
| Adaline | YIN-DELTA-LMS | `delta=t-y_in` | Adaline learns from magnitude |
| BPN | F-B-U | Feed-forward, Backprop, Update | Three stages in order |

---

## STEP 5: 30-MINUTE EXECUTION PLAN

- Minutes 0-10: Perceptron training and testing steps.
- Minutes 10-20: Adaline model and delta-rule epoch table.
- Minutes 20-25: BPN architecture and three-stage mnemonic.
- Minutes 25-30: write one mini answer for each cluster.

---

## STEP 6: ACTIVE TESTING (10 HIGH-PROBABILITY QUESTIONS)

1. Explain perceptron training algorithm. [3]
2. State perceptron testing algorithm. [3]
3. Implement OR using perceptron up to two epochs. [6]
4. Implement AND using perceptron with bipolar targets. [8]
5. Explain Adaline architecture and delta rule. [3]
6. Explain Adaline training algorithm for single output class. [6]
7. Perform one epoch of Adaline for AND with given initial weights. [8]
8. What is Adaline? Draw its model. [4]
9. List stages involved in BPN. [3]
10. Explain BPN architecture and significance of error terms. [8]

---

## STEP 7: FINAL 10-MINUTE WAR ROOM

## Priority Revision List
1. Perceptron update rule and stop condition.
2. Adaline delta formula with `y_in`.
3. BPN three stages in exact order.
4. One clear diagram each for perceptron, adaline, BPN.

## Absolute Skip List
- Long derivations of gradient equations.
- Rare theoretical side notes.

## Paper Attempt Strategy
- Read full paper first: YES.
- Attempt order: Part A algorithms -> Adaline/BPN long answer -> remaining.
- Time per mark: `1.8 min`.
- If stuck: write algorithm bullets + labeled diagram.

## Presentation Hacks
- Separate formulas from steps.
- Keep update tables neat.
- Box final learned weights/bias.

## Emergency Tactic
Write algorithm skeleton and one formula line.
This secures method marks even with partial numbers.
