#!/bin/bash

echo "=== Testing All Fixed REST Endpoints ==="
echo ""

# Use a known concept ID
CONCEPT_ID="8ddc08c1-65d7-46b5-8ed9-c330bdc1c089"
echo "Using concept ID: $CONCEPT_ID (Cryptography from BCT)"
echo ""

# Test 1: Flashcard generation
echo "1. Testing POST /api/flashcards/generate..."
FLASHCARD_RESULT=$(curl -s -X POST http://localhost:8000/api/flashcards/generate \
  -H "Content-Type: application/json" \
  -d "{\"concept_id\": \"$CONCEPT_ID\", \"count\": 3}")
echo "$FLASHCARD_RESULT" | python3 -m json.tool
echo ""

# Test 2: Quiz generation
echo "2. Testing POST /api/quiz/generate..."
QUIZ_RESULT=$(curl -s -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d "{\"concept_id\": \"$CONCEPT_ID\", \"count\": 2}")
echo "$QUIZ_RESULT" | python3 -m json.tool
echo ""

# Get question ID for evaluation
QUESTION_ID=$(echo "$QUIZ_RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['questions'][0]['id'] if data.get('questions') and len(data['questions']) > 0 else '')" 2>/dev/null)

if [ -n "$QUESTION_ID" ]; then
    echo "3. Testing POST /api/quiz/evaluate with question ID: $QUESTION_ID..."
    curl -s -X POST http://localhost:8000/api/quiz/evaluate \
      -H "Content-Type: application/json" \
      -d "{\"question_id\": \"$QUESTION_ID\", \"answer\": \"Cryptography is the practice of secure communication\", \"confidence\": 75, \"response_time_ms\": 4000}" | python3 -m json.tool
    echo ""
else
    echo "⚠️  No question ID available, skipping evaluation test"
    echo ""
fi

# Test 4: TTS synthesis
echo "4. Testing POST /api/tts/synthesize..."
TTS_RESULT=$(curl -s -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello! This is Goku teaching you about cryptography!"}' 2>&1)

if echo "$TTS_RESULT" | grep -q "audio_url"; then
    echo "$TTS_RESULT" | python3 -m json.tool
    echo "✅ TTS endpoint working!"
else
    echo "$TTS_RESULT"
    echo "⚠️  TTS not available (Coqui TTS may not be installed)"
fi
echo ""

# Test 5: Get flashcards for concept
echo "5. Testing GET /api/concepts/$CONCEPT_ID/flashcards..."
curl -s "http://localhost:8000/api/concepts/$CONCEPT_ID/flashcards" | python3 -m json.tool
echo ""

echo "=== All endpoint tests complete ==="
