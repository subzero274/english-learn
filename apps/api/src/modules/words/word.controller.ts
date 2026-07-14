import * as fs from 'fs';
import { Request, Response, NextFunction } from 'express';
import { AppError } from '@/middleware/errorHandler';
import * as service from '@/modules/words/word.service';
import {
  CreateWordInput,
  UpdateWordInput,
  ListWordsQuery,
} from '@/modules/words/word.schema';

export async function listWordsHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const result = await service.listWords(req.validatedQuery as ListWordsQuery);
    res.json({ data: result.data, pagination: result.pagination });
  } catch (error) {
    next(error);
  }
}

export async function getWordHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const id = parseInt(req.params.id, 10);
    if (Number.isNaN(id)) {
      throw new AppError(400, 'Invalid word id', 'BAD_REQUEST');
    }

    const word = await service.getWordById(id);
    if (!word) {
      throw new AppError(404, 'Word not found', 'NOT_FOUND');
    }

    res.json({ data: word });
  } catch (error) {
    next(error);
  }
}

export async function getWordAudioHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const id = parseInt(req.params.id, 10);
    if (Number.isNaN(id)) {
      throw new AppError(400, 'Invalid word id', 'BAD_REQUEST');
    }

    const { filePath } = await service.getWordAudio(id);

    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    fs.createReadStream(filePath).pipe(res);
  } catch (error) {
    next(error);
  }
}

export async function createWordHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const word = await service.createWord(req.validatedBody as CreateWordInput);
    res.status(201).json({ data: word });
  } catch (error) {
    next(error);
  }
}

export async function updateWordHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const id = parseInt(req.params.id, 10);
    if (Number.isNaN(id)) {
      throw new AppError(400, 'Invalid word id', 'BAD_REQUEST');
    }

    const word = await service.updateWord(id, req.validatedBody as UpdateWordInput);
    res.json({ data: word });
  } catch (error) {
    next(error);
  }
}

export async function deleteWordHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const id = parseInt(req.params.id, 10);
    if (Number.isNaN(id)) {
      throw new AppError(400, 'Invalid word id', 'BAD_REQUEST');
    }

    await service.deleteWord(id);
    res.status(204).send();
  } catch (error) {
    next(error);
  }
}
