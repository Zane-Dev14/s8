import {
  CourseMapNode,
  ComprehensionCheck,
  InteractiveTeach,
  JobStatus,
  QuizQuestion,
  TutorAnswer,
  TutorStart,
  VoiceProfile,
  WeakArea,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export function resolveApiUrl(pathOrUrl: string): string {
  if (!pathOrUrl) {
    return "";
  }
  if (pathOrUrl.startsWith("http://") || pathOrUrl.startsWith("https://")) {
    return pathOrUrl;
  }
  return `${API_BASE}${pathOrUrl}`;
}

export async function uploadZip(file: File): Promise<{ job_id: string; status: string; stage: string }> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE}/api/ingest/upload`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error("Upload failed");
  }
  return response.json();
}

export async function getJobStatus(jobId: string): Promise<JobStatus> {
  const response = await fetch(`${API_BASE}/api/ingest/${jobId}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Unable to fetch job status");
  }
  return response.json();
}

export async function getTimeline(jobId: string): Promise<Record<string, Array<Record<string, unknown>>>> {
  const response = await fetch(`${API_BASE}/api/timeline/${jobId}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Unable to fetch timeline");
  }
  return response.json();
}

export async function startTutor(
  userId: string,
  mode: "lesson" | "interview" = "lesson",
  conceptId?: string,
): Promise<TutorStart> {
  const conceptParam = conceptId ? `&concept_id=${encodeURIComponent(conceptId)}` : "";
  const response = await fetch(
    `${API_BASE}/api/tutor/start?user_id=${encodeURIComponent(userId)}&mode=${encodeURIComponent(mode)}${conceptParam}`,
    {
    cache: "no-store",
    },
  );
  if (!response.ok) {
    throw new Error("No lesson available");
  }
  return response.json();
}

export async function getCourseMapNodes(): Promise<CourseMapNode[]> {
  const response = await fetch(`${API_BASE}/api/course-map`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Unable to load course map");
  }
  const data = await response.json();
  return (data.nodes ?? []) as CourseMapNode[];
}

export async function submitTutorAnswer(payload: {
  user_id: string;
  concept_id: string;
  question: string;
  user_answer: string;
  user_confidence: number;
  response_time_ms: number;
  mode: "lesson" | "interview";
}): Promise<TutorAnswer> {
  const response = await fetch(`${API_BASE}/api/tutor/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error("Answer evaluation failed");
  }
  return response.json();
}

export async function nextQuizQuestion(): Promise<QuizQuestion> {
  const response = await fetch(`${API_BASE}/api/quiz/next`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("No quiz question available");
  }
  return response.json();
}

export async function weakAreas(userId: string): Promise<WeakArea[]> {
  const response = await fetch(`${API_BASE}/api/analytics/weak-areas?user_id=${encodeURIComponent(userId)}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Unable to fetch weak areas");
  }
  const body = await response.json();
  return body.weak_areas as WeakArea[];
}

export async function checkContentAvailable(): Promise<{ has_content: boolean; concept_count: number }> {
  const response = await fetch(`${API_BASE}/api/course-map`, { cache: "no-store" });
  if (!response.ok) {
    return { has_content: false, concept_count: 0 };
  }
  const data = await response.json();
  const conceptCount = data.nodes?.length ?? 0;
  return { has_content: conceptCount > 0, concept_count: conceptCount };
}

export async function getInteractiveTeaching(
  conceptId: string,
  userId: string,
  voiceProfile?: string,
  generateAudio = false,
): Promise<InteractiveTeach> {
  const profileParam = voiceProfile ? `&voice_profile=${encodeURIComponent(voiceProfile)}` : "";
  const audioParam = `&generate_audio=${generateAudio ? "true" : "false"}`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), generateAudio ? 45000 : 22000);
  const response = await fetch(
    `${API_BASE}/api/tutor/interactive-teach?concept_id=${encodeURIComponent(conceptId)}&user_id=${encodeURIComponent(userId)}${profileParam}${audioParam}`,
    { cache: "no-store", signal: controller.signal },
  );
  clearTimeout(timeout);
  if (!response.ok) {
    throw new Error("Unable to load interactive teaching session");
  }
  return response.json();
}

export async function checkComprehension(payload: {
  user_id: string;
  concept_id: string;
  summary_in_own_words: string;
  real_world_example: string;
  failure_mode: string;
}): Promise<ComprehensionCheck> {
  const response = await fetch(`${API_BASE}/api/tutor/comprehension-check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error("Unable to evaluate understanding");
  }
  return response.json();
}

export async function listVoiceProfiles(): Promise<VoiceProfile[]> {
  const response = await fetch(`${API_BASE}/api/voice/profiles`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Unable to list voice profiles");
  }
  return response.json();
}

export async function trainVoiceProfile(profileName: string, clip: File): Promise<VoiceProfile> {
  const form = new FormData();
  form.append("profile_name", profileName);
  form.append("clip", clip);

  const response = await fetch(`${API_BASE}/api/voice/train-profile`, {
    method: "POST",
    body: form,
  });
  if (!response.ok) {
    throw new Error("Unable to train voice profile");
  }
  return response.json();
}
