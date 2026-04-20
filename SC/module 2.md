## STEP 3: MODULE 2 CRASH GUIDE (HIGH-QUALITY VERSION)

Module focus:
- Perceptron training and testing
- Adaline and delta rule
- Perceptron vs Adaline differences
- Backpropagation network (BPN) architecture and full step flow
- Worked numericals with every step shown

How to use this file:
1. For theory: write definition -> formula -> algorithm -> key difference.
2. For numericals: reproduce the row-by-row tables exactly.
3. For 14-mark answers: use the long-answer template at the end of each topic.

---

## Topic 1: Perceptron Network (Training + Testing)

### Definition
Perceptron is a single-layer supervised classifier for linearly separable data.

### Core formula set (first use with term meaning)

$$
Y_{in} = \sum_{i=1}^{n} w_i x_i + b
$$

$$
y = \operatorname{sign}(Y_{in}) =
\begin{cases}
+1, & Y_{in} \ge 0 \\
-1, & Y_{in} < 0
\end{cases}
$$

$$
\Delta w_i = \eta (t-y) x_i,
\quad
w_i^{new} = w_i^{old} + \Delta w_i,
\quad
b^{new} = b^{old} + \eta (t-y)
$$

Term meaning:
- x_i: i-th input
- w_i: i-th weight
- b: bias
- Yin: net input before activation
- y: predicted class
- t: target class
- eta: learning rate

### Training algorithm (strict step order)
1. Initialize weights and bias.
2. Choose eta.
3. For each training pattern:
4. Compute Yin.
5. Compute y using sign function.
6. Compute error term e = t-y.
7. If e != 0, update w_i and b.
8. Repeat for all patterns (one epoch).
9. Continue epochs until no updates or max epoch reached.

### Testing algorithm
1. Freeze trained weights and bias.
2. For each test sample, compute Yin.
3. Compute y via sign(Yin).
4. Compare with expected class.
5. Report correctness/accuracy.

### Worked numerical: Perceptron OR gate (2 epochs)

Given:
- Inputs are binary, targets are bipolar
- Patterns: (0,0)->-1, (0,1)->+1, (1,0)->+1, (1,1)->+1
- Initial w1=0, w2=0, b=0, eta=1

Epoch 1 calculation table:

| Pattern | x1 | x2 | t | Yin=w1x1+w2x2+b | y | e=t-y | w1(new) | w2(new) | b(new) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 0 | -1 | 0 | +1 | -2 | 0 | 0 | -2 |
| P2 | 0 | 1 | +1 | -2 | -1 | +2 | 0 | 2 | 0 |
| P3 | 1 | 0 | +1 | 0 | +1 | 0 | 0 | 2 | 0 |
| P4 | 1 | 1 | +1 | 2 | +1 | 0 | 0 | 2 | 0 |

Epoch 2 quick check:
- P1: Yin=0*0+2*0+0=0 => y=+1 (wrong for t=-1)
- Update: e=-2 -> b=-2
- P2: Yin=0*0+2*1-2=0 => y=+1 (correct)
- P3: Yin=0*1+2*0-2=-2 => y=-1 (wrong for t=+1)
- Update: e=+2 -> w1=2, b=0
- P4: Yin=2*1+2*1+0=4 => y=+1 (correct)

Continue epochs similarly until all rows are correct.

### Perceptron convergence note
- Converges for linearly separable classes.
- Does not converge for XOR-like non-separable classes.

---

## Topic 2: Adaline and Delta Rule

### Definition
Adaline (Adaptive Linear Neuron) uses net-input error for continuous correction.

### Why Adaline differs from Perceptron

| Point | Perceptron | Adaline |
|---|---|---|
| Error source | t-y (class error) | t-Yin (net error) |
| Learning style | Discrete correction | Continuous correction |
| Objective | Classification correctness | MSE reduction |
| Common rule name | Perceptron update | Delta/LMS rule |

### Adaline core formulas (with term explanation)

$$
Y_{in}=\sum_i w_i x_i + b
$$

$$
\delta = t - Y_{in}
$$

$$
\Delta w_i = \eta \delta x_i,
\quad
w_i^{new}=w_i^{old}+\Delta w_i,
\quad
b^{new}=b^{old}+\eta\delta
$$

$$
MSE = \frac{1}{N}\sum_{p=1}^{N}(t_p-Y_{in,p})^2
$$

Term meaning:
- delta: instantaneous net error
- N: number of patterns
- MSE: average squared error over set

### Adaline training algorithm
1. Initialize weights and bias (small values).
2. Choose eta and stopping rule.
3. For each pattern, compute Yin.
4. Compute delta=t-Yin.
5. Update all weights and bias.
6. Complete epoch and compute error trend.
7. Stop at tolerance or max epoch.

### Worked numerical: one epoch Adaline for AND

Given:
- Patterns: (0,0)->-1, (0,1)->-1, (1,0)->-1, (1,1)->+1
- Initial w1=0.2, w2=0.1, b=0, eta=0.2

Row-by-row epoch table:

| Pattern | x1 | x2 | t | Yin | delta=t-Yin | w1(new)=w1+eta*delta*x1 | w2(new)=w2+eta*delta*x2 | b(new)=b+eta*delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 0 | -1 | 0.000 | -1.000 | 0.200 | 0.100 | -0.200 |
| P2 | 0 | 1 | -1 | -0.100 | -0.900 | 0.200 | -0.080 | -0.380 |
| P3 | 1 | 0 | -1 | -0.180 | -0.820 | 0.036 | -0.080 | -0.544 |
| P4 | 1 | 1 | +1 | -0.588 | +1.588 | 0.354 | 0.238 | -0.226 |

After one epoch:
- w1=0.354, w2=0.238, b=-0.226
- Continue more epochs for convergence.

---

## Topic 3: Backpropagation Network (BPN)

### Architecture
A typical BPN has three layers:
1. Input layer
2. Hidden layer
3. Output layer

Diagram:

```text
Input layer        Hidden layer         Output layer
x1 ----\          h1 ----\
x2 ----- >-------- h2 ----- >---------- o1
x3 ----/          h3 ----/

Forward pass: x -> h -> o
Backward pass: error o -> h
```

### Symbol table (must define in exam when first used)

| Symbol | Meaning |
|---|---|
| x_i | i-th input |
| v_ij | weight from input i to hidden j |
| z_j | hidden neuron output |
| w_jk | weight from hidden j to output k |
| y_k | output neuron output |
| t_k | target at output k |
| eta | learning rate |
| delta_k | output layer error term |
| delta_j | hidden layer error term |

### BPN equations

Forward pass:

$$
zin_j = \sum_i v_{ij}x_i + b_j,\quad z_j = f(zin_j)
$$

$$
yin_k = \sum_j w_{jk}z_j + b_k,\quad y_k = f(yin_k)
$$

Output error term:

$$
\delta_k=(t_k-y_k)f'(yin_k)
$$

Hidden error term:

$$
\delta_j=f'(zin_j)\sum_k\delta_k w_{jk}
$$

Weight updates:

$$
\Delta w_{jk}=\eta\delta_k z_j,
\quad
\Delta v_{ij}=\eta\delta_j x_i
$$

### Complete BPN training sequence
1. Initialize all v_ij, w_jk, and biases.
2. Feedforward input to hidden and output layers.
3. Compute output error terms delta_k.
4. Backpropagate to hidden and compute delta_j.
5. Update output-layer weights and biases.
6. Update hidden-layer weights and biases.
7. Repeat per pattern and per epoch.

### Worked numerical: one full BPN iteration (2-2-1 network)

Given:
- Inputs: x1=0.05, x2=0.10
- Target: t1=0.01
- Learning rate eta=0.5
- Activation: sigmoid f(a)=1/(1+e^-a)
- Initial weights:
  - Input->Hidden: v11=0.15, v21=0.20, v12=0.25, v22=0.30
  - Hidden->Output: w11=0.40, w21=0.45
- Biases: b_h1=0.35, b_h2=0.35, b_o1=0.60

Step A: Hidden layer forward pass
1. zin1 = 0.05*0.15 + 0.10*0.20 + 0.35 = 0.3775
2. z1 = sigmoid(0.3775) = 0.59327
3. zin2 = 0.05*0.25 + 0.10*0.30 + 0.35 = 0.3925
4. z2 = sigmoid(0.3925) = 0.59688

Step B: Output layer forward pass
1. yin1 = z1*0.40 + z2*0.45 + 0.60
2. yin1 = 0.59327*0.40 + 0.59688*0.45 + 0.60 = 1.10591
3. y1 = sigmoid(1.10591) = 0.75137

Step C: Output error term
1. f'(yin1) = y1*(1-y1) = 0.75137*(0.24863) = 0.18682
2. delta1 = (t1-y1)*f'(yin1)
3. delta1 = (0.01-0.75137)*0.18682 = -0.13850

Step D: Hidden error terms
1. f'(zin1) = z1*(1-z1) = 0.59327*0.40673 = 0.24130
2. f'(zin2) = z2*(1-z2) = 0.59688*0.40312 = 0.24061
3. delta_h1 = f'(zin1)*(delta1*w11)
4. delta_h1 = 0.24130*(-0.13850*0.40) = -0.01337
5. delta_h2 = f'(zin2)*(delta1*w21)
6. delta_h2 = 0.24061*(-0.13850*0.45) = -0.01500

Step E: Update hidden->output weights
1. Delta w11 = eta*delta1*z1 = 0.5*(-0.13850)*0.59327 = -0.04110
2. Delta w21 = eta*delta1*z2 = 0.5*(-0.13850)*0.59688 = -0.04134
3. w11(new)=0.40-0.04110=0.35890
4. w21(new)=0.45-0.04134=0.40866

Step F: Update input->hidden weights
1. Delta v11 = eta*delta_h1*x1 = 0.5*(-0.01337)*0.05 = -0.00033
2. Delta v21 = eta*delta_h1*x2 = 0.5*(-0.01337)*0.10 = -0.00067
3. Delta v12 = eta*delta_h2*x1 = 0.5*(-0.01500)*0.05 = -0.00038
4. Delta v22 = eta*delta_h2*x2 = 0.5*(-0.01500)*0.10 = -0.00075
5. v11(new)=0.14967, v21(new)=0.19933
6. v12(new)=0.24962, v22(new)=0.29925

That completes one full forward + backward + update cycle.

---

## Topic 4: Significance of Error Terms in BPN

1. delta_k measures output-layer responsibility for total error.
2. delta_j transfers responsibility to hidden units.
3. Without delta_j, hidden-layer weights cannot learn.
4. Magnitude of delta controls update size.
5. Sign of delta controls update direction.
6. Correct delta computation ensures gradient-descent movement.

---

## PYQ Bottom Section (deduplicated answer drill)

### Part A quick set
1. Explain training algorithm of perceptron network.
2. State testing algorithm used in perceptron network.
3. Explain Adaline architecture and delta rule.
4. List stages involved in BPN.

### Part B long set
1. Implement OR/AND using perceptron for given epochs.
2. Train Adaline for given gate data and report updated weights.
3. Draw BPN architecture and explain full training algorithm.
4. Explain significance and calculation of BPN error terms.

14-mark answer sequence:
1. Definition
2. Formula with term definitions
3. Initial values/assumptions
4. Row-by-row numerical table
5. Final parameter values
6. Verification output
7. Conclusion
