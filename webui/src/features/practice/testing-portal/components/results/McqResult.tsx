// src/features/practice/testing-portal/components/results/McqResult.tsx
/**
 * Displays the generated MCQs as an interactive quiz with scoring and a
 * "try again" reset.
 */
"use client";

import { ListChecks } from "lucide-react";
import type { McqResponse } from "../../types";
import { McqQuiz } from "../quiz/McqQuiz";

export function McqResult({ result }: { result: McqResponse }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <ListChecks className="h-5 w-5 text-primary" />
        <h2 className="text-lg font-semibold">
          {result.questions.length} question{result.questions.length === 1 ? "" : "s"}
        </h2>
      </div>
      <McqQuiz questions={result.questions} />
    </div>
  );
}
