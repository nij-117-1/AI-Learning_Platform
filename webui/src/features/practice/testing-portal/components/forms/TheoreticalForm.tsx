// src/features/practice/testing-portal/components/forms/TheoreticalForm.tsx
/**
 * Theoretical question generation form: topic, question style, count,
 * difficulty, scenario, source context and instructions. The generated
 * questions can be answered inline and graded via the Performance Grader.
 */
"use client";

import { FileQuestion } from "lucide-react";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import { InputField, SelectField, SliderField, TextareaField } from "@/features/learning/explainer/components/fields";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { generateTheoreticalAction } from "../../actions/generateTheoretical";
import {
  TheoreticalFormSchema,
  type TheoreticalFormValues,
  type TheoreticalResponse,
} from "../../types";
import { theoreticalDifficultyLevelOptions, theoreticalQuestionTypeOptions } from "../../lib/options";
import { TheoreticalResult } from "../results/TheoreticalResult";

const STORAGE_KEY = "practice.testing-portal.theoretical.v1";

const DEFAULTS: TheoreticalFormValues = {
  topic: "Microservices",
  question_type: "architectural",
  num_questions: 2,
  difficulty_level: "advanced",
  context_setting: "High-Tech Enterprise Interview",
  source_context: "",
  custom_instructions: "",
  past_questions: "",
};

export function TheoreticalForm() {
  const persisted = usePersistedForm<TheoreticalFormValues, TheoreticalResponse>({
    schema: TheoreticalFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const tool = useToolRequest<TheoreticalFormValues, TheoreticalResponse>({
    run: generateTheoreticalAction,
    onSuccess: persisted.setResult,
  });

  const errors = persisted.form.formState.errors;
  const result = tool.data ?? persisted.result;

  return (
    <ExplainerPageShell
      title="Theoretical Questions"
      description="Generate open-ended, scenario-based questions — then write and grade an answer right here."
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
            label="Topic"
            htmlFor="theo_topic"
            placeholder="e.g. Microservices"
            disabled={tool.isPending}
            {...persisted.form.register("topic")}
            error={errors.topic?.message}
          />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <SelectField
              label="Question Type"
              name="question_type"
              htmlFor="theo_question_type"
              control={persisted.form.control}
              options={theoreticalQuestionTypeOptions}
              disabled={tool.isPending}
              error={errors.question_type?.message}
            />
            <SelectField
              label="Difficulty"
              name="difficulty_level"
              htmlFor="theo_difficulty"
              control={persisted.form.control}
              options={theoreticalDifficultyLevelOptions}
              disabled={tool.isPending}
              error={errors.difficulty_level?.message}
            />
          </div>
          <SliderField
            label="Number of Questions"
            name="num_questions"
            htmlFor="theo_num"
            control={persisted.form.control}
            min={1}
            max={5}
            formatValue={(value) => `${value} question${value === 1 ? "" : "s"}`}
            disabled={tool.isPending}
          />
          <InputField
            label="Context Setting"
            htmlFor="theo_context"
            placeholder="e.g. High-Tech Enterprise Interview"
            disabled={tool.isPending}
            {...persisted.form.register("context_setting")}
            error={errors.context_setting?.message}
          />
          <TextareaField
            label="Source Context (optional)"
            htmlFor="theo_source"
            placeholder="Paste source text or data to analyze."
            disabled={tool.isPending}
            {...persisted.form.register("source_context")}
            error={errors.source_context?.message}
          />
          <TextareaField
            label="Custom Instructions (optional)"
            htmlFor="theo_instructions"
            placeholder="e.g. Focus on speed vs consistency."
            disabled={tool.isPending}
            {...persisted.form.register("custom_instructions")}
            error={errors.custom_instructions?.message}
          />
          <TextareaField
            label="Past Questions (optional)"
            htmlFor="theo_past"
            placeholder="Previous questions to ensure variety."
            disabled={tool.isPending}
            {...persisted.form.register("past_questions")}
            error={errors.past_questions?.message}
          />
          <FormActions
            isPending={tool.isPending}
            error={tool.error}
            submitLabel="Generate Questions"
            submitPendingLabel="Generating questions…"
          />
        </form>
      }
      result={
        result ? (
          <TheoreticalResult
            result={result}
            contextSetting={persisted.form.getValues("context_setting")}
            difficultyLevel={persisted.form.getValues("difficulty_level")}
          />
        ) : (
          <EmptyResult
            icon={FileQuestion}
            title="No questions yet"
            description="Fill in the form and generate to get open-ended questions for practice."
          />
        )
      }
    />
  );
}
