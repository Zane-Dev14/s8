# STEP 2: Module 1 Crash Guide (Cryptography, Hashing, Merkle, DHT)

Module focus:
- Cryptographic foundations for blockchain trust
- Hashing and integrity structures
- Exam-oriented algorithm writing

---

## 1) Symmetric vs Asymmetric Cryptography

| Point | Symmetric | Asymmetric |
|---|---|---|
| Key usage | One shared key for encrypt/decrypt | Public key and private key pair |
| Speed | Faster | Slower |
| Key distribution | Difficult and risky | Easier public-key distribution |
| Typical use | Bulk data encryption | Signatures, key exchange |
| Blockchain role | Session confidentiality support | Identity, signature, non-repudiation |

One-line exam closure:
Blockchain systems combine both for speed plus trust.

---

## 2) AES Essentials

Write these fixed points:
1. Block size is 128 bits.
2. Key sizes are 128, 192, or 256 bits.
3. Round operations are SubBytes, ShiftRows, MixColumns, AddRoundKey.
4. Final round omits MixColumns.

---

## 3) RSA Workflow with Worked Example

## Key generation formulas
1. Choose primes p and q.
2. Compute n = p*q.
3. Compute phi(n) = (p-1)(q-1).
4. Choose e such that gcd(e, phi(n)) = 1.
5. Compute d such that e*d congruent 1 mod phi(n).
6. Public key = (e, n), private key = (d, n).

## Encryption and decryption
$$
C = M^e \bmod n, \quad M = C^d \bmod n
$$

## Mini solved example
Given p=17, q=11.
1. n = 17*11 = 187.
2. phi(n) = 16*10 = 160.
3. Choose e = 7 (coprime to 160).
4. Compute d where 7d mod 160 = 1, so d = 23.
5. Public key = (7,187), private key = (23,187).
6. For message M=10, ciphertext C = 10^7 mod 187 = 175.

Method-mark note:
Even if final arithmetic slips, showing phi, e, d steps earns marks.

---

## 4) ECC Core Point

Elliptic curve standard form:
$$
y^2 = x^3 + ax + b
$$

Why ECC appears in blockchain discussions:
1. Smaller key sizes for same security class.
2. Lower storage and bandwidth footprint.
3. Efficient for constrained devices.

---

## 5) Secure Hash Functions and SHA-256

Security properties:
1. Pre-image resistance.
2. Second pre-image resistance.
3. Collision resistance.
4. Avalanche effect.

SHA-256 role in blockchain:
1. Secures block links through previous hash references.
2. Secures transaction set integrity through Merkle roots.

---

## 6) Merkle Tree

Definition:
Parent hash is computed from concatenated child hashes.

Structure:
```text
          Merkle Root
           /       \
        H12         H34
       /  \         /  \
      H1  H2       H3  H4
```

Benefits asked in exams:
1. Logarithmic proof size for inclusion checks.
2. Fast tamper detection.
3. Efficient verification for light clients.

---

## 7) DHT (Distributed Hash Table)

Working steps:
1. Key is hashed to identifier space.
2. Routing finds responsible node.
3. Value is stored/retrieved in decentralized lookup.

One-line exam use:
DHT enables scalable decentralized discovery and storage mapping.

---

## 8) Module 1 Final Drill

1. Write symmetric vs asymmetric table from memory.
2. Recite RSA steps in exact order.
3. Draw Merkle tree once cleanly.
4. List three hash security properties without pause.
