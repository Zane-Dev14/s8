# Blockchain Technologies PYQ Solved Master (All Modules)

Subject: CST428 Blockchain Technologies

Built from:
- BCT/ocr_work/qp/questions_extracted.json
- BCT/STEP2_Module1_CrashGuide.md
- BCT/STEP3_Module2_CrashGuide.md
- BCT/STEP4_Module3_CrashGuide.md
- BCT/STEP5_Module4_CrashGuide.md
- BCT/STEP6_Module5_CrashGuide.md

Goal:
- Complete high-quality answer bank for the hardest subject
- 3-mark rapid answers + 14-mark structured answers
- Diagrams/formulas/code where required

---

## How To Score with This File

For every 14-mark answer use:
1. Definition/context
2. Core architecture or formula
3. Ordered steps
4. Neat diagram
5. Use-case/security note
6. Conclusion

For coding questions:
1. State variables
2. Constructor/setup (if needed)
3. Required functions only
4. require-based checks
5. Event or getter for visibility

---

## Module 1 Solved Answers

### M1-Q1: Differentiate symmetric and asymmetric cryptography (3 marks)

Answer:
1. Symmetric uses one shared key; asymmetric uses public/private key pair.
2. Symmetric is faster; asymmetric is computationally heavier.
3. Symmetric has key-distribution challenge; asymmetric solves easier public distribution.
4. Symmetric examples: AES; asymmetric examples: RSA, ECC.
5. Blockchain systems use both together for practical security-performance balance.

---

### M1-Q2: Benefits of Merkle trees (3 marks)

Answer:
1. Efficient transaction inclusion proof (logarithmic proof size).
2. Fast integrity verification without downloading full block data.
3. Tamper evidence: leaf change propagates to root hash change.
4. Scalable for large transaction sets.
5. Essential for lightweight/SPV-style verification.

---

### M1-Q3: How secure hash functions strengthen blockchain

Answer:
1. They bind block contents to compact digest values.
2. They make tampering detectable because changed data changes hash.
3. They link blocks through previous-hash pointers.
4. They support Merkle roots for transaction integrity.
5. Security relies on pre-image and collision resistance.

---

### M1-Q4: RSA workflow (short long-answer form)

Steps:
1. Select primes $p,q$.
2. Compute $n=pq$.
3. Compute $\phi(n)=(p-1)(q-1)$.
4. Select $e$ with $gcd(e,\phi(n))=1$.
5. Compute $d$ such that $ed\equiv1\ (mod\ \phi(n))$.
6. Public key $(e,n)$, private key $(d,n)$.
7. Encrypt: $C=M^e\ mod\ n$.
8. Decrypt: $M=C^d\ mod\ n$.

---

## Module 2 Solved Answers

### M2-Q1: Define blockchain and key terminologies (3 marks)

Answer:
1. Blockchain is a distributed append-only ledger maintained by consensus.
2. Transaction: state-change request.
3. Block: validated transaction container.
4. Previous hash: pointer to prior block.
5. Nonce: variable used in proof computations.
6. Merkle root: compact summary of block transactions.

---

### M2-Q2: Explain working of blockchain with neat diagram (7 marks)

Answer structure:
1. User creates and signs transaction.
2. Transaction broadcast over P2P network.
3. Nodes verify transaction validity.
4. Valid transactions are grouped into candidate block.
5. Consensus algorithm selects valid next block.
6. Block is appended with previous-hash link.
7. Ledger copy is updated across participating nodes.

Diagram:

```text
Create TX -> Broadcast -> Validate -> Form Block -> Consensus -> Append -> Replicate
```

Conclusion:
- This process gives tamper-evident, decentralized agreement without central authority.

---

### M2-Q3: Explain layered blockchain architecture (7 marks)

Answer:
1. Network layer: base communication.
2. P2P layer: node discovery and propagation.
3. Cryptography layer: hashing and signatures.
4. Consensus layer: agreement logic.
5. Execution layer: transaction and contract execution.
6. Application layer: user-facing services and DApps.

Diagram:

```text
Application
Execution
Consensus
Cryptography
P2P
Network
```

---

### M2-Q4: Centralized vs decentralized systems

Answer:
1. Centralized has single authority; decentralized has distributed control.
2. Centralized has single-point failure; decentralized improves fault tolerance.
3. Centralized trust is institution-based; decentralized trust is protocol-based.
4. Decentralized systems are more censorship resistant.
5. Tradeoff: decentralization can add coordination overhead.

---

## Module 3 Solved Answers

### M3-Q1: Need for consensus + CFT/BFT (7 marks)

Answer:
1. Blockchain needs consensus because no central final authority exists.
2. Consensus prevents conflicting ledger states and double spend.
3. CFT handles crash/silent faults.
4. BFT handles malicious/Byzantine faults.
5. PoW/PoS style protocols secure open blockchain participation.
6. PBFT-style protocols provide deterministic fault-tolerant agreement in constrained settings.

---

### M3-Q2: Paxos algorithm for crash fault tolerance (7/8 marks)

Roles:
- Proposer, Acceptor, Learner.

Phases:
1. Prepare(N): proposer asks acceptors.
2. Promise: acceptors promise not to accept lower-numbered proposals.
3. Accept(V): proposer requests acceptance of value.
4. Learn: majority-accepted value becomes chosen.

Diagram:

```text
Proposer -> Acceptors : PREPARE
Acceptors -> Proposer : PROMISE
Proposer -> Acceptors : ACCEPT
Acceptors -> Learners : LEARN
```

Why correct:
- Majority intersection ensures a single consistent chosen value.

---

### M3-Q3: Compare PoW and PoS (7 marks)

| Aspect | PoW | PoS |
|---|---|---|
| Leader selection | Hash puzzle winner | Stake-weighted validator selection |
| Resource base | Computational power | Economic stake |
| Energy usage | High | Lower |
| Attack cost | Requires dominant hash power | Requires dominant stake + slashing risk |
| Hardware dependency | High | Lower |

---

### M3-Q4: Bitcoin mining algorithm + role of miner

Answer:
1. Miner collects pending transactions from mempool.
2. Miner validates each transaction.
3. Miner builds block candidate.
4. Miner iterates nonce until hash meets target.
5. Successful block is broadcast and verified.
6. Miner receives reward/fees.

Flowchart:

```text
Mempool -> Verify -> Build Candidate -> Hash Loop -> Target? -> Broadcast
```

---

### M3-Q5: Bitcoin payment flow from user perspective

Answer:
1. Sender wallet selects recipient and amount.
2. Wallet picks spendable UTXOs as inputs.
3. Transaction outputs created for receiver and change.
4. Sender signs transaction with private key.
5. Transaction broadcast to network.
6. Nodes validate and miners include in block.
7. Confirmations accumulate for final confidence.

---

### M3-Q6: Transaction validation and UTXO use

Validation checklist:
1. Signature is valid.
2. Referenced UTXO exists.
3. Referenced UTXO unspent.
4. Input value >= output value.
5. Script checks pass.

UTXO role:
- UTXOs are spendable outputs; each input consumes prior UTXO references.

Diagram:

```text
Inputs (prev UTXOs + signatures) -> Transaction Core -> Outputs (recipient + change)
```

---

### M3-Q7: PBFT minimum nodes numerical

Question pattern:
- If Byzantine nodes $f=6$, find minimum nodes $n$.

Formula:
$$
n \ge 3f+1
$$
Substitute:
$$
n \ge 3(6)+1=19
$$
Final answer:
- Minimum required nodes = 19.

---

## Module 4 Solved Answers

### M4-Q1: Define smart contracts and properties (3 marks)

Answer:
1. Smart contract is blockchain-deployed program logic.
2. Executes automatically when trigger conditions are met.
3. Behavior is deterministic and auditable.
4. Reduces intermediary dependence.
5. Provides tamper-resistant execution history.

---

### M4-Q2: Explain oracle types (3/7 marks)

Types:
1. Software oracle
2. Hardware oracle
3. Inbound oracle
4. Outbound oracle
5. Centralized oracle
6. Decentralized oracle

Key point:
- Oracles bridge off-chain data to on-chain contract logic.

---

### M4-Q3: Generic data flow from smart contract to oracle (7 marks)

Answer:
1. Contract emits data request.
2. Oracle nodes fetch requested external data.
3. Data is validated/normalized.
4. Multiple responses can be aggregated (often median).
5. Verified value is posted on-chain.
6. Contract consumes returned value and executes action.

Diagram:

```text
Contract Request -> Oracle Fetch -> Validate/Aggregate -> On-chain Response -> Contract Action
```

---

### M4-Q4: DApp architecture and design (7 marks)

Answer:
1. Frontend UI for user interaction.
2. Wallet/signing layer for user authorization.
3. Web3 library to call blockchain RPC.
4. Smart contract backend for business logic.
5. Blockchain state/events for persistent trust layer.
6. Optional off-chain storage for large files.

Diagram:

```text
UI -> Wallet/Web3 -> RPC Node -> Smart Contract -> Blockchain State
```

---

### M4-Q5: Use-case answers (government, finance, healthcare, supply chain)

Government:
- Land records, subsidy flow, procurement audit, verifiable certificates.

Finance:
- Faster settlement, programmable escrow, auditability, reduced reconciliation overhead.

Healthcare:
- Consent-based sharing, immutable logs, medicine provenance.

Supply chain:
- Product traceability, sensor-backed verification, milestone payment automation.

---

## Module 5 Solved Answers

### M5-Q1: Role of EVM in Ethereum network (3 marks)

Answer:
1. EVM executes smart contract bytecode deterministically across nodes.
2. It enforces gas-based metering to bound computation.
3. It applies state transitions after valid transaction execution.
4. It enables Ethereum’s programmable blockchain model.

---

### M5-Q2: Ethereum account types and differences

Answer:
1. EOA: controlled by private key, can initiate transactions.
2. Contract account: controlled by code, executes on invocation.
3. EOAs do not store contract bytecode.
4. Contract accounts include code and persistent storage.

---

### M5-Q3: Ethereum transaction types

Answer:
1. Value transfer transaction.
2. Contract interaction (function call) transaction.
3. Contract creation transaction.

---

### M5-Q4: Explain transaction processing in Ethereum + gas effect

Processing flow:
1. Wallet signs transaction.
2. Transaction broadcast.
3. Validators/miners execute via EVM.
4. State updates if execution succeeds.
5. Receipt/logs generated and block inclusion occurs.

Gas formula:
$$
\text{Fee} = \text{Gas Used} \times \text{Effective Gas Price}
$$

Impact:
1. Complex operations cost more.
2. Insufficient gas causes revert while consuming spent computation.

---

### M5-Q5: Relationship between transactions, trie, and block header

Answer:
1. Transactions are organized in transaction trie.
2. Trie root hash is written into block header.
3. Any transaction modification changes trie root.
4. Changed root changes header hash.
5. Therefore block header secures full transaction-set integrity.

---

### M5-Q6: Ethereum world state (Bitcoin vs Ethereum answer support)

World state definition:
- Snapshot mapping of all account balances, nonces, contract code and storage at a block height.

State transition view:

```text
Pre-State + Transactions -> EVM Execution -> Post-State + New State Root
```

Bitcoin vs Ethereum core compare:
1. Bitcoin: UTXO-focused value-transfer chain.
2. Ethereum: account-state + programmable contracts.

---

### M5-Q7: Solidity datatypes and control structures

Datatypes:
1. Value: bool, uint, int, address, bytes32
2. Reference: array, string, struct
3. Mapping: mapping(key => value)

Control structures:
1. if/else
2. for/while
3. require/revert/assert

---

### M5-Q8: Solidity bank contract template (exam-ready)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleBank {
    mapping(address => uint256) private balances;

    function deposit() external payable {
        require(msg.value > 0, "Zero deposit");
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Zero amount");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function viewBalance() external view returns (uint256) {
        return balances[msg.sender];
    }
}
```

---

### M5-Q9: Solidity voting contract template (exam-ready)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Voting {
    struct Candidate { string name; uint256 votes; }
    Candidate[] public candidates;
    mapping(address => bool) public hasVoted;

    constructor(string[] memory names) {
        for (uint i = 0; i < names.length; i++) {
            candidates.push(Candidate(names[i], 0));
        }
    }

    function vote(uint256 candidateId) external {
        require(!hasVoted[msg.sender], "Already voted");
        require(candidateId < candidates.length, "Invalid candidate");
        hasVoted[msg.sender] = true;
        candidates[candidateId].votes += 1;
    }
}
```

---

### M5-Q10: Solidity simple string storage template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StringStore {
    string private value;

    function setValue(string calldata newValue) external {
        value = newValue;
    }

    function getValue() external view returns (string memory) {
        return value;
    }
}
```

---

## Final 45-Minute BCT Drill

1. Revise fixed comparison tables:
   - Symmetric vs asymmetric
   - PoW vs PoS
   - Bitcoin vs Ethereum
2. Revise fixed formulas:
   - PBFT: $n \ge 3f+1$
   - Ethereum fee: gas used * effective gas price
3. Practice three must-draw diagrams:
   - Blockchain workflow
   - Oracle data flow
   - Transactions -> trie -> header
4. Practice one Solidity code answer from memory.
5. Attempt one full Module 3 and one full Module 5 long answer in exam format.
