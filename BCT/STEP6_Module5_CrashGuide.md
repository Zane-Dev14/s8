# STEP 6: Module 5 Crash Guide (Ethereum, EVM, Gas, Solidity)

Module focus:
- Ethereum execution model
- Gas and transaction lifecycle
- Solidity exam coding templates

---

## 1) Ethereum and EVM

Definition:
Ethereum is a programmable blockchain where smart contracts execute in the EVM.

EVM responsibilities:
1. Deterministic bytecode execution.
2. Gas-metered resource accounting.
3. State transition application.

---

## 2) Ethereum Account Types

1. EOA (Externally Owned Account): controlled by private key and initiates transactions.
2. Contract account: controlled by deployed bytecode and executes when called.

Difference summary:
- EOA has no contract code.
- Contract account stores code and persistent storage.

---

## 3) Ethereum Transaction Types

1. Value transfer transaction.
2. Contract interaction call transaction.
3. Contract creation transaction.

Common fields:
nonce, to, value, data, gas limit, fee fields, signature.

---

## 4) Transaction Processing Flow

1. User signs transaction in wallet.
2. Transaction is broadcast to peers.
3. Validators execute payload via EVM.
4. State transition applied if valid.
5. Receipt and logs generated.
6. Transaction included in block and finalized.

Flow sketch:
```text
Sign -> Broadcast -> Execute(EVM) -> State Update -> Receipt -> Block Inclusion
```

---

## 5) Gas Concept and Formula

Main formula:
$$
TransactionFee = GasUsed \times EffectiveGasPrice
$$

EIP-1559 simplified:
$$
EffectiveGasPrice = BaseFee + PriorityFee
$$

Mini numeric example:
If GasUsed = 21000 and EffectiveGasPrice = 30 gwei,
Fee = 21000 * 30 gwei = 630000 gwei.

Exam line:
Out-of-gas reverts state change but still consumes spent computation fee.

---

## 6) Ethereum Elements and World State

Core elements:
1. Block header
2. Transaction list
3. Receipt list
4. State root
5. Transaction root
6. Receipt root
7. Event logs

World state:
Mapping snapshot of all account balances, nonces, code, and storage at a block height.

---

## 7) Transactions, Trie, and Block Header

Relation steps:
1. Transactions are organized in a transaction trie.
2. Trie root hash is stored in block header.
3. Any transaction change changes trie root.
4. Header hash changes accordingly.

Diagram:
```text
Transactions -> Transaction Trie -> Transaction Root -> Block Header Integrity
```

---

## 8) Solidity Datatypes and Control Structures

Datatypes:
1. Value types: bool, uint, int, address, bytes32.
2. Reference types: array, string, struct.
3. Mapping type: mapping(key => value).

Control structures:
1. if/else
2. for/while
3. break/continue/return
4. require/revert/assert

---

## 9) Solidity Coding Templates

## Simple bank contract pattern
Functions:
1. deposit()
2. withdraw(uint amount)
3. viewBalance()

## Voting contract pattern
Functions:
1. addCandidate()
2. vote(candidateId)
3. getResult()

## String storage pattern
Functions:
1. setValue(string)
2. getValue()

Safety line for exam:
Use require checks before every state-changing update.

---

## 10) Bitcoin vs Ethereum Quick Comparison

| Aspect | Bitcoin | Ethereum |
|---|---|---|
| Core goal | Digital value transfer | General programmable platform |
| State model | UTXO | Account-state |
| Script flexibility | Limited script model | EVM smart contracts |
| Typical workload | Payments | DApps and programmable logic |

---

## 11) Module 5 Final Drill

1. Memorize gas fee formula and one numeric.
2. Draw transaction-to-trie-to-header relation.
3. Write one bank contract skeleton from memory.
4. Recite EOA vs contract account differences.
