# Distributed Computing - OCR Supported Complete Answer Bank

Course: CST402 Distributed Computing

Rule used in this file:
- Every Part A answer has exactly 5 points.
- Every Part B answer has exactly 10 points.
- Wording is constrained to OCR-supported content from the DC OCR corpus.

OCR support used:
- DC/ocr_output/CST402_papers_merged.txt
- DC/ocr_output/Model_QP_Solved.txt
- DC/ocr_output/DCSeries1.txt
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Dcmod2.txt
- DC/ocr_output/DCmod3.txt
- DC/ocr_output/dcMod4.txt

---

## Module 1

### Part A (3 marks)

#### 1) List the characteristics/features of a distributed system.
1. A distributed system is made of multiple autonomous computers that cooperate.
2. There is no shared memory; processes communicate through message passing.
3. There is no single global clock across all nodes.
4. Components can be geographically distributed and heterogeneous.
5. It targets resource sharing, scalability, reliability, and remote access.

#### 2) Define causal precedence relation in distributed executions.
1. Causal precedence is Lamport happened-before relation between events.
2. If two events are in same process and one occurs earlier, it causally precedes.
3. If one event is send of message and other is receive of same message, send precedes receive.
4. The relation is transitive across event chains.
5. Events with no causal relation in either direction are concurrent.

#### 3) Explain transparency requirements of distributed systems.
1. Access transparency hides differences between local and remote access.
2. Location transparency hides physical location of resources.
3. Concurrency and replication transparency hide simultaneous access and replica management.
4. Failure and mobility transparency hide failures and movement of users/resources.
5. Performance and scaling transparency hide load changes and system growth.

#### 4) Explain different forms/meaning of load balancing in distributed systems.
1. Load balancing means distributing work across nodes to avoid overload at one node.
2. It is used to maintain performance transparency during varying demand.
3. It improves response time and throughput by sharing requests.
4. It supports scalability transparency when nodes are added.
5. It improves resource utilization by shifting work to less loaded machines.

#### 5) Explain the advantages of distributed systems.
1. Resources and services can be shared among many users and processes.
2. Reliability improves because one node failure need not stop whole service.
3. Scalability is achieved by adding more machines.
4. Parallel and distributed execution can improve performance.
5. Users can access services remotely with transparent operation.

#### 6) What do you mean by a distributed system?
1. It is a collection of independent computers cooperating as one system view.
2. The computers communicate by messages, not shared memory.
3. Each node has local state and local clock.
4. System behavior is coordinated through distributed algorithms.
5. To users, resource access is presented with transparency.

### Part B (14 marks)

#### 1) Explain design issues and algorithmic challenges of distributed systems.
1. Core design functions include communication, process management, naming, and synchronization.
2. Data storage and access must be designed with consistency and replication control.
3. Fault tolerance must handle crashes, delays, and partial failures.
4. Security must address authentication, authorization, and secure communication.
5. API design must provide transparency while hiding distribution complexity.
6. Scalability and modularity are required as users and nodes increase.
7. Message ordering and timing uncertainty complicate correctness proofs.
8. Heterogeneous hardware and software environments must interoperate.
9. Reliable recovery and stable-state reasoning are needed for long-running services.
10. Final challenge is balancing correctness, performance, and transparency simultaneously.

#### 2) Compare logical concurrency and physical concurrency.
1. Physical concurrency refers to overlap in real time on different processors/nodes.
2. Logical concurrency refers to events with no happened-before relation.
3. Two physically overlapping events may still be causally related through messaging.
4. Two physically separate events can be logically concurrent if causality is absent.
5. Logical clocks are used to reason about logical ordering.
6. Physical clocks alone are insufficient due to no global synchronized time.
7. Logical concurrency is central for proving distributed algorithm correctness.
8. Physical concurrency is central for performance and throughput analysis.
9. Concurrency reasoning often uses cuts, past, and future in execution diagrams.
10. Hence distributed algorithms prioritize logical relations over pure wall-clock order.

#### 3) Explain past cone and future cone of an event.
1. In a space-time execution diagram, each event has causally related predecessors.
2. Past of event e contains events that can affect e via happened-before relation.
3. Future of event e contains events that are causally affected by e.
4. A cut divides execution into PAST and FUTURE event sets.
5. Every cut corresponds to one global state of processes and channels.
6. Past/future cones help identify consistent and inconsistent observation points.
7. A consistent cut does not include receive without corresponding send.
8. These cones provide graphical reasoning for global-state algorithms.
9. They are used in snapshot and recovery analysis.
10. Formal view: causality relation defines membership in past and future sets.

#### 4) Explain applications of distributed computing.
1. OCR material highlights mobile and pervasive/ubiquitous systems as distributed applications.
2. Sensor-network style systems use distributed nodes for data collection/processing.
3. Cloud-backed services use distributed servers for scale and reliability.
4. Large web and storage platforms rely on distributed access and replication.
5. Distributed computing supports remote resource sharing and collaboration.
6. High-availability services use distribution for fault tolerance.
7. Parallel workloads are split across nodes for speed.
8. User-facing services hide node locations via transparency.
9. Distributed design supports growth from small to very large deployments.
10. Core motivation is reliability, scalability, and efficient shared resource use.

#### 5) Explain models of communication networks / service models.
1. OCR defines three models: FIFO, Non-FIFO, and causal ordering.
2. FIFO model preserves send order per channel at receive side.
3. Non-FIFO model may deliver messages in arbitrary order.
4. Causal ordering enforces delivery consistent with happened-before relation.
5. Causal property: if send(m1) -> send(m2), then rec(m1) -> rec(m2).
6. Causal ordering is stronger than pure non-FIFO behavior.
7. Causal ordering simplifies distributed algorithm design.
8. Service model chosen affects protocol assumptions and proofs.
9. Message delivery model impacts synchronization complexity.
10. Therefore model specification is a first-class design decision.

#### 6) Explain different versions of send and receive primitives for distributed communication.
1. Basic primitives are Send(destination, buffer) and Receive(source, buffer).
2. Send can be buffered, where data is copied into communication buffer.
3. Send can be unbuffered, requiring direct rendezvous behavior.
4. Primitives can be synchronous with sender-receiver handshake completion.
5. Send can be asynchronous where control returns after local copy-out.
6. Receive side behavior can be blocking or non-blocking in OCR note set.
7. Primitive choice affects waiting behavior and throughput.
8. Primitive choice also affects message loss/retry/recovery handling.
9. Correct algorithm design depends on primitive semantics.
10. Hence communication primitives are central to distributed program behavior.

#### 7) Discuss global state of distributed systems.
1. Global state is collection of local process states plus channel states.
2. Process state includes registers, stack, local memory, and application context.
3. Channel state is the set of in-transit messages.
4. Internal, send, and receive events change process/channel states.
5. Snapshot algorithms record these states consistently.
6. Without global clock, snapshot timing must be protocol-driven.
7. Inconsistent snapshots can include impossible receive/send combinations.
8. Consistent global state is required for recovery and termination checks.
9. Cut-based representation maps directly to global states.
10. Snapshot tools like marker-based methods capture this safely.

#### 8) Relate a computer system to a distributed system with neat sketches.
1. Single computer system has centralized processor/memory and local control.
2. Distributed system has multiple processors with local memories and message links.
3. Single system uses direct memory access; distributed system uses message passing.
4. Single system has one local clock view; distributed system has no common global clock.
5. Single system failure may halt service; distributed design can continue with surviving nodes.
6. Single system scaling is vertical; distributed system scales by adding nodes.
7. Distributed systems need transparency layer to appear unified to users.
8. Distributed correctness relies on causality and ordering protocols.
9. Sketch (single): CPU <-> Memory <-> IO in one box.
10. Sketch (distributed): Node1 <-> Node2 <-> Node3 over network, each with local memory.

---

## Module 2

### Part A (3 marks)

#### 1) What are leader election algorithms? Name any two.
1. Leader election algorithms choose one coordinator among distributed processes.
2. They are used when current coordinator fails or system starts coordination phase.
3. Correctness requires one leader view for consistent control behavior.
4. OCR covers Bully algorithm and Ring-based election algorithm.
5. These algorithms use message exchange and process identifiers to elect leader.

#### 2) Define logical clock.
1. Logical clock is a counter-based time representation for event ordering.
2. It does not represent physical time; it represents causality/order information.
3. Each process maintains local logical clock value.
4. Clock values are updated on local/send/receive events.
5. Logical clocks support happened-before reasoning in distributed systems.

#### 3) Define termination detection.
1. Termination detection decides when distributed computation has fully finished.
2. Condition requires all processes passive (idle) globally.
3. Condition also requires no messages in transit.
4. Detection must be done without breaking normal computation semantics.
5. It is a stable property once true.

#### 4) What are the basic properties/rules of scalar time?
1. R1: before each event, process increments local scalar clock.
2. R2: on receive, process sets clock to max(local, received) then increments.
3. Consistency: if a -> b, then C(a) < C(b).
4. Total ordering can be obtained using pair (timestamp, process id).
5. Scalar time gives logical ordering but not full strong causality equivalence.

#### 5) Specify issues in recording a global state.
1. No global clock exists, so simultaneous capture is not directly possible.
2. Messages may be in transit at snapshot boundary.
3. Need rules to decide whether message belongs to process or channel state.
4. Independent local snapshots can produce inconsistent global cut.
5. Coordination protocol is needed to capture meaningful consistent state.

#### 6) Define vector time.
1. Vector time uses vector of counters, one slot per process.
2. It tracks local progress and known progress of others.
3. On local event, process increments its own vector component.
4. On receive, process performs component-wise max and then increments own component.
5. Vector clocks capture partial order and concurrency more precisely than scalar clocks.

### Part B (14 marks)

#### 1) Explain basic properties of scalar time and logical clock implementation.
1. Each process Pi maintains scalar clock Ci.
2. Local rule R1: before event execution, set Ci := Ci + d, usually d=1.
3. Message rule R2: piggyback timestamp in sent messages.
4. On receive at Pi with Cmsg, set Ci := max(Ci, Cmsg), then apply R1.
5. Property: if event a happened-before b, then C(a) < C(b).
6. Ties can occur across processes; break using process identifier.
7. Scalar clocks provide global sortable labels (t, pid).
8. They support event counting due to monotonic increment.
9. They do not fully encode causality equivalence (no strong consistency).
10. Implementation is lightweight and widely used in distributed protocols.

#### 2) Illustrate bully algorithm and discuss liveness and safety.
1. Bully assumes process with highest id among alive nodes becomes coordinator.
2. On coordinator failure detection, process Pi sends ELECTION to all higher-id nodes.
3. If no answer within timeout T, Pi declares itself coordinator.
4. If higher node replies, Pi waits for coordinator announcement.
5. A receiver of ELECTION sends answer and may start election unless already active.
6. Winner announces via COORDINATOR message to others.
7. Safety: at convergence, only one highest alive process acts coordinator.
8. Liveness: with finite delays and alive processes, election completes.
9. Recovering high-id process can re-run election and take leadership.
10. Message types used: ELECTION, ANSWER/OK, COORDINATOR.

#### 3) Explain ring-based election algorithm with example.
1. Processes are organized in logical ring structure.
2. Process detecting failure starts election token circulation.
3. Election message traverses ring and carries candidate information.
4. Highest process id encountered becomes winner.
5. Winner announcement then circulates around ring.
6. All processes update coordinator id after announcement receipt.
7. Safety holds because one maximum id is selected.
8. Liveness holds if ring links and active nodes can forward token.
9. Example: P2 starts; token passes P3, P4, P1; P4 highest so elected.
10. Ring method is simple and deterministic in topology-aware systems.

#### 4) Explain Chandy-Lamport algorithm in detail.
1. Assumes reliable FIFO channels and marker control messages.
2. Initiator records local state and sends marker on all outgoing channels.
3. On first marker receive, process records local state and marks that channel empty.
4. Process then sends markers on all outgoing channels before normal messages.
5. For other incoming channels, record all messages until marker arrives on each.
6. Marker separates pre-snapshot and post-snapshot channel traffic.
7. Channel state is messages recorded between local-state record and marker arrival.
8. Algorithm ends when each process gets marker on all incoming channels.
9. Local snapshots and channel states are combined to global snapshot.
10. Method captures consistent cut without stopping normal computation.

#### 5) Explain how local snapshots are combined to form global snapshot in Chandy-Lamport.
1. Each process contributes one recorded local state.
2. Each incoming channel contributes one recorded channel state.
3. First marker event defines process snapshot boundary.
4. Messages before boundary are process/channel history; after boundary excluded.
5. For first-marker channel at process, channel state recorded as empty.
6. For other channels, state is set of in-transit messages before marker arrival.
7. Aggregating all process and channel records forms candidate global state.
8. Marker protocol guarantees this state is a consistent cut.
9. Multiple initiators can run if snapshot instances are distinguished by identifiers.
10. Collected snapshot supports stable-property checks like termination.

#### 6) Explain spanning-tree-based termination detection algorithm.
1. System uses fixed spanning tree with root process P0.
2. Leaf nodes initially hold tokens and send token to parent when they become idle.
3. Parent sends token upward only after it is idle and received child tokens.
4. Token wave contracts from leaves toward root.
5. White/black coloring tracks whether message-sending occurred in subtree.
6. If root receives black token information, root sends repeat wave outward.
7. Repeat signal reaches leaves and starts next token collection round.
8. Root declares termination only if root idle, root white, and all child tokens white.
9. This ensures no hidden activity or in-transit work remains.
10. Algorithm repeats token/repeat waves until stable termination is detected.

#### 7) Explain termination detection rules using distributed snapshots with assumptions.
1. Assumption: communication channels are reliable with finite but arbitrary delay.
2. Assumption: processes are active/idle and only active processes send computation messages.
3. Assumption: snapshot control should not interfere with ongoing computation.
4. There is a unique process that became idle last for successful request.
5. On active-to-idle transition, process requests all nodes to take local snapshot.
6. Receivers grant request and record snapshot if requester is considered later idle.
7. Request is successful when all processes record snapshot for that request.
8. Collected snapshots form global state for that request id.
9. Termination is detected if all processes are idle and no messages are in transit.
10. Since termination is stable, a consistent snapshot after termination must capture it.

#### 8) Explain weight-throwing based termination detection.
1. Controller starts computation with total weight normalized to one.
2. When work/message is delegated, associated fraction of weight is transferred.
3. Active process may split weight among outgoing tasks/messages.
4. Idle process returns held weight back toward controller.
5. Weight conservation invariant is maintained across system.
6. If delayed messages exist, corresponding weight is still outside controller.
7. Controller tracks returning weight and own activity state.
8. Termination condition: controller idle and full initial weight recollected.
9. This condition implies no active process and no pending computation message.
10. Method is practical for asynchronous distributed computation detection.

#### 9) Explain properties of vector time.
1. Vector time gives each event an N-dimensional timestamp for N processes.
2. Update rule on local event: increment own vector component.
3. Update rule on send: attach full current vector timestamp.
4. Update rule on receive: component-wise max of local and received, then increment own slot.
5. If V(a) < V(b) component-wise, then a causally precedes b.
6. If neither V(a) < V(b) nor V(b) < V(a), events are concurrent.
7. It preserves partial-order isomorphism with causality.
8. It provides stronger consistency information than scalar clocks.
9. It also preserves per-process event-count information.
10. Cost is larger timestamp size and merge operations.

#### 10) What is consistent global state?
1. Global state contains process local states plus channel states.
2. A state is consistent if it could occur in failure-free execution.
3. It cannot contain receive event without corresponding send event.
4. In cut view, consistency means causal closure of recorded past.
5. Inconsistent states are obsolete/incomplete combinations from remote observation.
6. Consistent snapshots are required for safe recovery and termination checks.
7. Marker-based snapshot algorithms are designed to guarantee consistency.
8. Channel state handles in-transit messages to preserve correctness.
9. Consistency avoids orphan-like impossible histories.
10. Therefore consistent global state is the valid basis for distributed control decisions.

---

## Module 3

### Part A (3 marks)

#### 1) List performance evaluation metrics of mutual exclusion algorithms.
1. Message complexity per critical-section request.
2. Synchronization delay between consecutive critical-section executions.
3. Response time from request to entry.
4. Throughput under load.
5. Fairness/starvation behavior.

#### 2) List requirements of mutual exclusion algorithms.
1. Safety: at most one process in critical section at any time.
2. Liveness: system must continue making progress.
3. No deadlock while processes request access.
4. No starvation for any requesting process.
5. Fairness in serving requests.

#### 3) Compare token-based and non-token-based mutual exclusion approaches.
1. Token-based approach grants entry only to token holder.
2. Non-token approach grants entry via permission messages.
3. Token-based generally uses fewer messages per entry.
4. Non-token approach avoids token-loss recovery problem.
5. Token-based may be faster under high load; non-token has higher message overhead.

#### 4) List strategies for deadlock handling in distributed environment.
1. Deadlock prevention.
2. Deadlock avoidance.
3. Deadlock detection.
4. Deadlock recovery by rollback/abort.
5. Cleanup of stale wait-for information to avoid phantom detections.

#### 5) Explain issues in deadlock detection.
1. Distributed wait-for graph is fragmented across sites.
2. Delayed or stale information can cause phantom deadlocks.
3. Algorithm must satisfy progress and safety conditions.
4. Cycle detection over distributed state is expensive.
5. Detected deadlock requires careful cycle-breaking and state cleanup.

#### 6) Describe how quorum-based mutual exclusion differs from other categories.
1. Quorum method asks only subset of sites, not all sites.
2. Quorums are designed to overlap to enforce mutual exclusion.
3. Message complexity is usually lower than all-site permission methods.
4. A quorum member grants one conflicting request at a time.
5. It scales better in larger systems with reduced communication.

#### 7) Numerical: find CS request rate when synchronization delay is 3 s and average CS time is 1 s.
1. Given synchronization delay = 3 seconds.
2. Given critical-section execution time = 1 second.
3. Total time per request = 3 + 1 = 4 seconds.
4. Request rate = 1/4 requests per second = 0.25 requests/second.
5. Equivalent rate = 15 requests per minute.

### Part B (14 marks)

#### 1) Explain Lamport's mutual exclusion algorithm.
1. Every site maintains logical clock and request queue sorted by timestamp.
2. Requesting site Si broadcasts REQUEST(ts,i) to all sites and queues own request.
3. Receiver Sj queues request and sends timestamped REPLY to Si.
4. Entry condition L1: Si has received messages with timestamp greater than its request from all others.
5. Entry condition L2: Si request is at top of local queue.
6. Si enters critical section only when both conditions hold.
7. On exit, Si removes own request and broadcasts RELEASE.
8. Receivers remove Si request on RELEASE receipt.
9. FIFO channel ordering is required by this algorithm.
10. It is fair because request service order follows logical timestamps.

#### 2) Explain Ricart-Agrawala mutual exclusion algorithm.
1. Algorithm uses two messages: REQUEST and REPLY.
2. Requesting process broadcasts timestamped REQUEST to all peers.
3. Receiver replies immediately if not requesting/executing, or if requester has priority.
4. Otherwise receiver defers reply and records deferred state.
5. Priority is based on Lamport timestamp and tie-break by process id.
6. Requester enters critical section after receiving REPLY from all.
7. On exit, process sends all deferred REPLY messages.
8. Deferred-reply bookkeeping array is maintained locally.
9. Only one request can satisfy global reply condition at a time.
10. Communication overhead is lower than Lamport in message types used.

#### 3) Explain Suzuki-Kasami broadcast algorithm.
1. It is a token-based mutual exclusion algorithm with one unique token.
2. Each process keeps request numbers RN; token carries last-served numbers LN and queue.
3. Process without token increments own RN and broadcasts REQUEST(i,sn).
4. Receiver updates RN using max of old and incoming sequence number.
5. Idle token holder sends token if request is outstanding condition RN[i]=LN[i]+1.
6. Process enters critical section only after receiving token.
7. On exit, token holder sets LN[i]=RN[i].
8. It appends pending requesters to token queue using RN/LN test.
9. Token passed to next queued requester if queue non-empty.
10. Correctness: single token guarantees mutual exclusion.

#### 4) Explain Maekawa's mutual exclusion algorithm with example.
1. Maekawa is quorum-based; each process has request set Ri.
2. Requesting process sends REQUEST to all members of Ri.
3. A quorum member grants REPLY only if it has not granted since last RELEASE.
4. If already granted, incoming requests are queued.
5. Requester enters critical section only after receiving all REPLYs from Ri.
6. On exit, requester sends RELEASE to all quorum members.
7. On RELEASE, quorum member grants next queued request if any.
8. Any two quorums intersect, preventing simultaneous conflicting entry.
9. Example: if P1 and P2 request together, common quorum node serializes grant order.
10. This reduces message count compared to all-site permission approaches.

#### 5) Explain wait-for graph based deadlock detection with example.
1. Build directed wait-for graph where nodes are processes.
2. Edge Pi -> Pj exists if Pi waits for resource held by Pj.
3. Collect local wait information from distributed sites.
4. Detect cycle or knot in combined graph.
5. In single-resource/AND models, cycle implies deadlock.
6. Example chain: P1->P2, P2->P3, P3->P1.
7. This cycle means each process waits forever on another in cycle.
8. To resolve, rollback or abort one process in cycle.
9. Remove stale wait edges after recovery to avoid phantom detections.
10. Continue monitoring to detect subsequent deadlocks.

#### 6) Explain deadlock handling strategies in distributed environment.
1. Prevention avoids deadlock by disallowing unsafe resource-allocation patterns.
2. Avoidance grants requests only if resulting state remains safe.
3. In distributed systems, full global-state knowledge is hard to maintain.
4. Detection allows deadlock to occur, then identifies it (e.g., WFG cycle checks).
5. Recovery breaks deadlock by rollback, preemption, or process termination.
6. Prevention can be too restrictive and waste resources.
7. Avoidance can be expensive due to dynamic state uncertainty.
8. Detection+recovery is often most practical for distributed deployments.
9. Correctness needs progress and safety (no phantom deadlocks).
10. After recovery, stale dependency data must be cleared promptly.

#### 7) Compare various models of deadlock.
1. Single-resource model: one outstanding request per process; cycle implies deadlock.
2. AND model: process needs all requested resources; cycle in WFG implies deadlock.
3. OR model: process proceeds with any one requested resource; cycle may not imply deadlock.
4. AND-OR model: mixed mandatory and optional resource requests.
5. P-out-of-Q model: process needs any P resources out of Q candidates.
6. Out-degree and cycle interpretation differ across models.
7. Detection complexity increases from single-resource to mixed models.
8. OR/AND-OR require deeper condition checks than plain cycle test.
9. Resource request semantics define model behavior.
10. Correct deadlock diagnosis must match the active request model.

#### 8) Explain differences between quorum-based and other mutual exclusion algorithms.
1. Lamport/RA typically require permission exchange with all sites.
2. Quorum method requires permissions from overlapping subset only.
3. Overlap guarantees conflicting requests meet at common grantor.
4. Message complexity is reduced in quorum approach.
5. Quorum members lock grant until RELEASE for serialization.
6. All-site methods have higher communication overhead.
7. Quorum approach generally scales better in large systems.
8. Quorum design must ensure intersection property always holds.
9. Failure handling differs because blocked quorum member can stall progress.
10. Choice depends on tradeoff among complexity, scalability, and robustness.

---

## Module 4

### Part A (3 marks)

#### 1) State advantages and disadvantages of distributed shared memory.
1. Advantage: simple shared-memory style programming over distributed nodes.
2. Advantage: single address-space abstraction and locality benefits.
3. Advantage: cost-effective with commodity systems and no single memory bottleneck.
4. Disadvantage: consistency/coherence rules are complex for programmers.
5. Disadvantage: heavy communication overhead can reduce performance.

#### 2) What are checkpoints?
1. Checkpoint is saved state of process at a time instant.
2. It is used for rollback recovery after failures.
3. It reduces amount of recomputation after crash.
4. It helps reconstruct consistent global state with other process checkpoints.
5. It is commonly stored periodically to stable storage.

#### 3) List different types of messages in rollback recovery.
1. In-transit messages.
2. Lost messages.
3. Delayed messages.
4. Orphan messages.
5. Duplicate messages.

#### 4) Explain no-orphans consistency condition.
1. Non-deterministic event determinants must be recoverable.
2. Depend(e) denotes processes whose state depends on event e.
3. Log(e) denotes processes storing determinant copies in volatile memory.
4. Stable(e) indicates determinant is on stable storage.
5. Condition ensures no surviving process depends on unrecoverable event determinant.

#### 5) Differentiate coordinated and uncoordinated checkpointing.
1. Uncoordinated: each process checkpoints independently.
2. Coordinated: processes checkpoint in coordinated global operation.
3. Uncoordinated may lead to domino effect and cascading rollback.
4. Coordinated gives consistent recovery line and avoids domino effect.
5. Coordinated has extra synchronization overhead during checkpoint phase.

#### 6) Differentiate deterministic and non-deterministic events in log-based rollback recovery.
1. Deterministic events are reproducible from prior state and program logic.
2. Non-deterministic events depend on external input/message arrival.
3. Deterministic events can be replayed without extra determinant logging.
4. Non-deterministic events require determinant logging for exact replay.
5. Recovery correctness depends on capturing all non-deterministic determinants.

#### 7) Discuss issues in implementing distributed shared memory software.
1. Define sharing semantics and consistency model clearly.
2. Decide replication policy and where copies are stored.
3. Locate correct/up-to-date data among replicas.
4. Handle coherence and update propagation efficiently.
5. Reduce excessive back-and-forth communication overhead.

### Part B (14 marks)

#### 1) Explain pessimistic and optimistic logging.
1. Log-based recovery records determinants of non-deterministic events.
2. Pessimistic logging records determinant safely before event is externally visible.
3. This gives strong immediate recoverability with low orphan risk.
4. Cost is higher runtime overhead due to synchronous logging.
5. Optimistic logging records determinants asynchronously.
6. Runtime overhead is lower in failure-free operation.
7. Recovery is more complex because temporary inconsistency can appear.
8. Dependency tracking is needed to recover correctly.
9. Pessimistic favors safety-first; optimistic favors performance-first.
10. Both are used with checkpoints to reduce rollback distance.

#### 2) Show Lamport's Bakery algorithm and verify 3 critical-section requirements.
1. Each process picks ticket number = max(current tickets)+1 when requesting CS.
2. Process waits while another process has smaller ticket.
3. If tickets equal, lower process id gets priority.
4. Process enters critical section when it has lexicographically smallest pair.
5. On exit, process resets its ticket to zero.
6. Mutual exclusion holds because only one lexicographically minimum process exists.
7. Progress holds because smallest waiting ticket eventually enters when CS free.
8. Bounded waiting holds because overtaking is limited by ticket ordering.
9. Tie-breaking by process id removes ambiguity in equal-ticket case.
10. Hence algorithm satisfies mutual exclusion, progress, and bounded waiting.

#### 3) Differentiate consistent and inconsistent state with example.
1. Consistent state can occur in normal failure-free execution.
2. It never includes receive of message without corresponding send.
3. Inconsistent state includes impossible causal combination.
4. Example consistent: A sends m1 and B receives m1, both events recorded.
5. Example inconsistent: B records receive m2 but A rolled back before sending m2.
6. Inconsistent state appears due to uncoordinated rollback/snapshot mismatch.
7. Consistent state is required for valid recovery.
8. Snapshot algorithms aim to produce only consistent states.
9. Orphan messages are key indicator of inconsistency.
10. Distributed recovery protocols eliminate such states via rollback/logging rules.

#### 4) Explain checkpoint-based rollback recovery.
1. System periodically saves checkpoints of process states.
2. On failure, affected processes roll back to last safe checkpoint.
3. Execution restarts from restored checkpoint state.
4. Recovery may involve one process or multiple dependent processes.
5. In-transit and lost/orphan messages are handled during recovery.
6. Checkpoint frequency trades runtime overhead against recovery work.
7. Coordinated checkpoints provide clear consistent recovery line.
8. Uncoordinated checkpoints can trigger cascading rollback.
9. Communication-induced checkpoints balance overhead and consistency.
10. Goal is to restore consistent global state with minimal recomputation.

#### 5) Explain coordinated and uncoordinated checkpointing in detail.
1. Uncoordinated checkpointing: each process independently saves local state.
2. Advantage: low coordination cost during normal execution.
3. Risk: inconsistent checkpoint combinations and domino effect.
4. Cascading rollback can push system to very old state.
5. Coordinated checkpointing: all processes synchronize checkpoint creation.
6. Coordinator/control protocol ensures one consistent global checkpoint.
7. Advantage: avoids domino effect and simplifies recovery.
8. Cost: synchronization messages and temporary checkpoint overhead.
9. Suitable for systems where predictable recovery is critical.
10. Both methods can be combined with message logging for stronger recovery.

#### 6) Explain types of messages in rollback recovery.
1. In-transit message: sent but not yet received at failure instant.
2. Lost message: sender retains send record but receiver rolled back before receive.
3. Delayed message: arrives after rollback boundary or after receiver restart.
4. Orphan message: receive survives but corresponding send has been undone.
5. Duplicate message: message replay/resend causes second reception.
6. In-transit usually resolved by eventual delivery/reprocessing.
7. Lost messages handled via sender-side message logging and retransmission.
8. Delayed/orphan messages require filtering by recovery rules.
9. Duplicate messages require idempotent handling or duplicate suppression.
10. Correct classification is essential for consistent post-failure state.

#### 7) Explain issues in failure recovery with examples.
1. Orphan messages arise when send rollback invalidates already-recorded receive.
2. Cascading rollback occurs when one rollback forces dependent processes to roll back.
3. Lost messages appear when receiver rollback removes received event.
4. Delayed messages can arrive around recovery window and cause confusion.
5. Delayed orphan messages may arrive even though causal send is undone.
6. Duplicate messages can appear after replay/resend.
7. Overlapping failures complicate dependency reconstruction.
8. Example chain in OCR shows Pi rollback to Ci,1 creating orphan H at Pj.
9. Pj rollback can create further orphan I at Pk, causing cascade.
10. Recovery needs logging + checkpoint policy + dependency cleanup.

#### 8) Explain log-based rollback recovery.
1. Execution consists of deterministic intervals separated by non-deterministic events.
2. Non-deterministic event determinants are logged to stable storage.
3. During failure-free run, logs and checkpoints are continuously maintained.
4. On crash, process rolls back to latest checkpoint.
5. Process replays logged determinants to reconstruct exact pre-failure behavior.
6. No-orphans condition is enforced using determinant availability.
7. Pessimistic, optimistic, and causal logging are major variants.
8. Pessimistic logs synchronously; optimistic logs asynchronously.
9. Causal logging tracks event dependencies to avoid orphan creation.
10. Result is consistent recovery with bounded recomputation.

#### 9) Explain DSM advantages/disadvantages.
1. Advantage: shields programmers from explicit send/receive message handling.
2. Advantage: single address-space style simplifies sharing of complex data.
3. Advantage: locality and distributed memory reduce single-bus bottleneck.
4. Advantage: portable interface across systems and large virtual memory view.
5. Disadvantage: consistency semantics are difficult to design and use correctly.
6. Disadvantage: replication/coherence traffic increases communication cost.
7. Disadvantage: locating latest copy and managing updates is complex.
8. Disadvantage: performance may lag specialized tightly-coupled solutions.
9. Disadvantage: frequent synchronization can reduce scalability under contention.
10. Overall, DSM offers programmability benefits with runtime coordination tradeoffs.

---

## Module 5

### Part A (3 marks)

#### 1) Define Byzantine agreement problem.
1. Byzantine agreement asks non-faulty processes to agree on one value.
2. Agreement: all non-faulty processes decide identical value.
3. Validity: if source is non-faulty, decision equals source initial value.
4. Termination: every non-faulty process eventually decides.
5. It models arbitrary fault tolerance requirements in distributed consensus.

#### 2) Write features/components/advantages of Google File System.
1. Master-server + chunk-server architecture is used.
2. Master manages metadata and chunk-location information.
3. Chunk servers store file chunks and replicas.
4. Clients ask master for locations then access chunk servers directly.
5. Replication gives fault tolerance and large-scale throughput.

#### 3) Define flat file service and directory service components.
1. Flat file service performs file-content operations using unique file identifiers.
2. Typical flat operations include read, write, create, delete, and attribute operations.
3. Directory service maps file names to file identifiers.
4. Directory service supports naming and lookup transparency.
5. Client module bridges user requests to directory and flat services.

#### 4) List distributed file system requirements.
1. Transparency (access, location, mobility).
2. Performance and scaling transparency under varying loads.
3. Concurrent updates and replication support.
4. Fault tolerance, consistency, and reliability.
5. Security, heterogeneity support, and overall efficiency.

#### 5) Differentiate whole file serving and whole file caching in Andrew File System.
1. Whole file serving sends complete file from server for access operations.
2. Whole file caching stores full file copy at client side.
3. Cached copy allows faster repeated local access.
4. Updates are synchronized back to server on close/commit.
5. Callback mechanism invalidates stale cached copies.

#### 6) Write features of SUN-NFS.
1. NFS provides network-transparent file access using client-server model.
2. It uses RPC-based communication between NFS client and NFS server.
3. VFS layer integrates local and remote file access path.
4. OCR comparison notes NFS server behavior as stateless in classic model.
5. NFS architecture includes system call layer, VFS, RPC stubs, server file interface.

### Part B (14 marks)

#### 1) Explain consensus algorithm for crash failures under synchronous systems.
1. Assume up to f crash failures among n processes.
2. Algorithm runs for f+1 synchronous rounds.
3. Each process starts with local candidate value x.
4. In each round, process broadcasts x if not already broadcast.
5. Process receives available values from peers for that round.
6. Process updates x using min-rule over received and local values.
7. After f+1 rounds, process outputs x as consensus value.
8. Agreement and validity follow from common round-based update rule.
9. Termination holds because protocol has fixed finite rounds.
10. Message complexity is O((f+1)n^2) as noted in OCR source.

#### 2) Explain assumptions made in consensus and agreement algorithms.
1. Process set size and fault bound are known.
2. Crash-failure model is assumed for synchronous crash-consensus variant.
3. Rounds are synchronous with bounded message delay.
4. Non-responding process in a round can be treated as failed.
5. All non-faulty processes execute same deterministic update rule.
6. Communication channel reliability is assumed for delivered messages in model.
7. Agreement property must hold across all non-faulty processes.
8. Validity property ties decision to proposed values/source condition.
9. Termination property requires eventual decision by every non-faulty process.
10. Byzantine definition in OCR adds same three properties under arbitrary-fault context.

#### 3) Explain SUN-NFS / Network File System architecture with diagram.
1. NFS follows client-server file-access architecture.
2. Client side includes system-call layer, VFS layer, NFS client, and RPC client stub.
3. Server side includes RPC server stub, NFS server, VFS layer, and local file interface.
4. Network RPC connects client stub and server stub.
5. Application performs open/read/write through normal file API.
6. VFS routes calls to local filesystem or NFS path.
7. NFS server executes remote file operations on server storage.
8. OCR notes classical NFS design as stateless compared with AFS.
9. Architecture diagram to draw in exam:
   Client: App -> System Call -> VFS -> NFS Client -> RPC Client Stub == Network == RPC Server Stub -> NFS Server -> VFS -> Local FS
10. This structure gives transparent remote-file access using standard interface.

#### 4) Explain file service architecture in detail.
1. File service architecture has three key parts: client module, directory service, flat file service.
2. Directory service maps names to UFIDs (unique file identifiers).
3. Flat file service handles file data operations by UFID.
4. Client module accepts user request and coordinates service calls.
5. Typical operations: Read(i,n), Write(i,data), Create(), Delete(UFID).
6. Metadata operations: GetAttributes(UFID), SetAttributes(UFID,newData).
7. Access flow: user asks file name -> directory returns UFID.
8. Client then calls flat service with UFID to fetch/update content.
9. Caching at client module improves repeated access performance.
10. Separation of naming and content improves modularity and scalability.

#### 5) Discuss requirements/characteristics of distributed file systems.
1. Access transparency so local/remote usage looks same.
2. Location transparency so file movement does not break naming.
3. Mobility transparency so clients continue access while resources move.
4. Performance transparency under dynamic multi-user load.
5. Scaling transparency for growth in users and data volume.
6. Support for concurrent updates with controlled consistency.
7. Replication for availability and load balancing.
8. Fault tolerance and high reliability under component failures.
9. Security through authentication, access control, and protection.
10. Heterogeneity and efficiency across varied platforms and networks.

#### 6) Explain Andrew File System architecture.
1. AFS is distributed file system optimized for scalable shared access.
2. Server-side component Vice stores shared files.
3. Client-side component Venus manages local cache and fetch/update logic.
4. AFS uses whole-file caching at client for speed.
5. On open, server sends file copy to client cache.
6. Client reads/writes mostly on cached local copy.
7. On close, updates are propagated back to server.
8. Callback promise mechanism maintains cache consistency.
9. If server invalidates callback, client fetches fresh file copy.
10. OCR comparison highlights AFS server statefulness for open-file tracking.

#### 7) Explain Google File System architecture and implementation.
1. GFS uses master and chunk-server architecture.
2. Master keeps metadata: namespace, chunk mapping, and placement info.
3. Chunk servers store large fixed-size chunks and replicas.
4. Client first asks master for chunk locations.
5. Client then reads/writes directly with chunk servers.
6. Read path minimizes master involvement after location lookup.
7. Write path uses master-selected chunk targets and replication.
8. Replicas improve availability and fault tolerance.
9. Master does coordination; data path remains server-client direct.
10. OCR notes this model is built for large-scale high-throughput workloads.

#### 8) Differentiate Andrew File System and NFS.
1. OCR states AFS server is stateful; NFS server is stateless in classic design.
2. AFS emphasizes whole-file caching with callback consistency.
3. NFS uses RPC file-operation model through VFS and server interface.
4. AFS tracks client-file relationships for callback invalidation.
5. NFS generally relies on stateless request handling semantics.
6. AFS can reduce repeated network reads through aggressive client cache.
7. NFS architecture is simpler in state management at server side.
8. AFS includes Venus/Vice named components in OCR material.
9. NFS architecture in OCR includes client stub, server stub, and VFS layers.
10. Both provide transparent remote file access but with different consistency/state tradeoffs.

---

## End Note

This file follows your requested structure and point count strictly:
- 5 points for every 3-mark question.
- 10 points for every 14-mark question.
