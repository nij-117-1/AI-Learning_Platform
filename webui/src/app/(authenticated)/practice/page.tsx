import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { ToolsCardGrid } from "@/features/learning/components/ToolsCardGrid";
import { testingPortalTools } from "@/features/practice/lib/testing-portal-tools";
import { graderTools } from "@/features/practice/lib/grader-tools";

export const metadata: Metadata = {
  title: "Practice Hub",
  description: "Generate practice questions, get expert answers, and grade your performance with AI feedback.",
};

export default function PracticePage() {
  return (
    <div className="mx-auto w-full max-w-7xl space-y-8">
      <SetPageTitle title="Practice Hub" />

      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Practice Hub</h1>
        <p className="max-w-2xl text-muted-foreground">
          Test yourself with generated questions, get subject-matter-expert
          answers, and grade your performance against clear objectives.
        </p>
      </header>

      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Assessment</h2>
        </div>
        <ToolsCardGrid tools={testingPortalTools} />
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Feedback</h2>
        </div>
        <ToolsCardGrid tools={graderTools} />
      </section>
    </div>
  );
}
