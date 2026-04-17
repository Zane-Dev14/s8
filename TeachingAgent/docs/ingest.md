# TASK: DATASET INGESTION

You are processing a ZIP dataset.

## INPUT
A directory structured like:

- Mixed files (videos, PDFs, XML, BPML, mappings)
- Webex recordings grouped by Day1–Day4
- Non-uniform naming

## YOUR JOB

Build a structured index.

## OUTPUT JSON PER FILE

{
  "path": "",
  "folder": "",
  "type": "",
  "is_video": false,
  "recording_day": "",
  "priority": ""
}

## RULES

- Use folder names as metadata
- Detect videos via .mp4
- Ignore .exe
- Tag recordings by Day folder
- DO NOT infer topic meaning yet

## GOAL

Create a clean dataset map for downstream learning.