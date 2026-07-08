import { CreateWordInput, UpdateWordInput, ListWordsQuery } from '@/modules/words/word.schema';
import * as repository from '@/modules/words/word.repository';

export async function createWord(data: CreateWordInput) {
  return repository.createWord(data);
}

export async function getWordById(id: number) {
  return repository.findWordById(id);
}

export async function updateWord(id: number, data: UpdateWordInput) {
  return repository.updateWord(id, data);
}

export async function deleteWord(id: number) {
  return repository.deleteWord(id);
}

export async function listWords(query: ListWordsQuery) {
  return repository.listWords(query);
}
