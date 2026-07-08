import { Request, Response, NextFunction } from 'express';
import { verifyToken } from '@/lib/jwt';
import { AppError } from '@/middleware/errorHandler';

declare global {
  namespace Express {
    interface Request {
      admin?: {
        adminId: number;
        email: string;
      };
    }
  }
}

export function requireAdmin(req: Request, _res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    next(new AppError(401, 'Authentication required', 'UNAUTHORIZED'));
    return;
  }

  const token = authHeader.slice(7);
  try {
    const payload = verifyToken(token);
    req.admin = { adminId: payload.adminId, email: payload.email };
    next();
  } catch {
    next(new AppError(401, 'Invalid or expired token', 'UNAUTHORIZED'));
  }
}
