# Teaching Agent API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required (add JWT/OAuth for production)

---

## Health & Status

### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-17T04:00:00Z"
}
```

---

## Subjects

### GET /api/subjects
List all available subjects.

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Blockchain Technology",
    "status": "ready",
    "concept_count": 19,
    "created_at": "2026-04-17T00:00:00Z"
  }
]
```

### GET /api/subjects/{subject_id}
Get details for a specific subject.

**Response:**
```json
{
  "id": "uuid",
  "name": "Blockchain Technology",
  "status": "ready",
  "concept_count": 19,
  "created_at": "2026-04-17T00:00:00Z"
}
```

### GET /api/subjects/{subject_id}/concepts
List all concepts for a subject.

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Cryptography",
    "plain_name": "Secure Communication",
    "difficulty": "intermediate",
    "mastery_level": 0,
    "prerequisites": []
  }
]
```

---

## Concepts

### GET /api/concepts/{concept_id}
Get details for a specific concept.

**Response:**
```json
{
  "id": "uuid",
  "name": "Cryptography",
  "plain_name": "Secure Communication",
  "difficulty": "intermediate",
  "subject_id": "uuid",
  "prerequisites": [],
  "mastery_level": 0
}
```

### GET /api/course-map
Get the complete concept dependency graph.

**Response:**
```json
{
  "nodes": [
    {
      "id": "uuid",
      "name": "Cryptography",
      "difficulty": "intermediate",
      "mastery_level": 0
    }
  ],
  "edges": [
    {
      "from": "uuid1",
      "to": "uuid2",
      "type": "prerequisite"
    }
  ]
}
```

---

## Teaching (Streaming)

### GET /api/stream/teach/{concept_id}?section={section}
Stream teaching content for a concept section.

**Query Parameters:**
- `section` (required): One of `hook`, `analogy`, `core`, `visual`, `example`, `mistake`, `practice`, `summary`

**Response:** Server-Sent Events (SSE)
```
data: {"type": "token", "section": "hook", "token": "Alright", "progress": "1/8"}

data: {"type": "token", "section": "hook", "token": "!", "progress": "1/8"}

data: {"type": "complete", "section": "hook", "full_text": "Alright! Let's talk about..."}
```

**Example:**
```bash
curl "http://localhost:8000/api/stream/teach/8ddc08c1-65d7-46b5-8ed9-c330bdc1c089?section=hook"
```

---

## Flashcards

### POST /api/flashcards/generate
Generate flashcards for a concept.

**Request Body:**
```json
{
  "concept_id": "uuid",
  "count": 5
}
```

**Response:**
```json
{
  "concept_id": "uuid",
  "cards_generated": 4,
  "cards": [
    {
      "id": "uuid",
      "card_type": "definition",
      "front": "What is Cryptography?",
      "back": "Cryptography is the practice of secure communication..."
    },
    {
      "id": "uuid",
      "card_type": "analogy",
      "front": "What's Cryptography like in real life?",
      "back": "It's like a secret code that keeps your messages safe..."
    },
    {
      "id": "uuid",
      "card_type": "application",
      "front": "Securing digital communication",
      "back": "Encryption algorithms are used to securely transmit..."
    },
    {
      "id": "uuid",
      "card_type": "mistake",
      "front": "Cryptography is only used in Blockchain.",
      "back": "Wrong! Cryptography is a broader concept used in..."
    }
  ]
}
```

### GET /api/concepts/{concept_id}/flashcards
Get all flashcards for a concept.

**Response:**
```json
[
  {
    "id": "uuid",
    "card_type": "definition",
    "front": "What is Cryptography?",
    "back": "Cryptography is...",
    "next_review": "2026-04-18T00:00:00Z",
    "interval_days": 1,
    "ease_factor": 2.5,
    "repetitions": 0
  }
]
```

### POST /api/flashcards/{card_id}/review
Record a flashcard review.

**Request Body:**
```json
{
  "correct": true,
  "confidence": 80
}
```

**Response:**
```json
{
  "card_id": "uuid",
  "next_review": "2026-04-20T00:00:00Z",
  "interval_days": 3,
  "ease_factor": 2.55
}
```

---

## Quiz

### POST /api/quiz/generate
Generate quiz questions for a concept.

**Request Body:**
```json
{
  "concept_id": "uuid",
  "count": 3
}
```

**Response:**
```json
{
  "concept_id": "uuid",
  "questions_generated": 3,
  "questions": [
    {
      "id": "uuid",
      "question_type": "multiple_choice",
      "question": "What is the primary purpose of cryptography?",
      "correct_answer": "Secure communication",
      "distractors": ["Data compression", "Speed optimization", "File storage"]
    }
  ]
}
```

### POST /api/quiz/evaluate
Evaluate a quiz answer.

**Request Body:**
```json
{
  "question_id": "uuid",
  "answer": "Secure communication",
  "confidence": 75,
  "response_time_ms": 3500
}
```

**Response:**
```json
{
  "is_correct": true,
  "score": 95,
  "feedback": "Excellent! You correctly identified...",
  "misconception_tag": null,
  "next_action": "continue"
}
```

---

## Text-to-Speech

### POST /api/tts/synthesize
Generate speech audio from text.

**Request Body:**
```json
{
  "text": "Hello! This is Goku teaching you about cryptography!",
  "voice_profile": "goku"
}
```

**Response:**
```json
{
  "audio_path": "/path/to/audio.wav",
  "audio_url": "/api/audio/tts_20260417_040000_123456.wav",
  "text": "Hello! This is Goku...",
  "voice_profile": "goku",
  "cached": false
}
```

### GET /api/audio/{file_name}
Serve generated audio file.

**Response:** Binary audio file (WAV format)

---

## Ingestion

### POST /api/ingest
Ingest new files for a subject.

**Request:** Multipart form data
- `subject_name` (string): Name of the subject
- `files` (file[]): One or more files to ingest

**Response:**
```json
{
  "job_id": "uuid",
  "subject_id": "uuid",
  "status": "queued",
  "message": "Ingestion started"
}
```

### GET /api/ingest/{job_id}/status
Check ingestion job status.

**Response:**
```json
{
  "job_id": "uuid",
  "status": "completed",
  "stage": "concept_extraction",
  "message": "Extracted 15 concepts",
  "progress": 100
}
```

---

## Error Responses

All endpoints return standard HTTP status codes:

### 200 OK
Request successful.

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Concept not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting
Currently no rate limiting (add for production)

---

## WebSocket Support
Not implemented yet. Use SSE for streaming.

---

## Examples

### Complete Teaching Session
```bash
# 1. Get subjects
curl http://localhost:8000/api/subjects

# 2. Get concepts
curl http://localhost:8000/api/subjects/{id}/concepts

# 3. Stream teaching
curl "http://localhost:8000/api/stream/teach/{concept_id}?section=hook"
curl "http://localhost:8000/api/stream/teach/{concept_id}?section=analogy"
curl "http://localhost:8000/api/stream/teach/{concept_id}?section=core"

# 4. Generate flashcards
curl -X POST http://localhost:8000/api/flashcards/generate \
  -H "Content-Type: application/json" \
  -d '{"concept_id": "{id}", "count": 5}'

# 5. Generate quiz
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"concept_id": "{id}", "count": 3}'

# 6. Evaluate answer
curl -X POST http://localhost:8000/api/quiz/evaluate \
  -H "Content-Type: application/json" \
  -d '{"question_id": "{id}", "answer": "...", "confidence": 80, "response_time_ms": 3000}'
```

### Batch Flashcard Generation
```python
import requests

subjects = requests.get("http://localhost:8000/api/subjects").json()

for subject in subjects:
    concepts = requests.get(
        f"http://localhost:8000/api/subjects/{subject['id']}/concepts"
    ).json()
    
    for concept in concepts:
        response = requests.post(
            "http://localhost:8000/api/flashcards/generate",
            json={"concept_id": concept["id"], "count": 5}
        )
        print(f"Generated {response.json()['cards_generated']} cards for {concept['name']}")
```

---

## Frontend Integration

### React Hook for Streaming
```typescript
import { useEffect, useState } from 'react';

export function useStreamingTeach(conceptId: string, section: string) {
  const [text, setText] = useState('');
  const [done, setDone] = useState(false);

  useEffect(() => {
    const es = new EventSource(
      `http://localhost:8000/api/stream/teach/${conceptId}?section=${section}`
    );
    
    es.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'token') {
        setText(prev => prev + data.token);
      } else if (data.type === 'complete') {
        setDone(true);
        es.close();
      }
    };
    
    return () => es.close();
  }, [conceptId, section]);

  return { text, done };
}
```

### Usage
```tsx
function TeachingSession({ conceptId }: { conceptId: string }) {
  const { text, done } = useStreamingTeach(conceptId, 'hook');
  
  return (
    <div>
      <p>{text}</p>
      {done && <button>Next Section</button>}
    </div>
  );
}
```

---

## Performance

### Response Times (Typical)
- Health check: <10ms
- List subjects: <50ms
- Get concept: <50ms
- Stream first token: <500ms
- Generate flashcards: 3-5 seconds
- Generate quiz: 2-4 seconds
- TTS synthesis: 1-3 seconds

### Optimization Tips
1. Cache flashcards and questions
2. Pre-generate audio for common phrases
3. Use connection pooling for database
4. Implement Redis for session storage
5. Use CDN for static assets

---

## Security Considerations

### For Production
1. Add JWT authentication
2. Implement rate limiting
3. Add CORS configuration
4. Use HTTPS only
5. Sanitize user inputs
6. Add request validation
7. Implement API versioning
8. Add monitoring and logging
9. Use environment variables for secrets
10. Add database backups

---

## Changelog

### v1.0.0 (2026-04-17)
- Initial release
- Multi-subject support
- Streaming teaching
- Flashcard generation
- Quiz generation
- RESTful API
- SSE support

---

## Support

For issues or questions:
1. Check logs: `/tmp/backend.log`
2. Verify Ollama is running: `curl http://localhost:11434/api/tags`
3. Check database: `sqlite3 TeachingAgent/backend/data/learning.db`
4. Review deployment guide: `TeachingAgent/DEPLOYMENT_GUIDE.md`