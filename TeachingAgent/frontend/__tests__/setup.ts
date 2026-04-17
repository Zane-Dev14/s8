import { render, RenderOptions } from '@testing-library/react'
import { ReactElement } from 'react'
import type { TutorStart, TutorAnswer, WeakArea, JobStatus } from '@/lib/types'

// Custom render function that can be extended with providers
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { ...options })
}

// Mock data factories for consistent test data
export const mockJobStatus = (overrides?: Partial<JobStatus>): JobStatus => ({
  job_id: 'test-job-123',
  status: 'processing',
  stage: 'chunking',
  message: 'Processing content...',
  created_at: '2026-04-06T08:00:00Z',
  updated_at: '2026-04-06T08:05:00Z',
  files_indexed: 5,
  concepts_count: 10,
  ...overrides,
})

export const mockTutorStart = (overrides?: Partial<TutorStart>): TutorStart => ({
  concept_id: 'concept-123',
  mode: 'lesson',
  lesson_preview: {
    name: 'Test Concept',
    why_it_matters: 'This is important for understanding the system',
    intuition: 'Think of it like a pipeline',
    source_reference: 'Module 1, Section 2',
  },
  question: 'What is the purpose of this component?',
  answer_before_explanation: true,
  time_pressure_seconds: 60,
  ...overrides,
})

export const mockTutorAnswer = (overrides?: Partial<TutorAnswer>): TutorAnswer => ({
  question: 'What is the purpose of this component?',
  user_answer: 'It processes data',
  user_confidence: 75,
  correctness: true,
  answer: 'The component processes incoming data streams',
  explanation: 'This component is designed to handle real-time data processing',
  misconception_tag: 'none',
  next_action: 'harder',
  source_chunks: [
    'Chunk 1: Data processing overview',
    'Chunk 2: Component architecture',
    'Chunk 3: Real-time handling',
  ],
  confidence: 'high',
  uncertainty: 'low',
  next_question: 'How does the component handle errors?',
  feedback_delay_ms: 3000,
  ...overrides,
})

export const mockWeakArea = (overrides?: Partial<WeakArea>): WeakArea => ({
  concept_id: 'weak-concept-1',
  concept_name: 'Weak Concept',
  accuracy: 0.45,
  retries: 3,
  response_time_ms: 15000,
  mastered: false,
  pressure_failures: 2,
  ...overrides,
})

// Helper to wait for async updates
export const waitForAsync = () => new Promise(resolve => setTimeout(resolve, 0))

// Helper to advance timers and flush promises
export const advanceTimersAndFlush = async (ms: number) => {
  jest.advanceTimersByTime(ms)
  await waitForAsync()
}

// Mock fetch responses
export const mockFetchSuccess = (data: unknown) => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(data),
    } as Response)
  )
}

export const mockFetchError = (status = 500, statusText = 'Internal Server Error') => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: false,
      status,
      statusText,
      json: () => Promise.reject(new Error('Failed to parse JSON')),
    } as Response)
  )
}

// Helper to create mock File objects
export const createMockFile = (
  name = 'test.zip',
  size = 1024,
  type = 'application/zip'
): File => {
  const blob = new Blob(['test content'], { type })
  return new File([blob], name, { type })
}

// Re-export everything from testing library
export * from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'

// Made with Bob
