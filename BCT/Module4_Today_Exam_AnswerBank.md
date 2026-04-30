# CST428 Blockchain Technologies (BCT) — Module 4 Answer Bank (Smart Contracts, Oracles, DApps, Use‑Cases)
Date: 30 Apr 2026

Built from your extracted QPs (May 2024, June 2023, Oct 2023 Suppl.) + Module‑4 crash guide.

---

## 0) Acronyms (write expansions once, then use short forms)
- **SC**: Smart Contract
- **DApp**: Decentralized Application
- **UI**: User Interface
- **RPC**: Remote Procedure Call
- **JSON‑RPC**: JSON based RPC used by Ethereum nodes
- **API**: Application Programming Interface
- **ABI**: Application Binary Interface
- **Oracle**: Trusted data bridge (external ↔ on-chain)
- **IoT**: Internet of Things

---

## 1) Part A (5 marks each; write exactly 5 points)

### A1) Define smart contract + properties
1. Smart contract is deterministic program logic deployed on a blockchain.
2. It executes automatically when trigger/conditions are met.
3. Execution is deterministic across nodes (same input ⇒ same output).
4. Logic and results are transparent/auditable.
5. It reduces intermediary dependence and provides tamper-evident history.

**Mnemonic:** **ADTRA** → **A**utomatic, **D**eterministic, **T**ransparent, **R**esistant (tamper), **A**utomation replaces intermediary.

### A2) Types of oracles (list + 1-line each)
1. **Software oracle**: pulls data from online sources/APIs.
2. **Hardware oracle**: pulls data from sensors/IoT devices.
3. **Inbound oracle**: external → blockchain (price feeds, weather).
4. **Outbound oracle**: blockchain → external action (trigger a system).
5. **Centralized oracle**: single provider; simpler but single point of failure.

**Mnemonic:** **SHIOC** → **S**oftware, **H**ardware, **I**nbound, **O**utbound, **C**entralized.

---

## 2) Part B (10 marks each)

### B1) Discuss oracles in blockchain ecosystem + generic data flow (QP: May 2024)
1. Smart contracts cannot directly access off-chain data securely (oracle problem).
2. Oracle is an external system that fetches/verifies data and posts it on-chain.
3. Oracles enable real-world triggers: prices, identity, IoT readings, web APIs.
4. Oracle designs can be centralized (one source) or decentralized (many sources).
5. Data quality risks: manipulation, downtime, incorrect feeds.
6. Mitigation: multiple sources, reputation, cryptographic proofs, staking.
7. Generic flow: contract emits request/event for specific data.
8. Oracle fetches data from source(s), validates/normalizes it.
9. Oracle submits response to chain; contract reads response and executes logic.
10. Good oracle design improves reliability and reduces trust in a single party.

**Mnemonic:** **REQ‑FETCH‑POST‑ACT** → Request → Fetch → Post on-chain → Act in contract.

**Diagram to draw (20 seconds):**
```text
Contract Request -> Oracle Fetch -> Validate/Aggregate -> On-chain Response -> Contract Action
```

### B2) Outline DApp design / basic architecture with neat diagram (QP: May 2024, June 2023, Oct 2023)
1. DApp has a **frontend UI** for users.
2. Wallet layer signs transactions (user authentication via keys).
3. Web3/SDK builds calls/transactions from UI inputs.
4. UI connects to blockchain node via **RPC/JSON‑RPC**.
5. Smart contracts implement the backend business logic.
6. Blockchain stores state and event logs.
7. Read operations use calls (no state change), write operations use transactions (gas/fees).
8. Off-chain storage (IPFS/DB) can store large data; chain stores hashes/refs.
9. Events enable UI updates and indexing.
10. Trust shifts from platform operator to protocol/contract execution.

**Mnemonic:** **U‑W‑W‑R‑S‑B** → **U**I → **W**allet → **W**eb3 → **R**PC → **S**mart contract → **B**lockchain.

**How to draw (15 seconds):**
```text
UI -> Wallet/Web3 -> RPC Node -> Smart Contract -> Blockchain State/Events
                \-> (optional) Off-chain Storage
```

### B3) Government services use-cases (QP: May 2024)
1. **Land registry**: immutable ownership change history.
2. **Certificates**: verifiable educational/birth certificates.
3. **Public procurement**: audit trail for bids and awards.
4. **Welfare/subsidy**: transparent distribution and reduced leakage.
5. **Identity/KYC sharing**: consent-based verification across agencies.
6. **Voting** (conceptual): auditable counting + integrity (with strong design caveats).
7. **Tax/records**: tamper-evident logs.
8. Benefits: transparency, auditability, reduced fraud.
9. Needs: privacy controls + governance + legal acceptance.
10. Use blockchain mainly where multi-party trust/audit is required.

**Mnemonic:** **L‑C‑P‑W** → **L**and, **C**ertificates, **P**rocurement, **W**elfare.

### B4) Finance sector use-case (QP: May 2024, June 2023)
1. Problem: settlement is slow due to many intermediaries + reconciliation.
2. Blockchain enables shared ledger for faster settlement.
3. Smart contracts enable programmable escrow/conditional release.
4. Atomic delivery-versus-payment concepts reduce counterparty risk.
5. Transparent audit trails help compliance reporting.
6. Tokenization can represent assets digitally for transfer.
7. Reduced duplication of records across institutions.
8. Challenges: privacy, regulation, scalability.
9. Permissioned chains often used for enterprise finance.
10. Result: faster, auditable, and more automated workflows.

**Mnemonic:** **SEAT** → **S**ettlement, **E**scrow, **A**udit, **T**okenization.

### B5) Healthcare impact (QP: June 2023)
1. Healthcare needs controlled sharing of records across hospitals.
2. Blockchain can store hashes/permissions (not necessarily full data on-chain).
3. Patients can grant/revoke consent for record access.
4. Access logs become immutable for audits.
5. Drug supply provenance reduces counterfeits.
6. Interoperability improves through shared trust layer.
7. Smart contracts can automate insurance/claims workflows.
8. Privacy must be preserved (encryption, off-chain storage, access control).
9. Regulatory compliance is required.
10. Overall: better traceability + consent-based sharing + auditability.

**Mnemonic:** **CLAP‑DI** → **C**onsent, **L**ogs, **A**ccess control, **P**rovenance + **D**ata off-chain, **I**nteroperability.

### B6) Impact of blockchain on AI/cloud ecosystems (QP: June 2023)
1. AI needs trustworthy datasets and provenance.
2. Blockchain can record **data lineage** and version history.
3. Smart contracts can enforce access policies and payments for data.
4. Audit trails help compliance across organizations.
5. Federated/consortium settings benefit from shared trust layer.
6. Cloud workflows can use blockchain for cross-tenant coordination.
7. Limitations: throughput/latency; not suitable for heavy AI compute.
8. Store large data off-chain; store hashes + permissions on-chain.
9. Improves accountability of model/data usage.
10. Enables marketplaces for data/models with verifiable usage logs.

**Mnemonic:** **LAMP** → **L**ineage, **A**ccess control, **M**arketplace, **P**rovenance.

### B7) Supply chain management use-case (QP: Oct 2023 Suppl.)
1. Supply chains need traceability from source to customer.
2. Blockchain can record each handoff as an immutable event.
3. Provenance helps detect counterfeit goods.
4. IoT sensors (via oracles) can log temperature/location compliance.
5. Shared ledger reduces disputes and mismatched records.
6. Smart contracts automate milestone payments.
7. Improves recall processes by identifying affected batches quickly.
8. Needs: reliable data input (oracle trust is key).
9. Often implemented as permissioned consortium networks.
10. Result: transparency + trust + faster audits.

**Mnemonic:** **TRACE** → **T**raceability, **R**ecalls, **A**nti‑counterfeit, **C**ondition (IoT), **E**scrow payments.
