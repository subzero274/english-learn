"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { SentenceFields } from "@/components/admin/sentence-fields";
import { createWord, updateWord } from "@/lib/api";
import { getAdminToken } from "@/lib/auth";
import { Word, PARTS_OF_SPEECH, DIFFICULTY_LEVELS } from "@/types/word";

interface WordFormProps {
  word?: Word;
}

export function WordForm({ word }: WordFormProps) {
  const router = useRouter();
  const isEditing = !!word;

  const [wordValue, setWordValue] = useState(word?.word || "");
  const [phonetic, setPhonetic] = useState(word?.phonetic || "");
  const [meaning, setMeaning] = useState(word?.meaning || "");
  const [partOfSpeech, setPartOfSpeech] = useState(word?.partOfSpeech || "");
  const [difficulty, setDifficulty] = useState(word?.difficulty || "");
  const [tags, setTags] = useState(word?.tags || "");
  const [audioUrl, setAudioUrl] = useState(word?.audioUrl || "");
  const [sentences, setSentences] = useState(
    word?.exampleSentences.length
      ? word.exampleSentences.map((s) => ({ english: s.english, chinese: s.chinese }))
      : [{ english: "", chinese: "" }]
  );
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const token = getAdminToken();
    if (!token) {
      toast.error("Not authenticated");
      return;
    }

    const payload = {
      word: wordValue,
      phonetic,
      meaning,
      partOfSpeech: partOfSpeech || undefined,
      difficulty: difficulty || undefined,
      tags: tags || undefined,
      audioUrl: audioUrl || undefined,
      exampleSentences: sentences,
    };

    setLoading(true);
    try {
      if (isEditing) {
        await updateWord(word.id, payload, token);
        toast.success("Word updated");
      } else {
        await createWord(payload, token);
        toast.success("Word created");
      }
      router.push("/admin/words");
      router.refresh();
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to save word");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="word">Word</Label>
          <Input
            id="word"
            value={wordValue}
            onChange={(e) => setWordValue(e.target.value)}
            placeholder="e.g. ambiguous"
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="phonetic">Phonetic</Label>
          <Input
            id="phonetic"
            value={phonetic}
            onChange={(e) => setPhonetic(e.target.value)}
            placeholder="e.g. /æmˈbɪɡjuəs/"
            required
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="meaning">Chinese Meaning</Label>
        <Input
          id="meaning"
          value={meaning}
          onChange={(e) => setMeaning(e.target.value)}
          placeholder="e.g. 模棱两可的"
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Part of Speech</Label>
          <Select value={partOfSpeech} onValueChange={(value) => setPartOfSpeech(value || "")}>
            <SelectTrigger>
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">None</SelectItem>
              {PARTS_OF_SPEECH.map((pos) => (
                <SelectItem key={pos.value} value={pos.value}>
                  {pos.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>Difficulty</Label>
          <Select value={difficulty} onValueChange={(value) => setDifficulty(value || "")}>
            <SelectTrigger>
              <SelectValue placeholder="Select level" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">None</SelectItem>
              {DIFFICULTY_LEVELS.map((level) => (
                <SelectItem key={level.value} value={level.value}>
                  {level.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="tags">Tags (comma separated)</Label>
        <Input
          id="tags"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="e.g. ielts,academic"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="audioUrl">Audio URL (optional)</Label>
        <Input
          id="audioUrl"
          type="url"
          value={audioUrl}
          onChange={(e) => setAudioUrl(e.target.value)}
          placeholder="https://example.com/audio.mp3"
        />
      </div>

      <SentenceFields sentences={sentences} onChange={setSentences} />

      <div className="flex gap-4">
        <Button type="submit" disabled={loading}>
          {loading ? "Saving..." : isEditing ? "Update Word" : "Create Word"}
        </Button>
        <Button type="button" variant="outline" onClick={() => router.push("/admin/words")}>
          Cancel
        </Button>
      </div>
    </form>
  );
}
