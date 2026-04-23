# STEP 5: Module 4 Crash Guide (Smart Contracts, Oracles, DApps, Use-Cases)

Module focus:
- Programmable trust
- Off-chain data integration through oracles
- DApp design and real-world sectors

---

## 1) Smart Contracts

Definition:
A smart contract is deterministic program logic deployed on blockchain that executes when predefined conditions are satisfied.

Key properties:
1. Automatic execution.
2. Deterministic behavior.
3. Transparency and auditability.
4. Tamper-resistant history.
5. Reduced intermediary dependence.

---

## 2) Oracle Problem and Oracle Types

Why oracles are needed:
On-chain contracts cannot natively trust external data feeds.

Oracle types:
1. Software oracle.
2. Hardware oracle.
3. Inbound oracle.
4. Outbound oracle.
5. Centralized oracle.
6. Decentralized oracle.

Generic data-flow:
```text
Contract Request -> Oracle Fetch -> Validate/Aggregate -> On-chain Response -> Contract Action
```

Common aggregation formula:
$$
FinalValue = median(v_1, v_2, ..., v_n)
$$

---

## 3) DApp Architecture

Core blocks:
1. Frontend UI.
2. Wallet/signature layer.
3. Web3 client library.
4. RPC node interface.
5. Smart contract backend.
6. Blockchain state and events.
7. Optional off-chain storage.

Architecture sketch:
```text
UI -> Wallet/Web3 -> RPC -> Smart Contract -> Blockchain State
```

---

## 4) Government Use-Cases

1. Land registry with immutable change history.
2. Subsidy and welfare disbursal transparency.
3. Public procurement audit trails.
4. Verifiable certificates and document attestation.

---

## 5) Finance Use-Cases

1. Faster settlement and reconciliation.
2. Programmable escrow and conditional release.
3. Better compliance auditability.
4. Reduced intermediary and reconciliation overhead.

---

## 6) Healthcare Use-Cases

1. Consent-driven record sharing.
2. Immutable access logs for audits.
3. Drug provenance and anti-counterfeit tracking.
4. Cross-institution interoperability trust layer.

---

## 7) Supply Chain Use-Cases

1. End-to-end product traceability.
2. IoT and oracle-based condition verification.
3. Automated milestone-based payment release.
4. Lower dispute through shared immutable records.

---

## 8) Blockchain with AI and Cloud

1. AI data lineage and provenance tracking.
2. Smart-contract-based controlled data access.
3. Cross-organization trust layer for cloud workflows.
4. Compliance and audit support across distributed actors.

---

## 9) Module 4 Final Drill

1. Learn one-line smart contract definition exactly.
2. Draw oracle flow once from memory.
3. Draw DApp architecture once from memory.
4. Prepare four bullets each for government and finance use-cases.
