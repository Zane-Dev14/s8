# STEP 1: DC Priority Topics (OCR-Mapped)

Subject: Distributed Computing (CST402)

Mapped from:
- DC/ocr_output/Model_QP_Solved.txt
- DC/ocr_output/DCSeries1.txt
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Dcmod2.txt
- DC/ocr_output/DCmod3.txt
- DC/ocr_output/dcMod4.txt

---

## Exam Pattern Snapshot

From model paper OCR:
- Part A: 10 questions x 3 marks
- Part B: 5 modules, choose one question per module (14 marks each)

High-repeat style:
- Explain and illustrate algorithm
- Compare two models/approaches
- Define + list properties/issues
- Architecture with diagram
- One small numerical/performance-rate style question in mutual exclusion unit

---

## Module-Wise Priority Matrix

## Module 1 (Foundations + Communication)

Top priority:
1. Models of communication network (FIFO, non-FIFO, causal ordering)
2. Lamport happened-before and causal dependency
3. Distributed communication primitives (send/receive variants)
4. Reliability + fault tolerance strategies
5. Distributed system transparency requirements

Why:
- Appears in model Part A and Part B stems repeatedly.
- Easy to score with correct definitions + one clear diagram.

---

## Module 2 (Logical Time, Global State, Election, Termination)

Top priority:
1. Scalar time rules (R1, R2)
2. Issues in recording global state
3. Chandy-Lamport snapshot algorithm
4. Bully and Ring election algorithms + liveness/safety
5. Termination detection (rules/assumptions)

Why:
- Strongly represented in model paper and Dcmod2 topic list.
- Algorithm questions are direct and step-mark friendly.

---

## Module 3 (Mutual Exclusion + Deadlocks)

Top priority:
1. Lamport mutual exclusion algorithm
2. Ricart-Agrawala algorithm
3. Maekawa algorithm + deadlock handling messages
4. Wait-for graph deadlock detection
5. Deadlock models (single-resource, AND, OR, AND-OR, P-out-of-Q)
6. Critical-section request-rate numerical

Why:
- Highest density of repeated long-answer algorithm questions in DCmod3 + model paper.

---

## Module 4 (Recovery + DSM)

Top priority:
1. No-orphans consistency condition
2. Checkpointing and rollback recovery (types + comparison)
3. Log-based rollback recovery
4. Types of messages in rollback recovery
5. DSM advantages, disadvantages, and implementation issues
6. Deterministic vs non-deterministic events

Why:
- Direct PYQ stems in dcMod4 and DCSeries2.

---

## Module 5 (Consensus + Distributed File Systems)

Top priority:
1. Consensus algorithm for crash failures in synchronous system
2. File service architecture (flat file service, directory service, client module)
3. Andrew file system
4. Google file system basics
5. Distributed file-system requirements
6. AFS vs NFS and Sun NFS architecture

Why:
- Model paper has exact 14-mark questions here.

---

## 2-Day Revision Order

Day 1:
1. Module 3 algorithms
2. Module 2 algorithms
3. Module 4 recovery basics

Day 2:
1. Module 1 communication + happened-before
2. Module 5 DFS + consensus
3. Final PYQ answer writing drill

---

## Answer Writing Rule (DC)

For every long answer, use this fixed order:
1. Definition
2. Assumptions
3. Diagram
4. Algorithm steps
5. Example/walkthrough
6. Advantages/limitations
7. Conclusion

This structure maximizes method marks even when final wording is not perfect.
