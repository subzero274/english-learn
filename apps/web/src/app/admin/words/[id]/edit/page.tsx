export const dynamic = "force-dynamic";

import { notFound } from "next/navigation";
import { WordForm } from "@/components/admin/word-form";
import { getWord } from "@/lib/api";

interface EditWordPageProps {
  params: { id: string };
}

export default async function EditWordPage({ params }: EditWordPageProps) {
  const id = parseInt(params.id, 10);
  if (Number.isNaN(id)) {
    notFound();
  }

  const { data: word } = await getWord(id);
  if (!word) {
    notFound();
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Edit Word</h1>
      <WordForm word={word} />
    </div>
  );
}
