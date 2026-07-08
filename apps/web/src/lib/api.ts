import { Word, WordListQuery, PaginatedResponse } from "@/types/word";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000/api";

async function fetchApi<T>(
  path: string,
  options?: RequestInit & { params?: Record<string, unknown> }
): Promise<T> {
  let url = `${API_BASE}${path}`;

  if (options?.params) {
    const searchParams = new URLSearchParams();
    for (const [key, value] of Object.entries(options.params)) {
      if (value !== undefined && value !== "") {
        searchParams.set(key, String(value));
      }
    }
    const query = searchParams.toString();
    if (query) {
      url += `?${query}`;
    }
  }

  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error?.message || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function listWords(params: WordListQuery = {}): Promise<PaginatedResponse<Word>> {
  return fetchApi<PaginatedResponse<Word>>("/words", { params });
}

export async function getWord(id: number): Promise<{ data: Word }> {
  return fetchApi<{ data: Word }>(`/words/${id}`);
}

export async function createWord(
  data: unknown,
  token: string
): Promise<{ data: Word }> {
  return fetchApi<{ data: Word }>("/words", {
    method: "POST",
    body: JSON.stringify(data),
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function updateWord(
  id: number,
  data: unknown,
  token: string
): Promise<{ data: Word }> {
  return fetchApi<{ data: Word }>(`/words/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function deleteWord(id: number, token: string): Promise<void> {
  await fetchApi<void>(`/words/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function loginAdmin(data: { email: string; password: string }): Promise<{
  data: { token: string; admin: { id: number; email: string } };
}> {
  return fetchApi<{ data: { token: string; admin: { id: number; email: string } } }>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
