import { Prisma } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { CreateWordInput, UpdateWordInput, ListWordsQuery } from '@/modules/words/word.schema';

const wordInclude = {
  exampleSentences: {
    orderBy: { order: 'asc' as const },
  },
};

export async function createWord(data: CreateWordInput) {
  const { exampleSentences, ...wordData } = data;
  return prisma.word.create({
    data: {
      ...wordData,
      audioUrl: wordData.audioUrl || null,
      exampleSentences: {
        create: exampleSentences.map((s, index) => ({
          english: s.english,
          chinese: s.chinese,
          order: index,
        })),
      },
    },
    include: wordInclude,
  });
}

export async function findWordById(id: number) {
  return prisma.word.findUnique({
    where: { id },
    include: wordInclude,
  });
}

export async function updateWord(id: number, data: UpdateWordInput) {
  const { exampleSentences, ...wordData } = data;

  return prisma.$transaction(async (tx) => {
    if (exampleSentences) {
      await tx.exampleSentence.deleteMany({
        where: { wordId: id },
      });
    }

    return tx.word.update({
      where: { id },
      data: {
        ...wordData,
        audioUrl: wordData.audioUrl === '' ? null : wordData.audioUrl,
        exampleSentences: exampleSentences
          ? {
              create: exampleSentences.map((s, index) => ({
                english: s.english,
                chinese: s.chinese,
                order: index,
              })),
            }
          : undefined,
      },
      include: wordInclude,
    });
  });
}

export async function deleteWord(id: number) {
  return prisma.word.delete({
    where: { id },
  });
}

export async function listWords(query: ListWordsQuery) {
  const { page, limit, q, difficulty, partOfSpeech, tag } = query;
  const skip = (page - 1) * limit;

  const where: Prisma.WordWhereInput = {};

  if (q) {
    where.OR = [
      { word: { startsWith: q } },
      { meaning: { contains: q } },
    ];
  }

  if (difficulty) {
    where.difficulty = difficulty;
  }

  if (partOfSpeech) {
    where.partOfSpeech = partOfSpeech;
  }

  if (tag) {
    where.tags = { contains: tag };
  }

  const [data, total] = await Promise.all([
    prisma.word.findMany({
      where,
      skip,
      take: limit,
      orderBy: { createdAt: 'desc' },
      include: wordInclude,
    }),
    prisma.word.count({ where }),
  ]);

  return {
    data,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  };
}
