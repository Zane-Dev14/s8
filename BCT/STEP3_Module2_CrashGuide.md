# STEP 3: Module 2 Crash Guide (Blockchain Architecture + Decentralization)

Module 2 focus:
- Architecture and ecosystem understanding
- Repeated diagram-heavy long answers

Mapped from:
- BCT/module 2.md
- BCT/ocr_work/qp/questions_extracted.json

---

## Topic 1: Blockchain Definition + Terminologies

Definition:
- Blockchain is a peer-to-peer distributed, append-only ledger updated through consensus.

Must-mention terms:
1. Transaction
2. Block
3. Previous hash
4. Nonce
5. Merkle root
6. Genesis block
7. Consensus

---

## Topic 2: Working of Blockchain (High Repeat)

Step flow:
1. User creates and signs transaction
2. Transaction broadcast to P2P network
3. Nodes validate transaction
4. Valid transactions grouped into candidate block
5. Consensus mechanism approves next block
6. Block appended with previous-hash link
7. Ledger copy updated across nodes

Diagram:

```text
Create TX -> Broadcast -> Validate -> Form Block -> Consensus -> Append -> Replicate
```

---

## Topic 3: Layered Blockchain Architecture

Recommended layer sequence:
1. Network layer
2. P2P propagation layer
3. Cryptography layer
4. Consensus layer
5. Execution/transaction layer
6. Application layer (DApps/services)

Diagram:

```text
+ Application Layer
+ Execution Layer
+ Consensus Layer
+ Cryptography Layer
+ P2P Layer
+ Network Layer
```

---

## Topic 4: Centralized vs Decentralized Systems

Quick compare:
1. Control: one authority vs shared authority
2. Failure: single-point risk vs fault tolerance
3. Trust: institution-based vs protocol-based
4. Censorship resistance: lower vs higher

---

## Topic 5: Methods to Achieve Decentralization

Write these methods:
1. Distributed ledger replication
2. Consensus-driven state updates
3. Open validator/miner participation
4. Cryptographic verification
5. Incentive mechanisms for honest behavior

---

## Topic 6: Benefits, Features, Limitations

## Benefits
1. Transparency
2. Traceability
3. Tamper resistance
4. Reduced intermediary dependence

## Features
1. Append-only structure
2. Consensus-based update
3. Shared ledger copies

## Limitations
1. Scalability bottlenecks
2. Storage and communication overhead
3. Governance and upgrade complexity

---

## Topic 7: Consensus Categories (Module 2 Level)

Two major categories:
1. Proof-based (PoW/PoS style)
2. Fault-tolerance based (CFT/BFT family)

Note:
- Detailed protocol depth comes in Module 3.

---

## Module 2 PYQ Attack Set

1. Working of blockchain with neat diagram
2. Layered blockchain architecture
3. Methods to achieve decentralization
4. Ecosystem of decentralization
5. Benefits, features, limitations
6. Blockchain definition with key terminologies

---

## Last-Minute Revision Grid

1. Memorize one 7-step blockchain workflow.
2. Draw layer stack once from memory.
3. Keep one central vs decentralized mini-table ready.
4. Memorize 4-3-3 structure for benefits/features/limitations.
