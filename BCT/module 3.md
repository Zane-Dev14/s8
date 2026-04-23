# Module 3: Consensus and Bitcoin Transactions (Exam Sheet)

---

## Why Consensus

Consensus keeps all distributed nodes in one valid global ledger state.

Without consensus:
1. Conflicting histories
2. Double spend risk
3. Unreliable balances

---

## CFT and BFT

1. CFT handles crash faults.
2. BFT handles malicious faults.

PBFT formula:
$$
n \ge 3f + 1
$$
If f=6, n>=19.

---

## Paxos Algorithm

Roles:
1. Proposer
2. Acceptor
3. Learner

Phases:
1. Prepare
2. Promise
3. Accept
4. Learn

Flow:
```text
Proposer -> Acceptors : PREPARE
Acceptors -> Proposer : PROMISE
Proposer -> Acceptors : ACCEPT
Acceptors -> Learners : LEARN
```

---

## PoW and PoS

PoW:
1. Build block
2. Hash with nonce
3. Meet target
4. Broadcast

PoS:
1. Lock stake
2. Select proposer
3. Attest block
4. Finalize and reward/slash

---

## Bitcoin Mining

Miner tasks:
1. Collect mempool transactions.
2. Validate transaction rules.
3. Build candidate block.
4. Execute PoW loop.
5. Broadcast accepted block.

---

## Bitcoin Transaction Validation

Checklist:
1. Signature valid
2. UTXO exists
3. UTXO unspent
4. Input >= output
5. Script passes

UTXO means spendable unspent output from previous transaction.

---

## Wallet Types

1. Hot
2. Cold
3. Custodial
4. Non-custodial

---

## Security Terms

1. Byzantine fault: malicious inconsistent behavior.
2. Sybil attack: many fake identities by attacker.
3. Double-spend: same coin attempted in multiple spends.

---

## Module 3 Quick Recall

1. Remember PPAL for Paxos.
2. Solve PBFT node count once.
3. Write transaction validation checklist.
4. Draw mining flowchart from memory.
