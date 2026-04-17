# STEP 5: Module 4 Crash Guide (Smart Contracts, Oracles, DApps, Sector Use-Cases)

Module 4 focus:
- Programmable trust systems
- Oracle-assisted contract execution
- DApp architecture and applications

Mapped from:
- BCT/Important Notes ALl Modules/Module4_DApps_Notes.tex
- BCT/ocr_work/qp/questions_extracted.json

---

## Topic 1: Smart Contracts

Definition:
- A smart contract is blockchain-stored program logic that auto-executes when predefined conditions are satisfied.

Properties:
1. Automatic execution
2. Deterministic behavior
3. Transparent logic
4. Tamper resistance/immutability
5. Reduced intermediary dependence

---

## Topic 2: Oracles and Oracle Problem

Why needed:
- Contracts cannot directly fetch off-chain data securely by themselves.

Oracle types:
1. Software oracle
2. Hardware oracle
3. Inbound oracle
4. Outbound oracle
5. Centralized oracle
6. Decentralized oracle

Oracle data-flow:

```text
Contract request -> Oracle fetch -> Validate/Aggregate -> On-chain response -> Contract action
```

Aggregation idea (common):
$$
\text{Final value} = median(v_1, v_2, ..., v_n)
$$

---

## Topic 3: DApps (Decentralized Applications)

Definition:
- Apps where business logic is primarily on-chain via smart contracts.

Architecture blocks:
1. Frontend (web/mobile)
2. Wallet and signing layer
3. Web3 library
4. RPC/node access
5. Smart contract backend
6. Blockchain state/events
7. Optional off-chain file storage (IPFS etc.)

Diagram:

```text
UI -> Wallet/Web3 -> RPC Node -> Smart Contract -> Blockchain State
```

---

## Topic 4: Blockchain in Government Services

High-score points:
1. Tamper-evident land record management
2. Transparent subsidy disbursal
3. Procurement audit trails
4. Verifiable digital certificates and document attestation

---

## Topic 5: Blockchain in Finance

Use-case angles:
1. Faster settlement and reconciliation
2. Programmable escrow and conditional release
3. Auditability and compliance traceability
4. Reduced intermediary risk in multi-party workflows

---

## Topic 6: Blockchain in Healthcare

Use-case angles:
1. Consent-driven record sharing
2. Immutable access logs
3. Drug provenance and anti-counterfeit tracking
4. Cross-hospital trust and interoperability

---

## Topic 7: Blockchain in Supply Chain

Use-case angles:
1. End-to-end traceability
2. IoT/oracle driven condition verification
3. Smart-contract based milestone payments
4. Dispute reduction via shared immutable history

---

## Topic 8: Blockchain + AI / Cloud

Blockchain + AI:
1. Data lineage and traceability for model trust
2. Automated model access/payment logic via contracts

Blockchain + Cloud:
1. Shared trust layer across organizations
2. Compliance and audit support for cloud workflows

---

## Module 4 PYQ Attack Set

1. Define smart contracts and properties
2. Explain oracle types and data flow
3. Design/basic architecture of a DApp with diagram
4. Blockchain in government services
5. Blockchain in finance sector use-case
6. Blockchain in healthcare/supply chain
7. Impact of blockchain on AI/cloud

---

## Last-Minute Revision Grid

1. Memorize one-line smart contract definition.
2. Draw oracle flow in 20 seconds.
3. Draw DApp architecture once.
4. Keep 4 use-case bullets each for government and finance.
