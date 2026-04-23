# STEP 1: BCT Priority Topics (PYQ-Locked Plan)

Subject: CST428 Blockchain Technologies

PYQ source mapping:
- BCT/ocr_work/qp/questions_extracted.json
- BCT/ocr_work/qp/CST428-QP_May_2024.txt
- BCT/ocr_work/qp/June_2023_Regular.txt
- BCT/ocr_work/qp/October_2023_Supplementary.txt

---

## What Repeats Across Papers

Most repeated ask patterns:
1. Compare two concepts (symmetric vs asymmetric, PoW vs PoS, Bitcoin vs Ethereum).
2. Explain architecture with neat diagram (blockchain layers, DApp design, Ethereum trie relation).
3. Explain algorithm/protocol in fixed steps (Paxos, mining, transaction processing).
4. Write compact Solidity contracts (bank, voting, storage).
5. Explain applied use-cases (government, finance, healthcare, supply chain).

---

## Module-Wise Priority Matrix

## Module 1 (Cryptography and Hashing)

| Topic | Priority | PYQ recurrence reason |
|---|---|---|
| Symmetric vs asymmetric cryptography | Critical | Direct Part A repeat |
| Secure hash role and properties | Critical | Direct Part A repeat |
| Merkle tree benefits | Critical | Direct Part A repeat |
| RSA workflow | High | Core theory and algorithm ask |
| DHT concept and working | High | Repeated direct short question |

## Module 2 (Blockchain Architecture and Decentralization)

| Topic | Priority | PYQ recurrence reason |
|---|---|---|
| Blockchain definition and terminologies | Critical | Repeated in Part A |
| Working of blockchain | Critical | Core long-answer pattern |
| Layered architecture | Critical | Repeated diagram question |
| Centralized vs decentralized | High | Repeated comparison ask |
| Methods to achieve decentralization | High | Repeated long ask |

## Module 3 (Consensus and Bitcoin)

| Topic | Priority | PYQ recurrence reason |
|---|---|---|
| Need for consensus, CFT/BFT | Critical | Repeated direct ask |
| Paxos protocol | Critical | Repeated long answer |
| PoW and PoS | Critical | Repeated explain/compare |
| Bitcoin mining and miner role | Critical | Repeated long ask |
| Bitcoin transaction validation and UTXO | Critical | Repeated direct ask |
| PBFT sizing numerical | High | Direct short numerical ask |

## Module 4 (Smart Contracts, Oracles, DApps)

| Topic | Priority | PYQ recurrence reason |
|---|---|---|
| Smart contract definition and properties | Critical | Repeated Part A ask |
| Oracle types and data flow | Critical | Repeated Part A and Part B |
| DApp architecture | Critical | Repeated long answer |
| Sector use-cases | High | Repeated application ask |

## Module 5 (Ethereum and Solidity)

| Topic | Priority | PYQ recurrence reason |
|---|---|---|
| EVM role | Critical | Direct Part A repeat |
| Account types and transaction flow | Critical | Repeated theory ask |
| Trie-header relationship | Critical | Repeated diagram ask |
| Gas concept | Critical | Repeated long answer |
| Solidity datatypes and control structures | High | Repeated Part A ask |
| Solidity coding templates | High | Repeated Part B ask |

---

## Formula and Numeric Recall

1. PBFT minimum node condition:
$$
n \ge 3f + 1
$$
2. Ethereum fee formula:
$$
Fee = GasUsed \times EffectiveGasPrice
$$
3. EIP-1559 simplified:
$$
EffectiveGasPrice = BaseFee + PriorityFee
$$

---

## 3-Day Execution Order

Day 1:
1. Module 1 + Module 2 complete.
2. Draw all core diagrams once.

Day 2:
1. Module 3 deep focus (Paxos, PoW/PoS, mining, UTXO).
2. Solve one PBFT numerical and one transaction-flow answer.

Day 3:
1. Module 4 and Module 5.
2. Write one Solidity bank contract and one voting contract from memory.

---

## Final Score Safety Checklist

1. Can you compare PoW vs PoS in 5 lines?
2. Can you write Paxos as Prepare, Promise, Accept, Learn?
3. Can you draw DApp architecture in under 30 seconds?
4. Can you derive PBFT minimum nodes for any f?
5. Can you write one Solidity contract skeleton without notes?
