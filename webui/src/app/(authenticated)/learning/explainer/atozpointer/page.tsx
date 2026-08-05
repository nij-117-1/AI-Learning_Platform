import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { AtozPointerToolPage } from "@/features/learning/explainer/components/pages/AtozPointerToolPage";

export const metadata: Metadata = {
  title: "Knowledge Roadmap | Learning",
  description: "Build a structured A-to-Z roadmap with concept pointers for guided learning.",
};

export default function AtozPointerRoutePage() {
  return (
    <>
      <SetPageTitle title="Knowledge Roadmap" />
      <AtozPointerToolPage />
    </>
  );
}
