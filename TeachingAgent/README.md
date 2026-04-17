# B2Bi Brutal Tutor (Local-First)

Production-grade local adaptive tutoring system that ingests a mixed bootcamp ZIP and transforms it into an active-recall training engine.

## Stack

- Backend: FastAPI + SQLAlchemy + local workers
- Frontend: Next.js 14 + TypeScript + Tailwind + custom shadcn-style components
- Models: Ollama model routing by task
- Transcription: whisper.cpp CLI
- TTS: Piper CLI
- Storage: SQLite + filesystem cache

## System Behavior

- Enforces answer-before-explanation loop with mandatory confidence scoring (0-100)
- Uses delayed feedback gates to reduce guess-confirmation bias
- Tracks weak areas with strict mastery rule: 3 correct answers, spaced across time, under pressure, high confidence
- Detects lucky guesses, false confidence, fragile understanding, and hesitation confusion
- Preserves source linkage (path and timestamps)
- Uses graph-driven revisits: failing a concept re-queues prerequisites
- Includes an interactive teach-first coach with section-by-section guidance and visual diagrams
- Requires a plain-language comprehension check before checkpoint questions
- Supports local voice profile training from user-provided clips for personalized TTS delivery

## Model Routing

- Parsing/classification: llama3.1:8b-instruct
- Chunking/structuring: qwen2.5:32b-instruct-q5_K_M
- Knowledge graph extraction: deepseek-r1:32b
- Teaching/evaluation: qwen2.5:32b-instruct-q5_K_M (fallback deepseek-r1:32b)
- Quiz generation: qwen2.5:32b-instruct-q5_K_M
- Fast UI responses: openchat

## Backend Setup

1. Create Python environment and install dependencies.
2. Copy backend/.env.example to backend/.env and update paths for whisper and piper if needed.
3. Start Ollama daemon and ensure required models are available.
4. Run API server:

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend

## Frontend Setup

1. Install dependencies in frontend.
2. Set optional API URL in frontend/.env.local:

   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

3. Run app:

   npm run dev --prefix frontend

## Pipeline Flow

1. Upload ZIP through frontend.
2. Backend extracts safely and indexes metadata.
3. Videos are transcribed and keyframes extracted.
4. Documents and workflow artifacts are parsed.
5. Concept-aware chunks are generated (definition/example/edge case/workflow step + concept bundles).
6. Knowledge graph and quiz bank are built.
7. Tutor loop runs in lesson or interview mode with retrieval-grounded evaluation.

## API Highlights

- POST /api/ingest/upload
- GET /api/ingest/{job_id}
- GET /api/timeline/{job_id}
- GET /api/tutor/start
- GET /api/tutor/interactive-teach
- POST /api/tutor/comprehension-check
- POST /api/tutor/answer
- GET /api/quiz/next
- GET /api/analytics/weak-areas
- POST /api/tts/speak
- POST /api/voice/train-profile
- GET /api/voice/profiles

Tutor answer response is grounded by contract:

{
   "answer": "...",
   "source_chunks": ["..."],
   "confidence": "low|medium|high",
   "uncertainty": "..."
}

If no strong source chunks are found, tutor returns uncertain and avoids freestyling.
