# Blockchain Technologies PYQ Master (Strict Exam Writing Edition)

Subject: CST428 Blockchain Technologies

Source mapping:
- BCT/ocr_work/qp/questions_extracted.json
- BCT/ocr_work/qp/CST428-QP_May_2024.txt
- BCT/ocr_work/qp/June_2023_Regular.txt
- BCT/ocr_work/qp/October_2023_Supplementary.txt

---

## SECTION 1: Unique Questions Module-Wise (No Answers)

## Module 1
1. Differentiate symmetric and asymmetric cryptography.
2. Compare symmetric and asymmetric key cryptography.
3. Explain how secure hash functions strengthen blockchain.
4. What are the benefits of Merkle trees?
5. Describe distributed hash tables and how they work.
6. What are the major components of block header?

## Module 2
1. Define blockchain and elaborate key terminologies.
2. Explain ecosystem of decentralization in blockchain.
3. Compare centralized and decentralized systems.
4. Explain methods to achieve decentralization.
5. Explain layered architecture of blockchain with neat diagram.
6. Explain benefits, features, and limitations of blockchain.

## Module 3
1. Describe two main categories of consensus mechanisms.
2. Explain need for consensus algorithms in blockchain.
3. Explain Paxos for crash fault tolerance.
4. Compare PoW and PoS.
5. Explain working of PoW consensus mechanism.
6. Explain steps in mining and role of miner.
7. Explain Bitcoin transaction validation process.
8. Explain payment flow in Bitcoin from user perspective.
9. Explain transaction structure, UTXO, and its verification role.
10. If Byzantine nodes f=6, find minimum PBFT node count.
11. What is Byzantine Generals problem and relevance?
12. What is Sybil attack and how Bitcoin mitigates it?
13. What is a wallet? Explain wallet types.

## Module 4
1. Define smart contract and list its properties.
2. Explain different types of oracles.
3. Explain generic data flow from smart contract to oracle.
4. Explain DApp design and architecture.
5. Explain blockchain use-cases in government.
6. Explain blockchain use-case in finance sector.
7. Explain impact of blockchain on healthcare.
8. Explain blockchain in supply chain management.
9. Explain impact of blockchain on AI and cloud ecosystems.

## Module 5
1. Illustrate role of EVM in Ethereum network.
2. Explain account types in Ethereum.
3. Explain Ethereum transaction types.
4. Explain transaction processing flow in Ethereum.
5. Explain concept of gas and transaction processing effect.
6. Show relation between transaction, transaction trie, and block header.
7. Explain elements present in Ethereum blockchain.
8. Explain concept of Ethereum world state.
9. Explain control structures and datatypes in Solidity.
10. Explain library deployment in Solidity with example.
11. Write Solidity bank contract (deposit, withdraw, balance).
12. Write Solidity voting contract.
13. Write Solidity single string storage contract.
14. Compare Bitcoin and Ethereum.

---

## SECTION 2: Part A Answers (Exactly 5 Points Each)

## Q1) Symmetric vs asymmetric cryptography
1. Symmetric uses one secret key; asymmetric uses public/private key pair.
2. Symmetric is faster for bulk encryption; asymmetric is slower.
3. Symmetric has key-distribution challenge; asymmetric simplifies public sharing.
4. Symmetric is used for data confidentiality; asymmetric for signatures and identity.
5. Blockchain systems combine both for practical security and performance.

## Q2) Benefits of Merkle trees
1. Merkle trees summarize many transactions into one root hash.
2. Inclusion proofs are short and efficient in logarithmic depth.
3. Any leaf modification changes root hash and reveals tampering.
4. Lightweight clients can verify inclusion without full block download.
5. Merkle roots are stored in block headers to protect transaction integrity.

## Q3) Two categories of consensus mechanisms
1. Proof-based category uses resource competition or stake selection.
2. Fault-tolerant category uses replica agreement under defined fault model.
3. Proof-based examples include PoW and PoS style protocols.
4. Fault-tolerant examples include Paxos-family and PBFT-family protocols.
5. Both categories target consistent ledger state across distributed nodes.

## Q4) Centralized vs decentralized features
1. Centralized systems rely on one authority, decentralized systems share control.
2. Centralized systems have single-point failure risk, decentralized systems improve resilience.
3. Centralized trust is institution-based, decentralized trust is protocol-based.
4. Decentralized systems are typically more censorship resistant.
5. Decentralized governance and upgrades can be coordination-heavy.

## Q5) Bitcoin transaction validation
1. Node verifies sender signature authenticity.
2. Node checks referenced UTXO existence.
3. Node confirms referenced UTXO is unspent.
4. Node verifies input amount is at least output amount.
5. Node validates script conditions before relay or inclusion.

## Q6) Smart contract properties
1. Smart contracts execute automatically once conditions are met.
2. Execution is deterministic across all validating nodes.
3. On-chain code and outcomes are transparent and auditable.
4. Historical execution records are tamper resistant.
5. Intermediary dependency is reduced for rule-based workflows.

## Q7) Oracle types
1. Software oracles fetch digital-source data feeds.
2. Hardware oracles bridge physical sensor data on-chain.
3. Inbound oracles move external data into blockchain context.
4. Outbound oracles trigger external systems from on-chain events.
5. Decentralized oracle networks reduce single-source trust risk.

## Q8) EVM role
1. EVM executes Ethereum smart contract bytecode deterministically.
2. It meters computation using gas to prevent abuse.
3. It applies state transitions after successful execution.
4. It ensures all nodes compute identical contract outcomes.
5. It enables Ethereum as a programmable blockchain platform.

## Q9) Ethereum account types
1. EOAs are controlled by private keys and can initiate transactions.
2. Contract accounts are controlled by deployed code execution.
3. EOAs do not hold executable bytecode.
4. Contract accounts store code and persistent storage.
5. EOAs trigger contract functions through signed transactions.

## Q10) Solidity datatypes
1. Value types include bool, uint, int, address, and fixed-size bytes.
2. Reference types include arrays, strings, and structs.
3. Mapping type stores key-value association with hashed lookup.
4. Storage location semantics affect gas and mutability behavior.
5. Correct datatype selection improves safety and contract efficiency.

---

## SECTION 3: Part B Answers (Exactly 10 Points Each)

## Q1) Explain Paxos and crash fault tolerance
1. Paxos is a consensus protocol designed for crash fault tolerance.
2. Its main roles are proposer, acceptor, and learner.
3. Proposer starts with Prepare message carrying proposal number N.
4. Acceptors reply Promise and reject lower-numbered proposals.
5. Proposer sends Accept request for chosen value V.
6. Acceptors accept V if promise conditions are respected.
7. Learners receive accepted value updates from acceptors.
8. Majority intersection guarantees one consistent chosen value.
9. Protocol tolerates crash faults as long as majority remains reachable.
10. Typical message order is Prepare, Promise, Accept, Learn.

## Q2) Compare PoW and PoS with workflow
1. PoW chooses proposer by solving computational hash puzzle.
2. PoS chooses proposer primarily by staked economic weight.
3. PoW workflow is collect transactions, build block, iterate nonce, hit target, broadcast.
4. PoS workflow is stake lock, proposer selection, attestation, finalization.
5. PoW security cost is tied to dominant hash-power acquisition.
6. PoS security cost is tied to dominant stake and slashing exposure.
7. PoW has high energy footprint due puzzle competition.
8. PoS generally has lower energy demand than PoW.
9. Both require network-wide validation before canonical acceptance.
10. Both aim to prevent conflicting histories and double spending.

## Q3) Explain Bitcoin payment flow from user perspective
1. Sender wallet selects recipient address and transfer amount.
2. Wallet selects spendable UTXOs as transaction inputs.
3. Wallet creates outputs for recipient and possible change.
4. Sender signs transaction using private key.
5. Signed transaction is broadcast to P2P network.
6. Nodes verify signature, script, and UTXO validity.
7. Miners pick valid transaction from mempool.
8. Miner includes transaction in block candidate and mines block.
9. Network accepts block after consensus validation.
10. Receiver confidence increases with additional confirmations.

## Q4) Explain mining algorithm and role of miner
1. Miner collects unconfirmed transactions from mempool.
2. Miner validates each transaction against protocol rules.
3. Miner builds block candidate with valid transactions.
4. Miner computes block header hash with varying nonce.
5. Miner repeats hashing until target difficulty is met.
6. Winning miner broadcasts valid block to network.
7. Other nodes verify block and transaction validity.
8. Accepted block extends canonical chain state.
9. Miner receives block reward and transaction fees.
10. Mining secures ordering, immutability, and anti-double-spend guarantees.

## Q5) Explain transaction structure, UTXO, and verification
1. Bitcoin transaction consumes old outputs and creates new outputs.
2. Input references previous transaction ID and output index.
3. Input carries unlocking script and signature evidence.
4. Output defines amount and locking script conditions.
5. UTXO means unspent transaction output available for spending.
6. Verification checks referenced UTXO existence.
7. Verification ensures referenced UTXO is unspent.
8. Verification validates script and cryptographic signature.
9. Verification checks input sum is at least output sum.
10. This model prevents unauthorized spending and double spending.

## Q6) Explain oracle data flow and oracle ecosystem
1. Smart contract emits request for external data value.
2. Oracle nodes fetch requested data from configured sources.
3. Data is validated, normalized, and optionally filtered.
4. Multiple oracle responses are collected for robustness.
5. Aggregation rule such as median reduces outlier influence.
6. Aggregated value is posted to blockchain as response transaction.
7. Contract consumes response and executes conditional logic.
8. Inbound oracle brings external data on-chain.
9. Outbound oracle can trigger off-chain action from on-chain event.
10. Decentralized oracle design reduces single-source manipulation risk.

## Q7) Explain DApp architecture with neat design flow
1. DApp frontend provides user interface for interaction.
2. Wallet layer handles authentication and transaction signing.
3. Web3 library builds contract calls and submits transactions.
4. RPC interface connects client to blockchain node.
5. Smart contracts implement deterministic business logic.
6. Blockchain stores state transitions and event logs.
7. Optional off-chain storage handles large file payloads.
8. Read operations fetch state via calls without transaction cost.
9. Write operations produce signed transactions and gas spending.
10. Trust model shifts from platform operator to protocol execution.

## Q8) Explain Ethereum transaction processing and gas
1. User wallet prepares and signs Ethereum transaction.
2. Transaction includes nonce, destination, value, data, and gas parameters.
3. Signed transaction propagates through peer network mempools.
4. Validator executes transaction bytecode in EVM context.
5. Gas is consumed per opcode during execution.
6. If gas runs out, state update reverts while spent gas remains charged.
7. Successful execution generates receipt and log events.
8. Fee is computed as GasUsed multiplied by EffectiveGasPrice.
9. EffectiveGasPrice includes base fee and priority fee components.
10. Transaction finality follows block inclusion and protocol confirmation.

## Q9) Explain trie-header relation in Ethereum
1. Transactions are inserted into deterministic transaction trie structure.
2. Trie leaves represent encoded transaction data items.
3. Trie internal nodes hash child links recursively.
4. Trie root hash summarizes complete transaction set.
5. Transaction root is stored in block header field.
6. Any transaction mutation changes path hashes.
7. Changed path hashes update trie root hash value.
8. Changed root changes block header hash fingerprint.
9. Header hash chaining protects block history integrity.
10. Therefore header commitment secures all included transactions.

## Q10) Explain world state and compare Bitcoin vs Ethereum
1. Ethereum world state maps accounts to balances, nonce, code, and storage.
2. Each block execution transforms old state into new state.
3. State root in header commits cryptographically to entire world state.
4. EVM execution applies deterministic state transition function.
5. Receipts and logs provide execution outcome evidence.
6. Bitcoin model tracks UTXOs rather than account-state mapping.
7. Ethereum model supports direct account balance and contract storage updates.
8. Bitcoin script model is intentionally limited for simplicity.
9. Ethereum supports expressive smart contracts through EVM.
10. Both systems rely on consensus and cryptographic integrity guarantees.

## Q11) PBFT minimum nodes numerical (f=6)
1. Problem asks minimum total nodes for Byzantine tolerance when faults f=6.
2. PBFT condition is n greater than or equal to 3f plus 1.
3. Write formula: n >= 3f + 1.
4. Substitute f = 6 into expression.
5. Compute n >= 3*6 + 1.
6. Compute n >= 18 + 1.
7. Therefore n >= 19.
8. Minimum integer node count satisfying condition is 19.
9. With fewer than 19 nodes, PBFT guarantee is violated for f=6.
10. Final answer: required minimum nodes equal 19.
