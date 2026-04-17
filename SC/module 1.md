# MODULE 1: SOFT COMPUTING CRASH FILE (NO REPETITION)

This file is your single exam sheet for Module 1.
Use it top to bottom once, then revise PYQ templates only.

---

## STEP 1: PRIORITY TOPIC MATRIX (PYQ-DRIVEN)

| Topic | Importance | Why It Is Priority |
|---|---|---|
| Activation functions (binary and bipolar sigmoid) | CRITICAL | Part A in 2023 and 2024. Also appears in Part B numerical. |
| Biological vs artificial neuron | CRITICAL | Repeated Part A in 2023 and 2024. Direct 3-mark question. |
| MP neuron (AND/ANDNOT) | CRITICAL | Part B long question in 2023 and 2024. Easy diagram marks. |
| Hebb rule weight finding | CRITICAL | Repeated long question in 2023 and 2024. Predictable steps. |
| Linear separability and XOR | CRITICAL | Repeated Part B concept question in both years. |
| Net input and bias computation | HIGH | Asked in 2023 Part A and 2024 biased-network numerical. |
| Soft vs hard computing | HIGH | Frequent in question bank, quick scoring 3 marks. |

---

## STEP 2: ZERO-TO-EXAM TEACHING (CRITICAL + HIGH)

## TOPIC: Activation Functions

### What It Is
Activation maps neuron net input to final output.
It controls output range and nonlinearity.

### Why Exams Love It
It mixes definition, formulas, and easy calculations.

### Core Intuition
Think of a tap handle.
Input pressure enters the tap.
Activation decides output flow smoothly.
Not every input gives full output.

### Exam-Critical Definitions
- **ACTIVATION FUNCTION**: Function converting **NET INPUT** to neuron output.
- **BINARY SIGMOID**: Nonlinear function with output in **[0,1]**.
- **BIPOLAR SIGMOID**: Nonlinear function with output in **[-1,1]**.

### Key Formulas
- Binary sigmoid: `f(y_in)=1/(1+e^(-y_in))`
- Bipolar sigmoid: `f(y_in)=2/(1+e^(-y_in)) - 1`

### Algorithm/Steps
1. Write given x, w, and bias.
2. Compute `y_in=sum(w_i x_i)+b`.
3. Apply asked sigmoid formula.
4. Write final output and range.

### Diagram Description
- What to draw: two-input neuron with SUM, bias, activation, output.
- How to label: x1,x2,w1,w2,b,y_in,f(.),y.
- Arrows: x1/x2 and bias into SUM, SUM into activation, activation to output.

ASCII:

```
x1 --w1--\
          > ( SUM y_in ) --> [ ACTIVATION ] --> y
x2 --w2--/
        + b
```

### Common Exam Question Formats
- Explain role of activation function and any two types.
- Find output for binary and bipolar sigmoidal activation.

### Scoring Keywords
**NONLINEAR**, **NET INPUT**, **BOUNDED OUTPUT**, **SIGMOID**.

### What NOT to waste time on
Derivative proofs and rare activation types.

---

## TOPIC: Biological Neuron vs Artificial Neuron

### What It Is
Biological neuron is a living cell.
Artificial neuron is its computational abstraction.

### Why Exams Love It
Direct comparison gives fast clean marking.

### Core Intuition
Dendrites receive signals.
Soma processes them.
Axon carries output.
ANN copies this with inputs, weights, activation.

### Exam-Critical Definitions
- **BIOLOGICAL NEURON**: Dendrite-soma-axon-synapse based real neuron.
- **ARTIFICIAL NEURON**: Weighted-sum plus activation computational unit.

### Key Formula
- `y_in=sum(w_i x_i)+b`, `y=f(y_in)`

### Diagram Description
- What to draw: side-by-side biological and ANN block chain.
- How to label: dendrite, soma, axon, synapse and input, sum, activation, output.
- Arrows: left to right in both chains and optional mapping arrows.

ASCII:

```
Biological:  Dendrites -> Soma -> Axon -> Synapse
Artificial:  Inputs -> [SUM+BIAS] -> [ACTIVATION] -> Output
```

### Common Exam Question Formats
- Compare and contrast biological and artificial neuron.
- Draw simple artificial neuron and explain net input.

### Scoring Keywords
**DENDRITE**, **SOMA**, **AXON**, **SYNAPSE**, **WEIGHTS**, **BIAS**.

### What NOT to waste time on
Detailed biological chemistry.

---

## TOPIC: Net Input and Bias

### What It Is
Net input is weighted sum entering a neuron.
Bias shifts firing threshold.

### Why Exams Love It
It gives straightforward step-mark numericals.

### Core Intuition
Each input casts a vote.
Weight sets vote strength.
Bias adds fixed push.
Activation reads final vote score.

### Exam-Critical Definitions
- **NET INPUT**: Weighted sum plus bias.
- **BIAS**: Constant term shifting response threshold.

### Key Formula
- `y_in=w1x1+w2x2+...+wnxn+b`

### Algorithm/Steps
1. Multiply each input by weight.
2. Add all products.
3. Add bias.
4. Apply activation if asked.

### Diagram Description
- What to draw: multi-input lines into SUM plus separate bias arrow.
- Labels: xi, wi, b, y_in, y.

ASCII:

```
x1 --w1--\
x2 --w2---( SUM )----> y_in ----> f(.) ----> y
x3 --w3--/
      b --->+
```

### Common Exam Question Formats
- Draw ANN and discuss net input.
- Compute output with given x, w, b.

### Scoring Keywords
**WEIGHTED SUM**, **BIAS**, **THRESHOLD SHIFT**.

### What NOT to waste time on
Matrix notation for small 2-input problems.

---

## TOPIC: McCulloch-Pitts Neuron (AND/ANDNOT)

### What It Is
MP neuron is a binary threshold logic model.

### Why Exams Love It
It checks truth table, threshold design, and diagram.

### Core Intuition
A gate opens only when score crosses cutoff.
That cutoff is threshold.

### Exam-Critical Definitions
- **MP NEURON**: Binary neuron with threshold firing.
- **THRESHOLD CONDITION**: Output 1 when `y_in >= theta`.

### Key Formula
- `y_in=sum(w_i x_i)`
- `y=1 if y_in>=theta, else 0`

### Algorithm/Steps
1. Write truth table.
2. Choose weights and threshold.
3. Validate each row by y_in.
4. Draw final architecture.

### Diagram Description
- What to draw: 2-input threshold neuron for AND or ANDNOT.
- Label: x1,x2,w1,w2,theta,y.
- Arrows: both inputs into SUM, then threshold block, then output.

ASCII (AND):

```
x1 --(+1)--\
            >----( SUM )----> [ y_in >= 2 ? ] ---> y
x2 --(+1)--/
```

ASCII (ANDNOT: x1 AND NOT x2):

```
x1 --(+1)--\
            >----( SUM )----> [ y_in >= 1 ? ] ---> y
x2 --(-1)--/
```

### Common Exam Question Formats
- Implement ANDNOT with architecture and threshold.
- Implement AND logic using MP neuron.

### Scoring Keywords
**TRUTH TABLE**, **THRESHOLD**, **INHIBITORY INPUT**, **FIRING**.

### What NOT to waste time on
Historical details of MP model.

---

## TOPIC: Hebb Rule and Training

### What It Is
Hebb learning updates weights from input-target correlation.

### Why Exams Love It
Pattern classification question repeats with same procedure.

### Core Intuition
Neurons that fire together wire together.
Positive sign strengthens relation.
Negative sign weakens relation.

### Exam-Critical Definitions
- **HEBB RULE**: Weight change proportional to input and target.
- **BIPOLAR CODING**: Use values `+1` and `-1`.

### Key Formulas
- `Delta w_i = x_i * t`
- `w_i(new)=w_i(old)+Delta w_i`
- `b(new)=b(old)+t`

### Algorithm/Steps
1. Convert pattern values to bipolar.
2. Initialize all w and b to zero.
3. Update by each training pattern.
4. Accumulate final weights.
5. Test by sign of output.

### Diagram Description
- What to draw: flowchart from pattern input to update loop to testing.
- Labels: x,t,Delta w,w(new),testing.

ASCII:

```
(x, t) -> [Delta w = x*t] -> [Update w,b] -> [Next pattern] -> [Test]
```

### Common Exam Question Formats
- Using Hebb rule, find weights for given patterns.
- Explain Hebb training algorithm.
- Justify bipolar suitability statement.

### Scoring Keywords
**BIPOLAR**, **WEIGHT UPDATE**, **TARGET**, **CLASSIFICATION**, **TESTING**.

### What NOT to waste time on
Advanced Hebbian variants.

---

## TOPIC: Linear Separability and XOR

### What It Is
Linearly separable classes can be split by one line.
XOR cannot be split by one line.

### Why Exams Love It
Concept + graph gives easy method marks.

### Core Intuition
Place XOR points on corners.
Same class appears on opposite corners.
One line cannot isolate them correctly.

### Exam-Critical Definitions
- **LINEARLY SEPARABLE**: One linear boundary separates classes.
- **XOR NON-SEPARABLE**: No single straight boundary separates XOR classes.

### Key Formula
- Decision boundary: `w1x1+w2x2+b=0`

### Algorithm/Steps
1. Write XOR truth table.
2. Plot four binary points.
3. Mark class labels.
4. Show single-line failure.
5. Conclude non-separability.

### Diagram Description
- What to draw: x1-x2 axes with four corners and class marks.
- Labels: (0,0),(0,1),(1,0),(1,1), class 0/class 1.

ASCII:

```
x2
1 | X       O
  |
0 | O       X
  +--------------- x1
    0       1

XOR: no single straight line separates X and O.
```

### Common Exam Question Formats
- Define linear separability.
- Justify XOR is non-linearly separable.

### Scoring Keywords
**DECISION BOUNDARY**, **XOR**, **NON-SEPARABLE**, **SINGLE LINE FAILS**.

### What NOT to waste time on
Perceptron convergence theorem proofs.

---

## STEP 3: PYQ PATTERN EXPLOITATION (OFFICIAL PAPERS)

## Official PYQ Stems Collected
- 2023 Part A: Draw simple artificial neuron and net input.
- 2023 Part A: Compare biological and artificial neuron.
- 2023 Module I: Implement ANDNOT using MP neuron (8).
- 2023 Module I: Define linear separability, justify XOR non-separable (6).
- 2023 Module I: Compute neuron output using binary and bipolar sigmoid (6).
- 2023 Module I: Hebb rule weight finding for pattern classification (8).
- 2024 Part A: Role of activation function and any two activations.
- 2024 Part A: Compare biological and artificial neuron.
- 2024 Module I: Linear separability with AND/Hebb context (6).
- 2024 Module I: AND NOT using MP neuron with threshold (8).
- 2024 Module I: Hebb rule weight finding (8).
- 2024 Module I: Binary and bipolar sigmoid outputs for biased ANN.

## Cluster Templates

### Cluster A: MP AND/ANDNOT (8 marks)
- Repetition: 2/2 years.
- Master answer: definition -> truth table -> weight/theta choice -> row validation -> labeled diagram -> conclusion.
- Mark split: 1+2+2+1+2.
- Mandatory words: **THRESHOLD**, **TRUTH TABLE**, **INHIBITORY**.
- ⚠️ Mistake: missing theta or wrong sign for inhibitory input.

### Cluster B: XOR Separability (6 marks)
- Repetition: 2/2 years.
- Master answer: definition -> XOR table -> point plot -> single-line contradiction -> conclusion.
- Mark split: 1+1+2+1+1.
- Mandatory words: **DECISION BOUNDARY**, **NON-LINEARLY SEPARABLE**.
- ⚠️ Mistake: wrong class labels on corners.

### Cluster C: Hebb Weight Update (8 marks)
- Repetition: 2/2 years.
- Master answer: bipolar mapping -> initialization -> update table -> final weights -> testing table.
- Mark split: 1+1+3+1+2.
- Mandatory words: **BIPOLAR**, **DELTA W**, **TESTING**.
- ⚠️ Mistake: mixing binary and bipolar coding.

### Cluster D: Sigmoid Output Numerical (6 marks)
- Repetition: 2/2 years.
- Master answer: compute y_in -> binary output -> bipolar output -> range check.
- Mark split: 2+2+2.
- Mandatory words: **NET INPUT**, **BIAS**, **SIGMOID**.
- ⚠️ Mistake: forgetting bias term.

---

## STEP 4: MEMORY OPTIMIZATION

| Topic | Mnemonic | Must Memorize | Recall Trigger |
|---|---|---|---|
| Activation | BISO-BIPO | Two formulas and ranges | Same y_in, two output ranges |
| Bio vs ANN | DeSoAxSy -> InSumActOut | Part mappings | Biological chain maps to ANN blocks |
| Net input | SUM+PUSH | `y_in=sum(wx)+b` | Multiply, add, bias, activate |
| MP neuron | TABLE-THETA-TEST | Threshold condition | Truth table first |
| Hebb | FIRE TOGETHER WIRE TOGETHER | `Delta w=x*t` updates | Convert bipolar, update row-wise |
| XOR | ONE LINE FAILS XOR | Final conclusion line | Opposite corners block single line |

---

## STEP 5: 30-MINUTE EXECUTION PLAN

- Minutes 0-10: Activation + Bio vs ANN + Net input
  - Goal: lock 3-mark answers.
- Minutes 10-20: MP neuron + XOR
  - Goal: lock 6 and 8 mark structures.
- Minutes 20-25: Hebb update pattern
  - Goal: lock table sequence.
- Minutes 25-30: one self-test from each cluster
  - Goal: speed writing practice.

---

## STEP 6: ACTIVE TESTING (10 HIGH-PROBABILITY QUESTIONS)

1. Role of activation function; explain two activation functions. [3]
2. Compare biological and artificial neuron. [3]
3. Draw ANN and discuss net input. [3]
4. Implement ANDNOT using MP neuron with threshold. [8]
5. Define linear separability. Prove XOR non-separable. [6]
6. Hebb rule weight finding for I/O pattern class. [8]
7. Compute binary and bipolar sigmoid outputs for given x,w,b. [6]
8. Justify Hebb rule suits bipolar data. [3]
9. Differentiate soft and hard computing. [3]
10. Explain Hebb training algorithm steps. [3]

---

## STEP 7: FINAL 10-MINUTE WAR ROOM

## Priority Revision List
1. Sigmoid formulas and ranges.
2. MP ANDNOT threshold setup.
3. Hebb update equations.
4. XOR final sentence.
5. Net input with bias.

## Absolute Skip List
- Derivations not asked in PYQ.
- Long historical details.

## Paper Attempt Strategy
- Read full paper first: YES.
- Attempt order: easy Part A -> Module 1 long answer -> remaining modules.
- Time per mark: `180/100 = 1.8 min`.
- If stuck: write definition + diagram + keywords and move.

## Presentation Hacks
- Use headings: Definition, Steps, Diagram, Conclusion.
- Underline formulas and final answer.
- Keep one point per line.

## Emergency Tactic
Never leave blank.
Write a relevant formula, diagram, and three keywords for partial marks.
