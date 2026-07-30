// src/features/navigation/components/Navbar.tsx
/**
 * Main Navigation Bar - Server Component.
 * Fetches identity server-side and renders branding, theme toggle, and user menu.
 */
import Link from "next/link";
import { ThemeToggle } from "./ThemeToggle";
import { PageTitle } from "./PageTitle";
import { UserMenu } from "@/features/identity/components/UserMenu";
import { validateIdentity } from "@/features/identity/lib/auth-guard";

export async function Navbar() {
  const identity = await validateIdentity();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between gap-4">
        <div className="flex items-center gap-6">
          <Link href="/dashboard" className="flex items-center gap-1.5 font-bold text-xl tracking-tight shrink-0 pl-6">
            <span className="text-primary">AI</span>
            <span className="text-foreground">Studio</span>
          </Link>
          <PageTitle />
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <UserMenu identity={identity} />
        </div>
      </div>
    </header>
  );
}
