import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { MainDashboard } from '@/components/main-dashboard'
import { renderWithProviders, mockTutorStart } from './setup'

jest.mock('@/lib/api', () => ({
  checkComprehension: jest.fn(),
  checkContentAvailable: jest.fn(),
  getCourseMapNodes: jest.fn(),
  getInteractiveTeaching: jest.fn(),
  getJobStatus: jest.fn(),
  listVoiceProfiles: jest.fn(),
  nextQuizQuestion: jest.fn(),
  resolveApiUrl: jest.fn((path: string) => path),
  startTutor: jest.fn(),
  submitTutorAnswer: jest.fn(),
  trainVoiceProfile: jest.fn(),
  uploadZip: jest.fn(),
  weakAreas: jest.fn(),
}))

import * as api from '@/lib/api'

const interactiveTeachingPayload = {
  concept_name: 'SFTP Protocol',
  teaching_style: 'goku_conversational',
  learner_level: 'beginner',
  sections: {
    core_concept: 'SFTP sends files through SSH so the data stays protected.',
  },
  flashcards: [
    {
      id: 'core_concept',
      front: 'Explain SFTP in plain words.',
      back: 'SFTP uses SSH to move files safely.',
      cue: 'One short sentence.',
    },
  ],
  has_audio: true,
  diagrams: [],
  interactive_elements: [],
  audio: {
    total_duration_seconds: 8,
    voice_style: 'energetic_teacher',
    voice_profile: 'goku',
    segments: [
      {
        section: 'core_concept',
        audio_path: '/tmp/segment.wav',
        audio_url: '/api/assets/tts/segment.wav',
        duration_seconds: 8,
        text: 'SFTP uses SSH to move files safely.',
      },
    ],
  },
}

describe('MainDashboard teach-first experience', () => {
  beforeEach(() => {
    jest.clearAllMocks()

    ;(api.checkContentAvailable as jest.Mock).mockResolvedValue({ has_content: true, concept_count: 3 })
    ;(api.getCourseMapNodes as jest.Mock).mockResolvedValue([
      { id: 'concept-1', name: 'SFTP Protocol', source_reference: 'Day 1 notes' },
      { id: 'concept-2', name: 'Mailbox Concept', source_reference: 'Day 2 notes' },
      { id: 'concept-3', name: 'Routing Rules', source_reference: 'Day 3 notes' },
    ])
    ;(api.startTutor as jest.Mock).mockResolvedValue(
      mockTutorStart({
        lesson_preview: {
          name: 'SFTP Protocol',
          why_it_matters: 'Secure transfer protects your business data.',
          intuition: 'Think of it like a locked tunnel for files.',
          source_reference: 'Day 1 notes',
        },
      })
    )
    ;(api.weakAreas as jest.Mock).mockResolvedValue([])
    ;(api.listVoiceProfiles as jest.Mock).mockResolvedValue([
      {
        profile_name: 'goku',
        created_at: '',
        source_clip: '',
        sample_count: 4,
        samples: ['sample_001.wav'],
      },
    ])
    ;(api.getInteractiveTeaching as jest.Mock).mockResolvedValue(interactiveTeachingPayload)
    ;(api.checkComprehension as jest.Mock).mockResolvedValue({
      understood: true,
      score: 88,
      feedback: 'Clear understanding. Great job.',
      next_step: 'ready_for_question',
    })
    ;(api.nextQuizQuestion as jest.Mock).mockResolvedValue({
      question_id: 'quiz-1',
      concept_id: 'concept-1',
      question: 'Which protocol does SFTP rely on for security?',
      options: ['SSH', 'HTTP', 'SMTP', 'Telnet'],
      correct_answer: 'SSH',
      difficulty: 1,
    })
  })

  it('loads content-ready state with voice coach controls', async () => {
    renderWithProviders(<MainDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/Content Ready/i)).toBeInTheDocument()
    })

    expect(screen.getByText(/Voice Coach/i)).toBeInTheDocument()
    expect(screen.getByText(/Train profile from clip/i)).toBeInTheDocument()
  })

  it('shows diagrams/audio teaching support including subtitles and flashcards', async () => {
    renderWithProviders(<MainDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/Interactive Coach/i)).toBeInTheDocument()
    })

    await waitFor(() => {
      expect(screen.getByText(/Flashcard Drill/i)).toBeInTheDocument()
      expect(screen.getByText(/Reveal Answer/i)).toBeInTheDocument()
    })

  })

  it('keeps quiz locked until comprehension and flashcard review are complete', async () => {
    const user = userEvent.setup()
    renderWithProviders(<MainDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/Check My Understanding/i)).toBeInTheDocument()
    })

    await user.type(
      screen.getByPlaceholderText(/Explain this concept in your own words/i),
      'SFTP is a safe way to move files between systems.'
    )
    await user.type(
      screen.getByPlaceholderText(/Give one real-world situation/i),
      'A supplier sends purchase orders securely to a retailer.'
    )
    await user.type(
      screen.getByPlaceholderText(/What usually goes wrong/i),
      'People confuse SFTP with plain FTP and lose security.'
    )

    await user.click(screen.getByRole('button', { name: /Check My Understanding/i }))

    await waitFor(() => {
      expect(screen.getByText(/Understanding score:/i)).toBeInTheDocument()
    })

    const checkpointButtonBefore = screen.getByRole('button', { name: /Start Checkpoint Question/i })
    expect(checkpointButtonBefore).toBeDisabled()

    await user.click(screen.getByRole('button', { name: /Reveal Answer/i }))

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Start Checkpoint Question/i })).toBeEnabled()
      expect(screen.getByRole('button', { name: /Go To Quiz/i })).toBeEnabled()
    })
  })

  it('starts quiz only after unlock and evaluates selected option', async () => {
    const user = userEvent.setup()
    renderWithProviders(<MainDashboard />)

    await waitFor(() => {
      expect(screen.getByText(/Check My Understanding/i)).toBeInTheDocument()
    })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Reveal Answer/i })).toBeInTheDocument()
    })

    await user.click(screen.getByRole('button', { name: /Reveal Answer/i }))

    await user.type(
      screen.getByPlaceholderText(/Explain this concept in your own words/i),
      'SFTP protects file transfer by using SSH.'
    )
    await user.type(
      screen.getByPlaceholderText(/Give one real-world situation/i),
      'A finance team sends invoices securely.'
    )
    await user.type(
      screen.getByPlaceholderText(/What usually goes wrong/i),
      'Using FTP by mistake sends data without enough protection.'
    )

    await user.click(screen.getByRole('button', { name: /Check My Understanding/i }))

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Go To Quiz/i })).toBeEnabled()
    })

    await user.click(screen.getByRole('button', { name: /Go To Quiz/i }))

    await waitFor(() => {
      expect(screen.getByText(/Which protocol does SFTP rely on for security/i)).toBeInTheDocument()
    })

    await user.click(screen.getByRole('button', { name: 'SSH' }))
    await user.click(screen.getByRole('button', { name: /Check Quiz Answer/i }))

    await waitFor(() => {
      expect(screen.getByText(/You understood the idea clearly and applied it correctly/i)).toBeInTheDocument()
    })
  })
})
