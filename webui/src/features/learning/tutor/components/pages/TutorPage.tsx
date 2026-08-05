// src/features/learning/tutor/components/pages/TutorPage.tsx
/**
 * Adaptive Tutor tool page. Prefilled, localStorage-persisted form wired to
 * the tutor explain Server Action with full loading/error UX.
 */
"use client";

import type { z } from "zod";
import { Presentation } from "lucide-react";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import {
  InputField,
  SelectField,
  TextareaField,
} from "@/features/learning/explainer/components/fields";
import { TutorFormSchema, type TutorResponse } from "../../types";
import { tutorExplainAction } from "../../actions/explain";
import { TutorResult } from "../results/TutorResult";
import { learningStyleOptions } from "../../lib/options";

type TutorFormValues = z.infer<typeof TutorFormSchema>;

const STORAGE_KEY = "learning.tutor.explain.v1";

const DEFAULTS: TutorFormValues = {
  system_prompt:
    "You are a patient Socratic tutor who guides students with clear explanations and targeted questions. Adapt your language to the student's level, frame concepts using their preferred learning style, and always end with one thoughtful question to test their understanding.",
  user_query: "Why does water boil at 100°C?",
  student_level: "High School",
  learning_style: "analogical",
  current_scenario: "preparing for an exam",
  last_topic_taught: "states of matter",
};

export function TutorPage() {
  const persisted = usePersistedForm<TutorFormValues, TutorResponse>({
    schema: TutorFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const tool = useToolRequest<TutorFormValues, TutorResponse>({
    run: tutorExplainAction,
    onSuccess: persisted.setResult,
  });

  const errors = persisted.form.formState.errors;
  const result = tool.data ?? persisted.result;

  return (
    <ExplainerPageShell
      title="Adaptive Tutor"
      description="Get a personalized explanation adapted to your level, learning style, and current scenario — with an analogy and a question to test your understanding."
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
          <TextareaField
            label="System Prompt (Tutor Persona)"
            htmlFor="system_prompt"
            placeholder="How should the tutor behave and teach?"
            hint="The persona and pedagogical rules. Edit to change the tutoring style."
            disabled={tool.isPending}
            {...persisted.form.register("system_prompt")}
            error={errors.system_prompt?.message}
          />
          <TextareaField
            label="Your Question"
            htmlFor="user_query"
            placeholder="Ask the question you are struggling with…"
            disabled={tool.isPending}
            {...persisted.form.register("user_query")}
            error={errors.user_query?.message}
          />
          <InputField
            label="Student Level"
            htmlFor="student_level"
            placeholder="e.g. Toddler, High School, Expert"
            disabled={tool.isPending}
            {...persisted.form.register("student_level")}
            error={errors.student_level?.message}
          />
          <SelectField
            label="Learning Style"
            name="learning_style"
            htmlFor="learning_style"
            control={persisted.form.control}
            options={learningStyleOptions}
            disabled={tool.isPending}
            error={errors.learning_style?.message}
          />
          <InputField
            label="Current Scenario"
            htmlFor="current_scenario"
            placeholder="e.g. preparing for an exam"
            disabled={tool.isPending}
            {...persisted.form.register("current_scenario")}
            error={errors.current_scenario?.message}
          />
          <InputField
            label="Last Topic Taught"
            htmlFor="last_topic_taught"
            placeholder="Optional — previous lesson context…"
            hint="Optional."
            disabled={tool.isPending}
            {...persisted.form.register("last_topic_taught")}
            error={errors.last_topic_taught?.message}
          />
          <FormActions
            isPending={tool.isPending}
            error={tool.error}
            submitLabel="Explain It to Me"
            submitPendingLabel="Preparing your lesson…"
          />
        </form>
      }
      result={
        result ? (
          <TutorResult result={result} />
        ) : (
          <EmptyResult
            icon={Presentation}
            title="No lesson yet"
            description="Ask your question and generate to see an adapted explanation, analogy, and a follow-up question."
          />
        )
      }
    />
  );
}
