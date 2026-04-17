# STEP 2: Module 1 Crash Guide (Cryptography, Hashing, Merkle, DHT)

Module 1 focus:
- Cryptographic foundations for blockchain
- Hashing and integrity structures
- Exam-prone algorithm explanations

Mapped from:
- BCT/Important Notes ALl Modules/Module1_Blockchain_Technologies_Notes.tex
- BCT/ocr_work/qp/questions_extracted.json

---

## Topic 1: Symmetric vs Asymmetric Cryptography

## Symmetric
- Same key for encryption and decryption
- Fast for large data
- Key sharing is main weakness

## Asymmetric
- Public key for encryption/verification, private key for decryption/signing
- Slower than symmetric
- Enables authentication and non-repudiation

Exam-ready line:
- Blockchain uses both: symmetric for efficiency, asymmetric for identity/signatures.

---

## Topic 2: AES Basics

Must write:
1. Block size = 128 bits
2. Key sizes = 128/192/256
3. Round operations:
   - SubBytes
   - ShiftRows
   - MixColumns
   - AddRoundKey
4. Final round omits MixColumns

---

## Topic 3: RSA Workflow (Very Important)

Key generation steps:
1. Choose primes p and q
2. Compute n = p*q
3. Compute phi(n) = (p-1)(q-1)
4. Choose e such that gcd(e, phi(n)) = 1
5. Compute d so that e*d = 1 mod phi(n)
6. Public key = (e, n), private key = (d, n)

Operations:
- Encryption: C = M^e mod n
- Decryption: M = C^d mod n

Numerical solving rule:
- Always show phi(n), e selection, d computation before encryption/decryption substitution.

---

## Topic 4: ECC (Elliptic Curve Cryptography)

Core idea:
- Same security as RSA with smaller key sizes.

Basic equation form:
$$
y^2 = x^3 + ax + b
$$

Why blockchain likes ECC:
1. Smaller keys
2. Lower storage and bandwidth
3. Faster operations on constrained devices

---

## Topic 5: Hash Functions and SHA-256

Security properties:
1. Pre-image resistance
2. Second pre-image resistance
3. Collision resistance
4. Avalanche effect

SHA-256 key points:
1. 512-bit block processing
2. 256-bit digest output
3. Compression rounds with fixed constants

Exam shorthand:
- SHA-256 secures block linking and transaction integrity.

---

## Topic 6: Merkle Tree

Definition:
- Binary tree of hashes where parent = hash(left || right).

Benefits:
1. Efficient inclusion proof
2. Tamper detection
3. Scalable verification for large transaction sets

Diagram:

```text
        Merkle Root
         /       \
      H12         H34
     /  \         /  \
   H1   H2      H3   H4
```

---

## Topic 7: DHT (Distributed Hash Table)

Core flow:
1. Hash key to identifier space
2. Route query to responsible node
3. Store/retrieve value in decentralized way

Why asked:
- Appears in Part A as conceptual networking support for decentralized systems.

---

## Module 1 PYQ Attack Set

1. Symmetric vs asymmetric cryptography
2. Benefits of Merkle trees
3. Secure hash function role in blockchain
4. DHT definition and working
5. RSA and AES fundamentals

---

## Last-Minute Revision Grid

1. Learn one comparison table (sym vs asym).
2. Memorize RSA key-generation sequence.
3. Memorize three hash security properties.
4. Practice drawing Merkle tree in 20 seconds.
