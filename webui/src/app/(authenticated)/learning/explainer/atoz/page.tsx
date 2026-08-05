import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { AtozToolPage } from "@/features/learning/explainer/components/pages/AtozToolPage";

export const metadata: Metadata = {
  title: "A-to-Z Tutorial | Learning",
  description: "Generate a high-depth, markdown-formatted A-to-Z tutorial on any topic.",
};

export default function AtozRoutePage() {
  return (
    <>
      <SetPageTitle title="A-to-Z Tutorial" />
      <AtozToolPage />
    </>
  );
}
