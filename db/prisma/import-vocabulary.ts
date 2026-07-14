import * as fs from 'fs';
import * as readline from 'readline';
import { prisma } from '../src';

const DEFAULT_VOCABULARY_PATH = './prisma/vocabulary.txt';
const BATCH_SIZE = 100;

interface ParsedEntry {
  word: string;
  partOfSpeech: string;
  meaning: string;
  example: string | null;
  category: string;
}

function parseEntryLine(line: string, category: string): ParsedEntry | null {
  const parts = line.split('|').map((part) => part.trim());

  if (parts.length < 3) {
    console.warn(`Skipping malformed line (expected at least 3 fields): ${line}`);
    return null;
  }

  const [word, partOfSpeech, meaning, example, notes] = parts;

  if (!word || !meaning) {
    console.warn(`Skipping line with empty word or meaning: ${line}`);
    return null;
  }

  let finalMeaning = meaning;

  if (notes) {
    finalMeaning = `${meaning}\n\n补充：${notes}`;
  }

  return {
    word,
    partOfSpeech,
    meaning: finalMeaning,
    example: example || null,
    category,
  };
}

async function parseVocabularyFile(filePath: string): Promise<ParsedEntry[]> {
  const fileStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  const entries: ParsedEntry[] = [];
  const seenWords = new Set<string>();
  let currentCategory = '';
  let lineNumber = 0;

  for await (const rawLine of rl) {
    lineNumber += 1;
    const line = rawLine.trim();

    if (!line) continue;

    if (line === '===') {
      currentCategory = '';
      continue;
    }

    if (line === '+++' || line === '---') {
      continue;
    }

    if (line.includes('|')) {
      const entry = parseEntryLine(line, currentCategory);
      if (entry) {
        if (seenWords.has(entry.word)) {
          console.warn(
            `Duplicate word skipped at line ${lineNumber}: ${entry.word}`
          );
          continue;
        }
        seenWords.add(entry.word);
        entries.push(entry);
      }
      continue;
    }

    // Treat any other non-empty line as a category title
    currentCategory = line;
  }

  return entries;
}

async function importBatch(batch: ParsedEntry[]) {
  await prisma.$transaction(async (tx) => {
    for (const entry of batch) {
      const word = await tx.word.upsert({
        where: { word: entry.word },
        update: {
          partOfSpeech: entry.partOfSpeech,
          meaning: entry.meaning,
          tags: `category:${entry.category}`,
        },
        create: {
          word: entry.word,
          phonetic: null,
          meaning: entry.meaning,
          partOfSpeech: entry.partOfSpeech,
          difficulty: null,
          tags: `category:${entry.category}`,
          audioUrl: null,
        },
      });

      await tx.exampleSentence.deleteMany({
        where: { wordId: word.id },
      });

      if (entry.example) {
        await tx.exampleSentence.create({
          data: {
            english: entry.example,
            chinese: '',
            order: 0,
            wordId: word.id,
          },
        });
      }
    }
  });
}

async function main() {
  const filePath = process.env.VOCABULARY_FILE || DEFAULT_VOCABULARY_PATH;

  if (!fs.existsSync(filePath)) {
    console.error(`Vocabulary file not found: ${filePath}`);
    console.error(
      'Set VOCABULARY_FILE to a readable path, or move the file to the default location.'
    );
    process.exit(1);
  }

  console.log(`Parsing vocabulary file: ${filePath}`);
  const entries = await parseVocabularyFile(filePath);
  console.log(`Parsed ${entries.length} unique entries`);

  const existingCount = await prisma.word.count();
  console.log(`Database currently has ${existingCount} words`);

  for (let i = 0; i < entries.length; i += BATCH_SIZE) {
    const batch = entries.slice(i, i + BATCH_SIZE);
    await importBatch(batch);
    console.log(`Imported ${Math.min(i + batch.length, entries.length)}/${entries.length}`);
  }

  const finalCount = await prisma.word.count();
  const sentenceCount = await prisma.exampleSentence.count();
  console.log('✅ Vocabulary import complete');
  console.log(`   Words: ${finalCount}`);
  console.log(`   Example sentences: ${sentenceCount}`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
