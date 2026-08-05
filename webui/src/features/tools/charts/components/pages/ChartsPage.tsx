// src/features/tools/charts/components/pages/ChartsPage.tsx
/**
 * Chart.js Generator tool page. Persisted form wired to the generate Server
 * Action with full loading/error UX.
 */
"use client";

import type { z } from "zod";
import { BarChart3 } from "lucide-react";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import { TextareaField } from "@/features/learning/explainer/components/fields";
import { ChartsFormSchema, type ChartResponse } from "../../types";
import { generateChartAction } from "../../actions/generate";
import { ChartsResult } from "../results/ChartsResult";

type ChartsFormValues = z.infer<typeof ChartsFormSchema>;

const STORAGE_KEY = "tools.charts.generate.v1";

const DEFAULTS: ChartsFormValues = {
  data_input:
    "[{ label: 'Jan', value: 12 }, { label: 'Feb', value: 19 }, { label: 'Mar', value: 3 }]",
  custom_instructions: "Bar chart, blue bars, dark theme, rounded corners.",
  previous_code: "",
};

export function ChartsPage() {
  const persisted = usePersistedForm<ChartsFormValues, ChartResponse>({
    schema: ChartsFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const tool = useToolRequest<ChartsFormValues, ChartResponse>({
    run: generateChartAction,
    onSuccess: persisted.setResult,
  });

  const errors = persisted.form.formState.errors;
  const result = tool.data ?? persisted.result;

  return (
    <ExplainerPageShell
      title="Chart.js Generator"
      description="Generate a Chart.js HTML/JS visualization from raw data and your style preferences."
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
            label="Data Input"
            htmlFor="data_input"
            placeholder="JSON, CSV, or plain text…"
            className="min-h-32"
            disabled={tool.isPending}
            {...persisted.form.register("data_input")}
            error={errors.data_input?.message}
          />
          <TextareaField
            label="Custom Instructions"
            htmlFor="custom_instructions"
            placeholder="Chart type, colors, labels, theme…"
            disabled={tool.isPending}
            {...persisted.form.register("custom_instructions")}
            error={errors.custom_instructions?.message}
          />
          <TextareaField
            label="Previous Code (optional)"
            htmlFor="previous_code"
            placeholder="Existing Chart.js code to refactor…"
            className="min-h-32"
            disabled={tool.isPending}
            {...persisted.form.register("previous_code")}
            error={errors.previous_code?.message}
            hint="Leave empty to generate from scratch."
          />
          <FormActions
            isPending={tool.isPending}
            error={tool.error}
            submitLabel="Generate Chart"
            submitPendingLabel="Plotting…"
          />
        </form>
      }
      result={
        result ? (
          <ChartsResult result={result} />
        ) : (
          <EmptyResult
            icon={BarChart3}
            title="No chart yet"
            description="Paste some data and describe the chart you want."
          />
        )
      }
    />
  );
}
