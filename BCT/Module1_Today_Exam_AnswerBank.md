# CST428 Blockchain Technologies (BCT) — Module 1 Answer Bank (Crypto + Hashing + Merkle + DHT)
Date: 30 Apr 2026

Built from your extracted QPs + Module‑1 crash guide.

---

## 0) Acronyms
- **AES**: Advanced Encryption Standard
- **RSA**: Rivest–Shamir–Adleman
- **ECC**: Elliptic Curve Cryptography
- **SHA‑256**: Secure Hash Algorithm 256-bit
- **DHT**: Distributed Hash Table
- **MAC**: Message Authentication Code

---

## 1) Part A (5 marks each; write exactly 5 points)

### A1) Symmetric vs asymmetric cryptography (QP: May 2024, June 2023)
1. Symmetric uses one shared secret key; asymmetric uses public/private key pair.
2. Symmetric is faster for bulk data; asymmetric is slower.
3. Symmetric has key distribution problem; asymmetric eases public sharing.
4. Symmetric commonly gives confidentiality; asymmetric gives signatures/identity.
5. Blockchain systems combine both (asymmetric signatures + symmetric session encryption).

**Mnemonic:** **1K‑2K** → Symmetric = **1 key**, Asymmetric = **2 keys**.

### A2) Secure hash functions strengthen blockchain (QP: June 2023)
1. Hash links blocks: each block stores previous hash (tamper-evident chain).
2. Hash provides integrity: any change alters hash drastically (avalanche).
3. Preimage resistance prevents reversing to find original data.
4. Collision resistance prevents forging two different blocks with same hash.
5. Merkle roots/hash roots commit to many transactions efficiently.

**Mnemonic:** **L‑I‑P‑C‑M** → Link, Integrity, Preimage, Collision, Merkle.

### A3) Benefits of Merkle trees (QP: May 2024)
1. Merkle root summarizes many transactions into one hash.
2. Inclusion proofs are small (logarithmic size).
3. Efficient verification for light clients.
4. Any leaf change changes root (easy tamper detection).
5. Root stored in header commits to entire transaction set.

**Mnemonic:** **R‑P‑L‑T‑H** → Root, Proof, Light clients, Tamper detect, Header commit.

### A4) DHT: what it is and how it works (QP: Oct 2023)
1. DHT is a decentralized key→value lookup system.
2. Keys are hashed into an identifier space.
3. Each node is responsible for a range of identifiers.
4. Routing forwards query to closer nodes until responsible node is reached.
5. Enables scalable decentralized discovery/storage mapping.

**Mnemonic:** **H‑S‑R‑F‑R** → Hash, Space, Responsibility, Forward, Resolve.

---

## 2) Expanded (10 marks style) answers (use if asked as Part‑B)

### B1) RSA workflow (key generation + encrypt/decrypt steps)
1. Choose two primes `p` and `q`.
2. Compute `n = p*q`.
3. Compute `phi(n) = (p-1)(q-1)`.
4. Choose public exponent `e` such that `gcd(e, phi(n)) = 1`.
5. Compute private exponent `d` such that `e*d ≡ 1 (mod phi(n))`.
6. Public key = `(e, n)`; private key = `(d, n)`.
7. Encryption: `C = M^e mod n`.
8. Decryption: `M = C^d mod n`.
9. In blockchain, RSA is conceptually important; most modern blockchains use ECC for signatures.
10. Writing steps in correct order earns method marks.

**Mnemonic:** **P‑Q‑N‑Φ‑E‑D** → pick **P,Q**, compute **N**, compute **Φ**, choose **E**, find **D**.

### B2) AES essentials (exam fixed points)
1. AES is a symmetric block cipher.
2. Block size is 128 bits.
3. Key sizes are 128/192/256 bits.
4. Core round steps: SubBytes, ShiftRows, MixColumns, AddRoundKey.
5. Final round omits MixColumns.
6. Uses substitution-permutation network style.
7. Designed for speed and security in practice.
8. Used for bulk encryption, not for signatures.
9. Often combined with asymmetric crypto for secure key exchange.
10. Mention “fast for large data” to score comparison marks.

**Mnemonic:** **SSMA** → SubBytes, ShiftRows, MixColumns, AddRoundKey.

### B3) Hash security properties (write as list)
1. Preimage resistance.
2. Second preimage resistance.
3. Collision resistance.
4. Avalanche effect.
5. Deterministic output.
6. Fixed-length digest.
7. Efficient computation.
8. Infeasible to find two inputs with same output.
9. Used for integrity and commitments.
10. Used in block links and Merkle roots.

**Mnemonic:** **P2CA** → **P**reimage, **P**reimage‑2nd, **C**ollision, **A**valanche.

### B4) Merkle tree diagram + how to draw
1. Leaves are transaction hashes.
2. Parent hash = hash(concat(left, right)).
3. Continue until one root remains (Merkle root).
4. Root commits to the entire set.
5. Inclusion proof is path of sibling hashes.
6. Proof size is O(log n).
7. Any change changes root.
8. Root stored in block header.
9. Enables light client verification.
10. Used widely in blockchains.

**Mnemonic:** **L‑P‑R** → Leaves → Parents → Root.

**How to draw (10 seconds):**
```text
      Root
     /   \
   H12   H34
   /\     /\
  H1 H2  H3 H4
```
