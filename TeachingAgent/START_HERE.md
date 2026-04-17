# 🚀 TEACHING AGENT - QUICK START GUIDE

## Prerequisites

✅ **Already Installed** (verified):
- Python 3.x
- Node.js & npm
- Ollama with models (qwen2.5:32b, deepseek-r1:32b, etc.)

## 🎯 Quick Start (3 Steps)

### Step 1: Start Backend Server

```bash
cd TeachingAgent/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

### Step 2: Start Frontend (New Terminal)

```bash
cd TeachingAgent/frontend
npm run dev
```

Frontend will be available at: **http://localhost:3000**

### Step 3: Open Browser

Navigate to: **http://localhost:3000**

---

## 📚 How to Use the Teaching System

### First Time Setup: Ingest Content

1. **Prepare your bootcamp ZIP file**
   - Example: `B2Bi Bootcamp (BB101).zip`

2. **Upload via API or Frontend**
   ```bash
   # Using curl
   curl -X POST http://localhost:8000/api/ingest/upload \
     -F "file=@/path/to/B2Bi Bootcamp (BB101).zip"
   ```

3. **Monitor ingestion progress**
   - Check: http://localhost:8000/api/ingest/{job_id}
   - Wait for status: "completed"

### Using the Teaching Interface

Flow is now enforced in this order:
1. Interactive teaching sections
2. Diagram walkthrough
3. Audio playback with subtitles
4. Flashcard drill
5. Comprehension check (your own words)
6. Quiz unlock

### 0. Train Voice Profile (Optional but Recommended)

Use only voice clips you have permission to use.

```bash
cd TeachingAgent
./scripts/train_goku_voice_profile.sh http://localhost:8000 \
  ../All_Goku_Voice_Clips_Dragon_Ball_FighterZ_Voice_Lines_Sean_Schemmel_128kbps_10144730_cut.mp3 \
  goku
```

This creates a local voice profile used by the interactive teaching audio.

In the dashboard, pick the `goku` profile to apply voice cloning for teaching audio.

#### 1. **Start a Lesson**

**API Call:**
```bash
curl "http://localhost:8000/api/tutor/start?user_id=your-name&mode=lesson"
```

**Response:**
```json
{
  "concept_id": "sftp-protocol",
  "mode": "lesson",
  "lesson_preview": {
    "name": "SFTP Protocol",
    "why_it_matters": "Critical for secure B2B data exchange...",
    "intuition": "Think of SFTP as a secure tunnel...",
    "example": "When transferring EDI 850 purchase orders...",
    "common_mistake": "Confusing SFTP with FTPS..."
  },
  "question": "What makes SFTP different from regular FTP?",
  "time_pressure_seconds": 20
}
```

#### 2. **Answer the Question**

**Important**: You must provide:
- Your answer (text)
- Your confidence (0-100)
- Response time in milliseconds

**API Call:**
```bash
curl -X POST http://localhost:8000/api/tutor/answer \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your-name",
    "concept_id": "sftp-protocol",
    "question": "What makes SFTP different from regular FTP?",
    "user_answer": "SFTP uses SSH for encryption and authentication",
    "user_confidence": 85,
    "response_time_ms": 8000,
    "mode": "lesson"
  }'
```

**Response:**
```json
{
  "correctness": true,
  "explanation": "Excellent! SFTP indeed uses SSH...",
  "misconception_tag": "none",
  "next_action": "harder",
  "next_question": "Under what conditions would SFTP authentication fail?",
  "source_chunks": ["Day1-Recording.mp4 [concept_definition] SFTP is..."],
  "confidence": "high",
  "uncertainty": "low",
  "feedback_delay_ms": 900
}
```

#### 3. **Understanding the Response**

**Correctness**: `true` or `false`

**Misconception Tags**:
- `none` - Perfect understanding
- `lucky_guess` - Correct but low confidence
- `false_confidence` - Wrong but high confidence
- `fragile_understanding` - Correct but slow/uncertain
- `hesitation_confusion` - Wrong and very slow
- `guessing_pattern` - Wrong with very low confidence

**Next Actions**:
- `harder` - You're doing great, here's a challenge
- `review` - Need to review this concept
- `retry` - Try again with more thought
- `rebuild` - Fundamental misunderstanding, rebuild from scratch
- `interview` - Ready for interview-style pressure

**Feedback Delay**:
- `900ms` - For harder/interview (quick feedback)
- `1800ms` - For retry/review/rebuild (reflection time)

#### 4. **Track Your Progress**

```bash
curl "http://localhost:8000/api/analytics/weak-areas?user_id=your-name"
```

Shows your weakest concepts that need more practice.

---

## 🎓 Learning Modes

### Lesson Mode (Default)
- **Time Pressure**: 20 seconds
- **Focus**: Building understanding
- **Questions**: Checkpoint questions
- **Feedback**: Supportive and explanatory

### Interview Mode
- **Time Pressure**: 10 seconds (more intense!)
- **Focus**: Stress-testing knowledge
- **Questions**: Hard follow-ups and failure scenarios
- **Feedback**: Direct and challenging

**Switch to interview mode:**
```bash
curl "http://localhost:8000/api/tutor/start?user_id=your-name&mode=interview"
```

---

## 🏆 Mastery Requirements (Brutal!)

To master a concept, you need **ALL** of these:

1. ✅ **3 correct answers** (not 1, not 2, exactly 3+)
2. ✅ **Confidence ≥ 80%** (no lucky guesses)
3. ✅ **Response time ≤ 12 seconds** (under pressure)
4. ✅ **Spacing ≥ 8 minutes** between attempts (spaced repetition)

**Why so brutal?**
- Prevents shallow learning
- Ensures genuine understanding
- Forces spaced repetition
- Builds confidence under pressure

---

## 🔄 Forced Revisit System

The system automatically detects confusion and forces you to revisit concepts when:

1. **Lucky Guess**: Correct answer but confidence < 40%
2. **False Confidence**: Wrong answer but confidence ≥ 80%
3. **Hesitation Confusion**: Wrong answer and response time > 18s

These concepts are **prioritized** in your next lesson.

---

## 📊 API Endpoints Reference

### Health Check
```bash
GET http://localhost:8000/health
```

### Ingestion
```bash
POST http://localhost:8000/api/ingest/upload
GET  http://localhost:8000/api/ingest/{job_id}
GET  http://localhost:8000/api/timeline/{job_id}
GET  http://localhost:8000/api/course-map
```

### Learning
```bash
GET  http://localhost:8000/api/tutor/start?user_id=X&mode=lesson|interview
POST http://localhost:8000/api/tutor/answer
GET  http://localhost:8000/api/analytics/weak-areas?user_id=X
```

### Quiz
```bash
GET http://localhost:8000/api/quiz/next
```

### TTS (Text-to-Speech)
```bash
POST http://localhost:8000/api/tts/speak
```

### Interactive Teaching + Understanding Check
```bash
GET  http://localhost:8000/api/tutor/interactive-teach?concept_id=X&user_id=Y&voice_profile=goku
POST http://localhost:8000/api/tutor/comprehension-check
GET  http://localhost:8000/api/voice/profiles
POST http://localhost:8000/api/voice/train-profile
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Install dependencies
cd TeachingAgent/backend
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Install dependencies
cd TeachingAgent/frontend
npm install

# Clear cache
rm -rf .next node_modules
npm install
```

### Ollama not responding
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### No concepts available
- You need to ingest content first!
- Upload a bootcamp ZIP file via `/api/ingest/upload`

---

## 💡 Pro Tips

1. **Be Honest with Confidence**: The system uses your confidence to detect confusion
2. **Answer Quickly**: Time pressure is part of the learning system
3. **Read Feedback Carefully**: The tutor explains your misconceptions
4. **Don't Skip Forced Revisits**: They're there for a reason
5. **Use Interview Mode**: When you think you've mastered something
6. **Track Weak Areas**: Focus on concepts with low accuracy

---

## 🎯 Example Learning Session

```bash
# 1. Start lesson
curl "http://localhost:8000/api/tutor/start?user_id=alice&mode=lesson"

# 2. Answer question (take your time, be honest about confidence)
curl -X POST http://localhost:8000/api/tutor/answer \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "alice",
    "concept_id": "sftp-protocol",
    "question": "What makes SFTP different from FTP?",
    "user_answer": "SFTP encrypts data using SSH",
    "user_confidence": 75,
    "response_time_ms": 9000,
    "mode": "lesson"
  }'

# 3. Wait for feedback delay (900ms or 1800ms)

# 4. Read explanation and next question

# 5. Repeat until mastery!
```

---

## 📈 Success Metrics

Track your progress:
- **Accuracy**: % of correct answers
- **Confidence**: Your self-reported confidence
- **Response Time**: How fast you answer
- **Retries**: How many times you've revisited
- **Mastery**: Concepts you've fully mastered

---

## 🚀 Ready to Learn?

1. Start backend: `cd TeachingAgent/backend && uvicorn app.main:app --reload`
2. Start frontend: `cd TeachingAgent/frontend && npm run dev`
3. Open browser: http://localhost:3000
4. Start learning!

**The system is brutal but effective. Good luck! 🎓**