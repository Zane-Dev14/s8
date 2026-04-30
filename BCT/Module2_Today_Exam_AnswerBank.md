# CST428 Blockchain Technologies (BCT) — Module 2 Answer Bank (Architecture + Decentralization)
Date: 30 Apr 2026

Built from your extracted QPs + Module‑2 crash guide.

---

## 0) Acronyms
- **P2P**: Peer-to-Peer
- **TX**: Transaction
- **DLT**: Distributed Ledger Technology
- **PoW/PoS**: Proof of Work / Proof of Stake

---

## 1) Part A (5 marks each; write exactly 5 points)

### A1) Define blockchain + key terminologies (QP: Oct 2023)
1. Blockchain is a distributed append-only ledger maintained by a peer network.
2. **Transaction** is a signed state-change request.
3. **Block** groups transactions and references previous block hash.
4. **Genesis block** is the first block with no previous hash.
5. **Consensus** is the protocol that decides the next valid block.

**Mnemonic:** **T‑B‑G‑C‑H** → Transaction, Block, Genesis, Consensus, Hash‑link.

### A2) Centralized vs decentralized systems (QP: May 2024)
1. Centralized: single authority; decentralized: shared control among nodes.
2. Centralized has single point of failure; decentralized is fault-tolerant via replication.
3. Centralized trust is institution-based; decentralized trust is protocol/crypto-based.
4. Decentralized is more censorship resistant.
5. Decentralized upgrades/governance need coordination.

**Mnemonic:** **C5** → **C**ontrol, **C**rash point, **C**redibility model, **C**ensorship, **C**oordination.

### A3) Ecosystem of decentralization (QP: June 2023)
1. Many independent nodes replicate the ledger.
2. Open participation reduces reliance on a single operator.
3. Cryptography authenticates actions (signatures/hashes).
4. Consensus orders transactions into one history.
5. Incentives discourage dishonest behavior.

**Mnemonic:** **R‑O‑C‑C‑I** → Replication, Open nodes, Cryptography, Consensus, Incentives.

---

## 2) Expanded (10 marks style) answers (use if question comes as Part‑B)

### B1) Working of blockchain (step answer + mini diagram)
1. User creates and signs a transaction.
2. Transaction is broadcast to P2P network.
3. Nodes validate signature and protocol rules.
4. Valid transactions enter mempool.
5. A proposer/miner/validator forms a candidate block.
6. Consensus chooses the next block (PoW/PoS/BFT).
7. Block is appended with previous hash pointer.
8. Nodes verify and update their local copy.
9. Ledger state becomes consistent across network.
10. The chain becomes tamper-evident due to hash linking.

**Mnemonic:** **C‑B‑V‑M‑F‑C‑A‑R** → Create, Broadcast, Validate, Mempool, Form, Consensus, Append, Replicate.

**Diagram:**
```text
Create TX -> Broadcast -> Validate -> Form Block -> Consensus -> Append -> Replicate
```

### B2) Layered architecture of blockchain (draw-ready)
1. **Network layer**: underlying internet connectivity.
2. **P2P layer**: discovery and gossip/propagation.
3. **Cryptography layer**: hashing, signatures, identity.
4. **Consensus layer**: agreement on next block/state.
5. **Execution layer**: transaction processing/VM.
6. **Application layer**: DApps/services using the chain.
7. Layering improves modularity and reasoning.
8. Security depends on crypto + consensus layers.
9. Performance depends on network + P2P + consensus.
10. Apps interact through transactions and reads.

**Mnemonic:** **N‑P‑C‑C‑E‑A** → Network, P2P, Crypto, Consensus, Execution, Application.

**How to draw (10 seconds):**
```text
+ Application
+ Execution
+ Consensus
+ Cryptography
+ P2P
+ Network
```

### B3) Methods to achieve decentralization
1. Replicate ledger across many nodes.
2. Use consensus to approve updates.
3. Enable open/permissionless participation (where applicable).
4. Use cryptography to verify ownership and actions.
5. Use incentives/penalties to align behavior.
6. Avoid single admin keys/single servers.
7. Use transparent rules and public verification.
8. Provide redundancy and multiple implementations.
9. Encourage diverse validators/miners.
10. Use governance that distributes decision power.

**Mnemonic:** **R‑C‑O‑C‑I** → Replication, Consensus, Open participation, Cryptography, Incentives.

### B4) Benefits, features, limitations of blockchain
1. Benefits: transparency and traceability.
2. Benefits: tamper-evident history.
3. Benefits: reduced intermediary dependence.
4. Features: append-only blocks with hash links.
5. Features: consensus-based state updates.
6. Features: cryptographic verification.
7. Limitations: scalability/throughput constraints.
8. Limitations: storage and communication overhead.
9. Limitations: governance/upgrade complexity.
10. Limitations: privacy challenges (needs careful design).

**Mnemonic:** **TT‑RC / AHC / SSGP** → **T**ransparency‑**T**raceability, **R**educed intermediaries, **C**orrectness (tamper‑evident) / **A**ppend‑**H**ash‑**C**onsensus / **S**calability, **S**torage, **G**overnance, **P**rivacy.
