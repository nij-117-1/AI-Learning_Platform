import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { SocraticToolPage } from "@/features/learning/explainer/components/pages/SocraticToolPage";

export const metadata: Metadata = {
  title: "Socratic Mentor | Learning",
  description: "Challenge your understanding through guided discovery questions.",
};

export default function SocraticRoutePage() {
  return (
    <>
      <SetPageTitle title="Socratic Mentor" />
      <SocraticToolPage />
    </>
  );
}
