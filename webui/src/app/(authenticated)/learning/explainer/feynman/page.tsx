import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { FeynmanToolPage } from "@/features/learning/explainer/components/pages/FeynmanToolPage";

export const metadata: Metadata = {
  title: "Feynman Explainer | Learning",
  description: "Simplify jargon-heavy concepts using metaphors and child-friendly language.",
};

export default function FeynmanRoutePage() {
  return (
    <>
      <SetPageTitle title="Feynman Explainer" />
      <FeynmanToolPage />
    </>
  );
}
