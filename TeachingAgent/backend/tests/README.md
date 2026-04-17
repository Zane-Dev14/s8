# TeachingAgent Test Suite

Comprehensive test suite for high-ROI upgrades implementation.

## Test Coverage

### 1. Tutor Service Tests (`test_tutor_service.py`)
- **Answer-before-explanation contract**: Validates question-first approach
- **Mandatory confidence scoring**: Tests 0-100 confidence enforcement
- **Delayed feedback gates**: Verifies 1800ms vs 900ms delays
- **Response contract fields**: Tests all 11 required response fields
- **Retrieval-first guardrails**: Validates source grounding requirements
- **Uncertainty fallback**: Tests weak grounding detection
- **Interview mode**: Validates 10s pressure vs 20s lesson mode
- **Confusion detection**: Tests false confidence, lucky guess, fragile understanding, hesitation, guessing patterns
- **Next action adjustments**: Validates retry/review/rebuild/interview/harder logic

**Test Classes:**
- `TestAnswerBeforeExplanation` (2 tests)
- `TestMandatoryConfidenceScoring` (3 tests)
- `TestDelayedFeedbackGate` (2 tests)
- `TestTutorResponseContract` (2 tests)
- `TestRetrievalFirstGuardrails` (2 tests)
- `TestTutorRefusesFreestyling` (2 tests)
- `TestInterviewMode` (2 tests)
- `TestConfusionDetection` (3 tests)
- `TestNextActionAdjustments` (3 tests)
- `TestLearningAttemptPersistence` (1 test)

**Total: 22 tests**

### 2. Learning Service Tests (`test_learning_service.py`)
- **Brutal mastery requirements**: Tests 3 correct + high confidence + time pressure + spaced repetition
- **Forced revisit queue**: Validates false confidence, lucky guess, hesitation triggers
- **Rebuild loop activation**: Tests 5-7 minute intervals for rebuild actions
- **Graph-driven revisits**: Tests dependency prerequisite scheduling
- **Progress updates**: Validates accuracy EMA and interval logic
- **Next concept selection**: Tests prioritization and mastery filtering

**Test Classes:**
- `TestBrutalMasteryRequirements` (4 tests)
- `TestForcedRevisitQueue` (4 tests)
- `TestRebuildLoopActivation` (2 tests)
- `TestGraphDrivenRevisits` (3 tests)
- `TestProgressUpdateLogic` (4 tests)
- `TestEnsureProfiles` (2 tests)
- `TestNextConceptSelection` (3 tests)

**Total: 22 tests**

### 3. Chunking Service Tests (`test_chunking_service.py`)
- **Concept-aware roles**: Tests definition, example, edge_case, workflow_step classification
- **Concept bundles**: Validates explanation/example/mistake packaging
- **Retrieval scoring boosts**: Tests +0.08 for bundles/checkpoints, +0.04 for edge cases/workflows
- **Video learning nodes**: Tests what_changed, why_important, what_breaks, checkpoint_question generation
- **Chunking pipeline**: End-to-end video and document processing
- **Semantic splitting**: Tests sentence boundary respect
- **Lexical scoring**: Tests token overlap calculation

**Test Classes:**
- `TestConceptAwareChunkRoles` (4 tests)
- `TestConceptBundleGeneration` (2 tests)
- `TestRetrievalScoringBoosts` (4 tests)
- `TestVideoLearningNodeGeneration` (4 tests)
- `TestChunkingPipeline` (2 tests)
- `TestSemanticSplitting` (2 tests)
- `TestLexicalScoring` (3 tests)
- `TestTokenization` (2 tests)

**Total: 23 tests**

### 4. TTS Service Tests (`test_tts_service.py`)
- **Tone shaping**: Tests teaching vs challenge mode differences
- **Pacing pauses**: Validates pauses after ? and : markers
- **Emphasis handling**: Tests [EMPHASIS] marker removal and word wrapping
- **Speed windows**: Tests 1.15-1.25 (teaching) vs 1.20-1.30 (challenge) constraints
- **Output generation**: Tests file creation and fallback behavior
- **Edge cases**: Tests empty text, long text, special characters

**Test Classes:**
- `TestToneShaping` (3 tests)
- `TestPacingPauses` (3 tests)
- `TestEmphasisMarkerHandling` (2 tests)
- `TestSpeedWindows` (3 tests)
- `TestSynthesizeOutput` (4 tests)
- `TestPacingAndEmphasisIntegration` (2 tests)
- `TestEdgeCases` (6 tests)
- `TestSpeedBoundaries` (4 tests)

**Total: 27 tests**

## Running Tests

### Install Dependencies
```bash
cd TeachingAgent/backend
pip install -r requirements-test.txt
pip install -e .
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_tutor_service.py -v
pytest tests/test_learning_service.py -v
pytest tests/test_chunking_service.py -v
pytest tests/test_tts_service.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run Specific Test Class
```bash
pytest tests/test_tutor_service.py::TestAnswerBeforeExplanation -v
```

### Run Specific Test
```bash
pytest tests/test_tutor_service.py::TestAnswerBeforeExplanation::test_start_lesson_returns_question_first -v
```

## Test Summary

**Total Test Count: 94 tests**

- Tutor Service: 22 tests
- Learning Service: 22 tests
- Chunking Service: 23 tests
- TTS Service: 27 tests

## Key Features Validated

### High-ROI Upgrade #1: Answer-Before-Explanation Contract
✅ Question presented first
✅ Mandatory 0-100 confidence scoring
✅ Delayed feedback gates (1800ms vs 900ms)

### High-ROI Upgrade #2: Brutal Mastery Requirements
✅ 3 correct answers required
✅ High confidence (≥80) required
✅ Time pressure (≤12s) required
✅ Spaced repetition (≥8 min) required

### High-ROI Upgrade #3: Forced Revisit Queue
✅ False confidence detection (wrong + high confidence)
✅ Lucky guess detection (correct + low confidence)
✅ Hesitation confusion detection (wrong + slow)
✅ Fragile understanding detection

### High-ROI Upgrade #4: Rebuild Loop
✅ 5-7 minute intervals for rebuild
✅ "You thought you knew this" progression
✅ Retry increment on false confidence

### High-ROI Upgrade #5: Graph-Driven Revisits
✅ Dependency prerequisite scheduling
✅ Forced revisit prioritization
✅ Prerequisite repair before dependent concepts

### High-ROI Upgrade #6: Concept-Aware Chunking
✅ Definition/example/edge_case/workflow classification
✅ Concept bundle generation
✅ Retrieval scoring boosts

### High-ROI Upgrade #7: Video Learning Nodes
✅ what_changed detection
✅ why_important emphasis
✅ what_breaks failure impact
✅ checkpoint_question generation

### High-ROI Upgrade #8: Retrieval-First Guardrails
✅ Strong grounding requirement (score ≥0.18)
✅ Uncertainty fallback on weak grounding
✅ Source chunk inclusion in responses

### High-ROI Upgrade #9: Interview Mode
✅ 10s pressure window (vs 20s lesson)
✅ Hard follow-up questions
✅ Harder → interview action conversion

### High-ROI Upgrade #10: TTS Tone Shaping
✅ Teaching tone (1.15-1.25 speed, "Lock this in")
✅ Challenge tone (1.20-1.30 speed, "Focus...Answer now")
✅ Pacing pauses before key points
✅ Emphasis marker handling

## Notes

- Tests use in-memory SQLite database for isolation
- Mock OllamaRouter for LLM calls
- Type checker warnings are expected (false positives from optional query results)
- TTS tests create actual output files in data/tts directory
- All tests are independent and can run in any order