"use client";

import { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { toast } from "sonner";
import { Pencil, Trash2, Plus, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Pagination } from "@/components/pagination";
import { listWords, deleteWord } from "@/lib/api";
import { getAdminToken } from "@/lib/auth";
import { Word } from "@/types/word";

export default function AdminWordsPage() {
  const [words, setWords] = useState<Word[]>([]);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    totalPages: 0,
  });
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  async function loadWords(page = 1) {
    setLoading(true);
    try {
      const result = await listWords({ page, limit: 20, q: q || undefined });
      setWords(result.data);
      setPagination(result.pagination);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to load words");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadWords();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleDelete(id: number) {
    const token = getAdminToken();
    if (!token) return;

    setDeletingId(id);
    try {
      await deleteWord(id, token);
      toast.success("Word deleted");
      loadWords(pagination.page);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to delete word");
    } finally {
      setDeletingId(null);
    }
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    loadWords(1);
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-3xl font-bold">Manage Words</h1>
        <Button asChild>
          <Link href="/admin/words/new">
            <Plus className="h-4 w-4 mr-2" />
            Add Word
          </Link>
        </Button>
      </div>

      <form onSubmit={handleSearch} className="flex gap-2 max-w-md">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search words..."
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="pl-9"
          />
        </div>
        <Button type="submit">Search</Button>
      </form>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Word</TableHead>
              <TableHead>Phonetic</TableHead>
              <TableHead>Meaning</TableHead>
              <TableHead>Difficulty</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {words.map((word) => (
              <TableRow key={word.id}>
                <TableCell className="font-medium">{word.word}</TableCell>
                <TableCell>{word.phonetic}</TableCell>
                <TableCell className="max-w-xs truncate">{word.meaning}</TableCell>
                <TableCell>
                  {word.difficulty && <Badge variant="secondary">{word.difficulty}</Badge>}
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-2">
                    <Button variant="ghost" size="icon" asChild>
                      <Link href={`/admin/words/${word.id}/edit`}>
                        <Pencil className="h-4 w-4" />
                      </Link>
                    </Button>

                    <Dialog>
                      <DialogTrigger
                        render={
                          <Button variant="ghost" size="icon">
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        }
                      />
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Delete Word</DialogTitle>
                          <DialogDescription>
                            Are you sure you want to delete &quot;{word.word}&quot;? This action cannot be undone.
                          </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                          <Button
                            variant="destructive"
                            onClick={() => handleDelete(word.id)}
                            disabled={deletingId === word.id}
                          >
                            {deletingId === word.id ? "Deleting..." : "Delete"}
                          </Button>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {words.length === 0 && !loading && (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                  No words found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <Suspense fallback={<div className="h-10 bg-muted rounded" />}>
        <Pagination
          page={pagination.page}
          totalPages={pagination.totalPages}
        />
      </Suspense>
    </div>
  );
}
