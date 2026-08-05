// src/features/practice/testing-portal/components/forms/McqForm.tsx
/**
 * MCQ generation form: topic, question style, count, difficulty and scenario
 * wired to the generateMcq Server Action with persisted draft + result.
 */
"use client";

import { ListChecks } from "lucide-react";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import { InputField, SelectField, SliderField, TextareaField } from "@/features/learning/explainer/components/fields";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { generateMcqAction } from "../../actions/generateMcq";
import { McqFormSchema, type McqFormValues, type McqResponse } from "../../types";
import { mcqDifficultyLevelOptions, mcqQuestionTypeOptions } from "../../lib/options";
import { McqResult } from "../results/McqResult";

const STORAGE_KEY = "practice.testing-portal.mcq.v1";

const DEFAULTS: McqFormValues = {
  topic: "Python Concurrency",
  question_type: "practical",
  num_questions: 3,
  difficulty_level: "advanced",
  context_setting: "Senior Backend Engineer Interview",
  custom_instructions: "",
  past_questions: "",
};

export function McqForm() {
  const persisted = usePersistedForm<McqFormValues, McqResponse>({
    schema: McqFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const tool = useToolRequest<McqFormValues, McqResponse>({
    run: generateMcqAction,
    onSuccess: persisted.setResult,
  });

  const errors = persisted.form.formState.errors;
  const result = tool.data ?? persisted.result;

  return (
    <ExplainerPageShell
      title="Multiple Choice Questions"
      description="Generate a set of MCQs tuned to a difficulty level, question style, and interview or exam scenario."
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
            htmlFor="mcq_topic"
            placeholder="e.g. Python Concurrency"
            disabled={tool.isPending}
            {...persisted.form.register("topic")}
            error={errors.topic?.message}
          />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <SelectField
              label="Question Type"
              name="question_type"
              htmlFor="mcq_question_type"
              control={persisted.form.control}
              options={mcqQuestionTypeOptions}
              disabled={tool.isPending}
              error={errors.question_type?.message}
            />
            <SelectField
              label="Difficulty"
              name="difficulty_level"
              htmlFor="mcq_difficulty"
              control={persisted.form.control}
              options={mcqDifficultyLevelOptions}
              disabled={tool.isPending}
              error={errors.difficulty_level?.message}
            />
          </div>
          <SliderField
            label="Number of Questions"
            name="num_questions"
            htmlFor="mcq_num"
            control={persisted.form.control}
            min={1}
            max={10}
            formatValue={(value) => `${value} question${value === 1 ? "" : "s"}`}
            disabled={tool.isPending}
          />
          <InputField
            label="Context Setting"
            htmlFor="mcq_context"
            placeholder="e.g. Senior Backend Engineer Interview"
            disabled={tool.isPending}
            {...persisted.form.register("context_setting")}
            error={errors.context_setting?.message}
          />
          <TextareaField
            label="Custom Instructions (optional)"
            htmlFor="mcq_instructions"
            placeholder="e.g. Focus on GIL trade-offs."
            disabled={tool.isPending}
            {...persisted.form.register("custom_instructions")}
            error={errors.custom_instructions?.message}
          />
          <TextareaField
            label="Past Questions (optional)"
            htmlFor="mcq_past"
            placeholder="Paste previously generated questions to avoid repetition."
            disabled={tool.isPending}
            {...persisted.form.register("past_questions")}
            error={errors.past_questions?.message}
          />
          <FormActions
            isPending={tool.isPending}
            error={tool.error}
            submitLabel="Generate MCQs"
            submitPendingLabel="Generating questions…"
          />
        </form>
      }
      result={
        result ? (
          <McqResult result={result} />
        ) : (
          <EmptyResult
            icon={ListChecks}
            title="No questions yet"
            description="Fill in the form and generate to get a fresh set of multiple choice questions."
          />
        )
      }
    />
  );
}
