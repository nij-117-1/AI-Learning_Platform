import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { ExplainerToolsGrid } from "@/features/learning/components/ExplainerToolsGrid";

export const metadata: Metadata = {
  title: "Explainer Tools | Learning",
  description: "Seven AI-powered tools for explaining, simplifying, and mastering any topic.",
};

export default function ExplainerPage() {
  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <SetPageTitle title="Explainer Tools" />

      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Explainer Tools</h1>
        <p className="max-w-2xl text-muted-foreground">
          Choose a tool. Each one keeps your inputs saved locally, so you can close
          the page and pick up exactly where you left off.
        </p>
      </header>

      <ExplainerToolsGrid />
    </div>
  );
}
