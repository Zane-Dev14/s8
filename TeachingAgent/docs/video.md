# TASK: VIDEO INTELLIGENCE

Process each .mp4 file.

## REQUIREMENTS

1. Transcribe with timestamps
2. Split into segments (30–90 seconds)
3. Detect topic shifts
4. Extract key frames
5. Link everything

## OUTPUT

[
  {
    "timestamp_start": "",
    "timestamp_end": "",
    "text": "",
    "topic": "",
    "importance": 1-5
  }
]

## RULES

- Preserve timestamps exactly
- Group by Day1–Day4
- Do NOT summarize yet
- Keep raw learning signal intact