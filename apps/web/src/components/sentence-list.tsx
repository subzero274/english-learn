import { ExampleSentence } from "@/types/word";

interface SentenceListProps {
  sentences: ExampleSentence[];
}

export function SentenceList({ sentences }: SentenceListProps) {
  return (
    <div className="space-y-4">
      {sentences.map((sentence) => (
        <div key={sentence.id} className="border-l-2 border-primary pl-4 py-1">
          <p className="text-foreground font-medium">{sentence.english}</p>
          <p className="text-muted-foreground text-sm mt-1">{sentence.chinese}</p>
        </div>
      ))}
    </div>
  );
}
