import { Metadata } from "next";
import { SetPageTitle } from "@/features/navigation/components/SetPageTitle";
import { SkillArchitectPage } from "@/features/learning/skill-architect/components/pages/SkillArchitectPage";

export const metadata: Metadata = {
  title: "Skill Architect | Learning",
  description: "Deconstruct a domain into its root skills and a level-wise progression tree.",
};

export default function SkillArchitectRoutePage() {
  return (
    <>
      <SetPageTitle title="Skill Architect" />
      <SkillArchitectPage />
    </>
  );
}
