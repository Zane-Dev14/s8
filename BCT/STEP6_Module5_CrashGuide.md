# STEP 6: Module 5 Crash Guide (Ethereum + EVM + Solidity)

Module 5 focus:
- Ethereum processing model
- EVM execution and gas economics
- Solidity basics and exam coding patterns

Mapped from:
- BCT/Important Notes ALl Modules/Module5_Ethereum_Notes.tex
- BCT/ocr_work/qp/questions_extracted.json

---

## Topic 1: Ethereum Basics and EVM

Definition:
- Ethereum is a programmable blockchain where smart contracts execute inside EVM.

EVM role:
1. Deterministic contract execution across nodes
2. State transition engine
3. Gas-metered computation control

---

## Topic 2: Ethereum Account Types

1. EOA (Externally Owned Account): controlled by private key, initiates transactions.
2. Contract Account: controlled by code, executes when invoked.

Quick compare:
- EOAs have no contract bytecode.
- Contract accounts contain code and persistent storage.

---

## Topic 3: Transaction Types in Ethereum

1. Value transfer transaction
2. Contract interaction call transaction
3. Contract creation transaction (special case)

Common fields:
- nonce, to, value, data, gas limit, fee fields, signature

---

## Topic 4: Ethereum Transaction Processing Flow

Step flow:
1. User signs transaction in wallet
2. Transaction broadcast to network
3. Validators/miners execute via EVM
4. State transition occurs if valid
5. Receipt and logs generated
6. Included in block and finalized

---

## Topic 5: Gas Concept

Core formula:
$$
\text{Transaction Fee} = \text{Gas Used} \times \text{Effective Gas Price}
$$

EIP-1559 style simplified:
$$
\text{Effective Gas Price} = \text{Base Fee} + \text{Priority Fee}
$$

Exam points:
1. More complex code consumes more gas.
2. Out-of-gas reverts state change but consumes computation fee.

---

## Topic 6: Ethereum Elements and World State

Important elements:
1. Block header
2. Transaction list
3. Receipts list
4. State root
5. Transaction root
6. Receipts root
7. Logs/events

World state:
- Snapshot of all account balances/nonces/code/storage after a block.

---

## Topic 7: Transactions, Transaction Trie, Block Header

Relation:
1. Transactions organized in Merkle-Patricia trie
2. Trie root inserted into block header
3. Any transaction modification changes trie root and block hash

Diagram:

```text
Transactions -> Transaction Trie -> Transaction Root in Header -> Block Integrity
```

---

## Topic 8: Solidity Datatypes, Control Structures, Libraries

Datatypes:
1. Value types: bool, uint, int, address, bytes32
2. Reference types: array, struct, string
3. Mapping type: mapping(key => value)

Control structures:
1. if/else
2. for/while
3. break/continue/return
4. require/revert/assert

Libraries:
- Reusable deployed code units for shared utility logic.

---

## Topic 9: Solidity Coding Patterns (Frequently Asked)

## Simple bank contract pattern
Functions:
1. deposit()
2. withdraw(uint amount)
3. getBalance()

## Voting contract pattern
Functions:
1. addCandidate()
2. vote(candidateId)
3. result()

## Simple storage pattern
Functions:
1. setString(string memory s)
2. getString()

Safety baseline:
- Use require checks before state-changing operations.

---

## Topic 10: Bitcoin vs Ethereum (Quick Compare)

1. Purpose: digital cash vs programmable contracts
2. Model: UTXO vs account-state
3. Script capability: limited vs expressive VM-based
4. Native ecosystem: payments vs generalized DApps

---

## Module 5 PYQ Attack Set

1. Role of EVM
2. Ethereum account types
3. Transaction types and processing flow
4. Gas concept and effect
5. Elements in Ethereum blockchain
6. World state with diagram
7. Trie-header relationship
8. Solidity datatypes and control structures
9. Solidity bank/voting/string contracts
10. Bitcoin vs Ethereum comparison

---

## Last-Minute Revision Grid

1. Memorize gas fee formula.
2. Practice one flow answer for transaction processing.
3. Practice one compact bank contract skeleton.
4. Memorize EOA vs contract account 4-point comparison.
