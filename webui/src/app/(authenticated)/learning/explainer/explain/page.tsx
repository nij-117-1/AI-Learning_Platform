import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { ExplainToolPage } from "@/features/learning/explainer/components/pages/ExplainToolPage";

export const metadata: Metadata = {
  title: "Quick Explain | Learning",
  description: "Get a structured explanation of any topic, tuned to your expertise level.",
};

export default function ExplainRoutePage() {
  return (
    <>
      <SetPageTitle title="Quick Explain" />
      <ExplainToolPage />
    </>
  );
}
