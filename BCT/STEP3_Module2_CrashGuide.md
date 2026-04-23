# STEP 3: Module 2 Crash Guide (Blockchain Architecture and Decentralization)

Module focus:
- Blockchain internals and layered design
- Decentralization methods and ecosystem logic
- Diagram-heavy answer preparation

---

## 1) Blockchain Definition and Terminology

Definition:
Blockchain is a peer-to-peer distributed append-only ledger updated through consensus.

Must-write terms:
1. Transaction
2. Block
3. Previous hash
4. Nonce
5. Merkle root
6. Genesis block
7. Consensus

---

## 2) Working of Blockchain (Step Answer)

1. User creates and signs transaction.
2. Transaction is broadcast to P2P network.
3. Nodes validate transaction rules and signatures.
4. Valid transactions are grouped into candidate block.
5. Consensus mechanism decides valid next block.
6. New block is appended with previous hash pointer.
7. Updated ledger state is replicated across nodes.

Process sketch:
```text
Create TX -> Broadcast -> Validate -> Form Block -> Consensus -> Append -> Replicate
```

---

## 3) Layered Architecture

Six-layer reference stack:
1. Network layer
2. P2P propagation layer
3. Cryptography layer
4. Consensus layer
5. Execution layer
6. Application layer

Diagram:
```text
+ Application (DApps)
+ Execution (TX/VM)
+ Consensus (PoW/PoS/BFT)
+ Cryptography (Hash/Signatures)
+ P2P (Discovery/Propagation)
+ Network (Internet)
```

---

## 4) Centralized vs Decentralized Systems

| Aspect | Centralized | Decentralized |
|---|---|---|
| Control | Single authority | Shared protocol governance |
| Failure risk | Single point of failure | Fault tolerance through replication |
| Trust model | Institution-based | Protocol and cryptography based |
| Censorship resistance | Lower | Higher |
| Upgrade coordination | Easier centrally | Harder multi-party |

---

## 5) Methods to Achieve Decentralization

1. Distributed ledger replication among peers.
2. Consensus-driven state transition approval.
3. Open node participation and validation.
4. Cryptographic verification of actions.
5. Incentive mechanisms for honest behavior.

---

## 6) Benefits, Features, Limitations

## Benefits
1. Transparency and traceability.
2. Tamper-evident history.
3. Reduced dependency on central intermediary.
4. Better auditability.

## Features
1. Append-only record structure.
2. Cryptographic linking of blocks.
3. Consensus-based updates.

## Limitations
1. Throughput and scalability limits.
2. Storage and communication overhead.
3. Governance and upgrade complexity.

---

## 7) Consensus Categories (Module 2 Level)

1. Proof-based consensus (for example PoW, PoS).
2. Fault-tolerant consensus family (CFT/BFT style).

Note for exam:
Detailed protocol treatment belongs to Module 3.

---

## 8) Module 2 Final Drill

1. Write 7-step blockchain workflow without notes.
2. Draw layered architecture once from memory.
3. Prepare one central vs decentralized table.
4. Memorize 4 benefits, 3 features, 3 limitations.
