import { getIdToken } from "./firebase";
import type { Badge, ChatApiResponse, ScoreInfo, UserProfile } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchApi<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await getIdToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function registerUser(): Promise<UserProfile> {
  return fetchApi<UserProfile>("/api/auth/register", { method: "POST" });
}

export async function getMe(): Promise<UserProfile> {
  return fetchApi<UserProfile>("/api/auth/me");
}

export async function sendChatMessage(message: string): Promise<ChatApiResponse> {
  return fetchApi<ChatApiResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

export async function getScore(): Promise<ScoreInfo> {
  return fetchApi<ScoreInfo>("/api/score");
}

export async function getBadges(): Promise<Badge[]> {
  return fetchApi<Badge[]>("/api/badges");
}
