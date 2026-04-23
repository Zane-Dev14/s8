# STEP 4: Module 3 Crash Guide (Consensus and Bitcoin Transactions)

Module focus:
- Distributed agreement under faults
- Bitcoin mining and transaction validation
- Security attack basics

---

## 1) Why Consensus is Needed

Consensus is required so all nodes agree on one valid ledger history without central authority.

Without consensus:
1. Conflicting ledger states appear.
2. Double-spending becomes possible.
3. Network trust collapses.

---

## 2) CFT vs BFT

1. CFT handles crash or silent failures.
2. BFT handles malicious or arbitrary behavior.
3. CFT examples include Paxos-family protocols.
4. BFT examples include PBFT-family protocols.

PBFT sizing formula:
$$
n \ge 3f+1
$$
If f = 6, minimum n = 19.

---

## 3) Paxos Protocol (Crash Fault Tolerance)

Roles:
1. Proposer
2. Acceptor
3. Learner

Phases:
1. Prepare(N)
2. Promise
3. Accept(V)
4. Learn

Message flow:
```text
Proposer -> Acceptors : PREPARE(N)
Acceptors -> Proposer : PROMISE
Proposer -> Acceptors : ACCEPT(V)
Acceptors -> Learners : LEARN(V)
```

Exam correctness line:
Majority intersection ensures a single chosen value.

---

## 4) PoW and PoS

## PoW steps
1. Gather valid pending transactions.
2. Build candidate block.
3. Iterate nonce and hash.
4. Accept block if target condition satisfied.
5. Broadcast and verify.

## PoS steps
1. Validators lock stake.
2. Proposer is selected by protocol.
3. Other validators attest proposed block.
4. Finality achieved by protocol rule.
5. Reward honest behavior, slash malicious behavior.

Comparison table:

| Aspect | PoW | PoS |
|---|---|---|
| Leader basis | Hash puzzle solution | Stake-weighted selection |
| Main resource | Computation | Economic stake |
| Energy profile | High | Lower |
| Attack cost basis | Hash-power dominance | Stake dominance plus slashing risk |

---

## 5) Bitcoin Mining and Role of Miner

Miner tasks:
1. Collect transactions from mempool.
2. Validate scripts, signatures, and UTXO references.
3. Build block candidate and header.
4. Run proof-of-work loop.
5. Broadcast winning block.

Flowchart:
```text
Mempool -> Verify TX -> Build Block -> Nonce/Hash Loop -> Target Met -> Broadcast
```

---

## 6) Bitcoin Transaction Validation and UTXO

Validation checklist:
1. Signature is valid.
2. Referenced UTXO exists.
3. Referenced UTXO is unspent.
4. Input value is at least output value.
5. Script conditions pass.

UTXO meaning:
Unspent Transaction Output is a spendable output unit.

Transaction structure sketch:
```text
Inputs (prev outputs + unlocking script)
       -> Transaction core
Outputs (recipient + change + locking script)
```

---

## 7) Wallet Types

1. Hot wallet: online and convenient.
2. Cold wallet: offline and safer for long-term storage.
3. Custodial wallet: third party controls keys.
4. Non-custodial wallet: user controls keys.

---

## 8) Byzantine and Sybil Basics

1. Byzantine behavior means malicious or inconsistent node behavior.
2. Sybil attack means many fake identities under one attacker.
3. Bitcoin mitigates Sybil by tying influence to economic or computational resource cost.

---

## 9) Module 3 Final Drill

1. Recite Paxos phase order: Prepare, Promise, Accept, Learn.
2. Solve PBFT node count once.
3. Write 5-point transaction validation checklist.
4. Draw mining flowchart from memory.
