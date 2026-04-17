# TASK: BUILD KNOWLEDGE GRAPH

Input:
- transcripts
- documents
- mappings
- xml/bpml

## OUTPUT

Concept graph:

Nodes:
- concept
- workflow
- input/output

Edges:
- depends_on
- part_of
- transforms

## ALSO DETECT

- repeated concepts
- prerequisites
- common failure points

## RULES

- Merge duplicates
- Prefer clarity over completeness
- Do NOT hallucinate missing data