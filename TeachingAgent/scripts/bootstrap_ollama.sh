#!/usr/bin/env bash
set -euo pipefail

models=(
  "llama3.1:8b-instruct"
  "openchat"
  "qwen2.5:32b-instruct-q5_K_M"
  "deepseek-r1:32b"
  "Qwen3-coder:30b"
)

for model in "${models[@]}"; do
  echo "Pulling ${model}"
  ollama pull "${model}"
done

echo "Ollama model bootstrap complete."
