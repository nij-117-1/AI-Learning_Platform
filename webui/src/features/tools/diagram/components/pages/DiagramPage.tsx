// src/features/tools/diagram/components/pages/DiagramPage.tsx
/**
 * Diagram Generator tool page. Persisted form wired to the generate Server
 * Action with full loading/error UX.
 */
"use client";

import type { z } from "zod";
import { GitBranch } from "lucide-react";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import {
  SelectField,
  TextareaField,
} from "@/features/learning/explainer/components/fields";
import { DiagramFormSchema, type DiagramResponse } from "../../types";
import { generateDiagramAction } from "../../actions/generate";
import { diagramFormatOptions } from "../../lib/options";
import { DiagramResult } from "../results/DiagramResult";

type DiagramFormValues = z.infer<typeof DiagramFormSchema>;

const STORAGE_KEY = "tools.diagram.generate.v1";

const DEFAULTS: DiagramFormValues = {
  format: "mermaid",
  instruction: "Flowchart of the login flow",
  context:
    "User enters credentials, the system validates them, then routes to dashboard or shows an error.",
  existing_code: "",
};

export function DiagramPage() {
  const persisted = usePersistedForm<DiagramFormValues, DiagramResponse>({
    schema: DiagramFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const tool = useToolRequest<DiagramFormValues, DiagramResponse>({
    run: generateDiagramAction,
    onSuccess: persisted.setResult,
  });

  const errors = persisted.form.formState.errors;
  const result = tool.data ?? persisted.result;

  return (
    <ExplainerPageShell
      title="Diagram Generator"
      description="Generate or refine Mermaid / Draw.io diagram code from a natural-language instruction."
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
          <SelectField
            label="Format"
            name="format"
            htmlFor="format"
            control={persisted.form.control}
            options={diagramFormatOptions}
            disabled={tool.isPending}
            error={errors.format?.message}
          />
          <TextareaField
            label="Instruction"
            htmlFor="instruction"
            placeholder="e.g. Flowchart of the login flow"
            disabled={tool.isPending}
            {...persisted.form.register("instruction")}
            error={errors.instruction?.message}
          />
          <TextareaField
            label="Context (optional)"
            htmlFor="context"
            placeholder="Business logic or technical context…"
            disabled={tool.isPending}
            {...persisted.form.register("context")}
            error={errors.context?.message}
          />
          <TextareaField
            label="Existing Code (optional)"
            htmlFor="existing_code"
            placeholder="Paste existing diagram code to refine it…"
            className="min-h-32"
            disabled={tool.isPending}
            {...persisted.form.register("existing_code")}
            error={errors.existing_code?.message}
            hint="Leave empty to generate from scratch."
          />
          <FormActions
            isPending={tool.isPending}
            error={tool.error}
            submitLabel="Generate Diagram"
            submitPendingLabel="Drawing…"
          />
        </form>
      }
      result={
        result ? (
          <DiagramResult result={result} />
        ) : (
          <EmptyResult
            icon={GitBranch}
            title="No diagram yet"
            description="Describe a diagram and pick a format to generate its code."
          />
        )
      }
    />
  );
}
