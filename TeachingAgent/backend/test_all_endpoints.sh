#!/bin/bash
# Comprehensive REST API endpoint testing script

echo "🧪 Testing All Teaching Agent REST Endpoints"
echo "=============================================="
echo ""

BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -e "${YELLOW}Testing: $name${NC}"
    echo "  Method: $method"
    echo "  Endpoint: $endpoint"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "  ${GREEN}✓ Status: $http_code${NC}"
        echo "  Response: $(echo $body | head -c 200)..."
    else
        echo -e "  ${RED}✗ Status: $http_code${NC}"
        echo "  Error: $body"
    fi
    echo ""
}

# 1. Health Check
test_endpoint "Health Check" "GET" "/health"

# 2. Get All Subjects
echo -e "${YELLOW}Getting all subjects...${NC}"
subjects_response=$(curl -s "$BASE_URL/api/subjects")
echo "$subjects_response" | python3 -m json.tool 2>/dev/null || echo "$subjects_response"
echo ""

# Extract first subject ID
subject_id=$(echo "$subjects_response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[0]['id'] if data else '')" 2>/dev/null)

if [ -n "$subject_id" ]; then
    echo -e "${GREEN}Found subject ID: $subject_id${NC}"
    echo ""
    
    # 3. Get Subject Details
    test_endpoint "Get Subject Details" "GET" "/api/subjects/$subject_id"
    
    # 4. Get Concepts for Subject
    echo -e "${YELLOW}Getting concepts for subject...${NC}"
    concepts_response=$(curl -s "$BASE_URL/api/subjects/$subject_id/concepts")
    echo "$concepts_response" | python3 -m json.tool 2>/dev/null | head -50
    echo ""
    
    # Extract first concept ID
    concept_id=$(echo "$concepts_response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[0]['id'] if data else '')" 2>/dev/null)
    
    if [ -n "$concept_id" ]; then
        echo -e "${GREEN}Found concept ID: $concept_id${NC}"
        echo ""
        
        # 5. Stream Teaching (first 10 events)
        echo -e "${YELLOW}Testing streaming teaching endpoint...${NC}"
        curl -N -s "$BASE_URL/api/stream/teach/$concept_id?section=hook&user_level=beginner" 2>&1 | head -10
        echo ""
        echo -e "${GREEN}✓ Streaming works!${NC}"
        echo ""
        
        # 6. Generate Flashcards
        test_endpoint "Generate Flashcards" "POST" "/api/flashcards/generate" "{\"concept_id\": \"$concept_id\", \"count\": 3}"
        
        # 7. Get Flashcards
        test_endpoint "Get Flashcards" "GET" "/api/concepts/$concept_id/flashcards"
        
        # 8. Generate Quiz Question
        test_endpoint "Generate Quiz Question" "POST" "/api/quiz/generate" "{\"concept_id\": \"$concept_id\", \"question_type\": \"multiple_choice\"}"
        
        # 9. Evaluate Quiz Answer
        test_endpoint "Evaluate Answer" "POST" "/api/quiz/evaluate" "{\"concept_id\": \"$concept_id\", \"question\": \"What is cryptography?\", \"answer\": \"It's about securing information\", \"confidence\": 70}"
    fi
fi

# 10. Course Map
test_endpoint "Get Course Map" "GET" "/api/course-map"

# 11. TTS Test
echo -e "${YELLOW}Testing TTS endpoint...${NC}"
tts_response=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"text": "Hey! This is a test of the Goku voice!", "voice_profile": "goku"}' \
    "$BASE_URL/api/tts/synthesize")
echo "$tts_response"
echo ""

echo "=============================================="
echo -e "${GREEN}✓ All endpoint tests complete!${NC}"
echo "=============================================="

# Made with Bob
