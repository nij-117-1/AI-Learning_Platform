// src/features/practice/puzzle/components/results/PuzzleResult.tsx
/**
 * Displays the generated puzzle with its persona, an answer box, and the
 * evaluation (accuracy, feedback, hint redirection, metacognitive prompt).
 * The solution is revealed only after the user answers.
 */
"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { MarkdownContent } from "@/components/ui/markdown-content";
import {
  AlertTriangle,
  Brain,
  CheckCircle2,
  Eye,
  Lightbulb,
  Loader2,
  Sparkles,
  Target,
  XCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { PuzzleEvaluationResponse, PuzzleResponse } from "../../types";

interface PuzzleResultProps {
  puzzle: PuzzleResponse;
  evaluation: PuzzleEvaluationResponse | null;
  userAnswer: string;
  isPending: boolean;
  error: string | null;
  onAnswerChange: (answer: string) => void;
  onEvaluate: (answer: string) => void;
}

export function PuzzleResult({
  puzzle,
  evaluation,
  userAnswer,
  isPending,
  error,
  onAnswerChange,
  onEvaluate,
}: PuzzleResultProps) {
  const [showSolution, setShowSolution] = useState(false);
  const accuracyPct = evaluation ? Math.round(evaluation.accuracy_score * 100) : 0;

  return (
    <div className="space-y-4">
      <Card>
        <CardContent className="space-y-4 p-5">
          <div className="flex items-start gap-2 rounded-lg border border-border bg-muted/40 p-3">
            <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
            <p className="text-sm italic text-muted-foreground">{puzzle.puzzler_persona}</p>
          </div>

          <div className="flex items-start gap-2">
            <Brain className="mt-0.5 h-5 w-5 shrink-0 text-primary" />
            <MarkdownContent content={puzzle.puzzle_text} />
          </div>

          <div className="space-y-1.5 rounded-lg border border-border bg-muted/40 p-3">
            <p className="flex items-center gap-1.5 text-sm font-semibold">
              <Lightbulb className="h-4 w-4 text-amber-500" />
              Cognitive trigger
            </p>
            <p className="text-sm text-muted-foreground">{puzzle.cognitive_trigger}</p>
          </div>

          {!evaluation ? (
            <div className="space-y-2">
              <Textarea
                value={userAnswer}
                onChange={(event) => onAnswerChange(event.target.value)}
                placeholder="Your answer…"
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
                    Evaluating…
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
              <div className="flex flex-wrap items-center gap-3">
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
                <span className="inline-flex items-center gap-1.5 text-sm font-medium">
                  <Target className="h-4 w-4 text-primary" />
                  Accuracy: {accuracyPct}%
                </span>
              </div>
              <div className="space-y-1.5">
                <p className="text-sm font-semibold">Feedback</p>
                <MarkdownContent content={evaluation.evaluation_feedback} className="text-sm" />
              </div>
              {evaluation.hint_redirection && (
                <div className="space-y-1.5 rounded-lg border border-primary/20 bg-primary/5 p-3">
                  <p className="text-sm font-semibold">Nudge toward the right path</p>
                  <p className="text-sm">{evaluation.hint_redirection}</p>
                </div>
              )}
              <div className="space-y-1.5 rounded-lg border border-amber-500/20 bg-amber-500/5 p-3">
                <p className="text-sm font-semibold">Rethink it</p>
                <p className="text-sm">{evaluation.metacognitive_prompt}</p>
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
                  <p className="text-sm font-semibold">Solution &amp; breakdown</p>
                  <MarkdownContent content={puzzle.solution} className="text-sm" />
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
