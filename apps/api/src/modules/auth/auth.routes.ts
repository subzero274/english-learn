import { Router } from 'express';
import { loginHandler } from '@/modules/auth/auth.controller';
import { validateBody } from '@/middleware/validate';
import { LoginSchema } from '@/modules/auth/auth.schema';

const router: Router = Router();

router.post('/login', validateBody(LoginSchema), loginHandler);

export default router;
