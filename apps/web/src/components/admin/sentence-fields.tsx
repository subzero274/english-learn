"use client";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface SentenceFieldsProps {
  sentences: { english: string; chinese: string }[];
  onChange: (sentences: { english: string; chinese: string }[]) => void;
}

export function SentenceFields({ sentences, onChange }: SentenceFieldsProps) {
  function updateSentence(index: number, field: "english" | "chinese", value: string) {
    const next = [...sentences];
    next[index] = { ...next[index], [field]: value };
    onChange(next);
  }

  function addSentence() {
    onChange([...sentences, { english: "", chinese: "" }]);
  }

  function removeSentence(index: number) {
    const next = sentences.filter((_, i) => i !== index);
    onChange(next);
  }

  return (
    <div className="space-y-4">
      <Label>Example Sentences</Label>
      {sentences.map((sentence, index) => (
        <div key={index} className="border rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Sentence {index + 1}</span>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => removeSentence(index)}
              disabled={sentences.length <= 1}
            >
              Remove
            </Button>
          </div>
          <div className="space-y-2">
            <Textarea
              placeholder="English sentence"
              value={sentence.english}
              onChange={(e) => updateSentence(index, "english", e.target.value)}
              required
            />
            <Textarea
              placeholder="Chinese translation"
              value={sentence.chinese}
              onChange={(e) => updateSentence(index, "chinese", e.target.value)}
              required
            />
          </div>
        </div>
      ))}
      <Button type="button" variant="outline" onClick={addSentence}>
        + Add Sentence
      </Button>
    </div>
  );
}
