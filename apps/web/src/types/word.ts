export interface ExampleSentence {
  id: number;
  english: string;
  chinese: string;
  order: number;
  wordId: number;
}

export interface Word {
  id: number;
  word: string;
  phonetic: string;
  meaning: string;
  partOfSpeech: string | null;
  difficulty: string | null;
  tags: string | null;
  audioUrl: string | null;
  exampleSentences: ExampleSentence[];
  createdAt: string;
  updatedAt: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface WordListQuery {
  [key: string]: string | number | undefined;
  page?: number;
  limit?: number;
  q?: string;
  difficulty?: string;
  partOfSpeech?: string;
  tag?: string;
}

export const PARTS_OF_SPEECH = [
  { value: "noun", label: "Noun" },
  { value: "verb", label: "Verb" },
  { value: "adjective", label: "Adjective" },
  { value: "adverb", label: "Adverb" },
  { value: "pronoun", label: "Pronoun" },
  { value: "preposition", label: "Preposition" },
  { value: "conjunction", label: "Conjunction" },
  { value: "interjection", label: "Interjection" },
  { value: "phrase", label: "Phrase" },
] as const;

export const DIFFICULTY_LEVELS = [
  { value: "A1", label: "A1" },
  { value: "A2", label: "A2" },
  { value: "B1", label: "B1" },
  { value: "B2", label: "B2" },
  { value: "C1", label: "C1" },
  { value: "C2", label: "C2" },
  { value: "IELTS", label: "IELTS" },
] as const;

export type PartOfSpeech = (typeof PARTS_OF_SPEECH)[number]["value"];
export type DifficultyLevel = (typeof DIFFICULTY_LEVELS)[number]["value"];
