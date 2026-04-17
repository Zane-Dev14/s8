# STEP 3: Module 2 Crash Guide (Logical Time, Snapshot, Election, Termination)

Module 2 focus:
- Scalar and vector clocks
- Global state and distributed snapshots
- Leader election algorithms
- Termination detection

Mapped from OCR:
- DC/ocr_output/Dcmod2.txt
- DC/ocr_output/DCSeries1.txt
- DC/ocr_output/Model_QP_Solved.txt

---

## Topic 1: Scalar Logical Time (Lamport Clock)

### Definition (1 line)
Scalar logical time is a per-process counter used to order events without a global physical clock.

### Update rules (must memorize)
1. R1 (local/send event at process Pi):
   - Ci = Ci + 1
2. R2 (receive event at process Pi for message timestamp Tm):
   - Ci = max(Ci, Tm) + 1

### Why it works
If event a happened-before event b, then timestamp(a) < timestamp(b).

### Important exam note
The reverse is not always true. timestamp(a) < timestamp(b) does not always prove a -> b.

---

## Topic 2: Vector Time

### Definition (1 line)
Vector time uses a vector of counters to represent causal history more accurately than scalar clocks.

### Core rule summary
For n processes, each process Pi keeps vector Vi[1..n].
1. On local event at Pi: Vi[i] = Vi[i] + 1
2. On send from Pi: attach Vi to message
3. On receive at Pj with timestamp T:
   - For each k: Vj[k] = max(Vj[k], T[k])
   - Then Vj[j] = Vj[j] + 1

### Comparison rule
Given vectors X and Y:
- X < Y iff X[k] <= Y[k] for all k and strict < for at least one k
- If neither X < Y nor Y < X, events are concurrent

---

## Topic 3: Issues in Recording Global State

### What is global state
Global state = all process local states + all channel states (messages in transit).

### Main issues
1. No global clock, so simultaneous capture is impossible.
2. In-transit messages can be counted wrongly.
3. Naive snapshot may create inconsistent cut.

### Typical 3-mark answer format
1. Define global state.
2. Mention process + channel states.
3. Mention in-transit ambiguity.
4. Mention no-common-clock issue.
5. Mention consistency/cut requirement.

---

## Topic 4: Chandy-Lamport Snapshot Algorithm

### Assumptions
1. Reliable channels
2. FIFO channels
3. Marker messages supported

### Marker sending rule
When process Pi initiates (or gets first marker):
1. Record local state
2. Send marker on all outgoing channels before normal messages

### Marker receiving rule
On receiving marker on channel Cij at process Pj:
1. If first marker for this snapshot:
   - Record local state of Pj
   - Record channel Cij state as empty
   - Send markers on outgoing channels
2. Else:
   - Record all messages received on Cij after local state recording and before this marker

### Termination condition
Snapshot completes when each process has received marker on all incoming channels.

### Diagram to draw

```text
P1 (initiator): record state -> marker to P2,P3
P2: first marker -> record state -> forward marker
P3: first marker -> record state -> forward marker
```

---

## Topic 5: Bully Election Algorithm

### Core idea
Highest alive process ID becomes coordinator.

### Steps
1. Pi detects leader failure.
2. Pi sends ELECTION to all higher IDs.
3. If no OK reply: Pi becomes coordinator and broadcasts COORDINATOR.
4. If OK reply arrives: higher process continues election.

### Safety and liveness
- Safety: final coordinator is unique highest alive process.
- Liveness: election finishes if messages are eventually delivered and at least one process is alive.

### Message types to write
1. ELECTION
2. OK (answer)
3. COORDINATOR

---

## Topic 6: Ring Election Algorithm

### Core idea
Processes are in logical ring; election message circulates and highest ID wins.

### Steps
1. Initiator sends election message with candidate ID.
2. Each process forwards max(current ID, candidate ID).
3. When message returns to winner, winner sends elected/coordinator message around ring.

### Safety and liveness points
- Safety: one winner with highest ID in active ring.
- Liveness: holds if ring connectivity and message delivery hold.

---

## Topic 7: Termination Detection (Quick Core)

### Definition
A distributed computation has terminated iff:
1. All processes are passive (idle)
2. No messages are in transit

### Common assumptions
1. Message delivery is reliable
2. Delays finite but unpredictable
3. Processes active/passive transition correctly

### Two high-frequency methods
1. Weight-throwing method
2. Spanning-tree token method

---

## Topic 8: Weight-Throwing Method (Step Flow)

### Core invariant
Total weight in system is always 1.

### Rules
1. Controller starts with weight 1.
2. On activation message, process receives part of weight.
3. On becoming idle, process returns its weight to controller.
4. When controller regains total weight 1 and no pending work, termination detected.

### Quick mini example
- Controller sends 0.6 to P1, keeps 0.4
- P1 sends 0.3 to P2, keeps 0.3
- P2 returns 0.3 to controller, then P1 returns 0.3
- Controller total returns to 1 => terminate

---

## Topic 9: Spanning-Tree Termination Detection

### Core idea
Leaf nodes send tokens upward to root when done.

### Token coloring
- White token: no new work triggered in subtree
- Black token: message activity happened in subtree

### Root decision
Termination detected when root is idle and receives only white tokens from all children.
If black token appears, root starts another detection round.

---

## Module 2 PYQ Attack Set

1. Rules for scalar clock update
2. Define vector time and properties
3. Issues in recording global state
4. Chandy-Lamport algorithm in detail
5. Bully election with liveness/safety
6. Ring election with example
7. Termination detection assumptions and rules
8. Weight throwing / spanning tree method

---

## Last-Minute Revision Grid

1. Write R1 and R2 from memory.
2. Practice one complete Chandy-Lamport answer.
3. Practice one Bully and one Ring election trace.
4. Memorize termination condition: all idle + no in-transit messages.
5. Draw one snapshot diagram and one ring election diagram.
