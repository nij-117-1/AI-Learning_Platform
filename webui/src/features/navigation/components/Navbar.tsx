// src/features/navigation/components/Navbar.tsx
/**
 * Main Navigation Bar - Server Component.
 * Fetches identity server-side and renders branding, desktop/mobile nav,
 * command palette search, theme toggle, and user menu.
 */
import Link from "next/link";
import { NavigationNode, PageData } from "../types";
import { buildNavigationTree } from "../lib/build-navigation-tree";
import { DesktopNavigation } from "./DesktopNavigation";
import { MobileNavigation } from "./MobileNavigation";
import { NavSearch } from "./NavSearch";
import { ThemeToggle } from "./ThemeToggle";
import { UserMenu } from "@/features/identity/components/UserMenu";
import { validateIdentity } from "@/features/identity/lib/auth-guard";
import { getPages } from "@/features/masteradmin/admin/actions/page-actions";

export async function Navbar() {
  const identity = await validateIdentity();
  let pagesData = await getPages();
  const isAdmin = identity.groups.some((g) => g.toLowerCase() === "admin");
  if (!isAdmin) {
    pagesData = pagesData.filter((p) => !p.tags?.includes("admin"));
  }
  const rootNode = buildNavigationTree(pagesData as PageData[]);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between gap-4">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-1.5 font-bold text-xl tracking-tight shrink-0 pl-6">
            <span className="text-primary">AI</span>
            <span className="text-foreground">Studio</span>
          </Link>
          <DesktopNavigation rootNode={rootNode} />
        </div>

        <div className="flex items-center gap-2">
          <div className="hidden sm:flex">
            <NavSearch rootNode={rootNode} />
          </div>
          <ThemeToggle />
          <UserMenu identity={identity} />
          <MobileNavigation rootNode={rootNode} identity={identity} />
        </div>
      </div>
    </header>
  );
}
