import { Request, Response, NextFunction } from 'express';
import { login } from '@/modules/auth/auth.service';
import { LoginInput } from '@/modules/auth/auth.schema';

export async function loginHandler(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const result = await login(req.validatedBody as LoginInput);
    res.json({ data: result });
  } catch (error) {
    next(error);
  }
}
