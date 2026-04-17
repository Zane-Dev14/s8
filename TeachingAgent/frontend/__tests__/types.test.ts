import type {
  JobStatus,
  TutorStart,
  TutorAnswer,
  QuizQuestion,
  WeakArea,
} from '@/lib/types'

describe('TypeScript Type Definitions', () => {
  describe('TutorStart Interface', () => {
    it('should match backend schema with all required fields', () => {
      const tutorStart: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test Concept',
          why_it_matters: 'Important for understanding',
          intuition: 'Think of it like...',
          source_reference: 'Module 1',
        },
        question: 'What is this?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      // Type assertions to ensure all fields are present
      expect(tutorStart.concept_id).toBeDefined()
      expect(tutorStart.mode).toBeDefined()
      expect(tutorStart.lesson_preview).toBeDefined()
      expect(tutorStart.question).toBeDefined()
      expect(tutorStart.answer_before_explanation).toBeDefined()
      expect(tutorStart.time_pressure_seconds).toBeDefined()
    })

    it('should enforce mode as literal type', () => {
      const lessonMode: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test',
          why_it_matters: 'Test',
          intuition: 'Test',
          source_reference: 'Test',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      const interviewMode: TutorStart = {
        concept_id: 'concept-123',
        mode: 'interview',
        lesson_preview: {
          name: 'Test',
          why_it_matters: 'Test',
          intuition: 'Test',
          source_reference: 'Test',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 30,
      }

      expect(lessonMode.mode).toBe('lesson')
      expect(interviewMode.mode).toBe('interview')
    })

    it('should enforce answer_before_explanation as boolean', () => {
      const tutorStart: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test',
          why_it_matters: 'Test',
          intuition: 'Test',
          source_reference: 'Test',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      expect(typeof tutorStart.answer_before_explanation).toBe('boolean')
    })

    it('should enforce time_pressure_seconds as number', () => {
      const tutorStart: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test',
          why_it_matters: 'Test',
          intuition: 'Test',
          source_reference: 'Test',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      expect(typeof tutorStart.time_pressure_seconds).toBe('number')
    })

    it('should have lesson_preview with all required fields', () => {
      const tutorStart: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test Concept',
          why_it_matters: 'Important',
          intuition: 'Think of it',
          source_reference: 'Module 1',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      expect(tutorStart.lesson_preview.name).toBeDefined()
      expect(tutorStart.lesson_preview.why_it_matters).toBeDefined()
      expect(tutorStart.lesson_preview.intuition).toBeDefined()
      expect(tutorStart.lesson_preview.source_reference).toBeDefined()
    })
  })

  describe('TutorAnswer Interface - All 11 Fields', () => {
    it('should include all 11 required fields from new contract', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'What is this?',
        user_answer: 'My answer',
        user_confidence: 75,
        correctness: true,
        answer: 'The correct answer',
        explanation: 'Detailed explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: ['Chunk 1', 'Chunk 2'],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next question',
        feedback_delay_ms: 3000,
      }

      // Verify all 11 core fields
      expect(tutorAnswer.question).toBeDefined()
      expect(tutorAnswer.user_answer).toBeDefined()
      expect(tutorAnswer.user_confidence).toBeDefined()
      expect(tutorAnswer.correctness).toBeDefined()
      expect(tutorAnswer.answer).toBeDefined()
      expect(tutorAnswer.explanation).toBeDefined()
      expect(tutorAnswer.misconception_tag).toBeDefined()
      expect(tutorAnswer.next_action).toBeDefined()
      expect(tutorAnswer.source_chunks).toBeDefined()
      expect(tutorAnswer.confidence).toBeDefined()
      expect(tutorAnswer.uncertainty).toBeDefined()

      // Additional high-ROI fields
      expect(tutorAnswer.next_question).toBeDefined()
      expect(tutorAnswer.feedback_delay_ms).toBeDefined()
    })

    it('should enforce user_confidence as number', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 80,
        correctness: true,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: [],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(typeof tutorAnswer.user_confidence).toBe('number')
    })

    it('should enforce correctness as boolean', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 80,
        correctness: false,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'confusion',
        next_action: 'retry',
        source_chunks: [],
        confidence: 'medium',
        uncertainty: 'high',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(typeof tutorAnswer.correctness).toBe('boolean')
    })

    it('should enforce next_action as valid enum', () => {
      const validActions: Array<TutorAnswer['next_action']> = [
        'harder',
        'retry',
        'review',
        'rebuild',
        'interview',
      ]

      validActions.forEach((action) => {
        const tutorAnswer: TutorAnswer = {
          question: 'Test?',
          user_answer: 'Answer',
          user_confidence: 80,
          correctness: true,
          answer: 'Correct',
          explanation: 'Explanation',
          misconception_tag: 'none',
          next_action: action,
          source_chunks: [],
          confidence: 'high',
          uncertainty: 'low',
          next_question: 'Next',
          feedback_delay_ms: 3000,
        }

        expect(validActions).toContain(tutorAnswer.next_action)
      })
    })

    it('should enforce source_chunks as string array', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 80,
        correctness: true,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: ['Chunk 1', 'Chunk 2', 'Chunk 3'],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(Array.isArray(tutorAnswer.source_chunks)).toBe(true)
      tutorAnswer.source_chunks.forEach((chunk) => {
        expect(typeof chunk).toBe('string')
      })
    })

    it('should enforce feedback_delay_ms as number', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 80,
        correctness: true,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: [],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next',
        feedback_delay_ms: 5000,
      }

      expect(typeof tutorAnswer.feedback_delay_ms).toBe('number')
    })

    it('should include misconception_tag field', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Wrong answer',
        user_confidence: 80,
        correctness: false,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'confuses_async_with_sync',
        next_action: 'retry',
        source_chunks: [],
        confidence: 'medium',
        uncertainty: 'high',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(typeof tutorAnswer.misconception_tag).toBe('string')
    })

    it('should include confidence and uncertainty metrics', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 80,
        correctness: true,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: [],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(typeof tutorAnswer.confidence).toBe('string')
      expect(typeof tutorAnswer.uncertainty).toBe('string')
    })
  })

  describe('WeakArea Interface - Mastery Tracking', () => {
    it('should include all mastery tracking fields', () => {
      const weakArea: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.45,
        retries: 3,
        response_time_ms: 15000,
        mastered: false,
        pressure_failures: 2,
      }

      expect(weakArea.concept_id).toBeDefined()
      expect(weakArea.concept_name).toBeDefined()
      expect(weakArea.accuracy).toBeDefined()
      expect(weakArea.retries).toBeDefined()
      expect(weakArea.response_time_ms).toBeDefined()
      expect(weakArea.mastered).toBeDefined()
      expect(weakArea.pressure_failures).toBeDefined()
    })

    it('should enforce mastered as boolean', () => {
      const weakArea: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.45,
        retries: 3,
        response_time_ms: 15000,
        mastered: false,
        pressure_failures: 2,
      }

      expect(typeof weakArea.mastered).toBe('boolean')
    })

    it('should enforce pressure_failures as number', () => {
      const weakArea: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.45,
        retries: 3,
        response_time_ms: 15000,
        mastered: false,
        pressure_failures: 5,
      }

      expect(typeof weakArea.pressure_failures).toBe('number')
    })

    it('should enforce accuracy as number between 0 and 1', () => {
      const weakArea: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.67,
        retries: 3,
        response_time_ms: 15000,
        mastered: false,
        pressure_failures: 2,
      }

      expect(typeof weakArea.accuracy).toBe('number')
      expect(weakArea.accuracy).toBeGreaterThanOrEqual(0)
      expect(weakArea.accuracy).toBeLessThanOrEqual(1)
    })

    it('should enforce response_time_ms as number', () => {
      const weakArea: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.45,
        retries: 3,
        response_time_ms: 12500,
        mastered: false,
        pressure_failures: 2,
      }

      expect(typeof weakArea.response_time_ms).toBe('number')
    })
  })

  describe('JobStatus Interface', () => {
    it('should include all required fields', () => {
      const jobStatus: JobStatus = {
        job_id: 'job-123',
        status: 'processing',
        stage: 'chunking',
        message: 'Processing content',
        created_at: '2026-04-06T08:00:00Z',
        updated_at: '2026-04-06T08:05:00Z',
        files_indexed: 5,
        concepts_count: 10,
      }

      expect(jobStatus.job_id).toBeDefined()
      expect(jobStatus.status).toBeDefined()
      expect(jobStatus.stage).toBeDefined()
      expect(jobStatus.message).toBeDefined()
      expect(jobStatus.created_at).toBeDefined()
      expect(jobStatus.updated_at).toBeDefined()
      expect(jobStatus.files_indexed).toBeDefined()
      expect(jobStatus.concepts_count).toBeDefined()
    })

    it('should enforce numeric fields', () => {
      const jobStatus: JobStatus = {
        job_id: 'job-123',
        status: 'processing',
        stage: 'chunking',
        message: 'Processing content',
        created_at: '2026-04-06T08:00:00Z',
        updated_at: '2026-04-06T08:05:00Z',
        files_indexed: 5,
        concepts_count: 10,
      }

      expect(typeof jobStatus.files_indexed).toBe('number')
      expect(typeof jobStatus.concepts_count).toBe('number')
    })
  })

  describe('QuizQuestion Interface', () => {
    it('should include all required fields', () => {
      const quizQuestion: QuizQuestion = {
        question_id: 'q-123',
        concept_id: 'concept-123',
        question: 'What is this?',
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 'A',
        difficulty: 3,
      }

      expect(quizQuestion.question_id).toBeDefined()
      expect(quizQuestion.concept_id).toBeDefined()
      expect(quizQuestion.question).toBeDefined()
      expect(quizQuestion.options).toBeDefined()
      expect(quizQuestion.correct_answer).toBeDefined()
      expect(quizQuestion.difficulty).toBeDefined()
    })

    it('should enforce options as string array', () => {
      const quizQuestion: QuizQuestion = {
        question_id: 'q-123',
        concept_id: 'concept-123',
        question: 'What is this?',
        options: ['Option A', 'Option B', 'Option C', 'Option D'],
        correct_answer: 'Option A',
        difficulty: 3,
      }

      expect(Array.isArray(quizQuestion.options)).toBe(true)
      quizQuestion.options.forEach((option) => {
        expect(typeof option).toBe('string')
      })
    })

    it('should enforce difficulty as number', () => {
      const quizQuestion: QuizQuestion = {
        question_id: 'q-123',
        concept_id: 'concept-123',
        question: 'What is this?',
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 'A',
        difficulty: 5,
      }

      expect(typeof quizQuestion.difficulty).toBe('number')
    })
  })

  describe('Type Compatibility with Backend Schemas', () => {
    it('should ensure TutorStart matches backend TutorStartResponse', () => {
      // This test ensures frontend types align with backend contract
      const backendResponse: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test Concept',
          why_it_matters: 'Important',
          intuition: 'Think of it',
          source_reference: 'Module 1',
        },
        question: 'What is this?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      // All fields should be accessible without type errors
      expect(backendResponse.concept_id).toBe('concept-123')
      expect(backendResponse.mode).toBe('lesson')
      expect(backendResponse.answer_before_explanation).toBe(true)
      expect(backendResponse.time_pressure_seconds).toBe(60)
    })

    it('should ensure TutorAnswer matches backend TutorAnswerResponse', () => {
      // This test ensures frontend types align with backend contract
      const backendResponse: TutorAnswer = {
        question: 'What is this?',
        user_answer: 'My answer',
        user_confidence: 75,
        correctness: true,
        answer: 'Correct answer',
        explanation: 'Detailed explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: ['Chunk 1', 'Chunk 2'],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next question',
        feedback_delay_ms: 3000,
      }

      // All 11 core fields should be accessible
      expect(backendResponse.question).toBeDefined()
      expect(backendResponse.user_answer).toBeDefined()
      expect(backendResponse.user_confidence).toBeDefined()
      expect(backendResponse.correctness).toBeDefined()
      expect(backendResponse.answer).toBeDefined()
      expect(backendResponse.explanation).toBeDefined()
      expect(backendResponse.misconception_tag).toBeDefined()
      expect(backendResponse.next_action).toBeDefined()
      expect(backendResponse.source_chunks).toBeDefined()
      expect(backendResponse.confidence).toBeDefined()
      expect(backendResponse.uncertainty).toBeDefined()
      expect(backendResponse.next_question).toBeDefined()
      expect(backendResponse.feedback_delay_ms).toBeDefined()
    })

    it('should ensure WeakArea includes confusion detection fields', () => {
      const backendResponse: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.45,
        retries: 3,
        response_time_ms: 15000,
        mastered: false,
        pressure_failures: 2,
      }

      // Confusion detection field
      expect(backendResponse.pressure_failures).toBeDefined()
      expect(typeof backendResponse.pressure_failures).toBe('number')
    })
  })

  describe('High-ROI Upgrade Fields Validation', () => {
    it('should validate answer_before_explanation field exists', () => {
      const tutorStart: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test',
          why_it_matters: 'Test',
          intuition: 'Test',
          source_reference: 'Test',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      expect(tutorStart).toHaveProperty('answer_before_explanation')
    })

    it('should validate time_pressure_seconds field exists', () => {
      const tutorStart: TutorStart = {
        concept_id: 'concept-123',
        mode: 'lesson',
        lesson_preview: {
          name: 'Test',
          why_it_matters: 'Test',
          intuition: 'Test',
          source_reference: 'Test',
        },
        question: 'Test?',
        answer_before_explanation: true,
        time_pressure_seconds: 60,
      }

      expect(tutorStart).toHaveProperty('time_pressure_seconds')
    })

    it('should validate feedback_delay_ms field exists', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 80,
        correctness: true,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: [],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(tutorAnswer).toHaveProperty('feedback_delay_ms')
    })

    it('should validate user_confidence field exists in TutorAnswer', () => {
      const tutorAnswer: TutorAnswer = {
        question: 'Test?',
        user_answer: 'Answer',
        user_confidence: 75,
        correctness: true,
        answer: 'Correct',
        explanation: 'Explanation',
        misconception_tag: 'none',
        next_action: 'harder',
        source_chunks: [],
        confidence: 'high',
        uncertainty: 'low',
        next_question: 'Next',
        feedback_delay_ms: 3000,
      }

      expect(tutorAnswer).toHaveProperty('user_confidence')
    })

    it('should validate pressure_failures field exists in WeakArea', () => {
      const weakArea: WeakArea = {
        concept_id: 'weak-1',
        concept_name: 'Weak Concept',
        accuracy: 0.45,
        retries: 3,
        response_time_ms: 15000,
        mastered: false,
        pressure_failures: 2,
      }

      expect(weakArea).toHaveProperty('pressure_failures')
    })
  })
})

// Made with Bob
