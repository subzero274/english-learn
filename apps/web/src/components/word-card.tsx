import Link from "next/link";
import { Volume2 } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Word } from "@/types/word";

interface WordCardProps {
  word: Word;
}

export function WordCard({ word }: WordCardProps) {
  return (
    <Link href={`/words/${word.id}`}>
      <Card className="h-full transition-shadow hover:shadow-md cursor-pointer">
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-xl font-bold">{word.word}</h3>
              <p className="text-sm text-muted-foreground flex items-center gap-1">
                <Volume2 className="h-3 w-3" />
                {word.phonetic}
              </p>
            </div>
            {word.difficulty && <Badge variant="secondary">{word.difficulty}</Badge>}
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-foreground/90">{word.meaning}</p>
          {word.partOfSpeech && (
            <p className="text-xs text-muted-foreground mt-2 capitalize">{word.partOfSpeech}</p>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
