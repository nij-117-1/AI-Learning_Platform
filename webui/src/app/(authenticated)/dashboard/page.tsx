import { Metadata } from "next";
import { validateIdentity } from "@/features/identity/lib/auth-guard";
import { Footer } from "@/features/common/components/Footer";
import { PagesContainer } from "@/features/pages/components/PagesContainer";
import type { Page } from "@/features/pages/types/page";
import { getPages } from "@/features/masteradmin/admin/actions/page-actions";

export const dynamic = "force-dynamic";
export const revalidate = 0;

export const metadata: Metadata = {
  title: "Dashboard | Application Hub",
  description: "Access all your projects, websites, and practice tools from one place.",
};

export default async function DashboardPage() {
  const identity = await validateIdentity();

  let pages: Page[] = [];
  try {
    const allPages = await getPages();
    const isAdmin = identity.groups.some((g) => g.toLowerCase() === "admin");
    pages = isAdmin ? allPages : allPages.filter((p) => !p.tags?.includes("admin"));
  } catch (error) {
    console.error("[Dashboard] Error loading pages:", error);
    pages = [];
  }

  const categoryCounts = pages.reduce<Record<string, number>>((acc, p) => {
    acc[p.category] = (acc[p.category] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="flex min-h-screen flex-col bg-slate-50/50">
      <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-8 max-w-7xl">
        {/* Hero */}
        <header className="mb-6">
          <div className="flex flex-wrap gap-2">
            {Object.entries(categoryCounts).map(([cat, count]) => (
              <div
                key={cat}
                className="inline-flex items-center gap-1.5 rounded-full bg-white border border-slate-200 px-3 py-1 text-xs font-medium text-slate-600 shadow-sm"
              >
                {cat}
                <span className="text-primary font-bold">{count}</span>
              </div>
            ))}
          </div>
        </header>

        <section aria-label="Dashboard Content Grid">
          <PagesContainer initialPages={pages} />
        </section>
      </main>

      <Footer />
    </div>
  );
}
