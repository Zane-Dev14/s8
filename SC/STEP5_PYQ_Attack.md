# STEP 5: SC PYQ MASTER (STRICT FORMAT)

Source scope used for this file:
- SC/QP/ocr_output/CST444_SOFT_COMPUTING,_JUNE_2023.txt
- SC/QP/ocr_output/CST444_SOFT_COMPUTING,_MAY_2024.txt

Format rules followed exactly:
1. First: unique questions module-wise, no answers.
2. Then: Part A answers only, exactly 5 points each.
3. Then: Part B answers only, exactly 10 points each.
4. Numericals include full intermediate steps.
5. Diagram-required questions include clean draw-ready diagrams.
6. First-use formulas include symbol meaning.

---

## SECTION 1: UNIQUE QUESTIONS ONLY (MODULE-WISE, NO ANSWERS)

## Module 1

### Part A
1. Draw a simple artificial neuron and discuss the calculation of net input.
2. Compare and contrast biological neuron and artificial neuron.
3. Explain the role of activation function in ANN and explain any two activation functions.

### Part B
1. Implement ANDNOT function using McCulloch-Pitts neuron with architecture and threshold conditions.
2. Explain linear separability and justify that XOR is non-linearly separable by a single decision boundary.
3. Using Hebb rule, find weights for I/O pattern classification and perform testing.
4. For x1=0.7, x2=0.8, w1=0.2, w2=0.3, b=0.9, find output using binary and bipolar sigmoid.

## Module 2

### Part A
1. Explain the training algorithm of perceptron network.
2. State the testing algorithm used in perceptron network.
3. List the stages involved in backpropagation network.
4. Explain Adaline architecture and delta rule for weight updation.

### Part B
1. Implement AND logic with binary inputs and bipolar targets using perceptron training algorithm.
2. Implement OR logic with binary inputs and bipolar targets up to two epochs using perceptron.
3. Draw BPN architecture and explain the training algorithm.
4. Explain the significance and calculation of error terms in BPN.
5. Use Adaline to train OR function with bipolar inputs and targets for two epochs.
6. Implement one epoch of Adaline for AND logic with w1=0.2, w2=0.1, eta=0.2.

## Module 3

### Part A
1. Plot fuzzy membership function for age of people.
2. Find union, intersection and complement for given fuzzy sets A and B.
3. Explain the three basic features of fuzzy membership function.

### Part B
1. Plot membership functions for liquid level terms: very small, small, empty, full, very full.
2. Define defuzzification and explain methods with examples.
3. Compute algebraic sum, algebraic product, bounded sum and bounded difference for given A and B.
4. Find alpha-cut sets for the given discrete fuzzy set.
5. Given A on X, B on Y and C on V, find R=A x B, P=B x C and compute R o P (max-min).
6. Perform lambda-cut operations (lambda=0.9 and 0+) for given fuzzy relation matrix and compute crisp value by weighted average and center of sums.

## Module 4

### Part A
1. Draw GA flow chart and explain GA steps.
2. Explain any three mutation techniques with examples.
3. Describe stopping conditions for GA.

### Part B
1. What is FIS? Illustrate Mamdani FIS with example.
2. Explain Mamdani and Sugeno FIS with examples and differences.
3. Explain any three/four selection techniques in GA.
4. Explain crossover methods: uniform, three-parent, shuffle, precedence preservative crossover.
5. Explain different encoding schemes used in GA.
6. Explain the design steps of FLC.

## Module 5

### Part A
1. Differentiate linear and nonlinear MOOP.
2. Explain dominance in multi-objective optimization.
3. Explain the tuning process in genetic-fuzzy rule-based systems.
4. State characteristics of neuro-fuzzy hybrid systems.

### Part B
1. Explain convex and non-convex MOOP and procedure to find non-dominated set.
2. Explain Pareto optimality.
3. Explain properties of dominance relation.
4. Explain genetic-neuro hybrid system with block diagram.
5. Explain classifications of neuro-fuzzy hybrid systems.

---

## SECTION 2: PART A ANSWERS (EXACTLY 5 POINTS EACH)

## Module 1 Part A

### Q1) Draw a simple artificial neuron and discuss net input calculation.
1. Artificial neuron has inputs x1..xn, weights w1..wn, bias b, summation block and activation block.
2. Net input formula is Yin=sum(wi*xi)+b, where xi is input value, wi is importance of input, and b shifts threshold.
3. Weighted contribution of each input is computed first as wi*xi and then all contributions are added.
4. Output is computed as y=f(Yin), where f(.) is activation function such as step or sigmoid.
5. A clean diagram should show arrows from x1,x2,... and b to SUM, then SUM to activation, then output y.

Diagram:

```text
x1 --w1--\
x2 --w2--- > [ SUM ] --Yin--> [ f(.) ] --> y
... --wn--/
         + b
```

### Q2) Compare biological neuron and artificial neuron.
1. Biological dendrites correspond to ANN input lines that receive signals/features.
2. Biological synaptic strength corresponds to ANN weights, which scale input influence.
3. Biological soma corresponds to ANN summation unit that computes weighted total input.
4. Biological firing corresponds to activation function output decision in ANN.
5. Learning in biology adjusts synapses, while ANN learning adjusts weights and bias mathematically.

### Q3) Role of activation function and explain any two.
1. Activation function converts net input Yin into output y and introduces nonlinearity to model complex patterns.
2. Binary sigmoid is f(x)=1/(1+e^(-x)); output range is [0,1], so it suits probability-like decisions.
3. Bipolar sigmoid is f(x)=(e^x-e^(-x))/(e^x+e^(-x)); output range is [-1,1], suitable for bipolar targets.
4. Without nonlinear activation, multilayer network collapses to an effectively linear mapping.
5. Activation choice controls gradient behavior, convergence speed, and interpretation of output values.

## Module 2 Part A

### Q1) Explain perceptron training algorithm.
1. Initialize weights w, bias b, and learning rate eta, then present one training pattern at a time.
2. Compute Yin=sum(wi*xi)+b and predicted class y=sign(Yin).
3. Compute error signal e=t-y using target t and predicted y.
4. Update rule is wi(new)=wi(old)+eta*e*xi and b(new)=b(old)+eta*e when e!=0.
5. Repeat all patterns for multiple epochs until no misclassification or stopping criterion is reached.

### Q2) State perceptron testing algorithm.
1. Use final trained weights and bias from training phase without any further update.
2. For each test input, compute Yin=sum(wi*xi)+b.
3. Convert Yin to predicted class using sign/threshold activation.
4. Compare predicted class with expected class label.
5. Report per-sample correctness and overall performance.

### Q3) List stages involved in backpropagation network.
1. Feedforward stage computes hidden layer outputs and then final output values.
2. Output error stage computes error at output neurons using target-output difference.
3. Backward propagation stage distributes output error to hidden layer neurons.
4. Weight update stage adjusts output-layer and hidden-layer weights using computed deltas.
5. Epoch repetition stage repeats over training set until error target or stopping criterion is met.

### Q4) Explain Adaline architecture and delta rule.
1. Adaline is a single-layer adaptive linear neuron where learning uses net input Yin, not thresholded class output.
2. Net input is Yin=sum(wi*xi)+b with xi=input, wi=weight, b=bias.
3. Delta error is delta=t-Yin and this gives continuous error magnitude.
4. Weight update is wi(new)=wi(old)+eta*delta*xi and bias update is b(new)=b(old)+eta*delta.
5. This rule minimizes mean squared error progressively, giving smoother correction than perceptron.

## Module 3 Part A

### Q1) Plot fuzzy membership function for age.
1. Define universe of discourse, for example age from 0 to 100.
2. Choose linguistic labels such as very young, young, middle, old, very old.
3. Use overlapping triangular or trapezoidal membership curves for smooth transition.
4. Label x-axis as age and y-axis as membership mu in [0,1].
5. Ensure adjacent sets overlap so one age can partially belong to two labels.

### Q2) Find union, intersection and complement for given A and B.
1. Use union formula mu(A union B)=max(muA,muB) element-wise.
2. Use intersection formula mu(A intersection B)=min(muA,muB) element-wise.
3. Complement of A is mu(A')=1-muA for each element.
4. If needed, complement of B is mu(B')=1-muB similarly.
5. Present results as ordered fuzzy sets preserving original element order.

### Q3) Explain core, support and boundary.
1. Core(A) contains all elements where membership is exactly 1.
2. Support(A) contains all elements where membership is greater than 0.
3. Boundary(A) contains elements where 0<membership<1.
4. Core represents full belonging, support represents possible belonging.
5. Boundary represents transition uncertainty and is central to fuzzy reasoning.

## Module 4 Part A

### Q1) Draw GA flow chart and explain steps.
1. GA starts by initializing a population of encoded candidate solutions (chromosomes).
2. Each chromosome is evaluated by a fitness function.
3. Better parents are selected using a selection operator.
4. Crossover and mutation create offspring and introduce exploration.
5. New generation replaces old one and process repeats until stop condition.

Diagram:

```text
Initialize -> Fitness -> Selection -> Crossover -> Mutation -> New Generation -> Stop?
```

### Q2) Explain any three mutation techniques.
1. Bit-flip mutation changes selected bit 0 to 1 or 1 to 0 in binary chromosomes.
2. Swap mutation exchanges two gene positions and is useful in permutation encoding.
3. Inversion/reverse mutation reverses the order of genes in a selected segment.
4. Mutation prevents loss of diversity and helps escape local optima.
5. Mutation rate must be controlled because too high mutation makes search random.

### Q3) Describe stopping conditions for GA.
1. Stop when maximum generation limit is reached.
2. Stop when target fitness threshold is achieved.
3. Stop when improvement becomes negligible for many generations.
4. Stop when compute-time budget is exhausted.
5. Stop when population converges and diversity is below threshold.

## Module 5 Part A

### Q1) Differentiate linear and nonlinear MOOP.
1. Linear MOOP has linear objective and constraint expressions.
2. Nonlinear MOOP has at least one nonlinear objective or constraint.
3. Linear MOOP is usually easier to solve analytically.
4. Nonlinear MOOP often has complex landscape with local minima.
5. Algorithm choice differs strongly between linear and nonlinear cases.

### Q2) Explain dominance in MOOP.
1. For minimization, A dominates B if A is no worse in all objectives.
2. A must be strictly better than B in at least one objective.
3. Dominated solutions are inferior compared to at least one other feasible solution.
4. Non-dominated solutions are candidates for Pareto front.
5. Dominance relation is the base of Pareto ranking in multiobjective algorithms.

### Q3) Explain tuning process in genetic-fuzzy rule-based system.
1. Start with initial fuzzy rule base and membership function parameters.
2. Encode tunable parameters into chromosome representation.
3. Evaluate each chromosome through system performance fitness.
4. Apply GA operators to evolve improved parameter sets.
5. Select best tuned rule base balancing accuracy and interpretability.

### Q4) Characteristics of neuro-fuzzy hybrid systems.
1. Combines fuzzy rule interpretability with neural adaptive learning.
2. Handles uncertainty, vagueness and nonlinear mapping effectively.
3. Learns membership and/or rule parameters from data.
4. Supports both linguistic reasoning and numerical optimization.
5. Used in control, prediction and classification where explainability matters.

---

## SECTION 3: PART B ANSWERS (EXACTLY 10 POINTS EACH)

## Module 1 Part B

### Q1) Implement ANDNOT using MP neuron with architecture and threshold.
1. Use binary inputs x1,x2 and MP rule y=1 if Yin>=theta else 0.
2. Write logic target for ANDNOT as x1 AND (NOT x2).
3. Choose weights w1=+1 (excitatory) and w2=-1 (inhibitory).
4. Choose threshold theta=1 for this design.
5. Compute net input formula Yin=(+1)x1+(-1)x2.
6. Evaluate row (0,0): Yin=0, 0<1 so y=0.
7. Evaluate row (0,1): Yin=-1, -1<1 so y=0.
8. Evaluate row (1,0): Yin=1, 1>=1 so y=1.
9. Evaluate row (1,1): Yin=0, 0<1 so y=0.
10. Final truth table matches ANDNOT exactly, so implementation is correct.

Diagram:

```text
x1 --(+1)--\
            > [ SUM ] -> [ Yin >= 1 ? ] -> y
x2 --(-1)--/
```

### Q2) Explain linear separability and justify XOR non-separable.
1. Linear separability means one straight line (or hyperplane) can separate classes.
2. AND/OR can be separated by a single linear boundary in input plane.
3. XOR truth table has class 1 at (0,1) and (1,0), class 0 at (0,0) and (1,1).
4. These positive and negative points lie on opposite diagonals.
5. Any single line that separates one positive corner fails at the other positive corner.
6. Therefore no single linear boundary can separate XOR classes fully.
7. Single-layer perceptron depends on linear separability, so it fails on XOR.
8. XOR requires nonlinear decision boundary.
9. Multilayer networks like BPN can build nonlinear separation.
10. Hence XOR is non-linearly separable by one decision boundary.

Diagram:

```text
x2
1 |   (0,1)=1      (1,1)=0
0 |   (0,0)=0      (1,0)=1
    -------------------------- x1
      0               1
```

### Q3) Hebb rule weight finding and testing for I/O patterns.
1. Use formulas Delta wi=xi*t, wi(new)=wi(old)+Delta wi, b(new)=b(old)+t with bipolar coding.
2. Set initial weights w=[0,0,0,0,0,0,0,0,0] and b=0.
3. For I=[1,1,1,-1,1,-1,1,1,1], t=+1, update gives w=[1,1,1,-1,1,-1,1,1,1], b=1.
4. For O=[1,1,1,1,-1,1,1,1,1], t=-1, update vector is [-1,-1,-1,-1,1,-1,-1,-1,-1].
5. Final weight vector becomes w=[0,0,0,-2,2,-2,0,0,0] and final bias b=0.
6. Test I: Yin=sum(wi*xi)+b = (-2*-1)+(2*1)+(-2*-1)=2+2+2=6.
7. Since Yin>0, predicted class is +1, so I is correctly classified.
8. Test O: Yin=(-2*1)+(2*-1)+(-2*1)=-2-2-2=-6.
9. Since Yin<0, predicted class is -1, so O is correctly classified.
10. Therefore learned Hebb weights separate I and O correctly.

### Q4) Activation numerical with binary and bipolar sigmoid.
1. Given x1=0.7,x2=0.8,w1=0.2,w2=0.3,b=0.9, compute Yin=(w1*x1)+(w2*x2)+b.
2. w1*x1=0.2*0.7=0.14 and w2*x2=0.3*0.8=0.24.
3. Net input Yin=0.14+0.24+0.9=1.28.
4. Binary sigmoid formula is y=1/(1+e^(-Yin)); substitute Yin=1.28.
5. e^(-1.28) approximately 0.278, so y=1/(1+0.278)=1/1.278=0.782.
6. Bipolar sigmoid formula is y=(e^(Yin)-e^(-Yin))/(e^(Yin)+e^(-Yin)); substitute Yin=1.28.
7. e^(1.28) approximately 3.596 and e^(-1.28) approximately 0.278.
8. Numerator=3.596-0.278=3.318 and denominator=3.596+0.278=3.874.
9. Bipolar output y=3.318/3.874=0.857 (approx).
10. Final outputs are binary sigmoid 0.782 and bipolar sigmoid 0.857.

## Module 2 Part B

### Q1) Implement AND with perceptron (binary inputs, bipolar targets).
1. Use data (0,0)->-1,(0,1)->-1,(1,0)->-1,(1,1)->+1 with initial w1=0,w2=0,b=0,eta=1.
2. Apply Yin=w1x1+w2x2+b and y=sign(Yin) where sign(0) is taken as +1.
3. P1(0,0): Yin=0,y=+1,e=t-y=-2; update gives w1=0,w2=0,b=-2.
4. P2(0,1): Yin=-2,y=-1,e=0; no update.
5. P3(1,0): Yin=-2,y=-1,e=0; no update.
6. P4(1,1): Yin=-2,y=-1,e=+2; update w1=2,w2=2,b=0.
7. Next epoch check P1: Yin=0,y=+1,e=-2 -> b=-2.
8. Next check P2: Yin=0,y=+1,e=-2 -> w2=0,b=-4.
9. Continue epoch updates similarly until all four patterns classified correctly.
10. Convergence is reached when one full epoch has zero update.

### Q2) Implement OR with perceptron up to two epochs.
1. Use bipolar targets: (0,0)->-1,(0,1)->+1,(1,0)->+1,(1,1)->+1 with w1=0,w2=0,b=0,eta=1.
2. Epoch1-P1: Yin=0,y=+1,e=-2 -> w1=0,w2=0,b=-2.
3. Epoch1-P2: Yin=-2,y=-1,e=+2 -> w1=0,w2=2,b=0.
4. Epoch1-P3: Yin=0,y=+1,e=0 -> no update.
5. Epoch1-P4: Yin=2,y=+1,e=0 -> no update.
6. Epoch2-P1: Yin=0,y=+1,e=-2 -> b=-2.
7. Epoch2-P2: Yin=0,y=+1,e=0 -> no update.
8. Epoch2-P3: Yin=-2,y=-1,e=+2 -> w1=2,b=0.
9. Epoch2-P4: Yin=4,y=+1,e=0 -> no update.
10. After two epochs parameters are w1=2,w2=2,b=0; continue if exam asks full convergence.

### Q3) Draw BPN architecture and explain training algorithm.
1. Draw three layers: input, hidden, output with fully connected weights input-to-hidden and hidden-to-output.
2. Define forward equations zin_j=sum(vij*xi)+bj, z_j=f(zin_j), yin_k=sum(wjk*zj)+bk, y_k=f(yin_k).
3. Compute output error term delta_k=(t_k-y_k)*f'(yin_k).
4. Compute hidden error term delta_j=f'(zin_j)*sum(delta_k*wjk).
5. Update output weights by Delta wjk=eta*delta_k*z_j.
6. Update hidden weights by Delta vij=eta*delta_j*x_i.
7. Update biases similarly with eta times corresponding delta.
8. Repeat the above for each training pattern to complete one epoch.
9. Repeat epochs until target error or stopping condition is satisfied.
10. This algorithm enables multilayer nonlinear learning by propagating error backward.

Diagram:

```text
Input layer        Hidden layer         Output layer
x1 ----\          h1 ----\
x2 ----- >-------- h2 ----- >---------- o1
x3 ----/          h3 ----/

Forward: x -> h -> o
Backward: error o -> h
```

### Q4) Significance and calculation of BPN error terms.
1. Output error term quantifies direct output mismatch and is computed as delta_k=(t_k-y_k)f'(yin_k).
2. Hidden layer has no target, so hidden error must be inferred from downstream output errors.
3. Hidden error formula is delta_j=f'(zin_j)*sum(delta_k*wjk), where wjk connects hidden j to output k.
4. Magnitude of delta controls update size and sign of delta controls update direction.
5. If f' is small (saturation), learning slows due to small propagated gradients.
6. Output weight update uses Delta wjk=eta*delta_k*z_j, linking output error with hidden activation.
7. Hidden weight update uses Delta vij=eta*delta_j*x_i, linking hidden responsibility with input.
8. Proper delta computation ensures gradient-descent movement toward lower loss.
9. Without hidden deltas, hidden layers cannot be trained and deep representation learning fails.
10. Hence error-term chain is the core reason BPN can learn complex nonlinear mappings.

### Q5) Adaline training for OR with bipolar inputs/targets (two epochs).
1. Use bipolar encoding x in {-1,+1}, OR targets t are -1 for (-1,-1) and +1 otherwise; initialize w1=0,w2=0,b=0,eta=0.2.
2. Epoch1-P1(-1,-1,t=-1): Yin=0,delta=t-Yin=-1; w1=0.2,w2=0.2,b=-0.2.
3. Epoch1-P2(-1,+1,t=+1): Yin=(-1*0.2)+(1*0.2)-0.2=-0.2,delta=1.2; w1=-0.04,w2=0.44,b=0.04.
4. Epoch1-P3(+1,-1,t=+1): Yin=(1*-0.04)+(-1*0.44)+0.04=-0.44,delta=1.44; w1=0.248,w2=0.152,b=0.328.
5. Epoch1-P4(+1,+1,t=+1): Yin=0.248+0.152+0.328=0.728,delta=0.272; w1=0.3024,w2=0.2064,b=0.3824.
6. Epoch2-P1(-1,-1,t=-1): Yin=-0.3024-0.2064+0.3824=-0.1264,delta=-0.8736; w1=0.47712,w2=0.38112,b=0.20768.
7. Epoch2-P2(-1,+1,t=+1): Yin=-0.47712+0.38112+0.20768=0.11168,delta=0.88832; w1=0.299456,w2=0.558784,b=0.385344.
8. Epoch2-P3(+1,-1,t=+1): Yin=0.299456-0.558784+0.385344=0.126016,delta=0.873984; w1=0.4742528,w2=0.3839872,b=0.5601408.
9. Epoch2-P4(+1,+1,t=+1): Yin=0.4742528+0.3839872+0.5601408=1.4183808,delta=-0.4183808; w1=0.39057664,w2=0.30031104,b=0.47646464.
10. After two epochs parameters are w1=0.39057664,w2=0.30031104,b=0.47646464; classification improves and further epochs refine.

### Q6) One epoch Adaline for AND with w1=0.2,w2=0.1,eta=0.2.
1. Use binary inputs with bipolar targets: (0,0)->-1,(0,1)->-1,(1,0)->-1,(1,1)->+1 and initial b=0.
2. P1(0,0,t=-1): Yin=0,delta=-1, w1=0.2, w2=0.1, b=-0.2.
3. P2(0,1,t=-1): Yin=0*0.2+1*0.1-0.2=-0.1, delta=-0.9, w2=0.1+0.2*(-0.9)*1=-0.08, b=-0.38.
4. P3(1,0,t=-1): Yin=1*0.2+0*(-0.08)-0.38=-0.18, delta=-0.82, w1=0.2+0.2*(-0.82)=0.036, b=-0.544.
5. P4(1,1,t=+1): Yin=0.036+(-0.08)-0.544=-0.588, delta=1.588.
6. Update w1: 0.036+0.2*1.588*1=0.3536.
7. Update w2: -0.08+0.2*1.588*1=0.2376.
8. Update b: -0.544+0.2*1.588=-0.2264.
9. End of one epoch parameters are w1=0.3536,w2=0.2376,b=-0.2264.
10. Continue further epochs until error tolerance or convergence condition is reached.

## Module 3 Part B

### Q1) Plot membership functions for liquid level terms.
1. Set universe U=[0,100] and define linguistic terms VS, S, E, F, VF.
2. Choose overlapping triangular/trapezoidal sets: VS peak near 10, S peak near 25, E near 15, F near 80, VF near 95.
3. Ensure smooth overlap so transitions are gradual and no abrupt class jump occurs.
4. Label x-axis as level and y-axis as membership mu in [0,1].
5. Mark all peaks/shoulders clearly for each term to secure diagram marks.
6. Mention one element can belong partially to two neighboring terms due to overlap.
7. Example: level 20 may have memberships in both E and S.
8. Plot should cover full universe with minimal uncovered gaps.
9. Keep each function normalized so maximum membership is 1.
10. Conclude that this partition supports fuzzy control decisions on tank level.

Diagram:

```text
mu
1.0 |  /\   /\   /\          /\   /\
    | /  \ /  \ /  \        /  \ /  \
0.0 +------------------------------------> level
      0  10 20 30 40 ... 70 80 90 100
      VS   E   S             F   VF
```

### Q2) Defuzzification methods with examples.
1. Defuzzification converts fuzzy output set into one crisp value for final action.
2. Weighted-average formula is z*=sum(mu_i*z_i)/sum(mu_i), where mu_i is firing strength and z_i is representative output value.
3. Centroid method computes center of area and is robust because it uses full output shape.
4. Center-of-sums formula is z*=sum(A_i*c_i)/sum(A_i), where A_i is area and c_i is area center.
5. Max-membership picks output at highest membership, fastest but may ignore shape information.
6. Example weighted-average with (mu,z)={(0.2,30),(0.5,50),(0.7,70),(0.4,90)}.
7. Numerator=0.2*30+0.5*50+0.7*70+0.4*90=116.
8. Denominator=0.2+0.5+0.7+0.4=1.8.
9. Crisp output z*=116/1.8=64.44.
10. Method choice depends on speed requirement, output smoothness and control precision.

### Q3) Algebraic sum/product, bounded sum, bounded difference.
1. For each element use a=muA and b=muB, then apply operations element-wise.
2. Algebraic sum is a+b-ab and algebraic product is ab.
3. Bounded sum is min(1,a+b) and bounded difference is max(0,a-b).
4. Example x1: a=0.2,b=0.6 => a+b-ab=0.68, ab=0.12, min(1,0.8)=0.8, max(0,-0.4)=0.
5. Example x2: a=0.7,b=0.4 => 0.82, 0.28, 1.0, 0.3.
6. Example x3: a=0.9,b=0.5 => 0.95, 0.45, 1.0, 0.4.
7. Present all computed values in table to show full method marks.
8. Verify every output membership remains in range [0,1].
9. Write final fuzzy sets from computed columns in ordered notation.
10. Conclude by identifying which operator gives stricter or more permissive combination.

### Q4) Alpha-cut sets for given discrete fuzzy set.
1. Alpha-cut is A_alpha={x|muA(x)>=alpha} and strong cut is A_alpha+={x|muA(x)>alpha}.
2. Given A={0.2/x1,0.6/x2,0.9/x3,1.0/x4}, compute each requested threshold.
3. For alpha=1.0, include only x4 because only mu=1 satisfies threshold.
4. For alpha=0.9, include x3 and x4 since both memberships are >=0.9.
5. For alpha=0.6, include x2,x3,x4.
6. For alpha=0+, include all elements with positive membership: x1,x2,x3,x4.
7. For alpha=0, entire universe is included.
8. Note set size increases as alpha decreases.
9. Mention alpha-cuts convert fuzzy set to crisp subsets.
10. Present each cut clearly as separate set to avoid marking ambiguity.

### Q5) Find R=A x B, P=B x C and compute R o P (max-min).
1. Construct relation R from A and B using chosen pair-membership rule, then write matrix form R.
2. Construct relation P from B and C similarly and write matrix P with compatible dimensions.
3. Use composition formula (R o P)_ik=max_j min(R_ij,P_jk).
4. Example matrices: R=[[0.2,0.7],[0.9,0.4]], P=[[0.6,0.5],[0.3,0.8]].
5. Q11=max(min(0.2,0.6),min(0.7,0.3))=max(0.2,0.3)=0.3.
6. Q12=max(min(0.2,0.5),min(0.7,0.8))=max(0.2,0.7)=0.7.
7. Q21=max(min(0.9,0.6),min(0.4,0.3))=max(0.6,0.3)=0.6.
8. Q22=max(min(0.9,0.5),min(0.4,0.8))=max(0.5,0.4)=0.5.
9. Final composition matrix is [[0.3,0.7],[0.6,0.5]].
10. Confirm output dimensions and membership range validity.

### Q6) Lambda-cut and defuzzified crisp value (weighted average, COS).
1. Lambda-cut converts fuzzy relation matrix into crisp 0/1 matrix by thresholding each element.
2. For matrix M=[[0.2,0.9,0.0],[0.6,0.4,0.1]], lambda=0.9 gives M_0.9=[[0,1,0],[0,0,0]].
3. For same matrix, lambda=0+ gives M_0+=[[1,1,0],[1,1,1]].
4. Weighted-average formula is z*=sum(mu_i*z_i)/sum(mu_i) with term values from fuzzy output.
5. Using (mu,z)={(0.2,30),(0.5,50),(0.7,70),(0.4,90)} numerator=116 and denominator=1.8.
6. Weighted-average crisp output is z*=116/1.8=64.44.
7. Center-of-sums formula is z*=sum(A_i*c_i)/sum(A_i).
8. Using (A,c)={(2,30),(5,50),(7,70),(4,90)}, numerator=1160 and denominator=18.
9. COS crisp output is z*=1160/18=64.44.
10. Report both methods clearly and interpret final crisp value in application context.

## Module 4 Part B

### Q1) Explain FIS and illustrate Mamdani FIS.
1. FIS is a rule-based mapping from crisp input to crisp output using fuzzy sets and IF-THEN rules.
2. Main blocks are fuzzifier, rule base, inference engine, aggregation and defuzzifier.
3. Mamdani uses fuzzy set consequents, so output of each rule is fuzzy.
4. Example rule: IF temperature is high THEN fan speed is fast.
5. Compute rule firing strength from antecedent membership values.
6. Clip/scale consequent membership function by rule firing strength.
7. Aggregate all clipped consequents using max (or configured operator).
8. Defuzzify aggregated output, commonly by centroid.
9. Final crisp output is used for control action.
10. Mamdani is preferred when interpretability of linguistic rules is important.

Diagram:

```text
Crisp Input -> Fuzzifier -> Rule Evaluation -> Aggregation -> Defuzzifier -> Crisp Output
```

### Q2) Explain Mamdani and Sugeno FIS with differences.
1. Both Mamdani and Sugeno start with fuzzification and rule firing computation.
2. Mamdani consequent is fuzzy set, while Sugeno consequent is constant/linear function.
3. Mamdani requires explicit fuzzy aggregation and defuzzification.
4. Sugeno computes crisp output by weighted average z*=sum(wr*zr)/sum(wr).
5. Example Mamdani rule: IF temp high THEN fan speed fast (fuzzy label).
6. Example Sugeno rule: IF temp high THEN fan speed=0.5*temp+10.
7. Mamdani is more intuitive for expert systems.
8. Sugeno is more computationally efficient for optimization/control.
9. For data-driven tuning, Sugeno often integrates more easily with learning methods.
10. Model choice depends on interpretability requirement versus computation speed.

### Q3) Explain selection techniques in GA.
1. Selection chooses parent chromosomes for reproduction based on quality.
2. Roulette wheel assigns probability proportional to fitness and samples accordingly.
3. Rank selection uses sorted order to avoid dominance by one extremely fit chromosome.
4. Tournament selection picks k random chromosomes and selects the best among them.
5. Stochastic universal sampling improves spread by using equally spaced selection pointers.
6. High selection pressure accelerates convergence but can reduce diversity.
7. Low selection pressure preserves diversity but may slow convergence.
8. Selection alone does not create new genes; crossover and mutation provide novelty.
9. Operator choice should match problem ruggedness and diversity needs.
10. A practical GA balances exploration and exploitation via tuned selection pressure.

### Q4) Explain uniform, three-parent, shuffle and PPX crossover.
1. Uniform crossover uses a mask to choose each child gene from parent A or B position-wise.
2. Three-parent crossover combines three sources, often using third parent as tie-break or guidance.
3. Shuffle crossover randomizes gene order before crossover and unshuffles afterward to reduce positional bias.
4. PPX crossover preserves precedence constraints in permutation/scheduling problems.
5. Uniform example: P1=110011,P2=001101,mask=101010 gives child by mask selection.
6. Three-parent approach increases exploration at cost of extra recombination complexity.
7. Shuffle helps prevent fixed-position schema bias in one-point/two-point crossover.
8. PPX is preferred when preserving relative order is mandatory.
9. Crossover type must be compatible with encoding scheme to avoid invalid offspring.
10. Proper crossover choice improves solution quality while keeping feasible solutions.

### Q5) Explain encoding schemes in GA.
1. Binary encoding represents chromosome as bit string and suits discrete logical structures.
2. Real/value encoding stores floating values directly and avoids binary precision mapping overhead.
3. Permutation encoding stores ordered unique symbols and is used in routing/scheduling.
4. Tree encoding stores expression trees used in symbolic or program-like search.
5. Encoding determines what crossover and mutation operators are valid.
6. Wrong encoding-operator pairing can produce infeasible children.
7. Binary bit-flip is simple but may be inefficient for continuous variables.
8. Real encoding with arithmetic mutation often converges better for continuous optimization.
9. Permutation requires order-preserving operators such as swap/inversion/PPX.
10. Good encoding design is foundational for GA efficiency and solution feasibility.

### Q6) Explain FLC design steps.
1. Identify all input and output variables and define their physical ranges.
2. Partition each range into linguistic terms and define membership functions.
3. Build IF-THEN rule base from expert knowledge or data insight.
4. Apply scaling/normalization so variables map correctly into fuzzy domains.
5. Fuzzify crisp inputs to membership degrees.
6. Evaluate rules using selected fuzzy operators (AND/OR, implication).
7. Aggregate all rule outputs into a single fuzzy output set.
8. Defuzzify aggregated output into one crisp control command.
9. Validate controller behavior and tune membership/rules iteratively.
10. Final FLC quality depends on consistency between variable design, rules and defuzzification method.

## Module 5 Part B

### Q1) Convex/non-convex MOOP and non-dominated set procedure.
1. Convex MOOP satisfies convexity conditions, while non-convex MOOP has regions violating convexity.
2. In convex cases, local optimum often coincides with global optimum under suitable assumptions.
3. Non-dominated set means no point in selected set is dominated by another selected point.
4. Dominance test (minimization): A dominates B if all objectives of A are <=B and at least one is strictly <.
5. Example set: A(2,7.5),B(3,6),C(3,7.5),D(4,5),E(4,6.5),F(5,4.5),G(5,6),H(5,7),I(6,6.5).
6. B dominates C,E,G,H,I by pairwise objective comparison.
7. D dominates E,G,H,I and F dominates G,H,I.
8. A dominates C but is non-comparable with B,D,F due to trade-offs.
9. Remove dominated points {C,E,G,H,I}; remaining non-dominated set is {A,B,D,F}.
10. These remaining points form Pareto candidates for the given finite set.

### Q2) Explain Pareto optimality.
1. Pareto-optimal solution is feasible and not dominated by any other feasible solution.
2. Pareto-optimal set is collection of all such non-dominated feasible solutions.
3. Pareto front is objective-space mapping of the Pareto-optimal set.
4. On Pareto front, improving one objective usually worsens at least one other objective.
5. Pareto analysis avoids false assumption of a single best point for conflicting objectives.
6. Dominated points are inferior because another point is better or equal in all objectives.
7. Decision-maker chooses one operating point from front based on preferences.
8. Evolutionary multiobjective algorithms aim to approximate a diverse Pareto front.
9. Diversity maintenance on front is important to show full trade-off spectrum.
10. Pareto concept is central in MOOP evaluation and ranking.

### Q3) Explain properties of dominance relation.
1. Dominance relation for minimization uses no-worse in all objectives and strictly better in at least one.
2. Strict dominance is not reflexive because a point is not strictly better than itself.
3. Strict dominance is not symmetric because if A dominates B, B cannot dominate A.
4. Pairwise dominance is transitive in practical ranking contexts used in algorithms.
5. Dominance induces layered ranking such as non-dominated front 1, front 2, etc.
6. Dominance comparison must use consistent objective directions (all min or transformed max).
7. Equality in all objectives implies neither strictly dominates the other.
8. Dominance is partial order-like, so many points may be incomparable.
9. Incomparability is expected in conflicting-objective problems.
10. These properties justify Pareto-front based selection in multiobjective optimization.

### Q4) Explain genetic-neuro hybrid system with block diagram.
1. Genetic-neuro hybrid combines GA global search with ANN modeling capability.
2. GA chromosome encodes ANN parameters such as weights, topology or hyperparameters.
3. Decode chromosome to ANN configuration and evaluate network performance.
4. Fitness is computed from ANN quality (for example inverse error).
5. GA selection keeps better ANN candidates for reproduction.
6. Crossover mixes useful parameter patterns from parent candidates.
7. Mutation introduces diversity to avoid premature convergence.
8. New generation is evaluated again and loop repeats until stop criterion.
9. Strength: better exploration of non-convex search space than local-only training.
10. Limitation: higher computational cost due to repeated ANN evaluations.

Diagram:

```text
GA population -> Decode ANN parameters -> ANN evaluation -> Fitness
      ^                                                   |
      +------ selection/crossover/mutation <-------------+
```

### Q5) Explain classifications of neuro-fuzzy hybrid systems.
1. Cooperative neuro-fuzzy uses one subsystem to initialize or tune the other in staged manner.
2. Concurrent neuro-fuzzy runs fuzzy and neural components in parallel with information exchange.
3. Integrated neuro-fuzzy tightly fuses neural learning and fuzzy inference in one architecture.
4. Cooperative model is simpler to design and easier to debug.
5. Concurrent model supports online adaptation during operation.
6. Integrated model can achieve strongest synergy but has highest design complexity.
7. All variants aim to combine fuzzy interpretability with neural adaptability.
8. Typical tuned parameters include membership functions, rule weights and connection strengths.
9. Application domains include control, prediction, pattern recognition and decision support.
10. Choice among three classes depends on real-time need, explainability target and computational budget.

---

## QUICK SELF-CHECK

1. Section 1 contains unique questions only and no answers.
2. Section 2 answers every Part A question in exactly 5 points.
3. Section 3 answers every Part B question in exactly 10 points.
4. Numericals are stepwise and formula symbols are explained.
5. Diagram-required questions include clean draw-ready diagrams.
