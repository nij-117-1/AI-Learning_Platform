// src/features/practice/riddle/components/results/RiddleResult.tsx
/**
 * Displays the generated riddle, an answer box, and the evaluation feedback.
 * The solution is only revealed after the user has answered.
 */
"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { MarkdownContent } from "@/components/ui/markdown-content";
import { AlertTriangle, Brain, CheckCircle2, Eye, Lightbulb, Loader2, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { RiddleEvaluationResponse, RiddleResponse } from "../../types";

interface RiddleResultProps {
  riddle: RiddleResponse;
  evaluation: RiddleEvaluationResponse | null;
  userAnswer: string;
  isPending: boolean;
  error: string | null;
  onAnswerChange: (answer: string) => void;
  onEvaluate: (answer: string) => void;
}

export function RiddleResult({
  riddle,
  evaluation,
  userAnswer,
  isPending,
  error,
  onAnswerChange,
  onEvaluate,
}: RiddleResultProps) {
  const [showSolution, setShowSolution] = useState(false);

  return (
    <div className="space-y-4">
      <Card>
        <CardContent className="space-y-4 p-5">
          <div className="flex items-start gap-2">
            <Brain className="mt-0.5 h-5 w-5 shrink-0 text-primary" />
            <MarkdownContent content={riddle.riddle_text} />
          </div>

          <div className="space-y-1.5 rounded-lg border border-border bg-muted/40 p-3">
            <p className="flex items-center gap-1.5 text-sm font-semibold">
              <Lightbulb className="h-4 w-4 text-amber-500" />
              Mental hook being trained
            </p>
            <p className="text-sm text-muted-foreground">{riddle.cognitive_trigger}</p>
          </div>

          {!evaluation ? (
            <div className="space-y-2">
              <Textarea
                value={userAnswer}
                onChange={(event) => onAnswerChange(event.target.value)}
                placeholder="Your answer (or ask for a hint)…"
                disabled={isPending}
                className="min-h-24 resize-none bg-transparent"
              />
              {error && (
                <p role="alert" className="flex items-center gap-1.5 text-sm text-destructive">
                  <AlertTriangle className="h-4 w-4" />
                  {error}
                </p>
              )}
              <Button
                type="button"
                size="lg"
                disabled={!userAnswer.trim() || isPending}
                onClick={() => onEvaluate(userAnswer)}
                className="w-full gap-2"
              >
                {isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Checking answer…
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="h-4 w-4" />
                    Submit answer
                  </>
                )}
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <span
                className={cn(
                  "inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-sm font-medium",
                  evaluation.is_correct
                    ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
                    : "border-red-500/30 bg-red-500/10 text-red-600 dark:text-red-400"
                )}
              >
                {evaluation.is_correct ? (
                  <CheckCircle2 className="h-4 w-4" />
                ) : (
                  <XCircle className="h-4 w-4" />
                )}
                {evaluation.is_correct ? "Correct!" : "Not quite"}
              </span>
              <div className="space-y-1.5">
                <p className="text-sm font-semibold">Feedback</p>
                <MarkdownContent content={evaluation.feedback} className="text-sm" />
              </div>
              <div className="space-y-1.5 rounded-lg border border-primary/20 bg-primary/5 p-3">
                <p className="text-sm font-semibold">Shift your perspective</p>
                <p className="text-sm">{evaluation.thought_redirection}</p>
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                className="gap-2"
                onClick={() => setShowSolution((value) => !value)}
              >
                <Eye className="h-4 w-4" />
                {showSolution ? "Hide solution" : "Reveal solution"}
              </Button>
              {showSolution && (
                <div className="space-y-1.5 rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-3">
                  <p className="text-sm font-semibold">Solution</p>
                  <MarkdownContent content={riddle.solution} className="text-sm" />
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
