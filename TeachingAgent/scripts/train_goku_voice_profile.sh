#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

API_BASE_URL="${1:-http://localhost:8000}"
VOICE_CLIP_PATH="${2:-$SCRIPT_DIR/../../All_Goku_Voice_Clips_Dragon_Ball_FighterZ_Voice_Lines_Sean_Schemmel_128kbps_10144730_cut.mp3}"
PROFILE_NAME="${3:-goku}"

if [[ ! -f "$VOICE_CLIP_PATH" ]]; then
  echo "Voice clip not found: $VOICE_CLIP_PATH"
  echo "Provide the clip path as the second argument."
  exit 1
fi

echo "Training voice profile '$PROFILE_NAME' using clip: $VOICE_CLIP_PATH"
response=$(curl -sS -w "\n%{http_code}" -X POST "$API_BASE_URL/api/voice/train-profile" \
  -F "profile_name=$PROFILE_NAME" \
  -F "clip=@$VOICE_CLIP_PATH")

http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [[ "$http_code" != "200" ]]; then
  echo "Voice training failed (HTTP $http_code):"
  echo "$body"
  exit 1
fi

echo "$body"

echo

echo "Done. Available profiles:"
curl -sS "$API_BASE_URL/api/voice/profiles"
echo
