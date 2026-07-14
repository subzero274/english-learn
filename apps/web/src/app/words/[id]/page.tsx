import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, Volume2, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Header } from "@/components/header";
import { SentenceList } from "@/components/sentence-list";
import { getWord } from "@/lib/api";

interface WordDetailPageProps {
  params: { id: string };
}

export default async function WordDetailPage({ params }: WordDetailPageProps) {
  const { id } = params;
  const wordId = parseInt(id, 10);
  if (Number.isNaN(wordId)) {
    notFound();
  }

  const { data: word } = await getWord(wordId);
  if (!word) {
    notFound();
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6 flex items-center justify-between">
          <Button variant="outline" size="sm" asChild>
            <Link href="/words">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back to words
            </Link>
          </Button>
          <Button variant="ghost" size="sm" asChild>
            <Link href="/admin/login">
              <Shield className="h-4 w-4 mr-1" />
              Admin
            </Link>
          </Button>
        </div>

        <Card>
          <CardHeader>
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <CardTitle className="text-4xl font-bold mb-2">{word.word}</CardTitle>
                <p className="text-lg text-muted-foreground flex items-center gap-2">
                  <Volume2 className="h-5 w-5" />
                  {word.phonetic}
                </p>
              </div>
              <div className="flex gap-2">
                {word.difficulty && <Badge variant="secondary">{word.difficulty}</Badge>}
                {word.partOfSpeech && <Badge variant="outline">{word.partOfSpeech}</Badge>}
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-8">
            <div>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Meaning</h3>
              <p className="text-xl">{word.meaning}</p>
            </div>

            {word.audioUrl && (
              <div>
                <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-2">Pronunciation</h3>
                <audio controls src={`${process.env.NEXT_PUBLIC_API_URL}${word.audioUrl}`} className="w-full">
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}

            <div>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">Example Sentences</h3>
              <SentenceList sentences={word.exampleSentences} />
            </div>

            {word.tags && (
              <div className="flex flex-wrap gap-2">
                {word.tags.split(",").map((tag) => (
                  <Badge key={tag} variant="secondary">{tag.trim()}</Badge>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
