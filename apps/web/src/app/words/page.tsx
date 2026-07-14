import { Suspense } from "react";
import { Header } from "@/components/header";
import { SearchInput } from "@/components/search-input";
import { WordFilters } from "@/components/word-filters";
import { WordCard } from "@/components/word-card";
import { Pagination } from "@/components/pagination";
import { listWords } from "@/lib/api";

interface WordsPageProps {
  searchParams: {
    page?: string;
    limit?: string;
    q?: string;
    difficulty?: string;
    partOfSpeech?: string;
    tag?: string;
  };
}

export default async function WordsPage({ searchParams }: WordsPageProps) {
  const params = searchParams;
  const page = params.page ? parseInt(params.page, 10) : 1;
  const limit = params.limit ? parseInt(params.limit, 10) : 12;

  const result = await listWords({
    page,
    limit,
    q: params.q,
    difficulty: params.difficulty,
    partOfSpeech: params.partOfSpeech,
    tag: params.tag,
  });

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="mb-8 space-y-4">
          <h1 className="text-3xl font-bold">Word List</h1>
          <div className="flex flex-col md:flex-row md:items-center gap-4 justify-between">
            <Suspense fallback={<div className="h-10 w-full max-w-xl bg-muted rounded" />}>
              <SearchInput defaultValue={params.q} />
            </Suspense>
            <Suspense fallback={<div className="h-10 w-[320px] bg-muted rounded" />}>
              <WordFilters />
            </Suspense>
          </div>
        </div>

        {result.data.length === 0 ? (
          <div className="text-center py-20 text-muted-foreground">No words found.</div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {result.data.map((word) => (
                <WordCard key={word.id} word={word} />
              ))}
            </div>
            <Suspense fallback={<div className="h-10 bg-muted rounded" />}>
              <Pagination page={result.pagination.page} totalPages={result.pagination.totalPages} />
            </Suspense>
          </>
        )}
      </main>
    </div>
  );
}
