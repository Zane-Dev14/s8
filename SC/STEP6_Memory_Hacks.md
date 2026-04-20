# STEP 6: MEMORY HACKS AND QUICK RECALL (QUALITY VERSION)

Purpose:
- Fast recall before exam
- Formula memory with meaning
- Ready templates for 5-point and 10-point answers

---

## 1) Ultra-Fast Recall Map

## Module 1
- Soft vs Hard: uncertain/adaptive vs exact/rigid
- Neuron mapping: dendrite->input, synapse->weight, soma->sum, firing->activation
- Net input: Yin=sum(wi*xi)+b
- MP neuron: y=1 if Yin>=theta else 0
- Hebb: Delta w= x*t
- XOR: not linearly separable by single line

## Module 2
- Perceptron update: Delta w=eta(t-y)x
- Adaline update: Delta w=eta(t-Yin)x
- BPN stages: feedforward -> backprop -> update
- Output delta: (t-y)f'(yin)
- Hidden delta: f'(zin)sum(delta_out*w)

## Module 3
- Fuzzy set: mu in [0,1]
- Core/support/boundary: mu=1, mu>0, 0<mu<1
- Union/intersection/complement: max/min/1-mu
- Max-min composition: max_j min(Rij,Pjk)
- Defuzzification weighted average: z*=sum(mu_i z_i)/sum(mu_i)

## Module 4
- FIS blocks: fuzzifier, rule base, inference, aggregation, defuzzifier
- Mamdani: fuzzy consequent
- Sugeno: crisp function consequent
- GA loop: init, fitness, selection, crossover, mutation, stop

## Module 5
- Dominance (minimization): no worse in all, better in at least one
- Pareto optimal: not dominated by any feasible point
- Non-dominated set: remaining after removing dominated points
- Hybrid: genetic-neuro and neuro-fuzzy

---

## 2) Formula Card With Symbol Meaning

1. Yin=sum(wi*xi)+b
- xi: input
- wi: input weight
- b: bias shift

2. Perceptron
- Delta w=eta(t-y)x
- Delta b=eta(t-y)

3. Adaline
- delta=t-Yin
- Delta w=eta*delta*x
- Delta b=eta*delta

4. MP neuron
- y=1 if Yin>=theta else 0

5. BPN
- delta_k=(t_k-y_k)f'(yin_k)
- delta_j=f'(zin_j)sum(delta_k*w_jk)
- Delta w_jk=eta*delta_k*z_j
- Delta v_ij=eta*delta_j*x_i

6. Fuzzy operations
- union=max(a,b)
- intersection=min(a,b)
- complement=1-a
- algebraic sum=a+b-ab
- algebraic product=ab
- bounded sum=min(1,a+b)
- bounded difference=max(0,a-b)

7. Defuzzification
- weighted average: z*=sum(mu_i*z_i)/sum(mu_i)
- center of sums: z*=sum(A_i*c_i)/sum(A_i)

8. MOOP dominance
- A dominates B if all f_i(A)<=f_i(B) and at least one strict <

---

## 3) Memory Anchors (One-Line Triggers)

- Threshold -> MP neuron
- Bipolar target -> Hebb/Adaline style questions
- Two epochs -> perceptron or Adaline table problem
- Error propagation -> BPN long answer
- Membership plot -> fuzzy shape + overlap
- Crisp value -> defuzzification formula
- Trade-off/front -> Pareto and non-dominated set

---

## 4) Exam Writing Templates

## Part A (3 marks): write exactly 5 points
1. One-line definition
2. Key formula
3. Symbol meaning or block/component name
4. One use/importance line
5. One conclusion/contrast line

## Part B (14 marks): write exactly 10 points
1. Definition
2. Given/assumptions
3. Formula with symbol meaning
4. Diagram or architecture
5. Step 1 of method
6. Step 2 of method
7. Step 3 with calculation
8. Final computed/derived result
9. Verification/interpretation
10. Conclusion

---

## 5) Last-Minute 5-Question Self-Test

1. Can I write Hebb training and testing steps without seeing notes?
2. Can I do one full perceptron/Adaline row update correctly?
3. Can I write BPN forward and backward equations with symbols?
4. Can I solve one max-min composition cell correctly?
5. Can I perform weighted-average defuzzification without mistake?
