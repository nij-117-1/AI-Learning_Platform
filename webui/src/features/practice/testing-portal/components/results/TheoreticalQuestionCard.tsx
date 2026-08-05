// src/features/practice/testing-portal/components/results/TheoreticalQuestionCard.tsx
/**
 * A single theoretical question with an inline answer box. Submitting grades
 * the answer through the Performance Grader and renders the feedback inline.
 */
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Loader2 } from "lucide-react";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { evaluateTheoreticalAnswerAction } from "@/features/practice/grader/actions/evaluate";
import { GraderFeedback } from "@/features/practice/grader/components/results/GraderFeedback";
import type { ExpectedLevel, GradingResponse } from "@/features/practice/grader/types";
import type { TheoreticalItem } from "../../types";

interface TheoreticalQuestionCardProps {
  index: number;
  question: TheoreticalItem;
  contextSetting: string;
  expectedLevel: ExpectedLevel;
}

export function TheoreticalQuestionCard({
  index,
  question,
  contextSetting,
  expectedLevel,
}: TheoreticalQuestionCardProps) {
  const [answer, setAnswer] = useState("");
  const tool = useToolRequest<{ answer: string }, GradingResponse>({
    run: ({ answer: text }) =>
      evaluateTheoreticalAnswerAction({
        scenario: contextSetting,
        question_asked: question.question_text,
        target_objective: question.evaluation_criteria,
        expected_level: expectedLevel,
        user_answer_text: text,
      }),
  });

  return (
    <Card>
      <CardContent className="space-y-3 p-5">
        <div className="flex items-start gap-2">
          <span className="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
            {index + 1}
          </span>
          <div className="space-y-1">
            <p className="font-medium">{question.question_text}</p>
            <div className="flex flex-wrap gap-2">
              <span className="rounded-full border border-border bg-muted/40 px-2.5 py-0.5 text-xs font-medium">
                {question.focus_area}
              </span>
              <span className="text-xs text-muted-foreground">
                Great answers cover: {question.evaluation_criteria}
              </span>
            </div>
          </div>
        </div>

        <div className="space-y-2 border-t border-border pt-3">
          <label htmlFor={`theo_answer_${index}`} className="text-sm font-medium">
            Your answer
          </label>
          <Textarea
            id={`theo_answer_${index}`}
            className="min-h-20 resize-none bg-transparent"
            placeholder="Write your answer here, then grade it against the objective."
            value={answer}
            disabled={tool.isPending}
            onChange={(event) => setAnswer(event.target.value)}
          />
          <Button
            type="button"
            size="sm"
            disabled={tool.isPending || !answer.trim()}
            onClick={() => tool.execute({ answer })}
            className="gap-2"
          >
            {tool.isPending ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Grading…
              </>
            ) : (
              "Grade my answer"
            )}
          </Button>
        </div>

        {tool.error && (
          <p role="alert" className="rounded-lg border border-destructive/30 bg-destructive/5 p-3 text-sm text-destructive">
            {tool.error}
          </p>
        )}
        {tool.data && <GraderFeedback result={tool.data} />}
      </CardContent>
    </Card>
  );
}
