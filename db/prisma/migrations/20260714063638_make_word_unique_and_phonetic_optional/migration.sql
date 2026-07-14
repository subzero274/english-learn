-- CreateTable
CREATE TABLE "Word" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "word" TEXT NOT NULL,
    "phonetic" TEXT,
    "meaning" TEXT NOT NULL,
    "partOfSpeech" TEXT,
    "difficulty" TEXT,
    "tags" TEXT,
    "audioUrl" TEXT,
    "unit" INTEGER,
    "needsSpelling" BOOLEAN NOT NULL DEFAULT false,
    "reviewCount" INTEGER NOT NULL DEFAULT 0,
    "masteryLevel" TEXT NOT NULL DEFAULT 'NEW',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "ExampleSentence" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "english" TEXT NOT NULL,
    "chinese" TEXT NOT NULL,
    "order" INTEGER NOT NULL DEFAULT 0,
    "wordId" INTEGER NOT NULL,
    CONSTRAINT "ExampleSentence_wordId_fkey" FOREIGN KEY ("wordId") REFERENCES "Word" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AdminUser" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "Word_word_key" ON "Word"("word");

-- CreateIndex
CREATE INDEX "Word_word_idx" ON "Word"("word");

-- CreateIndex
CREATE INDEX "Word_difficulty_idx" ON "Word"("difficulty");

-- CreateIndex
CREATE INDEX "Word_partOfSpeech_idx" ON "Word"("partOfSpeech");

-- CreateIndex
CREATE INDEX "Word_unit_idx" ON "Word"("unit");

-- CreateIndex
CREATE INDEX "Word_masteryLevel_idx" ON "Word"("masteryLevel");

-- CreateIndex
CREATE INDEX "ExampleSentence_wordId_idx" ON "ExampleSentence"("wordId");

-- CreateIndex
CREATE UNIQUE INDEX "AdminUser_email_key" ON "AdminUser"("email");
