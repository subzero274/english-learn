import Link from "next/link";
import { BookOpen, Search, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Header() {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <BookOpen className="h-5 w-5" />
          <span>English Learn</span>
        </Link>

        <nav className="flex items-center gap-4">
          <Link
            href="/words"
            className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            Words
          </Link>
          <Link
            href="/search"
            className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            <Search className="h-4 w-4" />
          </Link>
          <Button variant="ghost" size="icon" asChild>
            <Link href="/admin/login" title="Admin">
              <Shield className="h-4 w-4" />
            </Link>
          </Button>
        </nav>
      </div>
    </header>
  );
}
