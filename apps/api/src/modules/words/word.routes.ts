import { Router } from 'express';
import {
  listWordsHandler,
  getWordHandler,
  createWordHandler,
  updateWordHandler,
  deleteWordHandler,
} from '@/modules/words/word.controller';
import { validateBody, validateQuery } from '@/middleware/validate';
import { requireAdmin } from '@/middleware/auth';
import {
  CreateWordSchema,
  UpdateWordSchema,
  ListWordsQuerySchema,
} from '@/modules/words/word.schema';

const router: Router = Router();

router.get('/', validateQuery(ListWordsQuerySchema), listWordsHandler);
router.get('/:id', getWordHandler);
router.post('/', requireAdmin, validateBody(CreateWordSchema), createWordHandler);
router.patch('/:id', requireAdmin, validateBody(UpdateWordSchema), updateWordHandler);
router.delete('/:id', requireAdmin, deleteWordHandler);

export default router;
