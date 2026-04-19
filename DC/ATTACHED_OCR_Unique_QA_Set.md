# CST402 Attached OCR - Unique Question Set + Full Answers

Source attachment used:
- DC/CST402_papers_merged.pdf

OCR-only source corpus used for answers:
- DC/ocr_output/CST402_papers_merged.txt
- DC/ocr_output/Model_QP_Solved.txt
- DC/ocr_output/DCSeries1.txt
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Dcmod2.txt
- DC/ocr_output/DCmod3.txt
- DC/ocr_output/dcMod4.txt

---

## Section 1 - Unique Questions Only (Module-wise, No Repeats)

### Module 1

#### Part A (3 marks)
1. List the characteristics/features of a distributed system.
2. Define causal precedence relation in distributed executions.
3. Explain transparency requirements of distributed systems.
4. Explain different forms/meaning of load balancing in distributed systems.
5. Explain the advantages of distributed systems.
6. What do you mean by a distributed system?

#### Part B (14 marks)
1. Explain design issues and algorithmic challenges of distributed systems.
2. Compare logical concurrency and physical concurrency.
3. Explain past cone and future cone of an event.
4. Explain applications of distributed computing.
5. Explain models of communication networks / service models.
6. Explain different versions of send and receive primitives for distributed communication.
7. Discuss global state of distributed systems.
8. Relate a computer system to a distributed system with neat sketches.

---

### Module 2

#### Part A (3 marks)
1. What are leader election algorithms? Name any two.
2. Define logical clock.
3. Define termination detection.
4. What are the basic properties/rules of scalar time?
5. Specify issues in recording a global state.
6. Define vector time.

#### Part B (14 marks)
1. Explain basic properties of scalar time and logical clock implementation.
2. Illustrate bully algorithm and discuss liveness and safety.
3. Explain ring-based election algorithm with example.
4. Explain Chandy-Lamport algorithm in detail.
5. Explain how local snapshots are combined to form global snapshot in Chandy-Lamport.
6. Explain spanning-tree-based termination detection algorithm.
7. Explain termination detection rules using distributed snapshots with assumptions.
8. Explain weight-throwing based termination detection.
9. Explain properties of vector time.
10. What is consistent global state?

---

### Module 3

#### Part A (3 marks)
1. List performance evaluation metrics of mutual exclusion algorithms.
2. List requirements of mutual exclusion algorithms.
3. Compare token-based and non-token-based mutual exclusion approaches.
4. List strategies for deadlock handling in distributed environment.
5. Explain issues in deadlock detection.
6. Describe how quorum-based mutual exclusion differs from other categories.
7. Numerical: find CS request rate when synchronization delay is 3 s and average CS time is 1 s.

#### Part B (14 marks)
1. Explain Lamport's mutual exclusion algorithm.
2. Explain Ricart-Agrawala mutual exclusion algorithm.
3. Explain Suzuki-Kasami broadcast algorithm.
4. Explain Maekawa's mutual exclusion algorithm with example.
5. Explain wait-for graph based deadlock detection with example.
6. Explain deadlock handling strategies in distributed environment.
7. Compare various models of deadlock.
8. Explain differences between quorum-based and other mutual exclusion algorithms.

---

### Module 4

#### Part A (3 marks)
1. State advantages and disadvantages of distributed shared memory.
2. What are checkpoints?
3. List different types of messages in rollback recovery.
4. Explain no-orphans consistency condition.
5. Differentiate coordinated and uncoordinated checkpointing.
6. Differentiate deterministic and non-deterministic events in log-based rollback recovery.
7. Discuss issues in implementing distributed shared memory software.

#### Part B (14 marks)
1. Explain pessimistic and optimistic logging.
2. Show Lamport's Bakery algorithm and verify 3 critical-section requirements.
3. Differentiate consistent and inconsistent state with example.
4. Explain checkpoint-based rollback recovery.
5. Explain coordinated and uncoordinated checkpointing in detail.
6. Explain types of messages in rollback recovery.
7. Explain issues in failure recovery with examples.
8. Explain log-based rollback recovery.
9. Explain DSM advantages/disadvantages.

---

### Module 5

#### Part A (3 marks)
1. Define Byzantine agreement problem.
2. Write features/components/advantages of Google File System.
3. Define flat file service and directory service components.
4. List distributed file system requirements.
5. Differentiate whole file serving and whole file caching in Andrew File System.
6. Write features of SUN-NFS.

#### Part B (14 marks)
1. Explain consensus algorithm for crash failures under synchronous systems.
2. Explain assumptions made in consensus and agreement algorithms.
3. Explain SUN-NFS / Network File System architecture with diagram.
4. Explain file service architecture in detail.
5. Discuss requirements/characteristics of distributed file systems.
6. Explain Andrew File System architecture.
7. Explain Google File System architecture and implementation.
8. Differentiate Andrew File System and NFS.

---

## Section 2 - Full Answers (OCR Corpus Based, Rewritten)

This section is rewritten for exam quality.
Long answers are in 14-mark style: definition, assumptions, algorithm steps, diagram, formulas, and conclusion.
Content is restricted to the OCR corpus listed at the top of this file.

---

### Module 1 - Long Answers (14 Marks)

#### 1) Design issues and algorithmic challenges of distributed systems

Core design functions (from OCR):
1. Communication
2. Processes
3. Naming
4. Synchronization
5. Data storage and access
6. Consistency and replication
7. Fault tolerance
8. Security
9. API and transparency
10. Scalability and modularity

How to present in answer sheet:
1. Start with definition: distributed system has autonomous nodes, no shared memory, no global clock.
2. Explain each design function in one line with an example.
3. Add implementation concern: network delay, partial failures, heterogeneity.
4. End with objective: transparency + correctness + performance under scale.

Diagram:

```text
Users/API
  |
Communication <-> Processes <-> Naming
  |
Synchronization <-> Data/Replication <-> Fault Tolerance
  |
Security + Scalability
```

#### 2) Physical concurrency vs logical concurrency

1. Physical concurrency: events overlap in real clock time.
2. Logical concurrency: no happened-before relation between events.
3. In distributed systems, logical order is primary for correctness.
4. Lamport relation is used to reason about causal order.

Diagram:

```text
P1: e1 -----> e2
P2:      f1 -----> f2

If neither e1 -> f1 nor f1 -> e1, then logically concurrent.
```

#### 3) Past cone and future cone of an event

1. Past(e): all events that can causally affect event e.
2. Future(e): all events causally affected by event e.
3. Used to reason about cuts and global states.
4. Helps identify whether a cut is consistent.

Diagram:

```text
Past(e)  ---->  e  ---->  Future(e)
```

#### 4) Models of communication network (FIFO, Non-FIFO, Causal)

OCR model points:
1. FIFO: each channel behaves as first-in-first-out queue.
2. Non-FIFO: receiver may remove messages in arbitrary order.
3. Causal ordering based on happened-before relation.

Formal property from OCR:

$$
CO:\ send(m_i) \rightarrow send(m_j) \Rightarrow rec(m_i) \rightarrow rec(m_j)
$$

OCR relation:

$$
CO \subset FIFO \subset Non\text{-}FIFO
$$

Conclusion:
1. Causal ordering simplifies algorithm design because causality is preserved by network service.

#### 5) Send and receive primitive versions

1. Send(destination, buffer), Receive(source, buffer).
2. Buffered send: data copied to intermediate buffer.
3. Unbuffered send: direct rendezvous behavior.
4. Synchronous primitives: send/receive handshake completion required.
5. Asynchronous send: control returns after copy-out from user buffer.
6. Receive may be blocking or non-blocking (from OCR notes set).

Flow diagram:

```text
Process A --Send()--> Channel/Buffer --Receive()--> Process B
```

#### 6) Global state of a distributed system

1. Global state is collection of local process states + channel states.
2. Channel state is in-transit messages.
3. Snapshot must avoid inconsistency (receive without corresponding send).
4. Used for checkpointing, deadlock detection, termination detection.

Diagram:

```text
GS = {LS1, LS2, ... , LSn} U {SC12, SC23, ...}
```

---

### Module 2 - Long Answers (14 Marks)

#### 1) Scalar time properties and implementation of logical clock

Rules from OCR:
1. R1: before each local/send/receive event at process i:

$$
C_i := C_i + d,\ d>0\ (typically\ d=1)
$$

2. R2: on receive of timestamped message with value Cmsg:

$$
C_i := max(C_i, C_{msg});\ then\ apply\ R1
$$

Properties:
1. Consistency: if $a \rightarrow b$, then $C(a) < C(b)$.
2. Total ordering with tie-breaker by process id: $(t,i)$.
3. Event counting: monotonic counters.
4. Not strong consistency: timestamp order does not imply causality in all cases.

Diagram:

```text
P1: event -> C1=C1+1 -> send(ts=C1)
P2: receive(ts) -> C2=max(C2,ts)+1
```

#### 2) Bully election algorithm (with safety and liveness)

Messages (OCR): ELECTION, ANSWER/OK, COORDINATOR.

Steps:
1. Process Pi suspects coordinator failure.
2. Pi sends ELECTION to all higher-id processes.
3. If no ANSWER within timeout T, Pi declares self coordinator and sends COORDINATOR to lower-id processes.
4. If ANSWER arrives, Pi waits for coordinator announcement.
5. Receiver of ELECTION sends ANSWER and may start higher-level election (if not already in election).
6. Highest alive process eventually wins and broadcasts COORDINATOR.

Safety:
1. Final coordinator is unique and highest-id among alive processes.

Liveness:
1. With finite delays and at least one alive process, election terminates.

Diagram:

```text
P2 -> P3,P4 : ELECTION
P4 -> P2    : ANSWER
P4 -> all   : COORDINATOR
```

#### 3) Ring-based election algorithm

Steps:
1. A process starts election token with its id.
2. Token traverses logical ring.
3. Highest id is retained/recognized.
4. Winner announcement traverses ring.
5. All processes update coordinator id.

Safety:
1. Only one winner (highest alive id).

Liveness:
1. Finite ring traversal ensures completion if channels/processes are alive enough.

Diagram:

```text
P1 -> P2 -> P3 -> P4 -> P1
    (election token circulates)
```

#### 4) Chandy-Lamport global snapshot algorithm

Assumptions (OCR): reliable FIFO channels.

Marker sending rule (OCR structure):
1. Process records own local state.
2. Sends marker on every outgoing channel before sending further application messages.

Marker receiving rule:
1. If first marker on channel C:
  - record state of C as empty,
  - record local state,
  - execute marker sending rule.
2. Else:
  - record state of C as messages received after local snapshot and before this marker.

Termination:
1. Snapshot ends after each process receives marker on all incoming channels.
2. Recorded local snapshots combine to global snapshot.

Diagram:

```text
P1 (initiator): record state; send MARKER to P2,P3
P2: first MARKER -> record state; forward MARKER
P3: first MARKER -> record state; forward MARKER
```

#### 5) Combining local snapshots into one consistent global snapshot

1. Collect all process-local snapshots.
2. Collect all recorded channel states from marker boundaries.
3. Form one global cut.
4. Check consistency condition: no receive without corresponding send inside cut.

#### 6) Spanning-tree based termination detection (token-repeat wave)

Assumptions from OCR:
1. Fixed connected graph, fixed spanning tree, root P0.
2. Reliable channels with finite delay.

Key signals:
1. Token: inward wave from leaves to root.
2. Repeat: outward wave from root to leaves if token wave indicates activity.

White/black coloring logic from OCR:
1. Nodes/tokens initially white.
2. Process turns black if it sends message.
3. Black token indicates activity in subtree.
4. Root restarts round on black token by sending Repeat.

Root declares termination only if:
1. Root is white.
2. Root is idle.
3. Root receives white token from each child.

Diagram:

```text
Leaves --token--> ... --token--> Root
Root --repeat--> ... --repeat--> Leaves
```

#### 7) Termination detection using distributed snapshots

OCR rule summary:
1. Computation termination is stable property.
2. A process going active->idle requests snapshot at all processes.
3. Request succeeds when all processes grant and take local snapshot.
4. Collected snapshot indicates termination iff:
  - all processes idle,
  - no message in transit.

#### 8) Weight-throwing based termination detection

1. Initial controlling process holds full weight.
2. Weight is split and attached to spawned computation/messages.
3. Idle processes return held weight.
4. Termination is detected when controller is idle and full weight is recollected.

Conservation formula (from OCR flow):

$$
\sum weights = 1\ (constant)
$$

#### 9) Vector time properties

Update rules from OCR notes:
1. Vector length = number of processes.
2. Local event at Pi increments component i.
3. Send attaches current vector.
4. Receive at Pj:

$$
V_j := max(V_j, V_{msg});\ then\ V_j[j] := V_j[j] + 1
$$

Properties:
1. Partial ordering (isomorphism).
2. Stronger causality capture than scalar clocks.
3. Supports event counting per process.

---

### Module 3 - Long Answers (14 Marks)

#### 1) Lamport mutual exclusion algorithm

Messages: REQUEST, REPLY, RELEASE.

Data structure:
1. Each site keeps request queue ordered by logical timestamp.

Request phase:
1. Site Si broadcasts REQUEST(tsi,i) to all.
2. Inserts own request into local queue.
3. Receiver Sj inserts request and sends timestamped REPLY.

Entry conditions from OCR:
1. L1: Si has received message with timestamp larger than (tsi,i) from all other sites.
2. L2: Si request is at top of local request queue.

Release phase:
1. On CS exit, Si removes own request and broadcasts RELEASE.
2. Receivers remove Si from queue.

Diagram:

```text
Si -> all : REQUEST(ts,i)
all -> Si : REPLY
Si enters CS when (L1 and L2)
Si -> all : RELEASE
```

#### 2) Ricart-Agrawala mutual exclusion algorithm

Messages: REQUEST, REPLY.

State:
1. Deferred-reply array RDi[] (OCR notation).

Steps:
1. Si broadcasts timestamped REQUEST.
2. Sj replies immediately if:
  - Sj not requesting/executing CS, or
  - Sj requesting but Si has higher priority timestamp.
3. Otherwise Sj defers reply and sets RDj[i] = 1.
4. Si enters CS after REPLY from all.
5. On exit, Si sends all deferred replies.

Diagram:

```text
Si -> all : REQUEST
Sj -> Si : REPLY (or defer)
Si enters CS after all REPLY
Si exit -> deferred REPLY flush
```

#### 3) Suzuki-Kasami broadcast token algorithm

OCR state variables:
1. RN array at each site.
2. LN array and token queue in token.

Requesting CS:
1. If Si has no token, increment RNi[i].
2. Broadcast REQUEST(i, sn) to all.
3. On receipt at Sj, set RNj[i] = max(RNj[i], sn).
4. If Sj has idle token and RNj[i] = LN[i] + 1, send token to Si.

Executing:
1. Si enters CS only after receiving token.

Releasing:
1. Set LN[i] = RNi[i].
2. For each process k not in token queue, if RNi[k] = LN[k] + 1, enqueue k.
3. If queue non-empty, send token to queue head.

Correctness from OCR:
1. Only one token exists -> mutual exclusion.

#### 4) Maekawa quorum-based algorithm

Key idea:
1. Each process requests permission from quorum set Ri, not from all sites.
2. Any two quorums intersect.

Steps from OCR:
1. Si sends REQUEST(i) to all sites in Ri.
2. Sj sends REPLY only if it has not granted since last RELEASE; else queue request.
3. Si enters CS after REPLY from every site in Ri.
4. On exit Si sends RELEASE(i) to all in Ri.
5. On RELEASE, Sj replies to next queued request.

Diagram:

```text
Si -> Ri members : REQUEST
Ri members -> Si : REPLY
Si enters CS
Si -> Ri members : RELEASE
```

#### 5) Wait-for graph deadlock detection

1. Build directed WFG: node = process.
2. Edge Pi -> Pj if Pi waits for resource held by Pj.
3. Detect cycle/knot.
4. Cycle implies deadlock for single-resource and AND models.

Diagram:

```text
P1 -> P2
P2 -> P3
P3 -> P1   => deadlock cycle
```

#### 6) Deadlock handling strategies in distributed systems

1. Prevention:
  - avoid one Coffman condition.
  - strict, often inefficient.
2. Avoidance:
  - grant request only if safe state remains.
  - requires near-global state knowledge, hard in distributed setup.
3. Detection and recovery:
  - allow deadlock, detect cycles, rollback/abort to break cycle.
  - practical in distributed systems.

#### 7) Deadlock models comparison

1. Single-resource model:
  - one outstanding resource request.
  - cycle in WFG => deadlock.
2. AND model:
  - multiple resources needed together.
  - cycle => deadlock.
3. OR model:
  - any one of requested resources sufficient.
  - cycle does not always imply deadlock.
4. AND-OR model:
  - combination of mandatory and optional resource sets.
5. P-out-of-Q model:
  - need any P resources out of Q.

#### 8) Quorum-based mutual exclusion vs all-site permission algorithms

From OCR comparison:
1. Lamport/RA ask all sites.
2. Quorum asks subset with overlap.
3. Message complexity lower in quorum approach.
4. Conflict resolution handled by quorum lock/reply constraints.
5. More scalable for large systems.

#### 9) Mutual exclusion performance numerical (from OCR question)

Given:
1. Synchronization delay = 3 s
2. CS execution time = 1 s

Formula:

$$
T_{per\ request} = T_{sync} + T_{CS} = 3 + 1 = 4\ s
$$

Rate:

$$
R = \frac{1}{4} = 0.25\ requests/s
$$

Per minute:

$$
0.25 \times 60 = 15\ requests/min
$$

---

### Module 4 - Long Answers (14 Marks)

#### 1) No-orphans consistency condition

OCR formal terms:
1. Depend(e): processes affected by non-deterministic event e.
2. Log(e): processes that logged e determinant in volatile memory.
3. Stable(e): predicate true if determinant of e is in stable storage.

Condition from OCR:

$$
\forall e:\ Stable(e) \Rightarrow Depend(e) \subseteq Log(e)
$$

Practical statement:
1. If a process depends on non-deterministic event, that event determinant must be stable or available in surviving memory.
2. This prevents orphan processes during recovery.

#### 2) Coordinated vs uncoordinated checkpointing

Uncoordinated:
1. Each process checkpoints independently.
2. Can lead to domino effect and cascading rollback.

Coordinated:
1. All processes take checkpoint in coordinated manner.
2. Produces consistent global checkpoint.
3. Prevents domino effect.

Diagram:

```text
Uncoordinated: P1|C1    P2|C2      P3|C3   (may be inconsistent line)
Coordinated : P1|Ck ---- P2|Ck ---- P3|Ck  (one consistent recovery line)
```

#### 3) Checkpointing and rollback recovery (full)

Definitions:
1. Checkpointing: save process state periodically.
2. Rollback recovery: restore to previous consistent checkpoint after failure.

Recovery steps:
1. Detect failure.
2. Restore latest valid checkpoint.
3. Re-execute from checkpoint.

Checkpointing classes:
1. Uncoordinated
2. Coordinated
3. Communication-induced

Message effects in rollback (OCR):
1. In-transit
2. Lost
3. Delayed
4. Orphan
5. Duplicate

#### 4) Log-based rollback recovery

Core OCR idea:
1. Log determinants of all non-deterministic events on stable storage.
2. Deterministic execution segments can be replayed from state + determinants.

Flow:
1. During failure-free execution, log non-deterministic determinants.
2. Take periodic checkpoints.
3. On failure, rollback to checkpoint and replay logged events.

Types from OCR:
1. Pessimistic logging: synchronous, safer, higher overhead.
2. Optimistic logging: asynchronous, lower overhead, may create temporary inconsistency.
3. Causal logging: balances consistency and overhead by tracking causal dependencies.

#### 5) Pessimistic vs optimistic logging

Pessimistic:
1. Log before event effect becomes visible.
2. Stronger immediate recoverability.
3. More runtime delay due to synchronous log writes.

Optimistic:
1. Log asynchronously.
2. Better runtime performance.
3. Recovery more complex; temporary orphan risk.

#### 6) Types of messages in rollback recovery

1. In-transit: sent but not yet received at failure instant.
2. Lost: sender state has send record, receiver rolled back before receive.
3. Delayed: arrives late around rollback/recovery boundary.
4. Orphan: receive exists but corresponding send rolled back.
5. Duplicate: replay/resend causes second delivery.

#### 7) Issues in failure recovery with example chain

Major issues from OCR:
1. Orphan messages
2. Cascading rollbacks
3. Lost messages
4. Delayed messages
5. Delayed orphan messages
6. Duplicate messages
7. Overlapping failures

Example pattern from OCR checkpoint figure:
1. Pi fails and rolls back to Ci,1.
2. This creates orphan message H at Pj.
3. Pj rollback can create further orphan I at Pk.
4. Cascading rollback occurs to regain consistency.
5. Message C delayed, D lost, E/F delayed orphan.

#### 8) Lamport Bakery algorithm and proof of three CS requirements

Ticket logic from OCR:
1. Process picks ticket = max(ticket[]) + 1.
2. Wait until own ticket is lexicographically smallest (ticket, process id).
3. Enter CS.
4. Exit CS by setting own ticket to 0.

Proof points:
1. Mutual exclusion:
  - only lexicographically minimum ticket enters.
2. Bounded waiting:
  - once ticket assigned, others cannot overtake indefinitely.
3. Progress:
  - if CS empty, smallest ticket process proceeds.

Diagram:

```text
P1: ticket 3
P2: ticket 5
P3: ticket 3 (tie -> higher pid waits)

Order: (3,P1) -> (3,P3) -> (5,P2)
```

#### 9) Consistent vs inconsistent state

Consistent state:
1. If receive(m) is in state, send(m) is also in state.

Inconsistent state:
1. receive(m) appears but send(m) absent due to rollback.
2. Such state cannot occur in failure-free execution.

#### 10) DSM issues and advantages/disadvantages

Implementation issues from OCR:
1. Sharing semantics definition.
2. Replication strategy and placement.
3. Data location tracking.
4. Communication overhead control.

Advantages:
1. Easier sharing abstraction.
2. Single address space view.
3. Locality benefits.
4. Cost-effective scaling.

Disadvantages:
1. Consistency rule complexity.
2. Heavy message traffic possible.
3. Not always optimal for specialized workloads.

---

### Module 5 - Long Answers (14 Marks)

#### 1) Consensus algorithm for crash failures under synchronous systems

OCR assumptions:
1. Up to f crash failures.
2. Synchronous rounds; bounded delay.
3. In f+1 rounds, at least one round has no failures.

OCR pseudocode skeleton:
1. Initialize local value x.
2. For round = 1 to f+1:
  - if x not yet broadcast, broadcast(x)
  - receive values yj in this round
  - update $x := min(x, yj)$
3. Output x as consensus value.

Properties from OCR:
1. Agreement
2. Validity
3. Termination

Complexity from OCR:

$$
Message\ complexity = O((f+1)n^2)
$$

Lower bound from OCR:

$$
Rounds\ needed \ge f+1
$$

#### 2) Assumptions in consensus and agreement algorithms

From OCR corpus:
1. Crash-only failures for this variant.
2. Round-based synchronous execution.
3. Detect non-response via timeout.
4. Agreement/Validity/Termination must hold.
5. Byzantine agreement (separate definition) also requires all non-faulty decide same value.

Byzantine short definition points from OCR:
1. Agreement: all non-faulty processes decide same value.
2. Validity: if source is non-faulty, decision equals source value.
3. Termination: every non-faulty process eventually decides.

#### 3) File service architecture (with neat diagram and operations)

Three components from OCR:
1. Flat file service (content operations via UFID)
2. Directory service (name -> UFID mapping)
3. Client module (bridge and cache)

Architecture diagram (OCR-aligned):

```text
Client Computer                         Server Computer
---------------                        -----------------
Application Program                    Directory Service
     |                                       |
Client Module  ------------------------>  Flat File Service
     |
  Local cache
```

Operation steps from OCR:
1. User requests file name.
2. Client module queries directory service for UFID.
3. Directory returns UFID.
4. Client module calls flat file service with UFID.
5. Flat file service performs read/write/create/delete/get/set attributes.

Core operations from OCR:
1. Read(i,n)
2. Write(i,data)
3. Create()
4. Delete(UFID)
5. GetAttributes(UFID)
6. SetAttributes(UFID,newData)

#### 4) Distributed file system requirements

OCR requirement set:
1. Access transparency
2. Location transparency
3. Mobility transparency
4. Performance transparency
5. Scaling transparency
6. Concurrent updates
7. File replication
8. Hardware/OS heterogeneity
9. Fault tolerance
10. Consistency
11. Security
12. Efficiency

#### 5) Andrew File System architecture

OCR components:
1. Vice (server-side file service)
2. Venus (client-side cache manager)

Workflow:
1. Client opens file.
2. Server sends whole file copy.
3. Client caches whole file locally.
4. User edits local copy.
5. On close, updates pushed to server.

Consistency mechanism from OCR:
1. Callback promise from server.
2. If file changes elsewhere, callback invalidates cached copy.
3. Client fetches fresh copy.

#### 6) Google File System architecture and implementation

OCR architecture:
1. Master server: metadata and chunk location tracking.
2. Chunk servers: store data chunks and replicas.
3. Clients: ask master for locations, then talk directly to chunk servers.

Read flow from OCR:
1. Client asks master for chunk locations.
2. Master returns chunk server list.
3. Client reads chunks directly from chunk servers.

Write flow from OCR:
1. Client sends write request to master.
2. Master selects/returns chunk server targets.
3. Client writes chunks (typically 64MB chunking in OCR notes).
4. Replication applied for fault tolerance.

#### 7) AFS vs NFS

OCR-supported comparison:
1. AFS server is stateful (tracks opened files/callback relation).
2. NFS server is stateless (as per OCR comparison line).
3. AFS uses whole-file caching aggressively at client.
4. NFS commonly represented with client/server RPC architecture.

#### 8) SUN-NFS / Network File System architecture

Recovered OCR architecture labels:
1. Client side system call layer
2. Client VFS layer
3. NFS client
4. RPC client stub
5. Network
6. RPC server stub
7. NFS server
8. Server VFS layer
9. Local file system interface
10. Server side system call layer

Diagram (constructed only from OCR-recognized labels):

```text
Client                                             Server
------                                             ------
System call layer                                  System call layer
    |                                                   |
   VFS layer                                        VFS layer
    |                                                   |
  NFS client ---- RPC client stub === Network === RPC server stub ---- NFS server
                                        |
                                Local file system interface
```

Note on source quality:
1. OCR on this specific NFS figure is partially degraded; labels above are only those recovered from OCR text of the source PDF.

---

## Final Source Integrity Note
1. Question section is unchanged.
2. Answers are rewritten using only content present in the OCR corpus/PDF extraction outputs listed at top.
3. For NFS, only OCR-recovered labels and statements are used because the scanned diagram text is partially degraded in source.
