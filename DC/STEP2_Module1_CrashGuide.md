# STEP 2: DC Module 1 Crash Guide (From Zero to Exam-Ready)

Module 1 focus:
- Distributed system basics
- Communication models
- Causal dependency and happened-before
- Primitives for distributed communication

Mapped from OCR:
- DC/ocr_output/DCSeries1.txt
- DC/ocr_output/Model_QP_Solved.txt

---

## Topic 1: Distributed System vs Distributed Programming

### What is it? (1 line)
A distributed system is many computers working as one system; distributed programming is how we write code for that system.

### Why this matters in exam
This is a common short-answer conceptual differentiation question.

### Perfect 6-point answer
1. Distributed system focuses on architecture of multiple cooperating nodes.
2. Distributed programming focuses on writing correct multi-node software.
3. Distributed systems are about resource sharing, reliability, and scalability.
4. Distributed programming handles messaging, synchronization, and failure handling.
5. In distributed systems, there is no shared memory and no global clock.
6. Distributed programming must handle latency, ordering, and partial failures.

---

## Topic 2: Transparency Requirements

### Must-remember list
1. Access transparency
2. Location transparency
3. Concurrency transparency
4. Replication transparency
5. Failure transparency
6. Mobility transparency
7. Performance transparency
8. Scaling transparency

### Memory trick
ALCRFMPS
(Access, Location, Concurrency, Replication, Failure, Mobility, Performance, Scaling)

### 3-mark answer format
- Define transparency in one line.
- Write any 3-4 types with one-line meaning each.

---

## Topic 3: Models of Communication Network

### Models
1. FIFO model
2. Non-FIFO model
3. Causal ordering model

### Key property to write
If send(m1) happened-before send(m2), then receive(m1) should happen-before receive(m2) under causal ordering.

### Diagram to draw

```text
P1: send m1 ----->
P2: send m2 -----> same destination

If send(m1) -> send(m2), then recv(m1) must happen before recv(m2)
```

### Perfect answer (6 points)
1. FIFO preserves per-channel send order.
2. Non-FIFO does not preserve send order.
3. Causal model preserves happened-before ordering.
4. Causal ordering is stronger for causally related messages.
5. Communication model affects algorithm correctness assumptions.
6. Causal support simplifies distributed synchronization logic.

---

## Topic 4: Lamport Happened-Before and Causal Dependency

### Formula-style rules
a -> b if:
1. a and b in same process and a occurs before b
2. a is send(m), b is receive(m)
3. transitive closure

### Concurrency
If neither a -> b nor b -> a, events are concurrent.

### 3-mark answer points
1. Define happened-before relation.
2. Write three rules.
3. Mention concurrency condition.
4. Mention why useful (causal reasoning).

---

## Topic 5: Send/Receive Primitives

### Types to mention
1. Synchronous vs asynchronous
2. Blocking vs non-blocking
3. Buffered vs unbuffered

### Mini explanation
- Synchronous: sender waits for receiver interaction.
- Asynchronous: sender continues without waiting.
- Blocking receive waits for message.
- Non-blocking receive returns immediately.

---

## Quick PYQ Attack Set (Module 1)

1. Explain three communication network service models.
2. Explain happened-before relation with one example.
3. Explain versions of send and receive primitives.
4. Explain reliability/fault tolerance strategies.

---

## Exam Strategy for Module 1

For 3 marks:
1. Write definition in first line.
2. Give 5-6 short points.
3. Use keywords: causal, FIFO, transparency, primitive.

For 6/8 marks:
1. Add assumptions.
2. Add one diagram.
3. Add one mini example.

This combination is enough to score consistently in Module 1.
