# CST428 Blockchain Technologies (BCT) — Module 3 Answer Bank (Consensus + Bitcoin)
Date: 30 Apr 2026

Built from your extracted QPs (May 2024, June 2023, Oct 2023 Suppl.) + Module‑3 crash guide.

---

## 0) Acronyms
- **PoW**: Proof of Work
- **PoS**: Proof of Stake
- **PBFT**: Practical Byzantine Fault Tolerance
- **CFT**: Crash Fault Tolerance
- **BFT**: Byzantine Fault Tolerance
- **P2P**: Peer-to-Peer
- **UTXO**: Unspent Transaction Output
- **DoS**: Denial of Service

---

## 1) Part A (5 marks each; write exactly 5 points)

### A1) Two categories of consensus mechanisms
1. Proof-based consensus selects leader via resource competition/weight.
2. Examples: PoW, PoS.
3. Fault-tolerant consensus uses replica agreement protocols.
4. Examples: Paxos family (CFT), PBFT family (BFT).
5. Goal: one consistent ledger history across nodes.

**Mnemonic:** **P‑F** → **P**roof-based vs **F**ault‑tolerant.

### A2) Explain working of PoW
1. Collect valid transactions from mempool.
2. Form a candidate block.
3. Compute block header hash with a nonce.
4. Repeat nonce until hash meets target difficulty.
5. Broadcast block; others verify and extend chain.

**Mnemonic:** **C‑B‑H‑T‑B** → Collect → Build → Hash → Target → Broadcast.

### A3) Bitcoin transaction validation (quick checklist)
1. Verify digital signatures.
2. Check referenced UTXOs exist.
3. Ensure UTXOs are unspent.
4. Ensure inputs ≥ outputs (fees non-negative).
5. Validate script/locking conditions.

**Mnemonic:** **S‑E‑U‑A‑S** → Signature, Exists, Unspent, Amount, Script.

---

## 2) Part B (10 marks each)

### B1) Need for consensus + crash fault tolerant algorithms (QP: June 2023)
1. Consensus is needed so all nodes agree on one valid ledger state.
2. Without consensus, forks/conflicts lead to inconsistent balances.
3. Double spending becomes possible without a single agreed order.
4. Consensus replaces a central authority with protocol rules.
5. Fault models: crash faults (silent fail) vs Byzantine (malicious).
6. **CFT** algorithms tolerate crash faults, not malicious behavior.
7. Example CFT family: Paxos-type protocols.
8. CFT requires majority of nodes remain alive/reachable.
9. CFT is used in many distributed systems for reliable agreement.
10. For malicious settings, BFT protocols are used instead.

**Mnemonic:** **3F** → **F**orks, **F**raud (double spend), **F**ailure without consensus.

### B2) Explain Paxos (CFT) with example / phase order (QP: May 2024, Oct 2023)
1. Paxos is a consensus protocol designed for crash fault tolerance.
2. Roles: proposer, acceptor, learner.
3. Proposer sends **Prepare(N)** with proposal number N.
4. Acceptors reply **Promise** not to accept lower-numbered proposals.
5. Proposer selects value V (respecting any prior accepted value).
6. Proposer sends **Accept(V)** request.
7. Acceptors accept if it matches promise conditions.
8. Learners learn the chosen value after majority acceptance.
9. Safety comes from majority intersection (two majorities overlap).
10. Liveness requires a stable leader/network conditions.

**Mnemonic:** **PPAL** → **P**repare, **P**romise, **A**ccept, **L**earn.

**Neat sketch to draw (15 seconds):**
```text
Proposer -> Acceptors : PREPARE(N)
Acceptors -> Proposer : PROMISE
Proposer -> Acceptors : ACCEPT(V)
Acceptors -> Learners : LEARN(V)
```

### B3) Compare PoW and PoS (QP: May 2024, June 2023)
1. PoW selects leader via solving a hash puzzle (work).
2. PoS selects leader mainly by stake weight (economic resource).
3. PoW steps: collect tx → build block → nonce hashing → target met → broadcast.
4. PoS steps: stake lock → proposer selection → attestations → finality.
5. PoW security cost: acquiring dominant hash power (energy/hardware).
6. PoS security cost: acquiring dominant stake + risk of slashing.
7. PoW has higher energy footprint.
8. PoS is typically lower energy.
9. Both aim to prevent conflicting histories and double spend.
10. Both require verification by the network.

**Mnemonic:** **W=Work, S=Stake** (and write one-line: “Work burns energy; Stake risks slashing”).

### B4) Bitcoin miner tasks + mining algorithm with flowchart (QP: Oct 2023; also June 2023)
1. Miner collects unconfirmed transactions from mempool.
2. Miner validates each transaction (signature, UTXO, scripts).
3. Miner builds a candidate block (header + tx list).
4. Miner computes block hash by varying nonce.
5. If hash < target, PoW is satisfied.
6. Winning miner broadcasts block to P2P network.
7. Other nodes verify PoW + transactions.
8. If valid, block is appended to the chain.
9. Miner earns block reward + transaction fees.
10. Mining secures ordering and makes history costly to rewrite.

**Mnemonic:** **V‑B‑N‑T‑B** → Validate → Build → Nonce → Target → Broadcast.

**Flowchart (draw):**
```text
Mempool -> Verify TX -> Build Block -> Nonce/Hash Loop -> Target Met -> Broadcast
```

### B5) Bitcoin payment flow (user perspective) (QP: May 2024)
1. Sender enters receiver address and amount in wallet.
2. Wallet selects spendable UTXOs as inputs.
3. Wallet creates outputs: receiver + change back to sender.
4. Sender signs transaction using private key.
5. Signed tx is broadcast to the P2P network.
6. Nodes verify signatures and UTXO validity.
7. Transaction stays in mempool awaiting inclusion.
8. Miner includes it in a block candidate and mines.
9. After block inclusion, receiver sees confirmation.
10. More confirmations increase finality confidence.

**Mnemonic:** **A‑U‑O‑S‑B‑M** → Address → UTXO → Outputs → Sign → Broadcast → Mine.

### B6) Transaction structure diagram + UTXO and verification role (QP: Oct 2023)
1. Bitcoin transaction consumes previous outputs and creates new outputs.
2. **Inputs** reference `(prevTxId, outputIndex)` + unlocking script/signature.
3. **Outputs** specify amount + locking script (spending condition).
4. UTXO set is the set of all unspent outputs available to spend.
5. To spend, an input must reference an existing UTXO.
6. Verification checks UTXO exists and is unspent.
7. Verification validates signature/script satisfies locking conditions.
8. Verification checks input sum ≥ output sum (difference = fee).
9. After inclusion, consumed UTXO is removed and new outputs become UTXOs.
10. This prevents double spending within the ledger rules.

**Mnemonic:** **R‑P‑S‑A** → **R**eference UTXO, **P**rove with signature, **S**atisfy script, **A**mounts balance.

**How to draw (20 seconds):**
```text
Inputs (prevTx + unlock)  --->  Transaction  --->  Outputs (amount + lock)
```

### B7) Wallet types (QP: May 2024)
1. Wallet manages keys + creates/signs transactions.
2. Hot wallet: connected to internet; convenient.
3. Cold wallet: offline; safer for long-term storage.
4. Custodial: third party holds keys.
5. Non-custodial: user controls keys.
6. Hardware wallet is a type of cold wallet.
7. Software wallet (mobile/desktop) is usually hot.
8. Security tradeoff: convenience vs exposure.
9. Backups/seed phrases are critical.
10. Losing private key means losing funds control.

**Mnemonic:** **HC‑CN** → **H**ot/**C**old and **C**ustodial/**N**on‑custodial.

### B8) Sybil attack + Bitcoin mitigation (Part A theme but frequently asked)
1. Sybil attack: attacker creates many fake identities/nodes.
2. Goal: gain influence over network decisions/communication.
3. Bitcoin mitigates by tying block production to PoW cost.
4. Influence is proportional to hash power, not number of identities.
5. Running many nodes doesn’t help without mining power.
6. Network-level protections (peer selection, rate limits) also help.
7. Attack cost becomes economically expensive.
8. Still, eclipse attacks exist at network layer if peers are controlled.
9. But consensus influence remains cost-bound.
10. Therefore Sybil resistance is achieved via resource-based voting.

**Mnemonic:** **ID ≠ Power** in Bitcoin; **Hash = Power**.

### B9) PBFT numerical (f=6) — show full steps (Part A theme)
1. For PBFT, required nodes $n \ge 3f + 1$.
2. Given faulty (Byzantine) nodes $f = 6$.
3. Substitute: $n \ge 3(6) + 1$.
4. Compute: $n \ge 18 + 1$.
5. Therefore $n \ge 19$.
6. Minimum integer satisfying is $n = 19$.
7. With fewer than 19, safety/liveness guarantees break.
8. This tolerates up to 6 Byzantine faults.
9. Majority/quorum steps rely on this bound.
10. Final answer: **19 nodes**.

**Mnemonic:** **3f+1** (say it as “three‑f plus one”).

### B10) Random leader instead of PoW: which attacks become possible? (QP: Oct 2023)
1. If leader selection is random and can pick a Byzantine node, ledger safety is weakened.
2. **Steal others’ Bitcoin directly?** Not possible without valid signatures (cryptography blocks theft).
3. **DoS attack?** Yes: malicious leader can refuse to include tx or delay block proposal.
4. **Double spend?** Potentially: malicious leader can try conflicting histories; network must resolve.
5. In PoW, rewriting history requires massive hash power.
6. In random leader scheme without strong BFT, adversary can cause inconsistent proposals.
7. If the protocol lacks finality rules, forks increase.
8. Attack impact depends on how many malicious leaders appear and protocol recovery.
9. Core takeaway: signature security prevents theft, but availability/ordering can be attacked.
10. Therefore statement (2) is true; (1) is false; (3) depends on protocol details (often more feasible than PoW).

**Mnemonic:** **SAD** → **S**ignatures stop theft; **A**vailability can be attacked; **D**ouble-spend risk rises if ordering/finality is weak.
