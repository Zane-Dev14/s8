export type JobStatus = {
  job_id: string;
  status: string;
  stage: string;
  message: string;
  created_at: string;
  updated_at: string;
  files_indexed: number;
  concepts_count: number;
};

export type CourseMapNode = {
  id: string;
  name: string;
  source_reference: string;
};

export type TutorStart = {
  concept_id: string;
  mode: "lesson" | "interview";
  lesson_preview: Record<string, string>;
  question: string;
  answer_before_explanation: boolean;
  time_pressure_seconds: number;
};

export type TutorAnswer = {
  question: string;
  user_answer: string;
  user_confidence: number;
  correctness: boolean;
  answer: string;
  explanation: string;
  misconception_tag: string;
  next_action: "harder" | "retry" | "review" | "rebuild" | "interview";
  source_chunks: string[];
  confidence: string;
  uncertainty: string;
  next_question: string;
  feedback_delay_ms: number;
};

export type QuizQuestion = {
  question_id: string;
  concept_id: string;
  question: string;
  options: string[];
  correct_answer: string;
  difficulty: number;
};

export type WeakArea = {
  concept_id: string;
  concept_name: string;
  accuracy: number;
  retries: number;
  response_time_ms: number;
  mastered: boolean;
  pressure_failures: number;
};

export type InteractiveTeachDiagram = {
  title: string;
  description: string;
  image_url: string;
  source_path: string;
  mermaid_code?: string;
};

export type InteractiveTeachAudioSegment = {
  section: string;
  audio_path: string;
  audio_url: string;
  duration_seconds: number;
  text: string;
};

export type InteractiveTeachFlashcard = {
  id: string;
  front: string;
  back: string;
  cue: string;
};

export type InteractiveTeach = {
  concept_name: string;
  teaching_style: string;
  learner_level: string;
  sections: Record<string, string>;
  flashcards: InteractiveTeachFlashcard[];
  has_audio: boolean;
  diagrams: InteractiveTeachDiagram[];
  interactive_elements: Array<Record<string, unknown>>;
  audio?: {
    total_duration_seconds: number;
    segments: InteractiveTeachAudioSegment[];
    voice_style: string;
    voice_profile: string;
  };
};

export type ComprehensionCheck = {
  understood: boolean;
  score: number;
  feedback: string;
  next_step: "ready_for_question" | "needs_reteach";
};

export type VoiceProfile = {
  profile_name: string;
  created_at: string;
  source_clip: string;
  sample_count: number;
  samples: string[];
};
