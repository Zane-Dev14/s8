/**
 * React hooks for Server-Sent Events (SSE) streaming
 * Handles real-time text generation from backend
 */
import { useState, useEffect, useCallback, useRef } from 'react';

export interface StreamToken {
  token: string;
  done: boolean;
  error?: string;
}

export interface TeachingEvent {
  type: 'token' | 'section_complete' | 'session_complete' | 'error';
  section?: string;
  token?: string;
  content?: string;
  audio_url?: string;
  progress?: string;
  done: boolean;
  error?: string;
}

export interface QuizEvaluationEvent {
  type: 'token' | 'evaluation_complete' | 'error';
  token?: string;
  evaluation?: {
    is_correct: boolean;
    score: number;
    feedback: string;
    misconception_tag: string;
    next_action: string;
  };
  done: boolean;
  error?: string;
}

/**
 * Hook for streaming text generation
 * Generic hook for any SSE endpoint
 */
export function useStreamingText(url: string | null) {
  const [text, setText] = useState('');
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!url) return;

    // Reset state
    setText('');
    setDone(false);
    setError(null);
    setIsStreaming(true);

    // Create EventSource
    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onmessage = (event) => {
      try {
        const data: StreamToken = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          setDone(true);
          setIsStreaming(false);
          es.close();
          return;
        }

        if (data.done) {
          setDone(true);
          setIsStreaming(false);
          es.close();
          return;
        }

        if (data.token) {
          setText((prev) => prev + data.token);
        }
      } catch (err) {
        console.error('Failed to parse SSE data:', err);
      }
    };

    es.onerror = (err) => {
      console.error('SSE error:', err);
      setError('Connection error');
      setDone(true);
      setIsStreaming(false);
      es.close();
    };

    // Cleanup
    return () => {
      es.close();
      eventSourceRef.current = null;
    };
  }, [url]);

  const reset = useCallback(() => {
    setText('');
    setDone(false);
    setError(null);
    setIsStreaming(false);
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  return { text, done, error, isStreaming, reset };
}

/**
 * Hook for streaming teaching sessions
 * Handles section-by-section teaching with audio
 */
export function useTeachingStream(conceptId: string | null, userLevel: string = 'beginner') {
  const [sections, setSections] = useState<Record<string, string>>({});
  const [currentSection, setCurrentSection] = useState<string | null>(null);
  const [audioUrls, setAudioUrls] = useState<Record<string, string>>({});
  const [progress, setProgress] = useState('0/8');
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!conceptId) return;

    // Reset state
    setSections({});
    setCurrentSection(null);
    setAudioUrls({});
    setProgress('0/8');
    setDone(false);
    setError(null);
    setIsStreaming(true);

    // Create EventSource
    const url = `/api/stream/teach/${conceptId}?user_level=${userLevel}`;
    const es = new EventSource(url);
    eventSourceRef.current = es;

    let currentSectionText = '';
    let currentSectionName = '';

    es.onmessage = (event) => {
      try {
        const data: TeachingEvent = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          setDone(true);
          setIsStreaming(false);
          es.close();
          return;
        }

        if (data.type === 'token' && data.section && data.token) {
          // Accumulate tokens for current section
          currentSectionName = data.section;
          currentSectionText += data.token;
          setCurrentSection(currentSectionName);
          setSections((prev) => ({
            ...prev,
            [currentSectionName]: currentSectionText,
          }));
          if (data.progress) {
            setProgress(data.progress);
          }
        } else if (data.type === 'section_complete' && data.section && data.content) {
          // Section complete - save final content and audio
          setSections((prev) => ({
            ...prev,
            [data.section!]: data.content!,
          }));
          if (data.audio_url) {
            setAudioUrls((prev) => ({
              ...prev,
              [data.section!]: data.audio_url!,
            }));
          }
          if (data.progress) {
            setProgress(data.progress);
          }
          // Reset for next section
          currentSectionText = '';
          currentSectionName = '';
        } else if (data.type === 'session_complete') {
          setDone(true);
          setIsStreaming(false);
          es.close();
        }
      } catch (err) {
        console.error('Failed to parse teaching event:', err);
      }
    };

    es.onerror = (err) => {
      console.error('Teaching stream error:', err);
      setError('Connection error');
      setDone(true);
      setIsStreaming(false);
      es.close();
    };

    // Cleanup
    return () => {
      es.close();
      eventSourceRef.current = null;
    };
  }, [conceptId, userLevel]);

  const reset = useCallback(() => {
    setSections({});
    setCurrentSection(null);
    setAudioUrls({});
    setProgress('0/8');
    setDone(false);
    setError(null);
    setIsStreaming(false);
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  return {
    sections,
    currentSection,
    audioUrls,
    progress,
    done,
    error,
    isStreaming,
    reset,
  };
}

/**
 * Hook for streaming quiz evaluation
 * Real-time feedback as answer is evaluated
 */
export function useQuizEvaluation() {
  const [feedback, setFeedback] = useState('');
  const [evaluation, setEvaluation] = useState<QuizEvaluationEvent['evaluation'] | null>(null);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  const evaluate = useCallback(
    (questionId: string, userAnswer: string, confidence: number, responseTimeMs: number) => {
      // Reset state
      setFeedback('');
      setEvaluation(null);
      setDone(false);
      setError(null);
      setIsEvaluating(true);

      // Create EventSource
      const params = new URLSearchParams({
        question_id: questionId,
        user_answer: userAnswer,
        confidence: confidence.toString(),
        response_time_ms: responseTimeMs.toString(),
      });
      const url = `/api/stream/quiz/evaluate?${params}`;
      const es = new EventSource(url);
      eventSourceRef.current = es;

      es.onmessage = (event) => {
        try {
          const data: QuizEvaluationEvent = JSON.parse(event.data);

          if (data.error) {
            setError(data.error);
            setDone(true);
            setIsEvaluating(false);
            es.close();
            return;
          }

          if (data.type === 'token' && data.token) {
            // Accumulate feedback tokens
            setFeedback((prev) => prev + data.token);
          } else if (data.type === 'evaluation_complete' && data.evaluation) {
            // Evaluation complete
            setEvaluation(data.evaluation);
            setDone(true);
            setIsEvaluating(false);
            es.close();
          }
        } catch (err) {
          console.error('Failed to parse evaluation event:', err);
        }
      };

      es.onerror = (err) => {
        console.error('Evaluation stream error:', err);
        setError('Connection error');
        setDone(true);
        setIsEvaluating(false);
        es.close();
      };
    },
    []
  );

  const reset = useCallback(() => {
    setFeedback('');
    setEvaluation(null);
    setDone(false);
    setError(null);
    setIsEvaluating(false);
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  return {
    feedback,
    evaluation,
    done,
    error,
    isEvaluating,
    evaluate,
    reset,
  };
}

/**
 * Hook for typewriter effect
 * Animates text appearance character by character
 */
export function useTypewriter(text: string, speed: number = 20) {
  const [displayText, setDisplayText] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    if (!text) {
      setDisplayText('');
      return;
    }

    setIsTyping(true);
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        setDisplayText(text.slice(0, index + 1));
        index++;
      } else {
        setIsTyping(false);
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed]);

  return { displayText, isTyping };
}

// Made with Bob
