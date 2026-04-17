"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  AlertTriangle,
  BookOpenCheck,
  BrainCircuit,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Gauge,
  ListChecks,
  Sparkles,
  Timer,
  UploadCloud,
  Volume2,
} from "lucide-react";

import {
  checkComprehension,
  checkContentAvailable,
  getCourseMapNodes,
  getJobStatus,
  getInteractiveTeaching,
  listVoiceProfiles,
  nextQuizQuestion,
  resolveApiUrl,
  startTutor,
  submitTutorAnswer,
  trainVoiceProfile,
  uploadZip,
  weakAreas,
} from "@/lib/api";
import type {
  CourseMapNode,
  ComprehensionCheck,
  InteractiveTeach,
  JobStatus,
  QuizQuestion,
  TutorAnswer,
  TutorStart,
  VoiceProfile,
  WeakArea,
} from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardText, CardTitle } from "@/components/ui/card";
import { DiagramViewer } from "@/components/diagram-viewer";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";

const USER_ID = "local-user";

const stageOrder = [
  "queued",
  "extracting",
  "indexing",
  "transcription",
  "parsing",
  "chunking",
  "embedding",
  "knowledge_graph",
  "quiz",
  "completed",
];

const DEFAULT_VISUAL_DESCRIPTION = "Picture the sender on one side, receiver on the other, and a verified secure path in the middle.";
const DEFAULT_REAL_EXAMPLE = "A partner file enters validation, moves through secure transfer, then lands in the destination mailbox.";
const TEACHING_SECTION_ORDER = [
  "hook",
  "analogy",
  "core_concept",
  "visual_description",
  "real_example",
  "why_it_matters",
  "practice_scenario",
  "encouragement",
  "common_mistake",
];

function buildLocalTeachingSession(tutor: TutorStart): InteractiveTeach {
  const sourceRef = tutor.lesson_preview.source_reference || "bootcamp source material";
  const conceptName = tutor.lesson_preview.name;
  const sections: Record<string, string> = {
    hook: `Alright, quick win. ${conceptName} becomes easy when you map the flow from sender to receiver.`,
    analogy:
      tutor.lesson_preview.intuition ||
      "Think of this as a gated delivery lane where every package is checked before moving.",
    core_concept:
      tutor.lesson_preview.explanation ||
      `This is the transfer control path your system uses to move files safely and reliably. Grounding: ${sourceRef}.`,
    visual_description: DEFAULT_VISUAL_DESCRIPTION,
    real_example: DEFAULT_REAL_EXAMPLE,
    why_it_matters:
      tutor.lesson_preview.why_it_matters ||
      "If this step fails, partner delivery windows are missed and downstream processing breaks.",
    practice_scenario: `You need to deliver a partner file today. How would you apply ${conceptName} so delivery stays secure?`,
    common_mistake:
      tutor.lesson_preview.common_mistake ||
      "Teams often skip transfer validation and only discover failures after SLA windows close.",
    encouragement: "Nice progress. Keep each step simple and you will master it.",
  };

  const flashcards = Object.entries(sections).map(([id, text]) => ({
    id,
    front: `Explain ${id.replaceAll("_", " ")} in plain words.`,
    back: text,
    cue: "Use one simple sentence.",
  }));

  return {
    concept_name: tutor.lesson_preview.name,
    teaching_style: "coach_plain",
    learner_level: "beginner",
    sections,
    flashcards,
    has_audio: false,
    diagrams: [],
    interactive_elements: [],
    audio: undefined,
  };
}

export function MainDashboard() {
  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState<JobStatus | null>(null);
  const [mode, setMode] = useState<"lesson" | "interview">("lesson");
  const [tutor, setTutor] = useState<TutorStart | null>(null);
  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState(60);
  const [answerResult, setAnswerResult] = useState<TutorAnswer | null>(null);
  const [pendingResult, setPendingResult] = useState<TutorAnswer | null>(null);
  const [revealCountdownMs, setRevealCountdownMs] = useState(0);
  const [weak, setWeak] = useState<WeakArea[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [timerTick, setTimerTick] = useState(0);
  const [hasExistingContent, setHasExistingContent] = useState(false);
  const [conceptCount, setConceptCount] = useState(0);
  const [courseTopics, setCourseTopics] = useState<CourseMapNode[]>([]);
  const [topicSwitching, setTopicSwitching] = useState(false);
  const [readyToAnswer, setReadyToAnswer] = useState(false);
  const [teaching, setTeaching] = useState<InteractiveTeach | null>(null);
  const [teachLoading, setTeachLoading] = useState(false);
  const [teachStep, setTeachStep] = useState(0);
  const [comprehensionDraft, setComprehensionDraft] = useState({
    summary: "",
    example: "",
    failure: "",
  });
  const [comprehensionResult, setComprehensionResult] = useState<ComprehensionCheck | null>(null);
  const [checkingComprehension, setCheckingComprehension] = useState(false);
  const [voiceProfiles, setVoiceProfiles] = useState<VoiceProfile[]>([]);
  const [selectedVoiceProfile, setSelectedVoiceProfile] = useState("goku");
  const [newVoiceProfileName, setNewVoiceProfileName] = useState("goku");
  const [voiceTrainingBusy, setVoiceTrainingBusy] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false);
  const [audioNotice, setAudioNotice] = useState("");
  const [visitedTeachSections, setVisitedTeachSections] = useState<Record<string, boolean>>({});
  const [activeFlashcard, setActiveFlashcard] = useState(0);
  const [flashcardRevealed, setFlashcardRevealed] = useState(false);
  const [seenFlashcards, setSeenFlashcards] = useState<Record<string, boolean>>({});
  const [quizQuestion, setQuizQuestion] = useState<QuizQuestion | null>(null);
  const [quizChoice, setQuizChoice] = useState("");
  const [quizFeedback, setQuizFeedback] = useState<{ correct: boolean; message: string } | null>(null);
  const [quizLoading, setQuizLoading] = useState(false);
  const [quizScore, setQuizScore] = useState({ correct: 0, total: 0 });
  const answerStart = useRef<number>(Date.now());
  const revealTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const revealTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  const stageProgress = useMemo(() => {
    if (!status) {
      return 0;
    }
    const index = stageOrder.indexOf(status.stage);
    if (index < 0) {
      return 0;
    }
    return Math.round((index / (stageOrder.length - 1)) * 100);
  }, [status]);

  useEffect(() => {
    if (!jobId || status?.status === "completed" || status?.status === "failed") {
      return;
    }

    const timer = setInterval(async () => {
      try {
        const current = await getJobStatus(jobId);
        setStatus(current);
      } catch {
        setError("Lost connection to backend while polling status.");
      }
    }, 3000);

    return () => clearInterval(timer);
  }, [jobId, status?.status]);

  useEffect(() => {
    if (status?.status !== "completed" || !jobId) {
      return;
    }

    void hydratePostIngest(jobId, mode);
  }, [jobId, status?.status, mode]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimerTick((value) => value + 1);
    }, 250);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    return () => {
      if (revealTimer.current) {
        clearInterval(revealTimer.current);
      }
      if (revealTimeout.current) {
        clearTimeout(revealTimeout.current);
      }
    };
  }, []);

  // Reset readyToAnswer when tutor changes (new concept loaded)
  useEffect(() => {
    if (tutor) {
      setReadyToAnswer(false);
      setTeachStep(0);
      setVisitedTeachSections({});
      setActiveFlashcard(0);
      setFlashcardRevealed(false);
      setSeenFlashcards({});
      setComprehensionDraft({ summary: "", example: "", failure: "" });
      setComprehensionResult(null);
      setQuizQuestion(null);
      setQuizChoice("");
      setQuizFeedback(null);
      setQuizScore({ correct: 0, total: 0 });
      setAudioLoading(false);
      setAudioNotice("");
    }
  }, [tutor?.concept_id]);

  useEffect(() => {
    async function loadVoiceProfiles() {
      try {
        const profiles = await listVoiceProfiles();
        if (profiles.length) {
          setVoiceProfiles(profiles);
          setSelectedVoiceProfile((current) => {
            const existing = profiles.find((profile) => profile.profile_name === current);
            return existing ? current : profiles[0].profile_name;
          });
        }
      } catch {
        // Keep default profile when backend has no trained voice profiles yet.
      }
    }

    void loadVoiceProfiles();
  }, []);

  useEffect(() => {
    if (!tutor) {
      setTeaching(null);
      return;
    }

    async function loadInteractiveTeaching() {
      const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
      const fetchWithRetry = async (withAudio: boolean, attempts: number): Promise<InteractiveTeach | null> => {
        for (let attempt = 0; attempt < attempts; attempt += 1) {
          try {
            return await getInteractiveTeaching(tutor.concept_id, USER_ID, selectedVoiceProfile, withAudio);
          } catch {
            if (attempt < attempts - 1) {
              await sleep(1200 * (attempt + 1));
            }
          }
        }
        return null;
      };

      try {
        setTeachLoading(true);
        setAudioLoading(false);
        setAudioNotice("");
        const session = await fetchWithRetry(false, 3);
        if (session) {
          setTeaching(session);
        } else {
          setTeaching((current) => current ?? buildLocalTeachingSession(tutor));
        }
      } catch {
        setTeaching((current) => current ?? buildLocalTeachingSession(tutor));
      } finally {
        setTeachLoading(false);
      }

      setAudioLoading(true);
      setAudioNotice("Generating coach audio automatically...");
      for (let attempt = 0; attempt < 3; attempt += 1) {
        const withAudio = await fetchWithRetry(true, 2);
        if (withAudio?.has_audio) {
          setTeaching((current) => ({
            ...(current ?? withAudio),
            ...withAudio,
          }));
          setAudioNotice("");
          setAudioLoading(false);
          return;
        }
        if (attempt < 2) {
          await sleep(2500);
        }
      }
      setAudioLoading(false);
      setAudioNotice("Audio is still processing in the background and will appear automatically when ready.");
    }

    void loadInteractiveTeaching();
  }, [tutor?.concept_id, selectedVoiceProfile]);

  useEffect(() => {
    if (!tutor || !courseTopics.length) {
      return;
    }
    const index = courseTopics.findIndex((topic) => topic.id === tutor.concept_id);
    if (index >= 0) {
      setConceptCount(courseTopics.length);
    }
  }, [tutor?.concept_id, courseTopics]);

  useEffect(() => {
    if (!tutor || teaching?.has_audio) {
      return;
    }

    const timer = setInterval(async () => {
      try {
        const withAudio = await getInteractiveTeaching(tutor.concept_id, USER_ID, selectedVoiceProfile, true);
        if (!withAudio.has_audio) {
          return;
        }
        setTeaching((current) => ({
          ...(current ?? withAudio),
          ...withAudio,
        }));
        setAudioNotice("");
        setAudioLoading(false);
      } catch {
        // Keep retrying silently in the background.
      }
    }, 7000);

    return () => clearInterval(timer);
  }, [tutor?.concept_id, teaching?.has_audio, selectedVoiceProfile]);

  async function bootstrapExistingContent(silent = false) {
    try {
      const [contentCheck, topics] = await Promise.all([checkContentAvailable(), getCourseMapNodes()]);
      const { has_content, concept_count } = contentCheck;
      setHasExistingContent(has_content);
      setConceptCount(concept_count);
      setCourseTopics(topics);

      if (!has_content) {
        return;
      }

      const [tutorData, weakData] = await Promise.all([startTutor(USER_ID, mode), weakAreas(USER_ID)]);
      setTutor(tutorData);
      setWeak(weakData);
      answerStart.current = Date.now();
      setStatus({
        job_id: "existing",
        status: "completed",
        stage: "completed",
        message: `${concept_count} concepts ready`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        files_indexed: 0,
        concepts_count: concept_count,
      });
      if (!silent) {
        setError("");
      }
    } catch (err) {
      if (!silent) {
        setError("Backend is not ready yet. Retrying automatically...");
      }
      console.error("Failed to bootstrap existing content:", err);
    }
  }

  // Check for existing content on mount
  useEffect(() => {
    void bootstrapExistingContent(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Auto-retry content bootstrap so the app recovers even if backend starts a bit later.
  useEffect(() => {
    if (tutor || busy || Boolean(jobId)) {
      return;
    }
    const timer = setInterval(() => {
      void bootstrapExistingContent(true);
    }, 7000);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tutor, busy, jobId, mode]);

  async function hydratePostIngest(localJobId: string, tutorMode: "lesson" | "interview") {
    try {
      const [tutorStartData, weakData, topics] = await Promise.all([
        startTutor(USER_ID, tutorMode),
        weakAreas(USER_ID),
        getCourseMapNodes(),
      ]);
      setTutor(tutorStartData);
      answerStart.current = Date.now();
      setWeak(weakData);
      setCourseTopics(topics);
      setConceptCount(topics.length || conceptCount);
    } catch {
      setError("Ingestion completed, but lesson bootstrap failed. Verify Ollama and parser services.");
    }
  }

  async function skipToNextTopic() {
    if (!tutor || !courseTopics.length) {
      return;
    }
    const currentIndex = courseTopics.findIndex((topic) => topic.id === tutor.concept_id);
    const nextIndex = currentIndex >= 0 ? (currentIndex + 1) % courseTopics.length : 0;
    const nextTopic = courseTopics[nextIndex];
    if (!nextTopic) {
      return;
    }

    try {
      setTopicSwitching(true);
      const [session, weakData] = await Promise.all([
        startTutor(USER_ID, mode, nextTopic.id),
        weakAreas(USER_ID),
      ]);
      setTutor(session);
      setWeak(weakData);
      setError("");
      answerStart.current = Date.now();
    } catch {
      setError("Unable to load the next topic right now.");
    } finally {
      setTopicSwitching(false);
    }
  }

  async function onUpload(file: File | null) {
    if (!file) {
      return;
    }
    setError("");
    setBusy(true);
    setStatus(null);
    setTutor(null);
    setAnswer("");
    setConfidence(60);
    setAnswerResult(null);
    setPendingResult(null);
    setRevealCountdownMs(0);
    setWeak([]);

    try {
      const res = await uploadZip(file);
      setJobId(res.job_id);
      const current = await getJobStatus(res.job_id);
      setStatus(current);
    } catch {
      setError("Upload failed. Ensure backend is running and reachable.");
    } finally {
      setBusy(false);
    }
  }

  async function evaluateComprehension() {
    if (!tutor) {
      return;
    }
    if (!comprehensionDraft.summary.trim() || !comprehensionDraft.example.trim() || !comprehensionDraft.failure.trim()) {
      setError("Fill out all understanding checks before continuing.");
      return;
    }

    try {
      setError("");
      setCheckingComprehension(true);
      const result = await checkComprehension({
        user_id: USER_ID,
        concept_id: tutor.concept_id,
        summary_in_own_words: comprehensionDraft.summary,
        real_world_example: comprehensionDraft.example,
        failure_mode: comprehensionDraft.failure,
      });
      setComprehensionResult(result);
    } catch {
      setError("Unable to evaluate understanding right now. Please retry.");
    } finally {
      setCheckingComprehension(false);
    }
  }

  async function onTrainVoiceClip(file: File | null) {
    if (!file) {
      return;
    }
    try {
      setVoiceTrainingBusy(true);
      const profile = await trainVoiceProfile(newVoiceProfileName, file);
      setSelectedVoiceProfile(profile.profile_name);
      setNewVoiceProfileName(profile.profile_name);
      const profiles = await listVoiceProfiles();
      setVoiceProfiles(profiles);
    } catch {
      setError("Voice profile training failed. Make sure ffmpeg is available on backend.");
    } finally {
      setVoiceTrainingBusy(false);
    }
  }

  async function loadNextQuizQuestion() {
    try {
      setQuizLoading(true);
      setQuizFeedback(null);
      const question = await nextQuizQuestion();
      setQuizQuestion(question);
      setQuizChoice("");
    } catch {
      setError("No quiz question is available right now. Try again after ingesting content.");
    } finally {
      setQuizLoading(false);
    }
  }

  function submitQuizAnswer() {
    if (!quizQuestion || !quizChoice) {
      return;
    }

    const correct = quizChoice === quizQuestion.correct_answer;
    setQuizScore((value) => ({
      correct: value.correct + (correct ? 1 : 0),
      total: value.total + 1,
    }));
    setQuizFeedback({
      correct,
      message: correct
        ? "Great job. You understood the idea clearly and applied it correctly."
        : `Not quite yet. Correct answer: ${quizQuestion.correct_answer}`,
    });
  }

  async function submitAnswer() {
    if (!tutor || !answer.trim()) {
      return;
    }
    try {
      const elapsed = Date.now() - answerStart.current;
      const result = await submitTutorAnswer({
        user_id: USER_ID,
        concept_id: tutor.concept_id,
        question: tutor.question,
        user_answer: answer,
        user_confidence: confidence,
        response_time_ms: elapsed,
        mode,
      });
      setPendingResult(result);
      setAnswerResult(null);
      setRevealCountdownMs(result.feedback_delay_ms);
      if (revealTimer.current) {
        clearInterval(revealTimer.current);
      }
      if (revealTimeout.current) {
        clearTimeout(revealTimeout.current);
      }
      revealTimer.current = setInterval(() => {
        setRevealCountdownMs((value) => Math.max(0, value - 100));
      }, 100);
      revealTimeout.current = setTimeout(() => {
        if (revealTimer.current) {
          clearInterval(revealTimer.current);
        }
        setAnswerResult(result);
      }, result.feedback_delay_ms);

      setAnswer("");
      answerStart.current = Date.now();
      const [nextLesson, weakData] = await Promise.all([startTutor(USER_ID, mode), weakAreas(USER_ID)]);
      setTutor(nextLesson);
      setWeak(weakData);
    } catch {
      setError("Tutor evaluation failed. Check backend model routing and database state.");
    }
  }

  async function swapMode(nextMode: "lesson" | "interview") {
    setMode(nextMode);
    if (!status || status.status !== "completed") {
      return;
    }
    try {
      const session = await startTutor(USER_ID, nextMode);
      setTutor(session);
      setAnswer("");
      setAnswerResult(null);
      setPendingResult(null);
      setRevealCountdownMs(0);
      answerStart.current = Date.now();
    } catch {
      setError("Unable to switch tutor mode right now.");
    }
  }

  const elapsedMs = timerTick >= 0 ? Date.now() - answerStart.current : 0;
  const remainingPressureSec = tutor
    ? Math.max(0, tutor.time_pressure_seconds - Math.floor(elapsedMs / 1000))
    : 0;

  const fallbackSections = tutor
    ? {
        hook: `Alright, let us learn ${tutor.lesson_preview.name} in simple steps.`,
        analogy: tutor.lesson_preview.intuition || "Think of this as a protected delivery lane between systems.",
        core_concept: tutor.lesson_preview.explanation || tutor.lesson_preview.intuition || "We will break this down in plain words.",
        visual_description: DEFAULT_VISUAL_DESCRIPTION,
        real_example: DEFAULT_REAL_EXAMPLE,
        why_it_matters: tutor.lesson_preview.why_it_matters || "If this fails, files get stuck or exposed.",
        practice_scenario: `A partner file needs to move now. Which secure path would you choose for ${tutor.lesson_preview.name}?`,
        common_mistake: tutor.lesson_preview.common_mistake || "Watch out for common confusion between similar protocols.",
        encouragement: "You are doing great. One clear mental picture at a time.",
      }
    : {};

  const teachingSource = teaching?.sections && Object.keys(teaching.sections).length > 0 ? teaching.sections : fallbackSections;
  const orderedTeachingEntries = TEACHING_SECTION_ORDER
    .filter((key) => Boolean(teachingSource[key]))
    .map((key) => [key, teachingSource[key]] as [string, string]);
  const extraTeachingEntries = Object.entries(teachingSource).filter(
    ([key]) => !TEACHING_SECTION_ORDER.includes(key),
  );
  const teachingEntries = [...orderedTeachingEntries, ...extraTeachingEntries];
  const activeEntry = teachingEntries[teachStep] ?? null;
  const activeAudio =
    teaching?.audio?.segments.find((segment) => segment.section === activeEntry?.[0]) ?? null;

  const flashcards =
    teaching?.flashcards && teaching.flashcards.length > 0
      ? teaching.flashcards
      : teachingEntries.map(([sectionName, sectionText]) => ({
          id: sectionName,
          front: `Explain ${sectionName.replaceAll("_", " ")} in plain words.`,
          back: sectionText,
          cue: "Use one short, simple sentence.",
        }));
  const activeFlashcardEntry = flashcards[activeFlashcard] ?? null;
  const teachingComplete =
    teachingEntries.length === 0 || teachingEntries.every(([sectionName]) => Boolean(visitedTeachSections[sectionName]));
  const flashcardsComplete =
    flashcards.length === 0 || flashcards.every((card) => Boolean(seenFlashcards[card.id]));
  const comprehensionPassed = comprehensionResult?.next_step === "ready_for_question";
  const quizUnlocked = teachingComplete && flashcardsComplete && comprehensionPassed;

  const activeSectionLabel = activeEntry?.[0]
    ? activeEntry[0]
        .split("_")
        .map((token) => token.charAt(0).toUpperCase() + token.slice(1))
        .join(" ")
    : "";

  useEffect(() => {
    if (!activeEntry?.[0]) {
      return;
    }
    setVisitedTeachSections((value) => ({
      ...value,
      [activeEntry[0]]: true,
    }));
  }, [activeEntry?.[0]]);

  return (
    <main className="min-h-screen bg-grid-fade px-4 py-6 md:px-8">
      <div className="mx-auto grid w-full max-w-[1050px] gap-4 lg:grid-cols-12">
        <section className="lg:col-span-12">
          <Card className="animate-rise-in border-surge/25">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <h1 className="font-display text-3xl font-bold tracking-tight text-dawn">B2Bi Learning Coach</h1>
                <CardText className="mt-1 max-w-2xl text-slate-300">
                  We teach step by step in simple words first. Then you review diagrams, flashcards, and subtitles before quiz mode unlocks.
                </CardText>
              </div>
              <div className="flex items-center gap-2">
                <Badge tone={status?.status === "completed" ? "success" : "warning"}>{status?.stage ?? "idle"}</Badge>
                <Badge tone="neutral">M4 Max Local</Badge>
                {tutor && courseTopics.length > 0 && (
                  <Badge tone="neutral">
                    Topic {Math.max(courseTopics.findIndex((topic) => topic.id === tutor.concept_id), 0) + 1}/{courseTopics.length}
                  </Badge>
                )}
                <Button variant={mode === "lesson" ? "primary" : "ghost"} onClick={() => void swapMode("lesson")}>
                  Lesson
                </Button>
                <Button variant={mode === "interview" ? "primary" : "ghost"} onClick={() => void swapMode("interview")}>
                  Interview
                </Button>
                <Button variant="ghost" onClick={() => void skipToNextTopic()} disabled={!tutor || !courseTopics.length || topicSwitching}>
                  {topicSwitching ? "Switching..." : "Next Topic"}
                </Button>
              </div>
            </div>
          </Card>
        </section>

        {!hasExistingContent && (
          <section className="lg:col-span-4">
            <Card className="h-full space-y-4 animate-rise-in">
              <CardTitle className="flex items-center gap-2">
                <UploadCloud className="h-5 w-5 text-surge" /> ZIP Intake
              </CardTitle>
              <CardText>Upload your source ZIP. After processing, the app explains concepts first and only then moves to quiz checks.</CardText>
              <label className="block cursor-pointer rounded-xl border border-dashed border-white/25 bg-ink/40 p-4 text-center text-sm text-slate-300 hover:border-surge/60">
                {busy ? "Uploading..." : "Drop ZIP or click to select"}
                <input
                  className="hidden"
                  type="file"
                  accept=".zip"
                  onChange={(event) => void onUpload(event.target.files?.[0] ?? null)}
                  disabled={busy}
                />
              </label>
              <Progress value={stageProgress} />
              <CardText className="font-mono text-xs text-slate-400">Job: {jobId || "none"}</CardText>
              {status && <CardText className="text-sm text-slate-200">{status.message}</CardText>}
              <div className="rounded-xl border border-white/10 bg-ink/50 p-3">
                <p className="text-xs uppercase tracking-wide text-slate-400">Strict Mastery Rule</p>
                <p className="mt-1 text-xs text-slate-300">3 correct answers, spaced in time, under pressure, high confidence.</p>
              </div>
              <div className="space-y-3 rounded-xl border border-white/10 bg-ink/50 p-3">
                <p className="text-xs uppercase tracking-wide text-slate-400">Voice Coach</p>
                <div>
                  <p className="mb-1 text-xs text-slate-300">Active profile</p>
                  <select
                    className="w-full rounded-lg border border-white/20 bg-ink px-2 py-2 text-sm text-slate-100"
                    value={selectedVoiceProfile}
                    onChange={(event) => setSelectedVoiceProfile(event.target.value)}
                  >
                    {["goku", ...voiceProfiles.map((profile) => profile.profile_name)]
                      .filter((value, index, values) => values.indexOf(value) === index)
                      .map((profileName) => (
                        <option key={profileName} value={profileName}>
                          {profileName}
                        </option>
                      ))}
                  </select>
                </div>
                <div>
                  <p className="mb-1 text-xs text-slate-300">Train profile from clip</p>
                  <input
                    className="mb-2 w-full rounded-lg border border-white/20 bg-ink px-2 py-2 text-sm text-slate-100"
                    value={newVoiceProfileName}
                    onChange={(event) => setNewVoiceProfileName(event.target.value)}
                    placeholder="goku"
                  />
                  <label className="block cursor-pointer rounded-lg border border-dashed border-white/25 bg-ink/40 p-3 text-center text-xs text-slate-300 hover:border-surge/60">
                    {voiceTrainingBusy ? "Training voice..." : "Upload voice clip to train"}
                    <input
                      className="hidden"
                      type="file"
                      accept="audio/*"
                      onChange={(event) => void onTrainVoiceClip(event.target.files?.[0] ?? null)}
                      disabled={voiceTrainingBusy}
                    />
                  </label>
                </div>
              </div>
              {error && (
                <div className="rounded-xl border border-red-400/40 bg-red-900/20 p-3 text-sm text-red-200">
                  <span className="inline-flex items-center gap-2 font-semibold">
                    <AlertTriangle className="h-4 w-4" /> {error}
                  </span>
                </div>
              )}
            </Card>
          </section>
        )}

        {hasExistingContent && (
          <section className="lg:col-span-4">
            <Card className="h-full space-y-4 animate-rise-in">
              <CardTitle className="flex items-center gap-2">
                <BrainCircuit className="h-5 w-5 text-surge" /> Content Ready
              </CardTitle>
              <div className="rounded-xl border border-surge/40 bg-surge/10 p-4">
                <p className="text-lg font-semibold text-dawn">{conceptCount} Concepts Loaded</p>
                <p className="mt-2 text-sm text-slate-200">Your bootcamp content is ready. We will teach first, then quiz.</p>
              </div>
              <div className="rounded-xl border border-white/10 bg-ink/50 p-3">
                <p className="text-xs uppercase tracking-wide text-slate-400">Strict Mastery Rule</p>
                <p className="mt-1 text-xs text-slate-300">3 correct answers, spaced in time, under pressure, high confidence.</p>
              </div>
              <div className="space-y-3 rounded-xl border border-white/10 bg-ink/50 p-3">
                <p className="text-xs uppercase tracking-wide text-slate-400">Voice Coach</p>
                <div>
                  <p className="mb-1 text-xs text-slate-300">Active profile</p>
                  <select
                    className="w-full rounded-lg border border-white/20 bg-ink px-2 py-2 text-sm text-slate-100"
                    value={selectedVoiceProfile}
                    onChange={(event) => setSelectedVoiceProfile(event.target.value)}
                  >
                    {["goku", ...voiceProfiles.map((profile) => profile.profile_name)]
                      .filter((value, index, values) => values.indexOf(value) === index)
                      .map((profileName) => (
                        <option key={profileName} value={profileName}>
                          {profileName}
                        </option>
                      ))}
                  </select>
                </div>
                <div>
                  <p className="mb-1 text-xs text-slate-300">Train profile from clip</p>
                  <input
                    className="mb-2 w-full rounded-lg border border-white/20 bg-ink px-2 py-2 text-sm text-slate-100"
                    value={newVoiceProfileName}
                    onChange={(event) => setNewVoiceProfileName(event.target.value)}
                    placeholder="goku"
                  />
                  <label className="block cursor-pointer rounded-lg border border-dashed border-white/25 bg-ink/40 p-3 text-center text-xs text-slate-300 hover:border-surge/60">
                    {voiceTrainingBusy ? "Training voice..." : "Upload voice clip to train"}
                    <input
                      className="hidden"
                      type="file"
                      accept="audio/*"
                      onChange={(event) => void onTrainVoiceClip(event.target.files?.[0] ?? null)}
                      disabled={voiceTrainingBusy}
                    />
                  </label>
                </div>
              </div>
              {error && (
                <div className="rounded-xl border border-red-400/40 bg-red-900/20 p-3 text-sm text-red-200">
                  <span className="inline-flex items-center gap-2 font-semibold">
                    <AlertTriangle className="h-4 w-4" /> {error}
                  </span>
                </div>
              )}
            </Card>
          </section>
        )}

        <section className={hasExistingContent ? "lg:col-span-8" : "lg:col-span-8"}>
          <Card className="h-full animate-rise-in space-y-3">
            <CardTitle className="flex items-center gap-2">
              <BrainCircuit className="h-5 w-5 text-surge" /> Tutor Core Loop
            </CardTitle>
            {!tutor ? (
              <CardText>{hasExistingContent ? "Loading lesson..." : "Complete ingestion to unlock active tutoring."}</CardText>
            ) : (
              <>
                <div className="space-y-3 rounded-xl border border-surge/40 bg-surge/10 p-4">
                  <div className="mb-2 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-surge" />
                      <p className="text-xs uppercase tracking-wide text-slate-300">Interactive Coach</p>
                    </div>
                    <Badge tone={mode === "interview" ? "warning" : "neutral"}>{mode}</Badge>
                  </div>

                  <h2 className="text-2xl font-bold text-dawn">{tutor.lesson_preview.name}</h2>

                  {teachLoading && <CardText>Preparing your teaching flow...</CardText>}

                  {!teachLoading && activeEntry && (
                    <div className="space-y-3">
                      <div className="grid gap-2 rounded-lg border border-white/10 bg-ink/40 p-3 sm:grid-cols-3">
                        <div className="rounded-md border border-white/10 p-2 text-xs text-slate-300">
                          <p className="inline-flex items-center gap-2 font-semibold uppercase tracking-wide">
                            <CheckCircle2 className={`h-3.5 w-3.5 ${teachingComplete ? "text-moss" : "text-slate-500"}`} />
                            Teach Flow
                          </p>
                          <p className="mt-1">{teachingComplete ? "Completed" : "View each teaching section"}</p>
                        </div>
                        <div className="rounded-md border border-white/10 p-2 text-xs text-slate-300">
                          <p className="inline-flex items-center gap-2 font-semibold uppercase tracking-wide">
                            <BookOpenCheck className={`h-3.5 w-3.5 ${flashcardsComplete ? "text-moss" : "text-slate-500"}`} />
                            Flashcards
                          </p>
                          <p className="mt-1">{flashcardsComplete ? "Reviewed" : "Reveal every card"}</p>
                        </div>
                        <div className="rounded-md border border-white/10 p-2 text-xs text-slate-300">
                          <p className="inline-flex items-center gap-2 font-semibold uppercase tracking-wide">
                            <ListChecks className={`h-3.5 w-3.5 ${comprehensionPassed ? "text-moss" : "text-slate-500"}`} />
                            Understanding
                          </p>
                          <p className="mt-1">{comprehensionPassed ? "Validated" : "Complete comprehension check"}</p>
                        </div>
                      </div>
                      <div className="flex gap-1">
                        {teachingEntries.map(([sectionName], index) => (
                          <div
                            key={sectionName}
                            className={`h-1.5 flex-1 rounded-full ${index <= teachStep ? "bg-surge" : "bg-white/15"}`}
                          />
                        ))}
                      </div>
                      <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                        <p className="text-xs font-semibold uppercase tracking-wide text-amber-300">{activeSectionLabel}</p>
                        <p className="mt-1 text-sm text-slate-200">{activeEntry[1]}</p>
                      </div>
                      {activeAudio?.audio_url && (
                        <div className="rounded-lg border border-white/10 bg-ink/40 p-3 space-y-2">
                          <p className="mb-2 inline-flex items-center gap-2 text-xs uppercase tracking-wide text-slate-300">
                            <Volume2 className="h-4 w-4" /> coach audio ({selectedVoiceProfile})
                          </p>
                          <audio controls className="w-full" src={resolveApiUrl(activeAudio.audio_url)} preload="none" />
                          <div className="rounded-md border border-white/10 bg-black/20 p-2">
                            <p className="text-[11px] uppercase tracking-wide text-slate-400">Subtitles (current section)</p>
                            <p className="mt-1 text-sm text-slate-100">{activeAudio.text}</p>
                          </div>
                        </div>
                      )}
                      {!activeAudio?.audio_url && (
                        <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                          <p className="inline-flex items-center gap-2 text-xs uppercase tracking-wide text-slate-300">
                            <Volume2 className="h-4 w-4" /> Coach voice
                          </p>
                          <p className="mt-2 text-xs text-slate-300">
                            Subtitles and flashcards are ready now. Audio is generated automatically at lesson start.
                          </p>
                          {audioLoading && <p className="mt-2 text-xs text-cyan-200">Generating coach audio...</p>}
                          {audioNotice && <p className="mt-2 text-xs text-amber-200">{audioNotice}</p>}
                        </div>
                      )}
                      <div className="flex items-center justify-between">
                        <Button
                          variant="ghost"
                          onClick={() => setTeachStep((value) => Math.max(value - 1, 0))}
                          disabled={teachStep === 0}
                        >
                          <ChevronLeft className="mr-1 h-4 w-4" /> Previous
                        </Button>
                        <Button
                          variant="ghost"
                          onClick={() => setTeachStep((value) => Math.min(value + 1, teachingEntries.length - 1))}
                          disabled={teachStep >= teachingEntries.length - 1}
                        >
                          Next <ChevronRight className="ml-1 h-4 w-4" />
                        </Button>
                      </div>
                      <DiagramViewer diagrams={teaching?.diagrams ?? []} />
                      <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                        <p className="text-xs font-semibold uppercase tracking-wide text-amber-300">Concept Flow Diagram</p>
                        <div className="mt-2 grid gap-2 md:grid-cols-2">
                          <div className="rounded border border-white/10 bg-black/20 p-2 text-xs text-slate-200">
                            <p className="font-semibold text-slate-100">Why It Matters</p>
                            <p className="mt-1">{tutor.lesson_preview.why_it_matters}</p>
                          </div>
                          <div className="rounded border border-white/10 bg-black/20 p-2 text-xs text-slate-200">
                            <p className="font-semibold text-slate-100">Core Idea</p>
                            <p className="mt-1">{tutor.lesson_preview.intuition}</p>
                          </div>
                          <div className="rounded border border-white/10 bg-black/20 p-2 text-xs text-slate-200">
                            <p className="font-semibold text-slate-100">Real Example</p>
                            <p className="mt-1">{tutor.lesson_preview.example || "Use one live business scenario from your project."}</p>
                          </div>
                          <div className="rounded border border-white/10 bg-black/20 p-2 text-xs text-slate-200">
                            <p className="font-semibold text-slate-100">Pitfall To Avoid</p>
                            <p className="mt-1">{tutor.lesson_preview.common_mistake || "Do not mix this concept with similar protocols."}</p>
                          </div>
                        </div>
                      </div>

                      {teaching?.audio?.segments?.length ? (
                        <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                          <p className="text-xs font-semibold uppercase tracking-wide text-amber-300">Subtitle Transcript</p>
                          <div className="mt-2 max-h-40 space-y-2 overflow-y-auto pr-1">
                            {teaching.audio.segments.map((segment) => (
                              <div
                                key={segment.section}
                                className={`rounded border p-2 text-xs ${
                                  segment.section === activeEntry[0]
                                    ? "border-surge/60 bg-surge/10 text-slate-100"
                                    : "border-white/10 bg-ink/50 text-slate-300"
                                }`}
                              >
                                <p className="font-semibold uppercase tracking-wide">{segment.section.replaceAll("_", " ")}</p>
                                <p className="mt-1 text-[12px] leading-5">{segment.text}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      ) : null}

                      {activeFlashcardEntry && (
                        <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                          <div className="mb-2 flex items-center justify-between">
                            <p className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-cyan-300">
                              <BookOpenCheck className="h-4 w-4" /> Flashcard Drill
                            </p>
                            <p className="text-xs text-slate-300">
                              {Object.keys(seenFlashcards).length}/{flashcards.length} reviewed
                            </p>
                          </div>
                          <div className="rounded-md border border-white/10 bg-black/20 p-3">
                            <p className="text-xs uppercase tracking-wide text-slate-400">Prompt</p>
                            <p className="mt-1 text-sm text-slate-100">{activeFlashcardEntry.front}</p>
                            <p className="mt-2 text-[11px] text-amber-300">Cue: {activeFlashcardEntry.cue}</p>
                            {flashcardRevealed && (
                              <>
                                <p className="mt-3 text-xs uppercase tracking-wide text-slate-400">Answer</p>
                                <p className="mt-1 text-sm text-slate-200">{activeFlashcardEntry.back}</p>
                              </>
                            )}
                          </div>
                          <div className="mt-3 flex items-center justify-between gap-2">
                            <Button
                              variant="ghost"
                              onClick={() => {
                                setActiveFlashcard((value) => Math.max(value - 1, 0));
                                setFlashcardRevealed(false);
                              }}
                              disabled={activeFlashcard === 0}
                            >
                              <ChevronLeft className="mr-1 h-4 w-4" /> Prev Card
                            </Button>
                            {!flashcardRevealed ? (
                              <Button
                                onClick={() => {
                                  setFlashcardRevealed(true);
                                  setSeenFlashcards((value) => ({
                                    ...value,
                                    [activeFlashcardEntry.id]: true,
                                  }));
                                }}
                              >
                                Reveal Answer
                              </Button>
                            ) : (
                              <Button
                                onClick={() => {
                                  setActiveFlashcard((value) => Math.min(value + 1, flashcards.length - 1));
                                  setFlashcardRevealed(false);
                                }}
                                disabled={activeFlashcard >= flashcards.length - 1}
                              >
                                Next Card <ChevronRight className="ml-1 h-4 w-4" />
                              </Button>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {!teachLoading && !teaching && <CardText>Preparing teaching sections...</CardText>}

                  {!teaching && <div className="space-y-3">
                    <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                      <p className="text-xs font-semibold uppercase tracking-wide text-amber-400">Why It Matters</p>
                      <p className="mt-1 text-sm text-slate-200">{tutor.lesson_preview.why_it_matters}</p>
                    </div>
                    <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                      <p className="text-xs font-semibold uppercase tracking-wide text-cyan-400">Intuition</p>
                      <p className="mt-1 text-sm text-slate-200">{tutor.lesson_preview.intuition}</p>
                    </div>
                    {tutor.lesson_preview.explanation && (
                      <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                        <p className="text-xs font-semibold uppercase tracking-wide text-green-400">Simple Explanation</p>
                        <p className="mt-1 text-sm text-slate-200">{tutor.lesson_preview.explanation}</p>
                      </div>
                    )}
                    {tutor.lesson_preview.example && (
                      <div className="rounded-lg border border-white/10 bg-ink/40 p-3">
                        <p className="text-xs font-semibold uppercase tracking-wide text-orange-300">Example</p>
                        <p className="mt-1 text-sm text-slate-200">{tutor.lesson_preview.example}</p>
                      </div>
                    )}
                    {tutor.lesson_preview.common_mistake && (
                      <div className="rounded-lg border border-red-400/40 bg-red-900/20 p-3">
                        <p className="text-xs font-semibold uppercase tracking-wide text-red-300">Common Mistake</p>
                        <p className="mt-1 text-sm text-red-100">{tutor.lesson_preview.common_mistake}</p>
                      </div>
                    )}
                    <p className="text-xs text-slate-400">Source: {tutor.lesson_preview.source_reference}</p>
                  </div>}
                </div>

                {!readyToAnswer && (
                  <div className="space-y-3 rounded-xl border border-moss/40 bg-moss/10 p-4">
                    <p className="text-sm text-slate-100">Before the checkpoint, prove you understand this in plain words.</p>
                    <Textarea
                      placeholder="1) Explain this concept in your own words like you're teaching a friend."
                      rows={3}
                      value={comprehensionDraft.summary}
                      onChange={(event) =>
                        setComprehensionDraft((value) => ({
                          ...value,
                          summary: event.target.value,
                        }))
                      }
                    />
                    <Textarea
                      placeholder="2) Give one real-world situation where this is used."
                      rows={3}
                      value={comprehensionDraft.example}
                      onChange={(event) =>
                        setComprehensionDraft((value) => ({
                          ...value,
                          example: event.target.value,
                        }))
                      }
                    />
                    <Textarea
                      placeholder="3) What usually goes wrong when people misunderstand this?"
                      rows={3}
                      value={comprehensionDraft.failure}
                      onChange={(event) =>
                        setComprehensionDraft((value) => ({
                          ...value,
                          failure: event.target.value,
                        }))
                      }
                    />
                    <Button onClick={() => void evaluateComprehension()} disabled={checkingComprehension}>
                      {checkingComprehension ? "Checking understanding..." : "Check My Understanding"}
                    </Button>

                    {comprehensionResult && (
                      <div
                        className={`rounded-lg border p-3 text-sm ${
                          comprehensionResult.understood
                            ? "border-moss/40 bg-moss/10 text-green-100"
                            : "border-ember/40 bg-ember/10 text-orange-100"
                        }`}
                      >
                        <p className="font-semibold">
                          Understanding score: {comprehensionResult.score}%
                          {comprehensionResult.understood ? " (ready)" : " (needs one more pass)"}
                        </p>
                        <p className="mt-1">{comprehensionResult.feedback}</p>
                        {comprehensionResult.understood && (
                          <div className="mt-3 space-y-2">
                            {!quizUnlocked && (
                              <p className="text-xs text-slate-200">
                                Finish all teaching sections and flashcards to unlock quiz mode.
                              </p>
                            )}
                            <div className="flex flex-wrap items-center gap-2">
                              <Button
                                onClick={() => {
                                  setReadyToAnswer(true);
                                  answerStart.current = Date.now();
                                }}
                                disabled={!quizUnlocked}
                              >
                                Start Checkpoint Question
                              </Button>
                              <Button
                                variant="ghost"
                                onClick={() => void loadNextQuizQuestion()}
                                disabled={!quizUnlocked || quizLoading}
                              >
                                {quizLoading ? "Loading quiz..." : "Go To Quiz"}
                              </Button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Question Section - Only show after ready */}
                {readyToAnswer && (
                  <>
                    <div className="rounded-xl border border-ember/40 bg-ember/10 p-3 animate-pulseedge">
                      <p className="text-sm font-semibold text-dawn">Checkpoint Question</p>
                      <p className="mt-1 text-sm text-slate-200">{tutor.question}</p>
                      <p className="mt-2 inline-flex items-center gap-2 text-xs text-slate-100">
                        <Timer className="h-4 w-4" /> pressure window: {remainingPressureSec}s
                      </p>
                    </div>
                    <Textarea
                      placeholder="Type your answer in simple, clear words."
                      value={answer}
                      onChange={(event) => setAnswer(event.target.value)}
                      rows={5}
                    />
                    <div className="rounded-xl border border-white/10 bg-ink/50 p-3">
                      <div className="flex items-center justify-between">
                        <p className="text-xs uppercase tracking-wide text-slate-400">Confidence (mandatory)</p>
                        <p className="text-sm font-semibold text-dawn">{confidence}%</p>
                      </div>
                      <input
                        className="mt-2 h-2 w-full cursor-pointer accent-amber-500"
                        type="range"
                        min={0}
                        max={100}
                        value={confidence}
                        onChange={(event) => setConfidence(Number(event.target.value))}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Button onClick={() => void submitAnswer()}>Submit Answer</Button>
                      <div className="inline-flex items-center gap-2 text-xs text-slate-300">
                        <Gauge className="h-4 w-4" /> confidence-accuracy mismatch detection active
                      </div>
                    </div>
                  </>
                )}

                {pendingResult && !answerResult && (
                  <div className="rounded-xl border border-surge/40 bg-surge/10 p-3 text-sm text-cyan-100">
                    Delayed feedback gate active... revealing in {(revealCountdownMs / 1000).toFixed(1)}s
                  </div>
                )}

                {answerResult && (
                  <div
                    className={`rounded-xl border p-3 text-sm ${
                      answerResult.correctness
                        ? "border-moss/40 bg-moss/10 text-green-200"
                        : "border-ember/40 bg-ember/10 text-orange-200"
                    }`}
                  >
                    <p className="font-semibold">{answerResult.correctness ? "Correct, escalate." : "Incorrect, rebuild."}</p>
                    <p className="mt-1">Grounded answer: {answerResult.answer}</p>
                    <p className="mt-1">{answerResult.explanation}</p>
                    <p className="mt-2 text-xs uppercase tracking-wide">Misconception: {answerResult.misconception_tag}</p>
                    <p className="mt-1 text-xs uppercase tracking-wide">Model confidence: {answerResult.confidence}</p>
                    <p className="mt-1 text-xs uppercase tracking-wide">Uncertainty: {answerResult.uncertainty}</p>
                    <p className="mt-2 text-xs text-slate-100">Grounded source chunks:</p>
                    <div className="mt-1 space-y-1">
                      {answerResult.source_chunks.slice(0, 4).map((chunk) => (
                        <p key={chunk} className="rounded border border-white/10 bg-ink/40 p-2 text-xs text-slate-200">
                          {chunk}
                        </p>
                      ))}
                    </div>
                    <p className="mt-2 text-xs uppercase tracking-wide">Next: {answerResult.next_question}</p>
                  </div>
                )}

                {quizUnlocked && (
                  <div className="rounded-xl border border-cyan-400/40 bg-cyan-900/10 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="inline-flex items-center gap-2 text-sm font-semibold text-cyan-100">
                        <ListChecks className="h-4 w-4" /> Quiz Mode (unlocked after teaching)
                      </p>
                      <p className="text-xs text-cyan-100">
                        Score: {quizScore.correct}/{quizScore.total}
                      </p>
                    </div>

                    {!quizQuestion ? (
                      <div className="mt-3">
                        <Button onClick={() => void loadNextQuizQuestion()} disabled={quizLoading}>
                          {quizLoading ? "Loading quiz..." : "Start Quiz"}
                        </Button>
                      </div>
                    ) : (
                      <div className="mt-3 space-y-3">
                        <p className="text-sm text-slate-100">{quizQuestion.question}</p>
                        <div className="grid gap-2">
                          {quizQuestion.options.map((option) => (
                            <button
                              key={option}
                              type="button"
                              onClick={() => setQuizChoice(option)}
                              className={`rounded-lg border px-3 py-2 text-left text-sm transition ${
                                quizChoice === option
                                  ? "border-cyan-400 bg-cyan-700/30 text-white"
                                  : "border-white/15 bg-ink/50 text-slate-200 hover:border-cyan-300/70"
                              }`}
                            >
                              {option}
                            </button>
                          ))}
                        </div>
                        <div className="flex flex-wrap items-center gap-2">
                          <Button onClick={submitQuizAnswer} disabled={!quizChoice}>
                            Check Quiz Answer
                          </Button>
                          <Button variant="ghost" onClick={() => void loadNextQuizQuestion()} disabled={quizLoading}>
                            Next Quiz Question
                          </Button>
                        </div>
                        {quizFeedback && (
                          <div
                            className={`rounded-lg border p-3 text-sm ${
                              quizFeedback.correct
                                ? "border-moss/40 bg-moss/10 text-green-100"
                                : "border-ember/40 bg-ember/10 text-orange-100"
                            }`}
                          >
                            <p>{quizFeedback.message}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </Card>
        </section>

        <section className="lg:col-span-12">
          <Card className="animate-rise-in">
            <CardTitle>Weak Area Tracker</CardTitle>
            <div className="mt-3 grid gap-2 md:grid-cols-2 lg:grid-cols-3">
              {weak.length === 0 && <CardText>No weak areas yet.</CardText>}
              {weak.map((item) => (
                <div key={item.concept_id} className="rounded-xl border border-white/10 bg-ink/50 p-3">
                  <p className="text-sm font-semibold text-dawn">{item.concept_name}</p>
                  <p className="mt-1 text-xs text-slate-300">Accuracy: {(item.accuracy * 100).toFixed(1)}%</p>
                  <p className="text-xs text-slate-300">Retries: {item.retries}</p>
                  <p className="text-xs text-slate-300">Response: {item.response_time_ms.toFixed(0)}ms</p>
                  <p className="text-xs text-slate-300">Pressure failures: {item.pressure_failures}</p>
                  <Badge tone={item.mastered ? "success" : "warning"} className="mt-2">
                    {item.mastered ? "Mastered" : "Not mastered"}
                  </Badge>
                </div>
              ))}
            </div>
          </Card>
        </section>
      </div>
    </main>
  );
}
