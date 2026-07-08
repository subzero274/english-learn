import { Suspense } from "react";
import { Header } from "@/components/header";
import { SearchInput } from "@/components/search-input";
import { WordCard } from "@/components/word-card";
import { listWords } from "@/lib/api";

interface SearchPageProps {
  searchParams: { q?: string };
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const { q } = searchParams;

  const result = q
    ? await listWords({ q, page: 1, limit: 24 })
    : { data: [], pagination: { page: 1, limit: 24, total: 0, totalPages: 0 } };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto mb-10 space-y-4">
          <h1 className="text-3xl font-bold text-center">Search Words</h1>
          <Suspense fallback={<div className="h-10 bg-muted rounded" />}>
            <SearchInput defaultValue={q} />
          </Suspense>
        </div>

        {q ? (
          <>
            <p className="text-muted-foreground mb-4">
              {result.pagination.total} result{result.pagination.total !== 1 && "s"} for &quot;{q}&quot;
            </p>
            {result.data.length === 0 ? (
              <div className="text-center py-20 text-muted-foreground">No matching words found.</div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {result.data.map((word) => (
                  <WordCard key={word.id} word={word} />
                ))}
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-20 text-muted-foreground">Enter a word or meaning to search.</div>
        )}
      </main>
    </div>
  );
}
