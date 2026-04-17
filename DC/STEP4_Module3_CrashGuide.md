# STEP 4: Module 3 Crash Guide (Mutual Exclusion and Deadlocks)

Module 3 focus:
- Mutual exclusion algorithms
- Quorum and token approaches
- Deadlock models and detection
- Performance metrics and numericals

Mapped from OCR:
- DC/ocr_output/DCmod3.txt
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Model_QP_Solved.txt

---

## Topic 1: Requirements of Mutual Exclusion Algorithm

### Must-write 3 properties
1. Safety
   - At most one process in critical section at a time.
2. Liveness
   - Requests eventually make progress.
3. Fairness (no starvation)
   - No process waits forever if it keeps requesting.

---

## Topic 2: Performance Metrics of ME Algorithms

Write any three:
1. Message complexity
2. Synchronization delay
3. Response time
4. Throughput

### Definitions
- Message complexity: messages per CS entry
- Synchronization delay: delay between one process leaving CS and next entering
- Response time: request to entry delay

---

## Topic 3: Lamport Mutual Exclusion Algorithm

### Messages used
1. REQUEST(ts, i)
2. REPLY
3. RELEASE

### Steps
1. Pi sends REQUEST to all and inserts request in local priority queue.
2. On receiving REQUEST from Pj, process inserts it and sends REPLY.
3. Pi enters CS only when:
   - own request at queue head, and
   - REPLY received from all other processes.
4. On exit, Pi removes request and broadcasts RELEASE.
5. On RELEASE from Pj, others remove Pj request from queue.

### Key assumptions
FIFO channels and logical timestamps.

### Message complexity
For n processes: 3(n-1) messages per CS entry.

---

## Topic 4: Ricart-Agrawala Algorithm

### Messages used
1. REQUEST
2. REPLY

### Steps
1. Pi sends timestamped REQUEST to all others.
2. Receiver sends REPLY immediately if:
   - not interested in CS, or
   - requester has higher priority.
3. Else receiver defers REPLY.
4. Pi enters CS after REPLY from all.
5. On exit, Pi sends all deferred replies.

### Why better than Lamport
No RELEASE broadcast, lower message count.

### Message complexity
2(n-1) messages per CS entry.

---

## Topic 5: Suzuki-Kasami Token Algorithm

### Core idea
Only token holder can enter critical section.

### Data structures
1. RN[i]: latest request number seen for process i
2. Token fields:
   - LN[i]: last request served for process i
   - Queue of pending requesters

### Steps
1. If Pi needs CS and has no token, increment RN[i], broadcast REQUEST(i, RN[i]).
2. Token holder sends token to Pi if request is pending and token idle.
3. Pi executes CS when token received.
4. On exit, update LN[i] and append newly pending requesters to queue.
5. If queue non-empty, send token to queue head.

### Strength
Low delay under high demand, strict mutual exclusion via single token.

---

## Topic 6: Maekawa Quorum-Based Algorithm

### Core idea
Each process requests permission only from quorum set Ri, not all processes.

### Messages
1. REQUEST
2. REPLY/GRANT
3. RELEASE

### Steps
1. Pi sends REQUEST to all nodes in Ri.
2. Node grants REPLY to one requester at a time; others wait in queue.
3. Pi enters CS after all REPLYs from Ri.
4. On exit Pi sends RELEASE to Ri.
5. Nodes grant next queued requester.

### Deadlock point
Circular waiting among quorums can occur; variants use priority/preemption/deadlock handling messages.

---

## Topic 7: Token-Based vs Non-Token-Based Approach

| Feature | Token-based | Non-token-based |
|---|---|---|
| Access control | Token possession | Permission messages |
| Message cost | Usually lower | Usually higher |
| Failure mode | Token loss issue | Process reply wait issue |
| Example | Suzuki-Kasami | Lamport, Ricart-Agrawala |

---

## Topic 8: Wait-For Graph (WFG) Deadlock Detection

### Definition
Directed graph with process as node.
Edge Pi -> Pj means Pi waits for Pj.

### Rule
Cycle/knot in WFG implies deadlock (under corresponding resource model assumptions).

### Mini example
P1 -> P2, P2 -> P3, P3 -> P1
Cycle exists => deadlock.

---

## Topic 9: Deadlock Models

### 1. Single-resource model
- One outstanding request per process
- Cycle implies deadlock

### 2. AND model
- Process needs all requested resources
- Cycle implies deadlock

### 3. OR model
- Process needs any one of requested resources
- Cycle alone may not imply deadlock

### 4. AND-OR model
- Mixed requirements; analysis is more complex

### 5. P-out-of-Q model
- Need any P among Q resources

---

## Topic 10: Critical Section Rate Numerical

Typical problem:
- Synchronization delay = 3 sec
- CS execution time = 1 sec

Step 1:
Total time per CS request = 3 + 1 = 4 sec

Step 2:
Rate = 1/4 requests per second = 0.25 requests/sec

Step 3 (optional):
Per minute = 0.25 x 60 = 15 requests/min

Final answer:
0.25 requests/sec (or 15 requests/min)

---

## Module 3 PYQ Attack Set

1. Lamport ME algorithm
2. Ricart-Agrawala with illustration
3. Suzuki-Kasami token algorithm
4. Maekawa algorithm and deadlock handling
5. WFG deadlock detection
6. Compare deadlock models
7. Compare token vs non-token ME
8. Critical section request rate numerical

---

## Last-Minute Revision Grid

1. Memorize message types and steps of Lamport, RA, Maekawa.
2. Memorize message counts: Lamport 3(n-1), RA 2(n-1).
3. Practice one WFG deadlock cycle example.
4. Practice one CS rate numerical.
5. Keep one comparison table ready (token vs non-token).
