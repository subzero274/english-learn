export const dynamic = "force-dynamic";

import { WordForm } from "@/components/admin/word-form";

export default function NewWordPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Add New Word</h1>
      <WordForm />
    </div>
  );
}
