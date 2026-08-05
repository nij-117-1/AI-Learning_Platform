import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { OrchestrateToolPage } from "@/features/learning/explainer/components/pages/OrchestrateToolPage";

export const metadata: Metadata = {
  title: "Orchestrated Journey | Learning",
  description: "Stream a live chapter-by-chapter deep dive into any topic.",
};

export default function OrchestrateRoutePage() {
  return (
    <>
      <SetPageTitle title="Orchestrated Journey" />
      <OrchestrateToolPage />
    </>
  );
}
