# STEP 6: Module 5 Crash Guide (Consensus and Distributed File Systems)

Module 5 focus:
- Consensus in synchronous crash-failure systems
- File service architecture
- AFS, GFS, NFS concepts
- DFS requirements and comparisons

Mapped from OCR:
- DC/ocr_output/DCSeries2.txt
- DC/ocr_output/Model_QP_Solved.txt

---

## Topic 1: Consensus for Crash Failures (Synchronous System)

### Definition
Consensus means all non-faulty processes agree on one decision value.

### System assumptions
1. Synchronous rounds
2. Bounded message delay
3. Bounded process step time
4. Crash failures only (not Byzantine)

### Core properties
1. Agreement: non-faulty processes decide same value
2. Validity: decided value is from proposed values (or source value in single-source variant)
3. Termination: non-faulty processes eventually decide

### Typical round-based flow
1. Each process starts with proposal x.
2. In each round, broadcast current x.
3. Collect received values within timeout.
4. Update x by deterministic rule (for example min/majority policy as specified).
5. After required rounds, decide x.

### Common result to mention
To tolerate f crash failures, at least f+1 rounds are needed in classic synchronous crash model formulations.

---

## Topic 2: File Service Architecture

### Core components
1. Flat File Service
   - Handles file content operations: read, write, create, delete.
2. Directory Service
   - Maps human-readable names to internal file identifiers.
3. Client Module
   - Interface bridge between application and file services.

### Block diagram to draw

```text
Application -> Client Module -> Directory Service
                     |
                     +-> Flat File Service
```

### Typical file open flow
1. Client asks directory service for file identifier.
2. Directory service returns identifier.
3. Client requests file content from flat file service.
4. Flat file service returns data.

---

## Topic 3: Distributed File System (DFS) Requirements

Write these in exam answers:
1. Access transparency
2. Location transparency
3. Mobility transparency
4. Performance transparency
5. Scaling transparency
6. Concurrent update support
7. File replication
8. Heterogeneity support
9. Fault tolerance
10. Consistency
11. Security
12. Efficiency

---

## Topic 4: Andrew File System (AFS)

### Core idea
AFS is a distributed file system that uses client-side whole-file caching.

### Components
1. Vice (server side)
2. Venus (client side)

### Key features
1. Whole-file caching
2. Whole-file serving
3. Callback-based consistency

### Callback concept
Server notifies clients when cached copy becomes stale.
Client then fetches fresh version.

---

## Topic 5: Google File System (GFS)

### Architecture
1. Master server
   - Maintains metadata, chunk mapping.
2. Chunk servers
   - Store file chunks and replicas.
3. Clients
   - Ask master for chunk locations, then read/write from chunk servers.

### Read flow
1. Client asks master for chunk locations.
2. Client reads chunks directly from chunk servers.

### Write flow
1. Client requests write path from master.
2. Data written to primary/replicated chunk servers.
3. Replication ensures fault tolerance.

---

## Topic 6: AFS vs NFS

| Feature | AFS | NFS |
|---|---|---|
| Server style | Stateful behavior with callbacks | Traditionally stateless server |
| Caching style | Whole-file client caching | Block/file-level access with validation |
| Consistency control | Callback invalidation | Timestamp/attribute checks |
| Scalability behavior | Strong for read-heavy workloads | Simpler deployment, different tradeoffs |

### One-line answer
AFS emphasizes whole-file caching with callback consistency, while classic NFS emphasizes stateless service simplicity.

---

## Topic 7: Sun NFS Architecture

### Layers to mention
1. Application layer
2. VFS interface
3. NFS client module
4. RPC/XDR transport
5. NFS server module
6. Server VFS + local file system

### Diagram

```text
Client App -> VFS -> NFS Client -> RPC/XDR -> NFS Server -> VFS -> Local FS
```

### Why important
NFS makes remote file access appear similar to local file access.

---

## Topic 8: DSM Advantage Question in Module 5 Crossovers

Sometimes DSM advantages appear in cross-module papers. Keep a short list ready:
1. Simple shared-memory abstraction
2. Easier data sharing
3. Locality benefits
4. Cost-effective commodity deployment

---

## Module 5 PYQ Attack Set

1. Consensus under crash failures in synchronous systems
2. File service architecture with neat diagram
3. Explain Andrew file system
4. Explain Google file system
5. Summarize DFS requirements
6. Differentiate AFS and NFS
7. Explain Sun NFS architecture with diagram

---

## Last-Minute Revision Grid

1. Memorize 3 consensus properties: agreement, validity, termination.
2. Practice one clean file service architecture diagram.
3. Memorize AFS terms: Vice, Venus, callback.
4. Memorize GFS terms: master, chunk server, replication.
5. Keep one AFS vs NFS comparison table ready.
