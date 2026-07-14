import { execSync } from 'child_process';
import path from 'path';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';

beforeAll(() => {
  // Ensure test database is migrated using the shared db package
  execSync('pnpm --filter @english-learn/db exec prisma migrate deploy', {
    cwd: path.resolve(__dirname, '../..'),
    env: { ...process.env, DATABASE_URL: process.env.DATABASE_URL },
    stdio: 'ignore',
  });
});

beforeEach(async () => {
  await prisma.$executeRawUnsafe('DELETE FROM ExampleSentence;');
  await prisma.$executeRawUnsafe('DELETE FROM Word;');
  await prisma.$executeRawUnsafe('DELETE FROM AdminUser;');

  await prisma.adminUser.create({
    data: {
      email: 'admin@test.com',
      password: await bcrypt.hash('test123', 10),
    },
  });
});

afterAll(async () => {
  await prisma.$disconnect();
});
