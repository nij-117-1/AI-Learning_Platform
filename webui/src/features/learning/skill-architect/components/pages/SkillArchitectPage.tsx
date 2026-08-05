// src/features/learning/skill-architect/components/pages/SkillArchitectPage.tsx
/**
 * Skill Architect tool page. Prefilled, localStorage-persisted form wired to
 * the skill-architect generate Server Action with full loading/error UX.
 */
"use client";

import type { z } from "zod";
import { TreePine } from "lucide-react";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import { InputField, TextareaField } from "@/features/learning/explainer/components/fields";
import { SkillArchitectFormSchema, type SkillArchitectResponse } from "../../types";
import { skillArchitectGenerateAction } from "../../actions/generate";
import { SkillArchitectResult } from "../results/SkillArchitectResult";

type SkillArchitectFormValues = z.infer<typeof SkillArchitectFormSchema>;

const STORAGE_KEY = "learning.skill-architect.generate.v1";

const DEFAULTS: SkillArchitectFormValues = {
  domain_or_skill: "System Design and Software Architecture",
  current_proficiency: "Junior Developer with 1 year of experience",
  target_mastery_level: "Staff Engineer / Principal Architect",
  learning_constraints: "I only have 5 hours a week to study.",
};

export function SkillArchitectPage() {
  const persisted = usePersistedForm<SkillArchitectFormValues, SkillArchitectResponse>({
    schema: SkillArchitectFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const tool = useToolRequest<SkillArchitectFormValues, SkillArchitectResponse>({
    run: skillArchitectGenerateAction,
    onSuccess: persisted.setResult,
  });

  const errors = persisted.form.formState.errors;
  const result = tool.data ?? persisted.result;

  return (
    <ExplainerPageShell
      title="Skill Architect"
      description="Deconstruct any domain into its fundamental root skills and a level-wise progression tree, with proof of mastery and unlock conditions at every step."
      headerAction={
        <DraftStatus
          status={persisted.status}
          onReset={persisted.resetDraft}
          onClear={persisted.clearDraft}
          disabled={tool.isPending}
        />
      }
      form={
        <form onSubmit={persisted.form.handleSubmit(tool.execute)} className="space-y-4">
          <InputField
            label="Domain or Skill"
            htmlFor="domain_or_skill"
            placeholder="e.g. System Design and Software Architecture"
            disabled={tool.isPending}
            {...persisted.form.register("domain_or_skill")}
            error={errors.domain_or_skill?.message}
          />
          <TextareaField
            label="Current Proficiency"
            htmlFor="current_proficiency"
            placeholder="Describe your current level…"
            hint="Where you are today, e.g. absolute beginner, self-taught, intermediate."
            disabled={tool.isPending}
            {...persisted.form.register("current_proficiency")}
            error={errors.current_proficiency?.message}
          />
          <InputField
            label="Target Mastery Level"
            htmlFor="target_mastery_level"
            placeholder="e.g. Competent Professional, Industry Expert, Master"
            disabled={tool.isPending}
            {...persisted.form.register("target_mastery_level")}
            error={errors.target_mastery_level?.message}
          />
          <TextareaField
            label="Learning Constraints"
            htmlFor="learning_constraints"
            placeholder="Optional — time, resources, or preferred learning style…"
            hint="Optional."
            disabled={tool.isPending}
            {...persisted.form.register("learning_constraints")}
            error={errors.learning_constraints?.message}
          />
          <FormActions
            isPending={tool.isPending}
            error={tool.error}
            submitLabel="Generate Skill Tree"
            submitPendingLabel="Deconstructing skills…"
          />
        </form>
      }
      result={
        result ? (
          <SkillArchitectResult result={result} />
        ) : (
          <EmptyResult
            icon={TreePine}
            title="No skill tree yet"
            description="Tell us what you want to master and generate to see your root-skill progression tree."
          />
        )
      }
    />
  );
}
