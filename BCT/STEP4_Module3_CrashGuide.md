# STEP 4: Module 3 Crash Guide (Consensus + Bitcoin Transactions)

Module 3 focus:
- Consensus reliability and attack resistance
- Bitcoin mining and transaction validation flow

Mapped from:
- BCT/module 3.md
- BCT/Important Notes ALl Modules/Module3_Consensus_Notes.tex
- BCT/ocr_work/qp/questions_extracted.json

---

## Topic 1: Why Consensus is Needed

Core line:
- Consensus keeps all distributed ledger copies in one globally consistent state.

Without consensus:
1. Double spending risk
2. Conflicting histories
3. Inconsistent balances across nodes

---

## Topic 2: CFT vs BFT

1. CFT handles crash/silent failures.
2. BFT handles malicious or conflicting behavior.
3. CFT examples include Paxos family.
4. BFT examples include PBFT-style protocols.

PBFT sizing formula:
$$
n \ge 3f + 1
$$
If $f=6$, minimum $n=19$.

---

## Topic 3: Paxos (Crash Fault Tolerance)

Roles:
1. Proposer
2. Acceptor
3. Learner

Phases:
1. Prepare
2. Promise
3. Accept
4. Learn

Diagram:

```text
Proposer -> Acceptors : PREPARE(N)
Acceptors -> Proposer : PROMISE
Proposer -> Acceptors : ACCEPT(V)
Acceptors -> Learners : LEARN(V)
```

Exam tip:
- Write "majority accepted value is chosen" explicitly.

---

## Topic 4: PoW and PoS

## PoW flow
1. Build candidate block
2. Iterate nonce and hash
3. Check target condition
4. Broadcast valid block

## PoS flow
1. Validators lock stake
2. Proposer selected by protocol
3. Attestation/validation by others
4. Finality + reward/slashing

## Compare quick points
1. Resource: computation vs stake
2. Energy: high vs lower
3. Attack cost model: hash power vs economic stake

---

## Topic 5: Bitcoin Mining and Miner Role

Miner responsibilities:
1. Collect pending transactions
2. Validate transactions
3. Construct candidate block
4. Execute PoW
5. Broadcast successful block

Flowchart:

```text
Mempool -> Verify TX -> Build Block -> Hash Loop -> Target Met -> Broadcast
```

---

## Topic 6: Bitcoin Transaction Validation + UTXO

Validation checklist (memorize):
1. Signature valid
2. Referenced UTXO exists
3. Referenced UTXO unspent
4. Input sum >= output sum
5. Script checks pass

UTXO meaning:
- Unspent Transaction Output, i.e., spendable coin fragments.

Transaction structure:

```text
Inputs (prev tx refs + signatures) -> Transaction Core -> Outputs (recipient + change)
```

---

## Topic 7: Wallet Types

1. Hot wallet (online, convenient)
2. Cold wallet (offline, safer for long-term)
3. Custodial wallet (third-party key control)
4. Non-custodial wallet (user key control)

---

## Topic 8: Byzantine, Sybil, and Double-Spend Basics

1. Byzantine fault: node sends deceptive/conflicting data.
2. Sybil attack: attacker creates many fake identities.
3. Double-spend attack: same coin attempted in multiple transactions.
4. Bitcoin resists identity-level Sybil by economic/hash-power based control.

---

## Module 3 PYQ Attack Set

1. Need for consensus and CFT/BFT
2. Paxos protocol with steps
3. PoW vs PoS comparison
4. Mining algorithm with flowchart
5. Miner tasks
6. Bitcoin transaction validation
7. UTXO and transaction structure
8. Wallet types
9. PBFT minimum node numerical

---

## Last-Minute Revision Grid

1. Memorize PPAL sequence: Prepare, Promise, Accept, Learn.
2. Memorize validation checklist SEUIS.
3. Practice one PoW vs PoS comparison table.
4. Practice PBFT formula substitution once.
