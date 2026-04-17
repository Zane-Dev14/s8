# Distributed Computing PYQ Solved Master (OCR-Mapped)

Subject: CST402 Distributed Computing

Built from OCR sources:
- DC/ocr_output/Model_QP_Solved.txt
- DC/ocr_output/DCSeries1.txt
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Dcmod2.txt
- DC/ocr_output/DCmod3.txt
- DC/ocr_output/dcMod4.txt

Purpose:
- Direct exam-ready answers
- Easy language first, then technical precision
- Diagram-ready wherever relevant
- Step-by-step formula and walkthrough for numericals/algorithms

---

## How To Use This File

1. For Part A (3 marks): use compact 6-point answers.
2. For Part B (14 marks): use full sequence:
   Definition -> Assumptions -> Diagram -> Steps -> Example -> Conclusion.
3. For algorithm questions: always show message flow order.
4. For numerical/performance questions: write formula first, then substitute values.

---

## Module 1 Solved PYQ Set

### M1-Q1: Models of communication network

Answer (6 points):
1. Communication channels in distributed systems can follow FIFO, non-FIFO, or causal ordering behavior.
2. FIFO means first sent is first received on that channel.
3. Non-FIFO means message order is not guaranteed.
4. Causal ordering guarantees causally related messages are delivered in happened-before order.
5. Causal ordering is stronger than non-FIFO and helps simplify distributed algorithm design.
6. Choosing model affects correctness assumptions in protocols.

Quick relation:
- Causal ordering => FIFO behavior for causally related messages
- FIFO does not guarantee full causal ordering in all cases

---

### M1-Q2: Lamport happened-before and causal dependency

Answer:
1. Happened-before relation is written as a -> b.
2. If two events are in same process and a occurs before b, then a -> b.
3. If a is send(m) and b is receive(m), then a -> b.
4. Relation is transitive: if a -> b and b -> c, then a -> c.
5. Two events with neither a -> b nor b -> a are concurrent.
6. Causal dependency in distributed execution is identified using this relation.

Diagram to draw:

```text
P1:  a ---- send(m) ------------>
P2:             receive(m) ---- b

send(m) -> receive(m)
```

---

### M1-Q3: Distributed communication primitives (versions of send/receive)

Answer:
1. Basic primitives are send() and receive().
2. Communication can be synchronous or asynchronous.
3. In synchronous mode, sender/receiver may block until handshake is complete.
4. In asynchronous mode, send returns immediately and buffering is used.
5. Receive can be blocking (wait until message arrives) or non-blocking (poll/check).
6. Buffered communication decouples sender and receiver timing.
7. Unbuffered communication requires direct rendezvous.
8. Primitive choice affects latency, throughput, and program complexity.

---

### M1-Q4: Strategies for reliable and fault-tolerant distributed systems

Answer (exam flow):
1. Add redundancy (replication of service/data).
2. Use failure detection and timeouts.
3. Use checkpointing and rollback recovery.
4. Use consensus/agreement mechanisms for consistent decisions.
5. Use idempotent operations and retry-safe communication.
6. Isolate faults and support graceful degradation.
7. Maintain persistent logs for recovery.
8. Validate state consistency after failures.

Conclusion:
- Fault tolerance combines prevention, detection, isolation, and recovery.

---

## Module 2 Solved PYQ Set

### M2-Q1: Rules to update scalar clocks (Lamport logical clocks)

Given:
- Each process Pi has logical clock Ci.

Rules:
1. Before each local event/send/receive at Pi:
   - Ci = Ci + d (usually d=1)
2. On receive of message timestamp Tm at Pi:
   - Ci = max(Ci, Tm)
   - then apply increment rule (Ci = Ci + 1)

Why this works:
- Preserves happened-before direction in logical timestamps.

---

### M2-Q2: Issues in recording global state

Answer:
1. Global state includes local process states + channel states (in-transit messages).
2. Different processes have no shared clock, so simultaneous recording is difficult.
3. Messages can be in transit during snapshot.
4. Naive recording can produce inconsistent cut.
5. Need a coordinated marker/control mechanism.
6. Snapshot method must avoid disturbing normal computation.

---

### M2-Q3: Chandy-Lamport snapshot algorithm (detailed)

Assumptions:
1. Reliable channels
2. FIFO channels
3. Marker message support

Step-by-step:
1. Initiator records its local state.
2. Initiator sends marker on all outgoing channels.
3. On receiving first marker, a process records local state and marks that incoming channel empty.
4. It forwards marker on all outgoing channels.
5. For other incoming channels, it records messages received until marker arrives on that channel.
6. When marker received on all incoming channels, that process snapshot is complete.

What gets captured:
- Local state of each process
- In-transit channel messages

Why consistent:
- Marker boundaries prevent mixing future messages into past snapshot.

Diagram sketch:

```text
P1 (initiator): record state -> send marker to P2,P3
P2: first marker => record state, forward markers
P3: first marker => record state, forward markers
```

---

### M2-Q4: Bully algorithm + liveness and safety

Core idea:
- Highest process ID among alive processes becomes coordinator.

Steps:
1. Process Pi detects coordinator failure.
2. Pi sends ELECTION to all processes with higher IDs.
3. If no reply, Pi declares itself coordinator and sends COORDINATOR message.
4. If any higher process replies, Pi waits; higher process continues election.

Safety:
- At most one highest alive process finally becomes coordinator.

Liveness:
- If at least one process is alive and messages eventually delivered, election terminates.

Limitation:
- High message cost when many processes start elections.

---

### M2-Q5: Ring election algorithm

Core idea:
- Processes arranged logically in ring; election message circulates.

Steps:
1. Initiator sends election message with its ID.
2. Each active process appends/compares IDs and forwards.
3. After one full round, highest ID is known winner.
4. Coordinator announcement circulates.

Strength:
- Structured and deterministic.

Weakness:
- Slower if ring is large or links are slow.

---

### M2-Q6: Termination detection assumptions/rules (short form)

Common points to include:
1. Processes alternate between active/passive states.
2. Messages may be delayed but are eventually delivered.
3. No process should be active and no message should be in transit at true termination.
4. Control messages/tokens can be used to detect global quiescence.
5. Detection should not interfere with underlying computation.

---

## Module 3 Solved PYQ Set

### M3-Q1: Requirements of mutual exclusion algorithm

Answer:
1. Safety: at most one process in critical section at a time.
2. Liveness: every request eventually gets chance to enter CS.
3. Fairness: no starvation, requests served in fair order.

---

### M3-Q2: Lamport mutual exclusion algorithm (step-by-step)

Messages used:
- REQUEST, REPLY, RELEASE

Steps:
1. To enter CS, Pi sends REQUEST(timestamp, i) to all.
2. Pi inserts request in local priority queue.
3. On receiving REQUEST from Pj, process inserts it and sends REPLY.
4. Pi enters CS when:
   - its request is at head of queue, and
   - REPLY received from all other processes.
5. On exit, Pi removes own request and broadcasts RELEASE.
6. On receiving RELEASE from Pj, processes remove Pj request from queue.

---

### M3-Q3: Ricart-Agrawala algorithm (step-by-step)

Messages used:
- REQUEST, REPLY

Steps:
1. Pi sends REQUEST to all with timestamp.
2. Receiver sends immediate REPLY if:
   - receiver not requesting CS, or
   - receiver request has lower priority.
3. Otherwise, receiver defers REPLY.
4. Pi enters CS after receiving REPLY from all.
5. On exit, Pi sends deferred REPLY messages.

Why popular:
- Fewer messages than Lamport in many settings.

---

### M3-Q4: Maekawa algorithm and deadlock handling messages

Core idea:
- Process asks permission from quorum set, not from all sites.

Messages often discussed:
- REQUEST, REPLY/GRANT, RELEASE (and deadlock-related control depending on variant).

Deadlock possibility:
- Circular wait among quorums can occur.

Handling idea:
- Use timestamp priority + withdrawal/retry mechanisms (variant dependent).

---

### M3-Q5: Wait-for graph for deadlock detection

Step-by-step:
1. Build graph with process as node.
2. Add edge Pi -> Pj if Pi waits for Pj.
3. Detect cycle/knot in graph.
4. If cycle exists (under model assumptions), deadlock exists.

Mini example:
- P1 -> P2, P2 -> P3, P3 -> P1 => deadlock cycle.

---

### M3-Q6: Numerical - rate of critical section requests

Typical question:
- Synchronization delay = 3 sec
- Critical section execution time = 1 sec
- Find max rate of CS requests.

Step 1: Formula
- Total time per request = synchronization delay + CS execution time

Step 2: Substitute values
- Total time = 3 + 1 = 4 sec/request

Step 3: Convert to rate
- Rate = 1 / 4 request per second = 0.25 requests/sec

Step 4: Optional per minute form
- 0.25 * 60 = 15 requests/minute

Final answer:
- Max request rate = 0.25 requests/sec (or 15 requests/min)

---

## Module 4 Solved PYQ Set

### M4-Q1: No-orphans consistency condition

Key terms:
- Depend(e): processes whose state depends on event e
- Log(e): processes that have logged determinant of e
- Stable(e): determinant of e safely on stable storage

Condition idea:
- If an event has affected other processes, recovery should not leave those effects without a valid causal source.

Easy statement:
- System must prevent orphan processes/events after rollback.

---

### M4-Q2: Coordinated vs uncoordinated checkpointing

| Feature | Coordinated | Uncoordinated |
|---|---|---|
| Checkpoint timing | All processes coordinate | Each process independently |
| Consistency | Global consistent checkpoint | May become inconsistent |
| Domino effect | Avoided | Possible |
| Overhead style | Coordination overhead | Recovery complexity overhead |

---

### M4-Q3: Checkpoint-based rollback recovery types

1. Uncoordinated checkpointing
2. Coordinated checkpointing
3. Communication-induced checkpointing

Write for each:
- how checkpoints are taken,
- consistency risk,
- recovery complexity.

---

### M4-Q4: Types of messages in rollback recovery

Common categories:
1. In-transit messages
2. Lost messages
3. Delayed messages
4. Orphan messages
5. Duplicate messages

Include one-line definition for each in exam.

---

### M4-Q5: DSM advantages and disadvantages

Advantages:
1. Single address-space style programming
2. Easier sharing abstraction
3. Locality benefits
4. Cost-effective using commodity systems

Disadvantages:
1. Communication overhead
2. Coherence/consistency complexity
3. Performance not always equal to tightly coupled multiprocessors
4. Extra implementation complexity

---

### M4-Q6: Deterministic vs non-deterministic events

Deterministic event:
- Outcome reproducible from same prior state/input.

Non-deterministic event:
- External timing/message arrival can change outcome.

Why important:
- Log-based recovery must record determinants of non-deterministic events.

---

## Module 5 Solved PYQ Set

### M5-Q1: Consensus for crash failures under synchronous system

Assumptions:
1. Bounded message delay
2. Bounded process step time
3. Crash failures only (no Byzantine behavior)

Step-wise idea:
1. Processes propose values.
2. Exchange values in rounds.
3. Detect missing messages as crash evidence via timeout.
4. Apply deterministic decision rule (e.g., majority/preference rule).
5. Non-faulty processes decide same value.

Properties to mention:
1. Agreement
2. Validity
3. Termination

---

### M5-Q2: Distributed file system requirements

Core requirements:
1. Access transparency
2. Location transparency
3. Mobility transparency
4. Performance transparency
5. Scaling transparency
6. Concurrency support for updates
7. Replication support
8. Heterogeneity support
9. Fault tolerance
10. Consistency
11. Security
12. Efficiency

---

### M5-Q3: File service architecture (with neat diagram)

Main components:
1. Flat File Service (content operations)
2. Directory Service (name to file-id mapping)
3. Client Module (interface/bridge)

Diagram:

```text
User <-> Client Module <-> Directory Service
          |
          +-------------> Flat File Service
```

Flow (open file):
1. Client asks directory for file identifier.
2. Directory returns file identifier.
3. Client requests content from flat file service.
4. Flat file service returns data to client.

---

### M5-Q4: Andrew File System (AFS)

Points:
1. Uses whole-file caching at client side.
2. Client component (Venus) + server component (Vice).
3. Reduces server load and network traffic for repeated reads.
4. Uses callback-based consistency mechanism.

Differentiate quickly:
- Whole-file serving: server transfers full file.
- Whole-file caching: client keeps file locally for faster reuse.

---

### M5-Q5: Sun NFS architecture with diagram

Key idea:
- Stateless server design in classic NFS approach.

Typical architecture blocks:
1. NFS client module
2. VFS (virtual file system interface)
3. RPC/XDR communication layer
4. NFS server module
5. Local file system

Diagram sketch:

```text
Client App -> VFS -> NFS Client -> RPC/XDR -> NFS Server -> VFS -> Local FS
```

Exam points:
1. Remote files appear local to client.
2. RPC-based request/response handling.
3. Statelessness improves recovery simplicity.

---

## High-Frequency Quick Revision List

1. Scalar clock rules (R1, R2)
2. Chandy-Lamport snapshot
3. Bully + ring election
4. Lamport and Ricart-Agrawala mutual exclusion
5. Wait-for graph deadlock detection
6. Checkpointing + rollback recovery
7. No-orphans condition
8. Consensus under crash failures
9. File service architecture
10. AFS and NFS

---

## Answer Writing Template (Use For Any 14-Mark DC Question)

1. One-line definition
2. Assumptions (if algorithm)
3. Diagram/block flow
4. Step-by-step algorithm
5. One mini example
6. Merits/limitations
7. Final conclusion

If this sequence is followed, answers remain clean, complete, and scorer-friendly.

---

## Step-by-Step Worked Answers (High-Frequency Long Questions)

These are fully structured for 8/14-mark questions.

### W1: Chandy-Lamport Snapshot (Full 14-mark style)

Definition:
Chandy-Lamport is a distributed algorithm to record a consistent global state without stopping normal computation.

Assumptions:
1. Channels are reliable.
2. Channels are FIFO.
3. Marker control messages are available.

Goal:
Capture:
1. Local state of every process.
2. State of every channel (in-transit messages).

Marker Sending Rule:
When process Pi initiates (or receives first marker for this snapshot):
1. Record local state of Pi immediately.
2. Send marker on all outgoing channels before sending further application messages.

Marker Receiving Rule at process Pj on channel Cij:
1. If marker is first marker seen by Pj for this snapshot:
   - Record local state of Pj.
   - Record state of Cij as empty.
   - Send marker on all outgoing channels.
2. Else:
   - Record state of Cij as all messages received on Cij after Pj recorded local state and before this marker.

Stop Condition:
Snapshot collection terminates after every process has received marker on all incoming channels.

Mini walkthrough (3 processes P1, P2, P3):
1. P1 initiates snapshot, records local state, sends markers to P2 and P3.
2. P2 receives first marker from P1, records local state, marks channel P1->P2 empty, forwards markers.
3. P3 receives first marker from P1, does same, forwards markers.
4. Suppose one normal message m was already in transit on P2->P3 before P2's marker reached P3.
5. P3 records m in channel state for P2->P3.

Why consistent:
No message is recorded as received without a valid causal send in the recorded cut.

Conclusion:
The algorithm produces a consistent global snapshot while allowing ongoing computation.

---

### W2: Bully Election with Safety and Liveness (Full format)

Definition:
Bully algorithm elects the highest-ID alive process as coordinator.

Message types:
1. ELECTION
2. OK
3. COORDINATOR

Step-by-step:
1. Pi suspects coordinator failure.
2. Pi sends ELECTION to all processes with IDs > i.
3. Case A: no OK reply before timeout.
   - Pi declares itself coordinator.
   - Pi broadcasts COORDINATOR to all lower IDs.
4. Case B: one or more OK replies arrive.
   - Pi waits; higher process runs election.
5. Eventually highest alive process declares coordinator.

Safety proof idea:
1. Only highest alive process can fail to receive OK from higher IDs.
2. Therefore only it can safely announce final coordination.
3. Final coordinator is unique.

Liveness proof idea:
1. With finite message delay and at least one alive process, some election chain reaches highest alive process.
2. That process sends COORDINATOR.
3. System eventually stabilizes with leader.

Complexity note:
Can have high message overhead in worst case when many processes start election together.

---

### W3: Ring Election with Worked Trace

Definition:
Processes are in logical ring; election message circulates and highest ID is chosen.

Worked trace (ring IDs in order):
3 -> 17 -> 24 -> 1 -> 28 -> 15 -> 9 -> 4 -> back to 3

Steps:
1. Process 17 detects failure and initiates election with candidate 17.
2. At process 24: max(17,24)=24, forward 24.
3. At process 1: max(24,1)=24, forward 24.
4. At process 28: max(24,28)=28, forward 28.
5. Remaining processes keep forwarding 28.
6. When 28 receives its own candidate back, it wins.
7. 28 sends COORDINATOR(28) around ring.

Safety:
Only highest active ID can return to itself as maximum.

Liveness:
If ring path and delivery hold, announcement completes.

---

### W4: Lamport Mutual Exclusion (Scoring version)

Messages:
1. REQUEST(ts, i)
2. REPLY
3. RELEASE

Algorithm:
1. Pi wants CS, timestamps request, sends REQUEST to all, inserts request in local queue.
2. On REQUEST from Pj, every process inserts Pj request and sends REPLY.
3. Pi enters CS only when:
   - Pi's request is at queue head.
   - Pi has REPLY from all other processes.
4. On exit, Pi removes own request and broadcasts RELEASE.
5. Others remove Pi request on RELEASE.

Why mutual exclusion holds:
All processes maintain timestamp-ordered queue; two requests cannot both be at head in all queues simultaneously.

Message complexity:
3(n-1) messages per CS entry.

---

### W5: Ricart-Agrawala vs Lamport (Exam compare answer)

Ricart-Agrawala steps:
1. Pi sends REQUEST(ts,i) to all.
2. Receiver replies immediately if not competing or Pi has higher priority.
3. Else receiver defers reply.
4. Pi enters CS after all replies.
5. On exit Pi sends deferred replies.

Difference from Lamport:
1. No RELEASE broadcast in core RA protocol.
2. Lower message count: 2(n-1) vs 3(n-1).
3. Still uses timestamp priority and deferred replies.

When to mention RA advantage:
Use in answer when asked for efficient permission-based ME.

---

### W6: Wait-For Graph Deadlock Detection (Worked)

Definition:
WFG is directed graph where node is process and edge Pi->Pj means Pi waits for Pj.

Worked case:
1. P1 waits for P2 => P1->P2
2. P2 waits for P3 => P2->P3
3. P3 waits for P1 => P3->P1

Cycle test:
P1->P2->P3->P1 is a cycle.

Conclusion:
Cycle indicates deadlock (for corresponding model assumptions such as single-resource/AND model).

How to write 3-mark answer quickly:
1. Define WFG.
2. State cycle condition.
3. Give one 3-node cycle example.

---

### W7: Failure Recovery Message Anomalies (Worked narrative)

Given scenario:
Pi, Pj, Pk exchange messages; Pi crashes and rolls back.

Step-by-step anomaly detection:
1. Pi rolls back to checkpoint Ci1.
2. If Pj had recorded receive of message H from Pi, but Pi rolled back before send(H), then H is orphan.
3. To remove orphan effect, Pj may need rollback (cascading rollback starts).
4. If send(D) exists in sender history but receive(D) removed in receiver rollback, D is lost.
5. Messages arriving after rollback cut are delayed messages.
6. Replayed logs can create duplicate messages if receiver side deduplication is absent.

Key exam line:
Main failure-recovery challenge is preserving a consistent cut while eliminating orphans and controlling rollback spread.

---

### W8: Consensus in Synchronous Crash-Failure Systems

Definition:
Consensus means all non-faulty processes decide same value despite crash failures.

Assumptions:
1. Synchronous rounds
2. Known timeout bounds
3. Crash failures only

Properties:
1. Agreement
2. Validity
3. Termination

Round-based skeleton:
1. Each process starts with proposal xi.
2. For each round r=1..f+1:
   - Broadcast current value.
   - Collect values from responsive processes.
   - Update local value by deterministic rule.
3. Decide after required rounds.

Why f+1 rounds appears:
With at most f crashes, at least one crash-free round exists to align surviving views.

---

### W9: File Service Architecture (14-mark direct answer)

Definition:
File service architecture separates file naming, file content operations, and client interaction.

Components:
1. Flat File Service
   - read, write, create, delete content by file identifier.
2. Directory Service
   - maps pathname/name to file identifier.
3. Client Module
   - receives app request, coordinates directory and flat services.

Operation flow example (open file):
1. User asks client module to open file name.
2. Client asks directory service for file ID.
3. Directory returns file ID.
4. Client requests file data from flat file service using file ID.
5. Flat file service returns data.

Why architecture is used:
1. Separation of concerns
2. Better scalability
3. Cleaner naming and access management

Diagram:

```text
Application -> Client Module -> Directory Service
                     |
                     +-> Flat File Service
```

---

### W10: Critical Section Throughput Numerical (Exam-safe format)

Question type:
Synchronization delay = 3 sec, CS time = 1 sec.

Step 1:
Total time per CS request = sync delay + CS time = 3 + 1 = 4 sec.

Step 2:
Rate in requests/sec = 1/4 = 0.25 requests/sec.

Step 3:
Rate in requests/min = 0.25 x 60 = 15 requests/min.

Final:
0.25 requests/sec or 15 requests/min.

