import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';
import { signToken } from '@/lib/jwt';
import { AppError } from '@/middleware/errorHandler';
import { LoginInput } from '@/modules/auth/auth.schema';

export async function login(input: LoginInput) {
  const admin = await prisma.adminUser.findUnique({
    where: { email: input.email },
  });

  if (!admin) {
    throw new AppError(401, 'Invalid credentials', 'INVALID_CREDENTIALS');
  }

  const isValid = await bcrypt.compare(input.password, admin.password);
  if (!isValid) {
    throw new AppError(401, 'Invalid credentials', 'INVALID_CREDENTIALS');
  }

  const token = signToken({ adminId: admin.id, email: admin.email });

  return {
    token,
    admin: {
      id: admin.id,
      email: admin.email,
    },
  };
}
