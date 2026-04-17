# MODULE 3: CONSENSUS + BITCOIN TRANSACTIONS (QUICK CRASH FILE)

Source used:
- OCR PYQ: May 2024, June 2023, October 2023
- Notes: `Module3_Consensus_Notes.tex`
- Scheme hints: Module III split from May 2024 scheme

---

## STEP 1: PRIORITY MATRIX (MODULE 3 ONLY)

| Topic | Priority | PYQ Evidence | Why Study Now |
|---|---|---|---|
| Need for consensus + CFT/BFT categories | CRITICAL | 2023 and 2024 and Oct 2023 | Repeats as short + long answer |
| Paxos protocol | CRITICAL | May 2024 and Oct 2023 long question | Stable 7/8 mark scoring pattern |
| PoW vs PoS | CRITICAL | 2023, 2024, Oct 2023 | Frequent compare question |
| Bitcoin mining + role of miner | CRITICAL | 2023 and Oct 2023 | Repeated process/flowchart ask |
| Bitcoin transaction validation + UTXO | CRITICAL | 2023, 2024, Oct 2023 | Direct long question repeats |
| Wallet definition and types | HIGH | May 2024 Part B | Easy 7-mark list answer |
| Byzantine generals + Sybil + PBFT formula | HIGH | Oct 2023 Part A | Fast 3-mark scoring set |

---

## STEP 2: ZERO-TO-EXAM TEACHING (NO REPETITION)

## TOPIC: Why Consensus is Needed

### What It Is
Consensus is network agreement on one valid ledger state.

### Why Exams Love It
It links theory to attacks and fault tolerance.

### Core Intuition
No central authority confirms transactions.
Nodes must agree despite failures and attackers.
Consensus prevents conflicting histories and double spending.

### Exam-Critical Definitions
- **CFT**: Crash fault tolerance for non-malicious failures.
- **BFT**: Byzantine fault tolerance for malicious behavior.
- **CONSENSUS**: Protocol for state agreement in distributed system.

### Quick write line
"Consensus keeps all distributed ledger copies in the same final state."

---

## TOPIC: Paxos Protocol (Crash Fault Tolerant)

### What It Is
Paxos is a CFT consensus protocol.

### Why Exams Love It
Frequent long question with fixed phase sequence.

### Core Intuition
A proposer asks for agreement.
Acceptors promise and then accept a value.
Learners finalize majority result.

### Roles
- Proposer
- Acceptor
- Learner

### Algorithm/Phases
1. Prepare: proposer sends proposal number.
2. Promise: acceptors reject lower numbers.
3. Accept: proposer requests acceptance.
4. Learn: majority accepted value becomes chosen.

### Diagram Description
- Draw three role boxes.
- Arrows labeled Prepare, Promise, Accept, Learn.

ASCII diagram:

```
Proposer --> Acceptors : PREPARE(N)
Acceptors --> Proposer : PROMISE
Proposer --> Acceptors : ACCEPT(V)
Acceptors --> Learners : LEARN(CHOSEN V)
```

### Common Exam Formats
- Explain Paxos algorithm solving consensus with CFT.
- Describe Paxos process with example implementation.

### Scoring Keywords
**PREPARE**, **PROMISE**, **ACCEPT**, **MAJORITY**, **LEARNER**.

---

## TOPIC: PoW and PoS

### What It Is
PoW uses computational work.
PoS uses economic stake.

### Why Exams Love It
Asked repeatedly as compare and explain question.

### Core Intuition
PoW leader is winner of hash race.
PoS leader is selected validator by stake.
Both make attacks expensive.

### PoW Steps
1. Collect valid transactions.
2. Build block header.
3. Vary nonce and hash repeatedly.
4. Check hash below target.
5. Broadcast valid block.

### PoS Steps
1. Validators lock stake.
2. Protocol selects proposer.
3. Others attest block validity.
4. Finalize block after quorum.
5. Reward honest, slash malicious.

### Diagram Description

ASCII PoW:

```
Mempool -> Validate TX -> Build Block -> Hash+Nonce Loop
                                    -> Target Met? -> Broadcast
```

ASCII PoS:

```
Stake Lock -> Validator Select -> Block Proposal -> Attestation
                                       -> Finality -> Reward/Slashing
```

### Common Exam Formats
- Explain PoW consensus mechanism.
- Explain PoS with neat sketch.
- Compare PoW and PoS.

### Scoring Keywords
**DIFFICULTY TARGET**, **NONCE**, **STAKE**, **VALIDATOR**, **SLASHING**.

---

## TOPIC: Bitcoin Mining and Miner Role

### What It Is
Mining validates transactions and creates new blocks in PoW.

### Why Exams Love It
Very stable 7-mark process question.

### Core Intuition
Miners package valid transactions.
They solve puzzle to earn block reward.
They secure the chain and ordering.

### Miner Responsibilities
- Verify transactions.
- Build candidate blocks.
- Run PoW hashing loop.
- Broadcast winning block.
- Support network security and finality.

### Diagram Description

ASCII flowchart:

```
Collect TX -> Verify -> Build Candidate Block -> Hash+Nonce
   -> If fail: retry
   -> If success: broadcast block
```

### Common Exam Formats
- Explain mining steps and role of miner.
- Explain mining algorithm with flowchart.

### Scoring Keywords
**MEMPOOL**, **BLOCK REWARD**, **PROOF OF WORK**, **VALIDATION**.

---

## TOPIC: Bitcoin Transactions + Validation + UTXO

### What It Is
Bitcoin spends UTXOs, not account balance rows.

### Why Exams Love It
Appears with diagrams and user-perspective flow.

### Core Intuition
Inputs consume old unspent outputs.
Outputs create new spendable outputs.
Validation blocks double spending.

### Validation Checklist
1. Signature valid.
2. Referenced UTXO exists.
3. Referenced UTXO unspent.
4. Input sum >= output sum.
5. Script conditions pass.

### UTXO Definition
UTXO means Unspent Transaction Output.
It is a spendable coin fragment.

### Diagram Description

ASCII structure:

```
Input(s): Prev TXID + Index + Unlock Script
                |
                v
          Transaction Core
                |
                v
Output(s): Value + Lock Script (Recipient, Change)
```

### Common Exam Formats
- How is payment sent in Bitcoin from user perspective?
- How are transactions validated in Bitcoin network?
- Explain transaction structure and UTXO use in verification.

### Scoring Keywords
**UTXO**, **INPUT REFERENCE**, **DIGITAL SIGNATURE**, **DOUBLE-SPEND PREVENTION**.

---

## TOPIC: Wallets + Byzantine + Sybil (Fast Marks)

### Wallet
- Wallet stores keys, not coins.
- Types:
  - Hot wallet
  - Cold wallet
  - Custodial
  - Non-custodial

### Byzantine and PBFT Formula
- Byzantine fault: malicious or conflicting behavior.
- PBFT node requirement: `n >= 3f + 1`
- If `f=6`, then `n=19` minimum.

### Sybil Attack
- Attacker creates many fake identities.
- Bitcoin resists by tying influence to hash power, not identity count.

---

## STEP 3: PYQ PATTERN EXPLOITATION (MODULE III)

## Repeated Question Clusters

### Cluster A: Consensus Need + CFT + PoW/PoS
- Appears: 3 times
- Marks: 7 to 8
- Variations:
  - Need for consensus, CFT algorithms, compare PoW and PoS
  - Consensus categories and examples

Master template:
1. Consensus need definition
2. CFT vs BFT
3. PoW flow
4. PoS flow
5. Compare table

Mark split:
- Intro: 1
- CFT/BFT: 2
- PoW/PoS explanation: 3
- Comparison summary: 1

### Cluster B: Paxos
- Appears: 2 times
- Marks: 7 or 8
- Variations:
  - Explain Paxos solving crash fault tolerance
  - Describe Paxos process with implementation example

Template:
- Roles
- Four phases
- Mini example with majority
- Final correctness statement

### Cluster C: Mining + Miner Role
- Appears: 2 times
- Marks: 7
- Variation:
  - Explain mining algorithm with flowchart and miner tasks

Template:
- Miner tasks list
- PoW algorithm steps
- Flowchart
- Incentive line

### Cluster D: Transaction Validation + UTXO + Wallet
- Appears: 3 times
- Marks: 7
- Variations:
  - Payment flow from user perspective
  - Transaction validation
  - UTXO structure + wallet types

Template:
- Payment steps
- Validation checklist
- UTXO diagram
- Wallet type table

### Cluster E: Byzantine/Sybil
- Appears: Oct 2023 direct Part A
- Marks: 3 each

Template:
- One-line definition
- One-line blockchain relevance
- One-line prevention mechanism

---

## STEP 4: MEMORY TOOLKIT

| Topic | Mnemonic | Must Recall |
|---|---|---|
| Consensus | A-G-R | Agree, global state, reject conflicts |
| Paxos | PPAL | Prepare, Promise, Accept, Learn |
| PoW | HNTB | Hash, Nonce, Target, Broadcast |
| Transaction validation | SEUIS | Signature, Existence, Unspent, Input>=Output, Script |
| PBFT formula | 3f+1 | If 6 Byzantine, need 19 nodes |
| Wallet types | HCCN | Hot, Cold, Custodial, Non-custodial |

One-line trigger:
"Validate first, then append, then finalize."

---

## STEP 5: 30-MINUTE EXECUTION PLAN (MODULE III)

- Minutes 0-8:
  - Consensus need + CFT/BFT + formula.
- Minutes 8-15:
  - Paxos roles and four phases.
- Minutes 15-23:
  - PoW vs PoS + miner flowchart.
- Minutes 23-30:
  - UTXO transaction diagram + wallet types + one 7-mark practice.

---

## STEP 6: ACTIVE TEST (HIGH PROBABILITY)

1. Explain need for consensus in blockchain. [7]
2. What are CFT algorithms? Compare PoW and PoS. [7]
3. Explain Paxos protocol for crash fault tolerance. [8]
4. Explain working of PoS with neat sketch. [6]
5. Explain transaction validation in Bitcoin network. [7]
6. Explain mining steps and role of miner in Bitcoin. [7]
7. Explain Bitcoin transaction structure and UTXO use in verification. [7]
8. What is wallet? Explain types. [7]
9. Solve PBFT node requirement for 6 Byzantine nodes. [3]
10. What is Sybil attack? How does Bitcoin resist it? [3]

---

## STEP 7: FINAL WAR ROOM (LAST 10 MIN)

Priority revision order:
1. Paxos phase order.
2. PoW and PoS flow.
3. UTXO validation checklist.
4. PBFT formula.
5. Miner tasks list.

Absolute skip list:
- Deep cryptographic math proofs.
- Non-module edge protocol details.

Paper attempt tactic:
- Pick one diagram-heavy question first.
- For each 7-mark answer: definition + 5 points + one diagram.
- Keep pace at 1.8 minutes per mark.

Emergency scoring tactic:
If unsure, write validation checklist and draw UTXO transaction structure.
This secures strong partial marks.
