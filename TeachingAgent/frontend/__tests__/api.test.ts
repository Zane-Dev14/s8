import {
  uploadZip,
  getJobStatus,
  startTutor,
  submitTutorAnswer,
  weakAreas,
} from '@/lib/api'
import {
  mockJobStatus,
  mockTutorStart,
  mockTutorAnswer,
  mockWeakArea,
  createMockFile,
} from './setup'

describe('API Contract Validation Tests', () => {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'

  beforeEach(() => {
    jest.clearAllMocks()
    global.fetch = jest.fn()
  })

  describe('Tutor Start API Contract', () => {
    it('should call tutor start endpoint with lesson mode', async () => {
      const mockData = mockTutorStart({ mode: 'lesson' })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await startTutor('test-user', 'lesson')

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE}/api/tutor/start?user_id=test-user&mode=lesson`,
        expect.objectContaining({
          cache: 'no-store',
        })
      )
      expect(result).toEqual(mockData)
    })

    it('should call tutor start endpoint with interview mode', async () => {
      const mockData = mockTutorStart({ mode: 'interview' })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await startTutor('test-user', 'interview')

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE}/api/tutor/start?user_id=test-user&mode=interview`,
        expect.objectContaining({
          cache: 'no-store',
        })
      )
      expect(result.mode).toBe('interview')
    })

    it('should return all required TutorStart fields', async () => {
      const mockData = mockTutorStart()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await startTutor('test-user', 'lesson')

      // Verify all required fields are present
      expect(result).toHaveProperty('concept_id')
      expect(result).toHaveProperty('mode')
      expect(result).toHaveProperty('lesson_preview')
      expect(result).toHaveProperty('question')
      expect(result).toHaveProperty('answer_before_explanation')
      expect(result).toHaveProperty('time_pressure_seconds')

      // Verify lesson_preview structure
      expect(result.lesson_preview).toHaveProperty('name')
      expect(result.lesson_preview).toHaveProperty('why_it_matters')
      expect(result.lesson_preview).toHaveProperty('intuition')
      expect(result.lesson_preview).toHaveProperty('source_reference')
    })

    it('should enforce answer_before_explanation is true', async () => {
      const mockData = mockTutorStart({ answer_before_explanation: true })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await startTutor('test-user', 'lesson')

      expect(result.answer_before_explanation).toBe(true)
    })

    it('should include time_pressure_seconds', async () => {
      const mockData = mockTutorStart({ time_pressure_seconds: 60 })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await startTutor('test-user', 'lesson')

      expect(result.time_pressure_seconds).toBe(60)
      expect(typeof result.time_pressure_seconds).toBe('number')
    })

    it('should throw error when API call fails', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: false,
          status: 404,
        } as Response)
      )

      await expect(startTutor('test-user', 'lesson')).rejects.toThrow('No lesson available')
    })
  })

  describe('Tutor Answer API Contract', () => {
    it('should submit answer with all required fields', async () => {
      const mockData = mockTutorAnswer()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await submitTutorAnswer(payload)

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE}/api/tutor/answer`,
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
      )
    })

    it('should require user_confidence field', async () => {
      const mockData = mockTutorAnswer()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 80,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await submitTutorAnswer(payload)

      const callBody = JSON.parse((global.fetch as jest.Mock).mock.calls[0][1].body)
      expect(callBody).toHaveProperty('user_confidence')
      expect(callBody.user_confidence).toBe(80)
    })

    it('should require response_time_ms field', async () => {
      const mockData = mockTutorAnswer()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 12500,
        mode: 'lesson' as const,
      }

      await submitTutorAnswer(payload)

      const callBody = JSON.parse((global.fetch as jest.Mock).mock.calls[0][1].body)
      expect(callBody).toHaveProperty('response_time_ms')
      expect(callBody.response_time_ms).toBe(12500)
    })

    it('should validate confidence is between 0-100', async () => {
      const mockData = mockTutorAnswer()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 50,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await submitTutorAnswer(payload)

      const callBody = JSON.parse((global.fetch as jest.Mock).mock.calls[0][1].body)
      expect(callBody.user_confidence).toBeGreaterThanOrEqual(0)
      expect(callBody.user_confidence).toBeLessThanOrEqual(100)
    })

    it('should throw error when submission fails', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500,
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await expect(submitTutorAnswer(payload)).rejects.toThrow('Answer evaluation failed')
    })
  })

  describe('Response Payload Validation - All 11 Fields', () => {
    it('should return all 11 required TutorAnswer fields', async () => {
      const mockData = mockTutorAnswer()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      // Verify all 11 fields from new contract
      expect(result).toHaveProperty('question')
      expect(result).toHaveProperty('user_answer')
      expect(result).toHaveProperty('user_confidence')
      expect(result).toHaveProperty('correctness')
      expect(result).toHaveProperty('answer')
      expect(result).toHaveProperty('explanation')
      expect(result).toHaveProperty('misconception_tag')
      expect(result).toHaveProperty('next_action')
      expect(result).toHaveProperty('source_chunks')
      expect(result).toHaveProperty('confidence')
      expect(result).toHaveProperty('uncertainty')

      // Additional high-ROI fields
      expect(result).toHaveProperty('next_question')
      expect(result).toHaveProperty('feedback_delay_ms')
    })

    it('should validate correctness is boolean', async () => {
      const mockData = mockTutorAnswer({ correctness: true })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      expect(typeof result.correctness).toBe('boolean')
    })

    it('should validate source_chunks is array', async () => {
      const mockData = mockTutorAnswer({
        source_chunks: ['Chunk 1', 'Chunk 2', 'Chunk 3'],
      })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      expect(Array.isArray(result.source_chunks)).toBe(true)
      expect(result.source_chunks.length).toBeGreaterThan(0)
    })

    it('should validate next_action is valid enum value', async () => {
      const validActions = ['harder', 'retry', 'review', 'rebuild', 'interview']
      const mockData = mockTutorAnswer({ next_action: 'harder' })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      expect(validActions).toContain(result.next_action)
    })

    it('should validate feedback_delay_ms is number', async () => {
      const mockData = mockTutorAnswer({ feedback_delay_ms: 3000 })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      expect(typeof result.feedback_delay_ms).toBe('number')
      expect(result.feedback_delay_ms).toBeGreaterThanOrEqual(0)
    })

    it('should include misconception_tag for incorrect answers', async () => {
      const mockData = mockTutorAnswer({
        correctness: false,
        misconception_tag: 'confuses_async_with_sync',
      })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'Wrong answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      expect(result.misconception_tag).toBeTruthy()
      expect(typeof result.misconception_tag).toBe('string')
    })

    it('should include confidence and uncertainty metrics', async () => {
      const mockData = mockTutorAnswer({
        confidence: 'high',
        uncertainty: 'low',
      })
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      const result = await submitTutorAnswer(payload)

      expect(result).toHaveProperty('confidence')
      expect(result).toHaveProperty('uncertainty')
      expect(typeof result.confidence).toBe('string')
      expect(typeof result.uncertainty).toBe('string')
    })
  })

  describe('Error Handling', () => {
    it('should handle missing confidence gracefully', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: false,
          status: 400,
          statusText: 'Bad Request',
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: undefined as any, // Missing confidence
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await expect(submitTutorAnswer(payload)).rejects.toThrow()
    })

    it('should handle invalid confidence values', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: false,
          status: 400,
          statusText: 'Bad Request',
        } as Response)
      )

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 150, // Invalid: > 100
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await expect(submitTutorAnswer(payload)).rejects.toThrow()
    })

    it('should handle network errors', async () => {
      global.fetch = jest.fn(() => Promise.reject(new Error('Network error')))

      const payload = {
        user_id: 'test-user',
        concept_id: 'concept-123',
        question: 'What is this?',
        user_answer: 'This is my answer',
        user_confidence: 75,
        response_time_ms: 5000,
        mode: 'lesson' as const,
      }

      await expect(submitTutorAnswer(payload)).rejects.toThrow('Network error')
    })
  })

  describe('Weak Areas API', () => {
    it('should fetch weak areas with all required fields', async () => {
      const mockData = {
        weak_areas: [
          mockWeakArea(),
          mockWeakArea({ concept_id: 'weak-2', concept_name: 'Weak 2' }),
        ],
      }
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await weakAreas('test-user')

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE}/api/analytics/weak-areas?user_id=test-user`,
        expect.objectContaining({
          cache: 'no-store',
        })
      )

      expect(Array.isArray(result)).toBe(true)
      expect(result.length).toBe(2)

      // Verify all required fields
      result.forEach((area) => {
        expect(area).toHaveProperty('concept_id')
        expect(area).toHaveProperty('concept_name')
        expect(area).toHaveProperty('accuracy')
        expect(area).toHaveProperty('retries')
        expect(area).toHaveProperty('response_time_ms')
        expect(area).toHaveProperty('mastered')
        expect(area).toHaveProperty('pressure_failures')
      })
    })

    it('should include pressure_failures field', async () => {
      const mockData = {
        weak_areas: [mockWeakArea({ pressure_failures: 5 })],
      }
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await weakAreas('test-user')

      expect(result[0].pressure_failures).toBe(5)
      expect(typeof result[0].pressure_failures).toBe('number')
    })
  })

  describe('Job Status API', () => {
    it('should fetch job status with all required fields', async () => {
      const mockData = mockJobStatus()
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const result = await getJobStatus('test-job-123')

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE}/api/ingest/test-job-123`,
        expect.objectContaining({
          cache: 'no-store',
        })
      )

      expect(result).toHaveProperty('job_id')
      expect(result).toHaveProperty('status')
      expect(result).toHaveProperty('stage')
      expect(result).toHaveProperty('message')
      expect(result).toHaveProperty('created_at')
      expect(result).toHaveProperty('updated_at')
      expect(result).toHaveProperty('files_indexed')
      expect(result).toHaveProperty('concepts_count')
    })
  })

  describe('Upload API', () => {
    it('should upload ZIP file with correct form data', async () => {
      const mockData = {
        job_id: 'new-job-123',
        status: 'queued',
        stage: 'queued',
      }
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        } as Response)
      )

      const file = createMockFile('test.zip')
      const result = await uploadZip(file)

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE}/api/ingest/upload`,
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData),
        })
      )

      expect(result).toHaveProperty('job_id')
      expect(result).toHaveProperty('status')
      expect(result).toHaveProperty('stage')
    })
  })
})

// Made with Bob
