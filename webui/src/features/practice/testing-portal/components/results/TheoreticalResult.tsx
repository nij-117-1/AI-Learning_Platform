// src/features/practice/testing-portal/components/results/TheoreticalResult.tsx
/**
 * Lists the generated theoretical questions. Each card lets the user write
 * an answer and grade it with the Performance Grader, using the question's
 * evaluation criteria as the target objective.
 */
"use client";

import { FileQuestion } from "lucide-react";
import type { ExpectedLevel } from "@/features/practice/grader/types";
import type { TheoreticalItem, TheoreticalResponse, TheoreticalFormValues } from "../../types";
import { TheoreticalQuestionCard } from "./TheoreticalQuestionCard";

function expectedLevelFor(difficulty: TheoreticalFormValues["difficulty_level"]): ExpectedLevel {
  switch (difficulty) {
    case "basic":
      return "beginner";
    case "advanced":
    case "architectural":
      return "expert";
    default:
      return "intermediate";
  }
}

interface TheoreticalResultProps {
  result: TheoreticalResponse;
  contextSetting: string;
  difficultyLevel: TheoreticalFormValues["difficulty_level"];
}

export function TheoreticalResult({
  result,
  contextSetting,
  difficultyLevel,
}: TheoreticalResultProps) {
  const expectedLevel = expectedLevelFor(difficultyLevel);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <FileQuestion className="h-5 w-5 text-primary" />
        <h2 className="text-lg font-semibold">
          {result.questions.length} question{result.questions.length === 1 ? "" : "s"}
        </h2>
      </div>
      {result.questions.map((question: TheoreticalItem, index) => (
        <TheoreticalQuestionCard
          key={index}
          index={index}
          question={question}
          contextSetting={contextSetting}
          expectedLevel={expectedLevel}
        />
      ))}
    </div>
  );
}
