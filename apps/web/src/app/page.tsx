import Link from "next/link";
import { BookOpen, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Header } from "@/components/header";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        <section className="container mx-auto px-4 py-20 md:py-32 text-center">
          <div className="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-6">
            <BookOpen className="h-6 w-6 text-primary" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
            Master IELTS Vocabulary
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Learn English words with phonetics, Chinese meanings, and bilingual example sentences.
            Curated for IELTS success.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/words">
                Start Learning
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/search">Search Words</Link>
            </Button>
          </div>
        </section>

        <section className="container mx-auto px-4 py-16 border-t">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">Phonetics Included</h3>
              <p className="text-muted-foreground">Every word comes with IPA pronunciation to help you speak correctly.</p>
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">Bilingual Examples</h3>
              <p className="text-muted-foreground">Understand usage through English sentences with Chinese translations.</p>
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">IELTS Focused</h3>
              <p className="text-muted-foreground">Words and difficulty levels aligned with IELTS requirements.</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} English Learn. Built for IELTS learners.
        </div>
      </footer>
    </div>
  );
}
