
# 🔥 B2Bi Bootcamp — Autonomous Learning Engine (LOCAL AI SYSTEM)

## ⚠️ OPERATING MODE

You are not assisting.  
You are **building the entire system end-to-end autonomously**.

- No placeholders
- No pseudo code
- No “you can implement later”
- No simplifications
- No skipping hard parts

You will:
1. Design architecture
2. Build backend
3. Build ingestion pipeline
4. Build learning engine
5. Build UI
6. Integrate Ollama
7. Integrate TTS
8. Optimize for Apple Silicon (M4 Max)
9. Ensure this actually teaches, not summarizes

---

# 🎯 PRIMARY OBJECTIVE

Convert a messy bootcamp ZIP into a **high-intensity adaptive tutor** that:

- Forces real understanding
- Identifies weak areas
- Uses active recall
- Adapts difficulty
- Compresses learning into hours

This is a **learning system**, not a content viewer.

---

# 🧠 CORE PHILOSOPHY (NON-NEGOTIABLE)

You MUST implement:

### ❌ DO NOT
- Summarize passively
- Dump transcripts
- Generate long explanations without interaction
- Ignore timestamps
- Lose source linkage
- Hallucinate missing info

### ✅ MUST DO
- Ask questions constantly
- Force the user to think
- Adapt based on mistakes
- Use retrieval practice
- Revisit weak areas
- Build mental models

---

# 📦 DATASET CONTEXT (CRITICAL)

ZIP contains:

### Structure
```

B2Bi Bootcamp (BB101)/
├── Broadcasting/
├── Business Process/
├── Mapping/
├── SFTP Files/
└── Webex Recordings/
├── Day1/
├── Day2/
├── Day3/
└── Day4/

```

### Key realities:
- 43 files total
- Mixed types (.mp4, .xml, .bpml, .pdf, .docx, .ddf, .mxl, images)
- Inconsistent naming
- Videos grouped by day (important signal)
- Some folders contain executables → IGNORE

### Critical requirement:
You MUST use:
- folder structure = metadata
- recording days = timeline
- file types = classification

---

# 🖥️ HARD CONSTRAINTS

- Fully LOCAL (no internet)
- Use Ollama for LLM
- Use full GPU of M4 Max
- Optimize for Apple Silicon
- No cloud APIs
- No external dependencies requiring internet

---

# 🧱 SYSTEM ARCHITECTURE

You will build:

```

/app
/backend
/ingestion
/transcription
/parsing
/chunking
/indexing
/knowledge_graph
/learning_engine
/tutor_engine
/quiz_engine
/tts
/storage
/frontend
/models
/cache

````

---

# ⚙️ PIPELINE (END-TO-END)

## 1. INGESTION

- Accept ZIP
- Extract safely (handle spaces, apostrophes)
- Traverse all files

Generate metadata:

```json
{
  "path": "",
  "folder": "",
  "extension": "",
  "type": "",
  "is_video": false,
  "recording_day": "",
  "size": 0
}
````

### Classification rules:

* .mp4 → video
* .bpml/.xml → workflow
* .ddf/.mxl/.txo → mapping
* .pdf/.docx → docs
* .png/.jpg → visual

IGNORE:

* .exe

---

## 2. VIDEO PIPELINE (VERY IMPORTANT)

For each video:

* Transcribe using local Whisper
* Generate timestamped chunks (30–60s)
* Detect topic shifts
* Extract keyframes
* Link:

```
timestamp ↔ transcript ↔ frame ↔ concept
```

### MUST:

* Preserve timestamps
* Group by Day1–Day4
* Build chronological flow

---

## 3. DOCUMENT PARSING

* Extract text from all docs
* Chunk into semantic blocks
* Tag with source + position

---

## 4. CHUNKING STRATEGY (CRITICAL)

Bad chunking = useless system

You MUST:

* Chunk by meaning, not size
* Keep context intact
* Avoid splitting concepts
* Link chunks back to source

---

## 5. KNOWLEDGE GRAPH

Build:

### Nodes:

* Concepts
* Systems
* Inputs/Outputs
* Workflows

### Edges:

* depends_on
* transforms
* triggers
* part_of

Also detect:

* repeated ideas
* prerequisites
* inconsistencies

---

# 🧠 LEARNING ENGINE (CORE)

## You MUST implement:

### 🔁 Active Learning Loop

For each concept:

1. Teach briefly
2. Ask question
3. WAIT for answer
4. Evaluate
5. Adapt:

   * correct → harder
   * wrong → explain + retry
6. Revisit later

---

## 🎯 Learning Techniques (MANDATORY)

* Retrieval practice
* Spaced repetition
* Interleaving topics
* Progressive difficulty
* Socratic questioning
* Error-driven feedback
* “Explain it back”

---

## 🧪 Modes

* Rapid Mastery (default)
* Deep Dive
* Drill Mode
* Weak Area Mode

---

# 📚 LESSON FORMAT

Each concept must produce:

```
- Name
- Why it matters
- Intuition
- Precise explanation
- Example from dataset
- Common mistake
- Checkpoint question
- Hard follow-up
- Source reference (file + timestamp)
```

---

# 🧠 ADAPTIVE INTELLIGENCE

Track:

* accuracy
* response time
* retries
* confidence

Use to:

* reorder topics
* adjust difficulty
* trigger review

---

# 🔊 TTS SYSTEM

You MUST implement local TTS.

### Voice requirements:

* High-energy anime mentor style
* Fast, intense, motivating
* Dynamic pacing

### DO NOT:

* Clone real/copyrighted voices

### Implement:

* speed control
* pause/resume
* replay
* emphasis

---

# 🎨 VISUAL SYSTEM

Generate:

* flow diagrams
* system diagrams
* step-by-step visuals

Derived from actual content, NOT random.

---

# 🧑‍💻 UI REQUIREMENTS

Must include:

* ZIP upload
* Processing dashboard
* Course map
* Lesson player
* Interactive tutor
* Quiz mode
* Weak area tracker
* Timeline (Day1 → Day4)
* Jump to timestamp

---

# 🤖 AI ORCHESTRATION

Use multiple roles:

* parser
* chunker
* concept extractor
* teacher
* evaluator
* quiz generator

---

# 🧠 MODEL STRATEGY (OLLAMA)

Use:

* small models → parsing
* large models → teaching

Use RAG:

* retrieve chunks
* ground responses
* avoid hallucination

---

# ⚡ PERFORMANCE

* Cache everything
* Batch operations
* Stream results
* Avoid recomputation
* Keep UI responsive

---

# 🧪 QUALITY RULES

DO NOT:

* output generic summaries
* over-explain basics
* hallucinate
* lose timestamps

ALWAYS:

* tie back to source
* teach actively
* challenge user

---

# 🚀 OUTPUT REQUIREMENTS

You MUST generate:

1. Full architecture
2. Data flow
3. Tech stack (Apple Silicon optimized)
4. Model plan (Ollama)
5. Full codebase (modular)
6. Setup instructions
7. Working system

---

# 🔥 FINAL DIRECTIVE

This is NOT a demo.

This must feel like:

> A brutal, high-performance personal tutor built from my own content.

If it feels like a summary tool → you failed.
If it forces learning → you succeeded.

---
