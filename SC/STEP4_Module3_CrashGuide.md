## STEP 4: MODULE 3 CRASH GUIDE (HIGH-QUALITY VERSION)

Module focus:
- Fuzzy sets and membership functions
- Core/support/boundary
- Basic and extended fuzzy operations
- Fuzzy relations and compositions (max-min, max-product)
- Alpha-cut/lambda-cut
- Defuzzification with full numericals

How to use this file:
1. Write formula first, then define each symbol.
2. For numericals, compute in a table and show each intermediate value.
3. For long answers, follow definition -> formula -> procedure -> worked result -> conclusion.

---

## Topic 1: Fuzzy Set Basics and Membership Functions

### Definition
A fuzzy set assigns each element a membership value between 0 and 1.

$$
A = \{(x,\mu_A(x))\mid x\in U,\;\mu_A(x)\in[0,1]\}
$$

Term meaning:
- U: universe of discourse
- x: element in universe
- mu_A(x): degree of belonging of x in set A

### Core, support, boundary

| Feature | Mathematical condition | Meaning |
|---|---|---|
| Core(A) | mu_A(x)=1 | Full membership |
| Support(A) | mu_A(x)>0 | Belongs at least partially |
| Boundary(A) | 0<mu_A(x)<1 | Transition region |

### Diagram (draw-ready)

```text
mu(x)
1.0 |        _________  <- Core
    |       /         \
    |      /           \ <- Boundary
0.0 +-----/-------------\---------------> x
         <----- Support ----->
```

### Membership function shapes
1. Triangular
2. Trapezoidal
3. Gaussian

```text
Triangular:         Trapezoidal:
mu                  mu
1.0   /\            1.0   ____
     /  \                /    \
0.0_/____\__        0.0_/______\__
     a b c              a b  c d
```

---

## Topic 2: Fuzzy Operations (Basic + Extended)

### Basic operations

$$
\mu_{A\cup B}(x)=\max(\mu_A(x),\mu_B(x))
$$

$$
\mu_{A\cap B}(x)=\min(\mu_A(x),\mu_B(x))
$$

$$
\mu_{\bar A}(x)=1-\mu_A(x)
$$

### Extended operations

$$
\text{Algebraic Sum}=a+b-ab
$$

$$
\text{Algebraic Product}=ab
$$

$$
\text{Bounded Sum}=\min(1,a+b)
$$

$$
\text{Bounded Difference}=\max(0,a-b)
$$

### Full worked numerical (all operations shown)

Given:
- A = {0.2/x1, 0.7/x2, 0.9/x3}
- B = {0.6/x1, 0.4/x2, 0.5/x3}

Step table:

| x | a=mu_A | b=mu_B | max(a,b) | min(a,b) | 1-a | a+b-ab | ab | min(1,a+b) | max(0,a-b) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| x1 | 0.2 | 0.6 | 0.6 | 0.2 | 0.8 | 0.68 | 0.12 | 0.8 | 0.0 |
| x2 | 0.7 | 0.4 | 0.7 | 0.4 | 0.3 | 0.82 | 0.28 | 1.0 | 0.3 |
| x3 | 0.9 | 0.5 | 0.9 | 0.5 | 0.1 | 0.95 | 0.45 | 1.0 | 0.4 |

Final sets:
1. A union B = {0.6/x1, 0.7/x2, 0.9/x3}
2. A intersection B = {0.2/x1, 0.4/x2, 0.5/x3}
3. A' = {0.8/x1, 0.3/x2, 0.1/x3}
4. Algebraic sum = {0.68/x1, 0.82/x2, 0.95/x3}
5. Algebraic product = {0.12/x1, 0.28/x2, 0.45/x3}
6. Bounded sum = {0.8/x1, 1.0/x2, 1.0/x3}
7. Bounded difference A-B = {0.0/x1, 0.3/x2, 0.4/x3}

---

## Topic 3: Fuzzy Relations and Composition

### Relation definition
A fuzzy relation R on XxY assigns a membership degree to each ordered pair (x,y).

### Composition formulas

Max-min composition:

$$
(R\circ P)_{ik}=\max_j\min(R_{ij},P_{jk})
$$

Max-product composition:

$$
(R\circ P)_{ik}=\max_j(R_{ij}P_{jk})
$$

### Worked max-min composition (every step)

Given:

$$
R=
\begin{bmatrix}
0.2 & 0.7 \\
0.9 & 0.4
\end{bmatrix},
\quad
P=
\begin{bmatrix}
0.6 & 0.5 \\
0.3 & 0.8
\end{bmatrix}
$$

Compute each cell of Q=R o P:

1. Q11 = max(min(0.2,0.6), min(0.7,0.3))
2. Q11 = max(0.2,0.3) = 0.3

3. Q12 = max(min(0.2,0.5), min(0.7,0.8))
4. Q12 = max(0.2,0.7) = 0.7

5. Q21 = max(min(0.9,0.6), min(0.4,0.3))
6. Q21 = max(0.6,0.3) = 0.6

7. Q22 = max(min(0.9,0.5), min(0.4,0.8))
8. Q22 = max(0.5,0.4) = 0.5

Final composition matrix:

$$
Q=
\begin{bmatrix}
0.3 & 0.7 \\
0.6 & 0.5
\end{bmatrix}
$$

---

## Topic 4: Alpha-cut and Lambda-cut

### Definitions
- Alpha-cut A_alpha = {x | mu_A(x) >= alpha}
- Strong alpha-cut A_alpha+ = {x | mu_A(x) > alpha}
- Lambda-cut on relation matrix converts to crisp 0/1 matrix by threshold.

### Worked alpha-cut example

Given:
A = {0.2/x1, 0.6/x2, 0.9/x3, 1.0/x4}

1. A_1.0 = {x4}
2. A_0.9 = {x3, x4}
3. A_0.6 = {x2, x3, x4}
4. A_0+ = {x1, x2, x3, x4}
5. A_0 = {x1, x2, x3, x4}

### Worked lambda-cut on matrix

Given relation:

$$
M=
\begin{bmatrix}
0.2 & 0.9 & 0.0 \\
0.6 & 0.4 & 0.1
\end{bmatrix}
$$

For lambda=0.9:

$$
M_{0.9}=
\begin{bmatrix}
0 & 1 & 0 \\
0 & 0 & 0
\end{bmatrix}
$$

For lambda=0+:

$$
M_{0+}=
\begin{bmatrix}
1 & 1 & 0 \\
1 & 1 & 1
\end{bmatrix}
$$

---

## Topic 5: Defuzzification (full numerical)

### Purpose
Convert fuzzy output into one crisp value for final decision/control.

### Common methods
1. Max-membership
2. Centroid
3. Weighted average
4. Center of sums
5. First of maxima

### Weighted average formula

$$
z^*=\frac{\sum_i \mu_i z_i}{\sum_i \mu_i}
$$

Term meaning:
- z_i: representative crisp value for rule/output set i
- mu_i: firing strength or membership weight

### Center of sums formula

$$
z^*=\frac{\sum_i A_i c_i}{\sum_i A_i}
$$

Term meaning:
- A_i: area of i-th output fuzzy set
- c_i: center of i-th output fuzzy set area

### Worked numerical

Given output terms:
- Poor(P): z1=30, mu1=0.2
- Fair(F): z2=50, mu2=0.5
- Good(G): z3=70, mu3=0.7
- VeryGood(VG): z4=90, mu4=0.4

Weighted average steps:
1. Numerator = 0.2*30 + 0.5*50 + 0.7*70 + 0.4*90
2. Numerator = 6 + 25 + 49 + 36 = 116
3. Denominator = 0.2 + 0.5 + 0.7 + 0.4 = 1.8
4. z* = 116/1.8 = 64.44

Center of sums example (assume areas/centers):
- A1=2, c1=30
- A2=5, c2=50
- A3=7, c3=70
- A4=4, c4=90

1. Numerator = 2*30 + 5*50 + 7*70 + 4*90
2. Numerator = 60 + 250 + 490 + 360 = 1160
3. Denominator = 2 + 5 + 7 + 4 = 18
4. z* = 1160/18 = 64.44

---

## PYQ Bottom Section (deduplicated answer drill)

### Part A quick set
1. Plot membership function for age of people.
2. Explain core, support, boundary.
3. Find union/intersection/complement for given sets.

### Part B long set
1. Compute algebraic sum/product and bounded operations.
2. Find alpha-cuts/lambda-cuts for given data.
3. Build relations and compute max-min composition.
4. Defuzzify using weighted average and center of sums.

14-mark answer sequence:
1. Definition
2. Formula with symbol meanings
3. Given data table/matrix
4. Row/element-wise calculations
5. Final set/matrix/crisp value
6. One-line interpretation
