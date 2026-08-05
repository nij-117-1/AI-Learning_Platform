import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { CurriculumToolPage } from "@/features/learning/explainer/components/pages/CurriculumToolPage";

export const metadata: Metadata = {
  title: "Curriculum Path | Learning",
  description: "Initialize a personalized learning roadmap that finds the crux of mastery.",
};

export default function CurriculumRoutePage() {
  return (
    <>
      <SetPageTitle title="Curriculum Path" />
      <CurriculumToolPage />
    </>
  );
}
