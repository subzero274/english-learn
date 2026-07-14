# English Learn

Full-stack English vocabulary learning system (IELTS focused).

## Tech Stack

- **Monorepo**: pnpm workspaces + Turbo
- **Backend**: Express.js + TypeScript + Prisma + SQLite
- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS + shadcn/ui
- **Admin**: Built into the same Next.js app under `/admin/*`

## Project Structure

```
english-learn/
├── apps/
│   ├── api/          # Express backend
│   └── web/          # Next.js frontend (user + admin)
├── db/               # Shared Prisma schema + database scripts
└── package.json      # Workspace root
```

## Getting Started

```bash
# Enable pnpm via corepack
corepack enable

# Install dependencies
pnpm install

# Set up environment
cp .env.example .env
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.local.example apps/web/.env.local

# Run database migrations and seed
pnpm db:migrate
pnpm db:seed

# (Optional) Import the full vocabulary list
# Place your vocabulary.txt at db/prisma/vocabulary.txt, then:
pnpm db:import-vocabulary
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:4000

## Default Admin Credentials

- Email: `admin@example.com`
- Password: `admin123`

> **Note**: Change these in production by updating the seed script or creating a new admin user.

## Useful Commands

| Command | Description |
|---|---|
| `pnpm dev` | Start all apps in development mode |
| `pnpm build` | Build all apps |
| `pnpm typecheck` | Run TypeScript checks |
| `pnpm lint` | Run linting |
| `pnpm test` | Run tests |
| `pnpm db:migrate` | Run Prisma migrations |
| `pnpm db:seed` | Seed the database |
| `pnpm db:import-vocabulary` | Import vocabulary.txt into the database |
| `pnpm db:reset` | Reset database and re-seed |

## Audio Pronunciation

Word detail pages show an audio player when a pronunciation URL is available. The first request for a word’s audio fetches it from Youdao, caches the MP3 file under `apps/api/public/audio/`, and stores the public path in the database. Subsequent requests serve the cached file directly. The `apps/api/public/audio/` directory is ignored by Git and is created automatically on the first audio request.
