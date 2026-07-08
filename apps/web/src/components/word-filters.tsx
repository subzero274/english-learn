"use client";

import { useRouter, useSearchParams } from "next/navigation";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DIFFICULTY_LEVELS, PARTS_OF_SPEECH } from "@/types/word";

export function WordFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const difficulty = searchParams.get("difficulty") || "";
  const partOfSpeech = searchParams.get("partOfSpeech") || "";

  function updateParam(key: string, value: string | null) {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    params.delete("page");
    router.push(`/words?${params.toString()}`);
  }

  return (
    <div className="flex flex-wrap gap-3">
      <Select value={difficulty || ""} onValueChange={(value) => updateParam("difficulty", value)}>
        <SelectTrigger className="w-[140px]">
          <SelectValue placeholder="Difficulty" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">All levels</SelectItem>
          {DIFFICULTY_LEVELS.map((level) => (
            <SelectItem key={level.value} value={level.value}>
              {level.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select value={partOfSpeech || ""} onValueChange={(value) => updateParam("partOfSpeech", value)}>
        <SelectTrigger className="w-[160px]">
          <SelectValue placeholder="Part of speech" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">All types</SelectItem>
          {PARTS_OF_SPEECH.map((pos) => (
            <SelectItem key={pos.value} value={pos.value}>
              {pos.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
