# STEP 5: Module 4 Crash Guide (Recovery and Distributed Shared Memory)

Module 4 focus:
- Checkpointing and rollback recovery
- Log-based recovery and consistency conditions
- Message anomalies after rollback
- Distributed shared memory (DSM)

Mapped from OCR:
- DC/ocr_output/dcMod4.txt
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Model_QP_Solved.txt

---

## Topic 1: Consistent vs Inconsistent Global State

### Consistent state
If a receive event is present, corresponding send event is also present.

### Inconsistent state
Receive is present but corresponding send is missing.

### Quick example
- Consistent: A sent m1, B received m1, both recorded.
- Inconsistent: B recorded receive(m2), A rolled back before send(m2).

---

## Topic 2: Checkpointing

### Definition
Checkpointing saves process state so recovery can resume from saved point after failure.

### Why checkpointing
1. Reduces re-computation
2. Speeds up recovery
3. Limits rollback depth

### Types
1. Uncoordinated checkpointing
2. Coordinated checkpointing
3. Communication-induced checkpointing

---

## Topic 3: Uncoordinated vs Coordinated Checkpointing

| Feature | Uncoordinated | Coordinated |
|---|---|---|
| Checkpoint timing | Independent per process | Global coordinated checkpoints |
| Consistency | May be inconsistent | Globally consistent checkpoint |
| Domino effect | Possible | Avoided |
| Runtime overhead | Lower coordination | Coordination overhead |
| Recovery complexity | Higher | Lower |

### Domino effect (must mention)
Rollback of one process may force others to roll back repeatedly to very old checkpoints.

---

## Topic 4: Rollback Recovery

### Definition
Recovery approach where failed process rolls back to checkpoint and replays required events.

### Basic steps
1. Detect failure
2. Restore checkpoint
3. Replay events/messages
4. Rejoin normal execution

---

## Topic 5: Message Types in Rollback Recovery

Write these five types in exams:
1. In-transit message
   - Sent but not yet received at snapshot/recovery cut.
2. Lost message
   - Send recorded, receive rolled back.
3. Delayed message
   - Message arrives late relative to recovered state.
4. Orphan message
   - Receive recorded but corresponding send rolled back.
5. Duplicate message
   - Message replay causes receiver to get same message again.

### One-line memory aid
In-Transit, Lost, Delayed, Orphan, Duplicate = ILDOD

---

## Topic 6: No-Orphans Consistency Condition

### Intuition
No process should depend on an event whose determinant is unavailable after recovery.

### Terms often used
1. Depend(e): processes causally dependent on event e
2. Log(e): processes that logged determinant of e
3. Stable(e): determinant of e on stable storage

### Condition idea
If event effects survive, determinant must survive (in memory of survivor or stable storage).

---

## Topic 7: Deterministic vs Non-Deterministic Events

### Deterministic event
Outcome fully reproducible from prior state.
Example: local computation step.

### Non-deterministic event
Outcome depends on external input/timing.
Example: message receive from network.

### Recovery implication
Determinants of non-deterministic events must be logged.

---

## Topic 8: Log-Based Rollback Recovery

### Core idea
Log determinants of non-deterministic events in stable storage.
After failure, restore checkpoint and replay using logs.

### Workflow
1. Normal run: take periodic checkpoints + log determinants.
2. Failure: roll back to latest checkpoint.
3. Replay logged determinants to reconstruct same execution path.

### Three styles
1. Pessimistic logging
   - Log to stable storage before event is allowed to affect state.
   - Safer, higher overhead.
2. Optimistic logging
   - Log asynchronously.
   - Lower overhead, may need more rollback handling.
3. Causal logging
   - Hybrid style preserving causal dependencies while reducing overhead.

---

## Topic 9: Issues in Failure Recovery

High-frequency issues to list:
1. Orphan processes/messages
2. Cascading rollback
3. Lost and delayed messages
4. Duplicate replayed messages
5. Overlapping failures
6. Checkpoint inconsistency

### Cascading rollback mini narrative
Pi fails and rolls back.
Pj had consumed message from Pi that no longer exists in Pi recovered history.
Pj must roll back.
This may force Pk to roll back, and so on.

---

## Topic 10: Distributed Shared Memory (DSM)

### Definition
DSM gives illusion of shared memory over distributed machines.

### Advantages
1. Easier data sharing model
2. Single address-space abstraction
3. Exploits locality
4. Cost-effective on commodity systems
5. Portable interface across platforms

### Disadvantages
1. High communication overhead
2. Complex coherence and consistency control
3. May underperform tailored message-passing design

### Implementation issues
1. What granularity is shared (page/object/variable)?
2. What consistency model is enforced?
3. Where are replicas placed?
4. How to locate data quickly?
5. How to reduce coherence traffic?

---

## Module 4 PYQ Attack Set

1. No-orphans consistency condition
2. Coordinated vs uncoordinated checkpointing
3. Types of rollback recovery messages
4. Deterministic vs non-deterministic events
5. Log-based rollback recovery
6. Failure recovery issues with examples
7. DSM advantages and disadvantages
8. DSM software implementation issues

---

## Last-Minute Revision Grid

1. Memorize 5 rollback message types.
2. Practice one no-orphans definition answer.
3. Practice one checkpoint comparison table.
4. Memorize pessimistic vs optimistic vs causal logging.
5. Keep one cascading rollback example ready.
