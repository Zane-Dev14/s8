#!/bin/bash

echo "=== Testing Fixed REST Endpoints ==="
echo ""

# Get a concept ID first
echo "1. Getting concept ID..."
CONCEPT_ID=$(curl -s http://localhost:8000/api/subjects/1/concepts | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['concepts'][0]['id'] if data.get('concepts') else '')")

if [ -z "$CONCEPT_ID" ]; then
    echo "❌ No concepts found. Cannot test."
    exit 1
fi

echo "✅ Using concept ID: $CONCEPT_ID"
echo ""

# Test flashcard generation
echo "2. Testing POST /api/flashcards/generate..."
curl -s -X POST http://localhost:8000/api/flashcards/generate \
  -H "Content-Type: application/json" \
  -d "{\"concept_id\": \"$CONCEPT_ID\", \"count\": 3}" | python3 -m json.tool
echo ""

# Test quiz generation
echo "3. Testing POST /api/quiz/generate..."
QUIZ_RESPONSE=$(curl -s -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d "{\"concept_id\": \"$CONCEPT_ID\", \"count\": 2}")
echo "$QUIZ_RESPONSE" | python3 -m json.tool
echo ""

# Get question ID for evaluation
QUESTION_ID=$(echo "$QUIZ_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['questions'][0]['id'] if data.get('questions') else '')")

if [ -n "$QUESTION_ID" ]; then
    echo "4. Testing POST /api/quiz/evaluate..."
    curl -s -X POST http://localhost:8000/api/quiz/evaluate \
      -H "Content-Type: application/json" \
      -d "{\"question_id\": \"$QUESTION_ID\", \"answer\": \"Test answer\", \"confidence\": 70, \"response_time_ms\": 3000}" | python3 -m json.tool
    echo ""
fi

# Test TTS (will fail if Coqui TTS not installed, but should not crash)
echo "5. Testing POST /api/tts/synthesize..."
curl -s -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello! This is a test."}' | python3 -m json.tool || echo "⚠️  TTS not available (expected if Coqui TTS not installed)"
echo ""

echo "=== All endpoint tests complete ==="
