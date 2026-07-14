import { z } from 'zod';

export const PARTS_OF_SPEECH = [
  'noun',
  'verb',
  'adjective',
  'adverb',
  'pronoun',
  'preposition',
  'conjunction',
  'interjection',
  'phrase',
] as const;

export const DIFFICULTY_LEVELS = [
  'A1',
  'A2',
  'B1',
  'B2',
  'C1',
  'C2',
  'IELTS',
] as const;

const SentenceSchema = z.object({
  english: z.string().min(1).max(500),
  chinese: z.string().min(1).max(500),
});

export const CreateWordSchema = z.object({
  word: z.string().min(1).max(100),
  phonetic: z.string().min(1).max(200),
  meaning: z.string().min(1).max(1000),
  partOfSpeech: z.enum(PARTS_OF_SPEECH).optional(),
  difficulty: z.enum(DIFFICULTY_LEVELS).optional(),
  tags: z.string().max(200).optional(),
  audioUrl: z.union([z.string().url().max(500), z.literal('')]).optional(),
  exampleSentences: z.array(SentenceSchema).min(1).max(20),
});

export const UpdateWordSchema = CreateWordSchema.partial().extend({
  exampleSentences: z.array(SentenceSchema).min(1).max(20).optional(),
});

export const ListWordsQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(12),
  q: z.string().max(100).optional(),
  difficulty: z.enum(DIFFICULTY_LEVELS).optional(),
  partOfSpeech: z.enum(PARTS_OF_SPEECH).optional(),
  tag: z.string().max(50).optional(),
});

export type CreateWordInput = z.infer<typeof CreateWordSchema>;
export type UpdateWordInput = z.infer<typeof UpdateWordSchema>;
export type ListWordsQuery = z.infer<typeof ListWordsQuerySchema>;
