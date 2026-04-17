# MODULE 2: BLOCKCHAIN ARCHITECTURE + DECENTRALIZATION (QUICK CRASH FILE)

Source used:
- OCR PYQ: May 2024, June 2023, October 2023
- Notes: M2 OCR text from `CST428-M2-Ktunotes.in.pdf` and `Module II-1.pdf`
- Scheme hints: `CST428-SCHEME_May_2024.txt`

---

## STEP 1: PRIORITY MATRIX (MODULE 2 ONLY)

| Topic | Priority | PYQ Evidence | Why Study Now |
|---|---|---|---|
| Working of blockchain with neat diagram | CRITICAL | Asked in 2023 and 2024 Part B | Guaranteed long-answer marks with diagram |
| Layered blockchain architecture | CRITICAL | Asked in Oct 2023 Part B | Direct 7-mark structure question |
| Decentralization methods/ecosystem | CRITICAL | Asked in 2023 and 2024 Part B | Repeats with wording changes |
| Benefits, features, limitations of blockchain | HIGH | Asked in 2024 and Oct 2023 | Easy scoring list format |
| Consensus basics and types | HIGH | Asked in Oct 2023 Module II | Links to Module III answers too |
| Types of blockchain | MEDIUM | Asked in Oct 2023 Part A | Fast backup 3-mark topic |

---

## STEP 2: ZERO-TO-EXAM TEACHING (NO REPETITION)

## TOPIC: Blockchain Definition + Core Properties

### What It Is
Blockchain is a peer-to-peer distributed ledger.
It is append-only and updated via consensus.

### Why Exams Love It
This appears in both short and long answers.

### Core Intuition
No central record keeper exists.
Every node holds a copy.
New data is appended after agreement.
Tampering becomes extremely hard.

### Exam-Critical Definitions
- **PEER-TO-PEER**: Nodes communicate directly without central controller.
- **DISTRIBUTED LEDGER**: Ledger copies are shared across peers.
- **APPEND-ONLY**: Data is added in time order, not edited.
- **UPDATEABLE VIA CONSENSUS**: New state accepted only after agreement.

### Diagram Description
- Draw layered view from network to applications.
- Label layers: Network, P2P, Cryptography, Consensus, Execution, Applications.

ASCII diagram:

```
Applications: DApps / Smart Contracts / Users
Execution   : Blocks / Transactions / VM
Consensus   : PoW / PoS / BFT
Crypto      : Hash / Signature / Public Key
P2P         : Gossip / Message Propagation
Network     : Internet / TCP-IP
```

### Common Exam Formats
- Define blockchain and explain key terminologies.
- Explain architecture of blockchain with neat diagram.

### Scoring Keywords
**P2P**, **DISTRIBUTED LEDGER**, **IMMUTABLE**, **APPEND-ONLY**, **CONSENSUS**.

---

## TOPIC: Layered Blockchain Architecture

### What It Is
Blockchain runs as stacked logical layers.
Each layer provides a specific service.

### Why Exams Love It
Repeated as direct 7-mark question.

### Core Intuition
Each layer depends on the lower layer.
Security and consensus support execution.
Applications run on top of all layers.

### Exam-Critical Layer Points
1. Network layer: base communication.
2. P2P layer: node-to-node propagation.
3. Cryptography layer: hashes, signatures.
4. Consensus layer: agreement protocol.
5. Execution layer: transactions, VM, smart contracts.
6. Application layer: DApps, user services.

### Diagram Description
- Draw six horizontal boxes stacked.
- Add upward arrows between layers.
- Mention user interaction at top.

ASCII diagram:

```
+-------------------------------+
| Application (DApp, DAO, User) |
+-------------------------------+
| Execution (TX, Blocks, VM)    |
+-------------------------------+
| Consensus (PoW/PoS/BFT)       |
+-------------------------------+
| Cryptography (PKI, Hash, Sig) |
+-------------------------------+
| P2P Propagation               |
+-------------------------------+
| Internet / TCP-IP             |
+-------------------------------+
```

### Common Exam Formats
- Explain layered architecture with diagram.
- Explain working of blockchain using architecture.

### Scoring Keywords
**NETWORK**, **CRYPTOGRAPHY**, **CONSENSUS**, **EXECUTION**, **APPLICATION**.

---

## TOPIC: Generic Elements of Blockchain

### What It Is
Elements are the core building blocks of chain data.

### Why Exams Love It
Part A and Part B both ask these as lists.

### Must-write Elements
- Address
- Transaction
- Block
- Previous hash
- Nonce
- Timestamp
- Merkle root
- Node
- Smart contract (platform-dependent)

### Block Structure Diagram

```
+----------------------------------+
| Block Header                     |
| - Prev Block Hash                |
| - Merkle Root                    |
| - Timestamp                      |
| - Nonce                          |
+----------------------------------+
| Transaction List                 |
| TX1, TX2, TX3, ...               |
+----------------------------------+
```

### Scoring Keywords
**MERKLE ROOT**, **NONCE**, **HASH POINTER**, **GENESIS BLOCK**.

---

## TOPIC: Decentralization in Blockchain

### What It Is
Decentralization removes single-point control and failure.

### Why Exams Love It
Asked repeatedly as methods/ecosystem/full decentralization.

### Core Intuition
No single authority owns state updates.
Consensus replaces central trust.
Competition and disintermediation reduce dependency.

### Methods to Achieve Decentralization
1. Distributed ledger replication.
2. Consensus-based validation.
3. Open participation of nodes.
4. Cryptographic verification.
5. Incentive-driven competition among validators/miners.

### Centralized vs Decentralized Quick Table

| Aspect | Centralized | Decentralized |
|---|---|---|
| Control | Single authority | Shared among nodes |
| Failure risk | Single point | Fault-tolerant |
| Trust model | Trusted intermediary | Protocol + consensus |
| Censorship resistance | Low | Higher |

### Common Exam Formats
- Explain methods used to achieve decentralization.
- Explain full ecosystem decentralization.

### Scoring Keywords
**DISINTERMEDIATION**, **FAULT TOLERANCE**, **COLLUSION RESISTANCE**, **TRUST MINIMIZATION**.

---

## TOPIC: Benefits, Features, and Limitations

### Benefits
- Transparency and shared visibility.
- Better integrity and tamper resistance.
- Reduced intermediary cost.
- Auditability and traceability.

### Features
- Append-only ledger.
- Consensus-based updates.
- Cryptographically secured records.

### Limitations
- Scalability constraints.
- Storage and communication overhead.
- Computation overhead for consensus.
- Governance complexity.

### Common Exam Formats
- Investigate benefits, features, and limitations of blockchain.

### Scoring Keywords
**SCALABILITY**, **STORAGE OVERHEAD**, **COMMUNICATION OVERHEAD**, **IMMUTABILITY**.

---

## TOPIC: Consensus Basics for Module II

### What It Is
Consensus is the protocol for network agreement.

### Two broad categories (write this exact split)
- **PROOF-BASED / LOTTERY-BASED** consensus (example: PoW, PoS)
- **BFT-BASED** consensus

### Why this matters in Module II
Module II asks concept and categories.
Detailed algorithms usually appear in Module III.

---

## STEP 3: PYQ PATTERN EXPLOITATION (MODULE II)

## Repeated Question Clusters

### Cluster A: Working of Blockchain + Diagram
- Appears: 3 times (2023, 2024, Oct 2023)
- Marks: 7
- Variations:
  - Working of blockchain with neat diagram
  - Illustrate blockchain working
  - Describe blockchain and full ecosystem decentralization

Master answer template:
1. Definition line
2. Transaction broadcast
3. Verification by nodes
4. Block formation
5. Consensus approval
6. Block append with hash link
7. Diagram + final benefit line

Mark distribution strategy:
- Intro: 1
- Steps: 4
- Diagram: 2

### Cluster B: Decentralization Methods
- Appears: 3 times (2023, 2024, Oct 2023 wording overlap)
- Marks: 7
- Variations:
  - Methods to achieve decentralization
  - Ecosystem of decentralization
  - Full ecosystem decentralization

Template:
- Definition
- 5 methods
- Centralized vs decentralized mini-compare
- Conclusion on trust minimization

### Cluster C: Layered Architecture
- Appears: 1 explicit long + many implicit architecture asks
- Marks: 7
- Variation:
  - Explain layered blockchain architecture with diagram

Template:
- Draw 6-layer stack
- Explain each layer in one line
- Mention cross-layer dependency

### Cluster D: Benefits/Features/Limitations
- Appears: 2 times
- Marks: 7
- Variation:
  - Benefits, features and limitations of blockchain

Template:
- 4 benefit points
- 3 feature points
- 3 limitation points
- One application wrap-up

---

## STEP 4: MEMORY TOOLKIT

| Topic | Mnemonic | Must Recall |
|---|---|---|
| Layers | NPCCEA | Network, P2P, Crypto, Consensus, Execution, Application |
| Block header | PNTM | Previous hash, Nonce, Timestamp, Merkle root |
| Decentralization | R-C-C-I | Replication, Consensus, Competition, Incentives |
| B/F/L | 4-3-3 | 4 benefits, 3 features, 3 limitations |

One-line trigger:
"Define, draw, list, compare, conclude."

---

## STEP 5: 30-MINUTE EXECUTION PLAN (MODULE II)

- Minutes 0-10:
  - Learn layered architecture + draw once.
- Minutes 10-18:
  - Learn blockchain working steps + block diagram.
- Minutes 18-24:
  - Memorize decentralization methods and comparison.
- Minutes 24-30:
  - Learn benefits/features/limitations list and practice one 7-mark answer.

---

## STEP 6: ACTIVE TEST (HIGH PROBABILITY)

1. With neat diagram explain working of blockchain. [7]
2. Explain layered blockchain architecture. [7]
3. Explain methods used to achieve decentralization. [7]
4. Explain ecosystem of decentralization in blockchain. [7]
5. Investigate benefits, features, and limitations of blockchain. [7]
6. Define consensus mechanism and explain categories. [7]
7. Define blockchain and explain key terminologies. [3]
8. List and explain types of blockchain. [3]

---

## STEP 7: FINAL WAR ROOM (LAST 10 MIN)

Priority revision order:
1. Layer diagram.
2. Blockchain working flow.
3. Decentralization points.
4. Benefits/features/limitations list.

Absolute skip list:
- Deep cryptography derivations from Module I.
- Very long case studies.

Paper attempt tactic:
- Start with diagram-rich Module II question first.
- For every 7-mark answer: definition + 6 points + diagram.
- Keep 1.8 minutes per mark pacing.

Emergency scoring tactic:
If blank-minded, draw the layered architecture and explain each layer.
That alone secures strong partial marks.
