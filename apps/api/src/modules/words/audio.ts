import * as fs from 'fs';
import * as path from 'path';
import { prisma } from '@/lib/prisma';
import { AppError } from '@/middleware/errorHandler';

const AUDIO_DIR = path.resolve(__dirname, '../../../../public/audio');
const YOUDAO_AUDIO_URL = 'https://dict.youdao.com/dictvoice';

function slugifyWord(word: string): string {
  return word
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function ensureAudioDir(): void {
  if (!fs.existsSync(AUDIO_DIR)) {
    fs.mkdirSync(AUDIO_DIR, { recursive: true });
  }
}

export function getAudioFilePath(word: string): string {
  const slug = slugifyWord(word);
  return path.join(AUDIO_DIR, `${slug}.mp3`);
}

export function getAudioUrl(word: string): string {
  const slug = slugifyWord(word);
  return `/audio/${slug}.mp3`;
}

async function fetchAudioFromYoudao(word: string): Promise<Buffer> {
  const url = `${YOUDAO_AUDIO_URL}?audio=${encodeURIComponent(word)}&type=1`;

  const response = await fetch(url, {
    headers: {
      Accept: '*/*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
      Referer: 'http://hefengxian.com/',
    },
  });

  if (!response.ok) {
    throw new AppError(
      502,
      `Failed to fetch audio from Youdao: ${response.status}`,
      'EXTERNAL_SERVICE_ERROR'
    );
  }

  const arrayBuffer = await response.arrayBuffer();
  return Buffer.from(arrayBuffer);
}

export async function getOrFetchAudio(wordId: number): Promise<{
  filePath: string;
  audioUrl: string;
}> {
  const word = await prisma.word.findUnique({
    where: { id: wordId },
  });

  if (!word) {
    throw new AppError(404, 'Word not found', 'NOT_FOUND');
  }

  ensureAudioDir();

  const filePath = getAudioFilePath(word.word);
  const audioUrl = getAudioUrl(word.word);

  if (!fs.existsSync(filePath)) {
    const audioBuffer = await fetchAudioFromYoudao(word.word);
    fs.writeFileSync(filePath, audioBuffer);
  }

  if (word.audioUrl !== audioUrl) {
    await prisma.word.update({
      where: { id: wordId },
      data: { audioUrl },
    });
  }

  return { filePath, audioUrl };
}
