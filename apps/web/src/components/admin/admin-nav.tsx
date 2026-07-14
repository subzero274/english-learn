"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { BookOpen, LogOut, Plus, List } from "lucide-react";
import { Button } from "@/components/ui/button";
import { clearAdminToken } from "@/lib/auth";

const navItems = [
  { href: "/admin/words", label: "Words", icon: List },
  { href: "/admin/words/new", label: "New Word", icon: Plus },
];

export function AdminNav() {
  const pathname = usePathname();
  const router = useRouter();

  function handleLogout() {
    clearAdminToken();
    router.push("/admin/login");
  }

  return (
    <aside className="w-64 border-r bg-muted/30 flex flex-col">
      <div className="h-14 flex items-center px-4 border-b">
        <Link href="/" className="flex items-center gap-2 font-bold">
          <BookOpen className="h-5 w-5" />
          <span>English Learn</span>
        </Link>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                pathname === item.href
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t">
        <Button variant="outline" className="w-full" onClick={handleLogout}>
          <LogOut className="h-4 w-4 mr-2" />
          Logout
        </Button>
      </div>
    </aside>
  );
}
