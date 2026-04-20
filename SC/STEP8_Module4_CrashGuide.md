## STEP 8: MODULE 4 CRASH GUIDE (HIGH-QUALITY VERSION)

Module focus:
- Fuzzy Inference System (FIS)
- Mamdani vs Sugeno
- FLC design steps
- Genetic Algorithm workflow and operators
- Selection/crossover/mutation numericals with full steps

How to use this file:
1. For theory answers: definition -> blocks -> equations -> procedure -> conclusion.
2. For numericals: show all intermediate values and final interpretation.
3. For long answers: use the 10-point structure in each topic.

---

## Topic 1: Fuzzy Inference System (FIS)

### Definition
FIS maps crisp input values to crisp output decisions through fuzzy rules.

### Core blocks
1. Fuzzifier
2. Knowledge base (database + rule base)
3. Inference engine
4. Defuzzifier

### Block diagram

```text
Crisp input -> Fuzzifier -> Inference engine + Rule base -> Defuzzifier -> Crisp output
```

### Symbol table

| Symbol | Meaning |
|---|---|
| x | Crisp input variable |
| mu_A(x) | Membership of x in fuzzy set A |
| w_r | Firing strength of rule r |
| z_r | Rule output |
| z* | Final defuzzified output |

### FIS procedure (exam order)
1. Read crisp input.
2. Compute membership values in input fuzzy sets.
3. Evaluate antecedents using min/max (or t-norm/s-norm).
4. Compute rule firing strengths.
5. Produce each rule consequent.
6. Aggregate all rule outputs.
7. Defuzzify to obtain crisp output.

### Worked mini-example (Mamdani style)

Rules:
- R1: IF temperature is Low THEN fan speed is Slow
- R2: IF temperature is High THEN fan speed is Fast

Given:
- mu_Low(temperature)=0.3
- mu_High(temperature)=0.7

Step-by-step:
1. Rule firing strengths: w1=0.3, w2=0.7
2. Clip Slow output set at 0.3
3. Clip Fast output set at 0.7
4. Aggregate clipped outputs using max operation
5. Apply centroid/weighted method to get final fan-speed value

---

## Topic 2: Mamdani vs Sugeno FIS

### Core difference
- Mamdani consequent is fuzzy set.
- Sugeno consequent is constant/linear function.

### Comparison table

| Parameter | Mamdani | Sugeno |
|---|---|---|
| Consequent form | Fuzzy linguistic set | Crisp function/constant |
| Output before final step | Fuzzy | Rule-wise crisp |
| Defuzzification | Mandatory | Weighted average style |
| Interpretability | Very high | Moderate |
| Computation speed | Slower | Faster |
| Suitability | Expert-rule systems | Control/optimization integration |

### Sugeno output formula

$$
z^* = \frac{\sum_r w_r z_r}{\sum_r w_r}
$$

Term meaning:
- w_r: firing strength of rule r
- z_r: rule consequent output (constant or linear expression)

### Worked Sugeno numerical (every step)

Given two rules:
- Rule 1 firing strength w1=0.4, rule output z1=30
- Rule 2 firing strength w2=0.6, rule output z2=70

1. Numerator = w1*z1 + w2*z2 = 0.4*30 + 0.6*70 = 12 + 42 = 54
2. Denominator = w1 + w2 = 1.0
3. z* = 54/1.0 = 54

Final Sugeno output: 54

---

## Topic 3: FLC Design Steps (structured procedure)

### 9-step design sequence
1. Identify input/output variables.
2. Define universe of discourse for each variable.
3. Partition into linguistic terms.
4. Assign membership functions.
5. Build IF-THEN rule base.
6. Set scaling/normalization factors.
7. Run fuzzification and inference.
8. Aggregate rule outputs.
9. Defuzzify to crisp output.

### Common mistakes to avoid
1. Missing scaling factors.
2. Writing rule base without membership definitions.
3. Skipping aggregation before defuzzification.
4. Not labeling units/axes in membership plots.

---

## Topic 4: Genetic Algorithm (GA)

### Definition
GA is a population-based optimization method inspired by natural evolution.

### Main steps
1. Chromosome encoding
2. Initial population
3. Fitness evaluation
4. Parent selection
5. Crossover
6. Mutation
7. Replacement/new generation
8. Stop test

### GA flow diagram

```text
Initialize -> Evaluate fitness -> Select parents -> Crossover -> Mutation -> New generation -> Stop?
```

### Key terms

| Term | Meaning |
|---|---|
| Chromosome | Encoded candidate solution |
| Gene | One variable/unit in chromosome |
| Fitness | Quality score of candidate |
| Selection pressure | Bias toward fitter candidates |
| Mutation rate | Probability of random gene change |

---

## Topic 5: Selection Operators (with worked numerical)

### Roulette-wheel selection

Given fitness values:
- C1=2, C2=6, C3=3, C4=1

Step 1: Total fitness
- F = 2+6+3+1 = 12

Step 2: Selection probabilities
- P(C1)=2/12=0.1667
- P(C2)=6/12=0.5000
- P(C3)=3/12=0.2500
- P(C4)=1/12=0.0833

Step 3: Cumulative ranges
- C1: [0.0000, 0.1667)
- C2: [0.1667, 0.6667)
- C3: [0.6667, 0.9167)
- C4: [0.9167, 1.0000]

Step 4: Random numbers (example)
- r1=0.12 -> C1
- r2=0.43 -> C2
- r3=0.81 -> C3
- r4=0.95 -> C4

Selected pool from this draw: C1, C2, C3, C4

### Other important selection operators
1. Rank selection
2. Tournament selection
3. Stochastic universal sampling

---

## Topic 6: Crossover and Mutation (worked examples)

### One-point crossover example

Parents:
- P1 = 110011
- P2 = 001101

Cut after position 3:
- Child1 = 110 + 101 = 110101
- Child2 = 001 + 011 = 001011

### Uniform crossover example
Mask: 1 0 1 0 1 0
- Take bit from P1 when mask=1, from P2 when mask=0

### Bit-flip mutation example
Before: 110101
Mutate bit 4 -> After: 110001

### Why mutation is needed
Mutation restores diversity and helps avoid premature convergence.

---

## Topic 7: Encoding Schemes

| Scheme | Representation | Typical use |
|---|---|---|
| Binary encoding | 0/1 strings | Logical/combinational problems |
| Real encoding | Floating values | Continuous optimization |
| Permutation encoding | Ordered sequence | Scheduling/routing |
| Tree encoding | Expression tree | Symbolic/program structures |

---

## PYQ Bottom Section (deduplicated answer drill)

### Part A quick set
1. Draw GA flow chart and explain GA steps.
2. Explain any three mutation techniques.
3. Describe stopping conditions of GA.

### Part B long set
1. Explain FIS and illustrate Mamdani with example.
2. Compare Mamdani and Sugeno with equations.
3. Explain selection operators and crossover operators.
4. Explain encoding schemes and mutation role.

14-mark answer sequence:
1. Definition
2. Block/flow diagram
3. Formula with symbol meanings
4. Stepwise procedure
5. Worked mini-example
6. Advantages/limitations
7. Conclusion
