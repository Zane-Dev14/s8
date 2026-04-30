# CST428 Blockchain Technologies (BCT) — Module 5 Answer Bank (Exam Day)
Date: 30 Apr 2026

This is a **Module 5-only** bank, built from your extracted QPs (May 2024, June 2023, Oct 2023 Suppl.) and your crash guide.

---

## 0) Acronyms + Quick Expansions (use inside Part‑B answers)

**Core Ethereum**
- **ETH**: Ether (native currency)
- **EVM**: Ethereum Virtual Machine
- **EOA**: Externally Owned Account
- **CA**: Contract Account
- **SC**: Smart Contract
- **DApp**: Decentralized Application

**Transactions & fees**
- **Tx**: Transaction
- **Nonce**: Per-account counter that prevents replay and orders Tx
- **Gas**: Unit of computation
- **GasLimit**: Max gas a Tx allows
- **GasUsed**: Actual gas consumed
- **Gwei**: Giga-wei, $1\ \text{gwei}=10^9\ \text{wei}$
- **EIP**: Ethereum Improvement Proposal
- **EIP‑1559**: Fee mechanism with base fee + priority fee
- **Base fee**: Protocol-set fee burned per gas
- **Priority fee / Tip**: Extra per gas paid to validator
- **Effective gas price**: Actual price paid per gas in the Tx

**Data structures / hashing**
- **MPT**: Merkle Patricia Trie
- **Tx trie**: Trie committing to all transactions in a block
- **Receipt trie**: Trie committing to all receipts/logs
- **State trie**: Trie committing to world state
- **Keccak‑256**: Hash function used by Ethereum (often called “SHA3” in Ethereum context)

**Interfaces**
- **ABI**: Application Binary Interface
- **RPC**: Remote Procedure Call
- **JSON‑RPC**: JSON based RPC protocol used by Ethereum nodes

---

## 1) Module 5 — Part A (5 marks each; write exactly 5 points)

### A1) Role of EVM in Ethereum
1. EVM executes smart contract bytecode deterministically on all nodes.
2. It applies the **state transition** from pre‑state to post‑state for each Tx.
3. It meters computation using **gas**, preventing infinite loops.
4. It defines a sandboxed runtime (stack, memory, storage, opcodes).
5. It outputs receipts/logs and success/revert outcome consistently.

### A2) Components/elements in Ethereum blockchain
1. **Block header** contains hashes/roots that commit to block contents.
2. **Transactions list** carries all included signed transactions.
3. **Receipts** store execution outcomes and emitted logs.
4. **State root / Tx root / Receipt root** commit to tries for integrity.
5. **World state** records account balances, nonces, code, and storage.

### A3) Two account types in Ethereum (EOA vs Contract Account)
1. EOA is controlled by a private key; contract account is controlled by code.
2. EOA initiates transactions; contracts execute when called.
3. EOA has no bytecode; contract account stores bytecode.
4. EOA state is mainly (nonce, balance); contract has (nonce, balance, code, storage).
5. EOAs sign; contracts do not “sign”, they run deterministically.

### A4) Solidity datatypes (quick)
1. Value types: `bool`, `uint/int`, `address`, fixed `bytesN`.
2. Reference types: arrays, `string`, `struct`.
3. Mapping: `mapping(key => value)` for key‑value storage.
4. Storage locations: `storage`, `memory`, `calldata` affect gas & mutability.
5. Use `require`/`revert`/`assert` for checks and safety.

---

## 2) Module 5 — Part B (10 marks each)

### B1) Define Ethereum transaction + explain transaction types
1. An Ethereum **transaction** is a signed message from an **EOA** that requests a state change.
2. It is authenticated by signature and ordered using the sender’s **nonce**.
3. Tx can move ETH (`value`) and/or execute contract code (`data`).
4. In Ethereum, the **two main types** are: **message-call** and **contract-creation**.
5. **Message-call Tx**: `to` is set (EOA or contract); can be pure value transfer or function call.
6. **Contract-creation Tx**: `to` is empty; `data` carries init/creation bytecode; creates a new contract.
7. Common fields: `nonce`, `to`, `value`, `data`, `gasLimit`, fee fields, signature.
8. Under modern Ethereum, typed Tx exist: legacy, access‑list, dynamic‑fee (EIP‑1559).
9. Invalid signature/nonce causes rejection before execution.
10. Execution produces a receipt and logs; failure can revert state but still spends gas.

**Mnemonic:** **TO rule** → **TO SET = CALL**, **TO ZERO = CREATE** (if `to` field is set, it’s a message-call; if `to` is empty, it’s contract creation).

### B2) Explain Ethereum transaction processing flow + add easy mnemonic
1. User builds Tx (nonce, to, value, data, gas parameters) in wallet.
2. Wallet signs Tx using private key (EOA).
3. Signed Tx is broadcast to the peer network and enters mempools.
4. A validator selects Tx and orders them in a block candidate.
5. Validator executes Tx in the **EVM** (bytecode if contract call).
6. Gas is charged per opcode; state updates happen as execution proceeds.
7. On `revert` or out‑of‑gas, changes are rolled back, but spent gas is not refunded.
8. Successful Tx updates balances/storage and may emit event logs.
9. Receipt is produced (status, gas used, logs).
10. Block inclusion + confirmations finalize the outcome.

**Mnemonic (write in exam margins):**
- **S‑B‑E‑S‑R‑B** = **Sign → Broadcast → Execute → State update → Receipt → Block**

### B3) Gas concept + fee formula + show one numeric step-by-step
1. **Gas** measures computation and storage usage in EVM execution.
2. Every opcode has a gas cost; storage writes are expensive.
3. Tx provides **GasLimit** (maximum allowed consumption).
4. Actual **GasUsed** depends on code path and storage changes.
5. Fee is paid even if transaction fails after consuming gas.
6. Basic fee equation:
   $$
   \text{TxFee} = \text{GasUsed} \times \text{EffectiveGasPrice}
   $$
7. EIP‑1559 idea: `EffectiveGasPrice = BaseFee + PriorityFee` (simplified).
8. If gas runs out: state reverts but the fee for used computation is still paid.
9. Users raise tip/fees for faster inclusion when blocks are full.
10. Gas protects the network against DoS and infinite loops.

**Numeric (show these exact steps):**
- Given: `GasUsed = 21000`, `EffectiveGasPrice = 30 gwei`
- Step 1: Fee $= 21000 \times 30\ \text{gwei}$
- Step 2: Fee $= 630000\ \text{gwei}$
- Step 3 (optional): $630000\ \text{gwei} = 0.00063\ \text{ETH}$ because $10^9\ \text{gwei} = 1\ \text{ETH}$

**Mnemonic:** **GLUF** → **G**as**L**imit caps, **U**sed is actual, **F**ee = Used × Price.

### B4) Explain elements present in Ethereum blockchain
1. **Blocks** group transactions and are linked by parent hash.
2. **Block header** contains commitments (roots/hashes) to block content.
3. **Transaction list** is the set of all included signed transactions.
4. **Receipts list** records execution results and log events.
5. **State trie (MPT)** commits to the entire world state (accounts).
6. **Transaction trie (MPT)** commits to all transactions in the block.
7. **Receipt trie (MPT)** commits to all receipts/logs for the block.
8. **Logs/events** enable indexing and off-chain app reactions.
9. **World state** represents balances, nonces, code, storage at a block height.
10. **EVM execution** is the mechanism that transforms state from block to block.

**Mnemonic:** **H‑TRS** → **H**eader commits to **T**ransactions, **R**eceipts, and **S**tate (via roots/tries).

### B5) Ethereum world state (explain + how to draw diagram)
1. World state is a mapping from addresses to account objects.
2. For each account it stores: `nonce`, `balance`, `codeHash`, `storageRoot`.
3. EOAs have no code; contracts have code and persistent storage.
4. Each block applies a deterministic state transition function to produce new state.
5. The **state root** in the block header commits to this world state.
6. Any state change changes the state trie and thus the state root.
7. This gives integrity: tampering changes header hash.
8. Reads (`view`) don’t change state; writes change state and cost gas.
9. State supports complex DApps because contracts can store arbitrary structured data.
10. It contrasts with Bitcoin’s UTXO set model.

**Mnemonic:** **BNCS** → account = **B**alance + **N**once + **C**ode + **S**torage.

**How to draw (30 seconds):**
1. Draw a big box: **World State (State Trie/MPT)**.
2. Inside, draw 2 rows: **EOA** and **Contract Account**.
3. For EOA list: `nonce`, `balance`.
4. For Contract list: `nonce`, `balance`, `code`, `storage`.
5. Arrow from “Block Execution (EVM)” into the state box: “updates state → new stateRoot”.

### B6) Transactions → Tx trie → Block header relation (explain + how to draw)
1. Transactions in a block are inserted into a deterministic **transaction trie**.
2. Trie nodes hash child links; leaves represent encoded transactions.
3. The final **transaction root hash** summarizes all transactions.
4. This root is stored in the **block header** as the Tx root field.
5. If any transaction changes, its leaf hash changes.
6. That change propagates upward changing internal node hashes.
7. The trie root changes.
8. Header hash changes because the header contains the root.
9. Therefore the header commits to all included transactions.
10. This gives tamper-evidence and efficient verification proofs.

**Mnemonic:** **TTRH** → **T**ransactions → **T**rie → **R**oot → **H**eader.

**How to draw (15 seconds):**
1. Draw 4 boxes left→right: `Transactions` → `Tx Trie (MPT)` → `Tx Root` → `Block Header`.
2. Add note under arrow: “any Tx change ⇒ root change ⇒ header hash change”.

### B7) Compare Bitcoin and Ethereum (10 points)
1. Goal: Bitcoin is primarily digital value transfer; Ethereum is a programmable platform.
2. State model: Bitcoin uses **UTXO**; Ethereum uses **account/world-state**.
3. Programming: Bitcoin has limited script; Ethereum has EVM smart contracts.
4. Transaction semantics: Bitcoin spends UTXOs; Ethereum updates account balances/storage.
5. Execution: Bitcoin script validation vs Ethereum general bytecode execution.
6. Fees: both have fees; Ethereum explicitly meters computation with gas.
7. Data structures: both use Merkle-style commitments; Ethereum uses MPT roots.
8. Typical apps: Bitcoin payments vs Ethereum DApps/DeFi/DAOs etc.
9. Flexibility vs simplicity: Ethereum is more flexible; Bitcoin is more minimal.
10. Both rely on cryptography + consensus to maintain a consistent ledger.

**Mnemonic:** **GSPEFA** → **G**oal, **S**tate model, **P**rogramming, **E**xecution, **F**ees, **A**pps.

### B8) Explain EVM (Ethereum Virtual Machine) with neat sketch idea
1. EVM is the runtime that executes contract bytecode.
2. It is deterministic: same input state + Tx ⇒ same output state.
3. It is stack-based (operates on a stack of 256-bit words).
4. It has **memory** (temporary) and **storage** (persistent per contract).
5. It has opcodes for arithmetic, control flow, calls, and storage access.
6. Gas is deducted per opcode; execution halts if gas is exhausted.
7. EVM runs in each node/validator during block validation.
8. It generates receipts/logs and success/revert result.
9. It enforces isolation: contracts cannot directly access external world data without oracles.
10. It is the “engine” that turns transactions into state transitions.

**Mnemonic:** **SMSG** → **S**tack, **M**emory, **S**torage, **G**as.

**Sketch to draw:**
- Box “EVM” with 3 inner boxes: `Stack`, `Memory`, `Storage`.
- Arrow in: “Tx data + gas”; arrow out: “State update + receipt/logs”.

### B9) Solidity control structures + how to score marks
1. `if/else` for branching decisions.
2. `for` loops for bounded iteration (careful: gas cost grows).
3. `while` loops (avoid unbounded loops in on-chain code).
4. `break` and `continue` for loop control.
5. `return` to exit with value.
6. `require(condition, msg)` for input/condition checks (refunds remaining gas on fail).
7. `revert(msg)` to explicitly revert.
8. `assert(condition)` for internal invariants (should never fail).
9. `try/catch` for external call failure handling.
10. Mention “prefer checks-effects-interactions pattern” for safety.

**Mnemonic:** **IFW + RRA** → **I**f/**F**or/**W**hile + **R**equire/**R**evert/**A**ssert.

### B10) Solidity datatypes (10 marks version)
1. Value types: `bool`, `uint/int`, `address`, `enum`.
2. Fixed bytes: `bytes1…bytes32` for hashes/IDs.
3. Dynamic bytes: `bytes` for variable-length.
4. `string` for UTF‑8 text (dynamic).
5. Arrays: fixed and dynamic arrays.
6. `struct` for custom records.
7. `mapping(K => V)` for key-value storage.
8. Storage locations: `storage`, `memory`, `calldata` and their use-cases.
9. Visibility: `public/private/internal/external` affects interface.
10. Mutability: `view/pure/payable` affects state-change and ETH receiving.

**Mnemonic:** **VFRM + SVM** → **V**alue, **F**ixed/dynamic bytes, **R**eference, **M**apping + **S**torage location, **V**isibility, **M**utability.

### B11) Solidity: Simple Bank contract (deposit/withdraw/view) + points
**Write this code (safe, simple, exam-friendly):**

```solidity
pragma solidity ^0.8.0;

contract SimpleBank {
    mapping(address => uint256) private balances;

    function deposit() external payable {
        require(msg.value > 0, "zero");
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "zero");
        require(balances[msg.sender] >= amount, "low");
        balances[msg.sender] -= amount;
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "fail");
    }

    function viewBalance() external view returns (uint256) {
        return balances[msg.sender];
    }
}
```

**10-mark explanation points (write as bullets/lines):**
1. Use mapping to store balance per address.
2. `deposit()` is `payable` to receive ETH.
3. Add `require(msg.value > 0)` to prevent empty deposits.
4. Update sender balance in mapping.
5. `withdraw(amount)` checks amount and sufficient balance.
6. Use checks‑effects‑interactions: reduce balance before sending.
7. Transfer using `call` and verify success.
8. `viewBalance()` is `view` and returns caller’s balance.
9. Functions use `msg.sender` for per-user accounting.
10. Require statements enforce safety and prevent invalid state.

**Mnemonic:** **DWB + CEI** → **D**eposit/**W**ithdraw/**B**alance + **C**hecks‑**E**ffects‑**I**nteractions.

### B12) Solidity: Voting contract (simple, prevents double voting)
```solidity
pragma solidity ^0.8.0;

contract SimpleVoting {
    struct Candidate {
        string name;
        uint256 voteCount;
    }

    Candidate[] private candidates;
    mapping(address => bool) private hasVoted;

    function addCandidate(string calldata name) external {
        candidates.push(Candidate({name: name, voteCount: 0}));
    }

    function vote(uint256 candidateId) external {
        require(!hasVoted[msg.sender], "voted");
        require(candidateId < candidates.length, "bad");
        hasVoted[msg.sender] = true;
        candidates[candidateId].voteCount += 1;
    }

    function getCandidate(uint256 id) external view returns (string memory, uint256) {
        require(id < candidates.length, "bad");
        Candidate storage c = candidates[id];
        return (c.name, c.voteCount);
    }
}
```

**10-mark scoring points:**
1. Candidate stored as struct; list stored in array.
2. `hasVoted` mapping prevents double voting.
3. `addCandidate` appends candidate.
4. `vote` checks not voted + valid id.
5. Mark voter as voted before increment.
6. Increment vote count.
7. Provide a view getter to read candidate name & votes.
8. Use `calldata` for input strings.
9. Use `require` for all constraints.
10. State changes cost gas; getters are `view`.

**Mnemonic:** **AVG + 1V** → **A**ddCandidate, **V**ote, **G**etCandidate + **1 voter = 1 vote**.

### B13) Solidity: Store & retrieve a single string
```solidity
pragma solidity ^0.8.0;

contract StringStore {
    string private value;

    function setValue(string calldata v) external {
        value = v;
    }

    function getValue() external view returns (string memory) {
        return value;
    }
}
```

**10-mark explanation points:**
1. `string` is a reference type stored in contract storage.
2. `setValue` writes to storage (costs gas).
3. Use `calldata` to avoid extra copy cost.
4. `getValue` is `view` (no state change).
5. Returns `string memory` for ABI return.
6. Demonstrates state persistence across calls.
7. Can be extended with access control if needed.
8. Shows basic contract interaction workflow.
9. Supports DApps needing on-chain text.
10. Simple example to demonstrate ABI-based function call.

**Mnemonic:** **SG** → **S**et then **G**et (write to storage, read via view).

### B14) Solidity libraries: how they are deployed/used (with example)
1. A Solidity **library** is reusable code that can be called by contracts.
2. Libraries typically contain `pure/view` helpers and avoid holding state.
3. Library functions can be `internal` (inlined) or `external` (linked to deployed library address).
4. Deployment flow: compile library → deploy library → link address into contract bytecode.
5. Linking is required when library functions are `external`.
6. `using X for Y;` attaches library functions as methods on a type.
7. Libraries reduce duplicate code and keep contracts smaller.
8. They can improve readability and maintainability.
9. They are commonly used for math, array utilities, and safe operations.
10. In exam, show both: the library code + contract using it.

**Mnemonic:** **CDLU** → **C**ompile → **D**eploy library → **L**ink address → **U**se in contract.

**Example:**
```solidity
pragma solidity ^0.8.0;

library MathLib {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        return a + b;
    }
}

contract UseLib {
    function sum(uint256 a, uint256 b) external pure returns (uint256) {
        return MathLib.add(a, b);
    }
}
```

---

## 3) 60-second Module 5 checklist (before entering exam hall)
- Write: `TxFee = GasUsed × EffectiveGasPrice` and 1 numeric example.
- Memorize: **S‑B‑E‑S‑R‑B** (Tx lifecycle).
- Draw: `Transactions → TxTrie → TxRoot → BlockHeader`.
- Code from memory: SimpleBank + StringStore skeleton.
