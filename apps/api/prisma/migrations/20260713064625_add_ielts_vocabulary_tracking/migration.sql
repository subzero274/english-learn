-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Word" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "word" TEXT NOT NULL,
    "phonetic" TEXT NOT NULL,
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
INSERT INTO "new_Word" ("audioUrl", "createdAt", "difficulty", "id", "meaning", "partOfSpeech", "phonetic", "tags", "updatedAt", "word") SELECT "audioUrl", "createdAt", "difficulty", "id", "meaning", "partOfSpeech", "phonetic", "tags", "updatedAt", "word" FROM "Word";
DROP TABLE "Word";
ALTER TABLE "new_Word" RENAME TO "Word";
CREATE INDEX "Word_word_idx" ON "Word"("word");
CREATE INDEX "Word_difficulty_idx" ON "Word"("difficulty");
CREATE INDEX "Word_partOfSpeech_idx" ON "Word"("partOfSpeech");
CREATE INDEX "Word_unit_idx" ON "Word"("unit");
CREATE INDEX "Word_masteryLevel_idx" ON "Word"("masteryLevel");
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
