#!/bin/bash

echo "========================================="
echo "Teaching Agent - Final System Test"
echo "========================================="
echo ""

CONCEPT_ID="8ddc08c1-65d7-46b5-8ed9-c330bdc1c089"
BASE_URL="http://localhost:8000"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
        echo "  Response: $body" | head -c 100
        return 1
    fi
}

passed=0
failed=0

echo "1. Core Endpoints"
echo "-----------------"
test_endpoint "Health Check" "$BASE_URL/health" && ((passed++)) || ((failed++))
test_endpoint "List Subjects" "$BASE_URL/api/subjects" && ((passed++)) || ((failed++))
test_endpoint "Get Concept" "$BASE_URL/api/concepts/$CONCEPT_ID" && ((passed++)) || ((failed++))
test_endpoint "Course Map" "$BASE_URL/api/course-map" && ((passed++)) || ((failed++))
echo ""

echo "2. Teaching & Learning"
echo "----------------------"
test_endpoint "Stream Teaching" "$BASE_URL/api/stream/teach/$CONCEPT_ID?section=hook" && ((passed++)) || ((failed++))
test_endpoint "Generate Flashcards" "$BASE_URL/api/flashcards/generate" "POST" "{\"concept_id\":\"$CONCEPT_ID\",\"count\":3}" && ((passed++)) || ((failed++))
test_endpoint "Generate Quiz" "$BASE_URL/api/quiz/generate" "POST" "{\"concept_id\":\"$CONCEPT_ID\",\"count\":2}" && ((passed++)) || ((failed++))
echo ""

echo "3. Database Stats"
echo "-----------------"
subjects=$(curl -s "$BASE_URL/api/subjects" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
echo "  Subjects: $subjects"

total_concepts=0
for i in {1..5}; do
    count=$(curl -s "$BASE_URL/api/subjects/$i/concepts" 2>/dev/null | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    total_concepts=$((total_concepts + count))
done
echo "  Total Concepts: $total_concepts"
echo ""

echo "4. Performance Check"
echo "--------------------"
echo -n "  First token latency: "
start=$(date +%s%N)
curl -s "$BASE_URL/api/stream/teach/$CONCEPT_ID?section=hook" | head -1 > /dev/null
end=$(date +%s%N)
latency=$(( (end - start) / 1000000 ))
if [ $latency -lt 1000 ]; then
    echo -e "${GREEN}${latency}ms ✓${NC}"
else
    echo -e "${YELLOW}${latency}ms (target: <500ms)${NC}"
fi
echo ""

echo "========================================="
echo "Test Results"
echo "========================================="
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo ""
    echo "System Status: READY FOR USE"
    echo ""
    echo "Next Steps:"
    echo "  1. Install Node.js to start frontend"
    echo "  2. Upgrade to Python 3.10+ for TTS"
    echo "  3. Add ChromaDB for better RAG"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Check logs: tail -50 /tmp/backend.log"
    exit 1
fi
