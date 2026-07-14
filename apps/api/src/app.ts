import express from 'express';
import path from 'path';
import cors from 'cors';
import { config } from '@/config';
import { errorHandler } from '@/middleware/errorHandler';
import authRoutes from '@/modules/auth/auth.routes';
import wordRoutes from '@/modules/words/word.routes';

export function createApp(): express.Express {
  const app = express();

  app.use(
    cors({
      origin: config.CORS_ORIGIN,
      credentials: true,
    })
  );
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  app.use('/audio', express.static(path.join(__dirname, '../public/audio')));

  app.get('/api/health', (_req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  app.use('/api/auth', authRoutes);
  app.use('/api/words', wordRoutes);

  app.use((_req, res) => {
    res.status(404).json({
      error: {
        message: 'Not found',
        code: 'NOT_FOUND',
      },
    });
  });

  app.use(errorHandler);

  return app;
}
