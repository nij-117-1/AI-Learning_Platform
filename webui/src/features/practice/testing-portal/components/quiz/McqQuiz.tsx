// src/features/practice/testing-portal/components/quiz/McqQuiz.tsx
/**
 * Interactive MCQ quiz. Users pick an answer for each generated question,
 * then Check Answers reveals correctness (using the provided key) and score.
 */
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { CheckCircle2, RefreshCcw, XCircle } from "lucide-react";
import type { McqItem } from "../../types";

const OPTION_KEYS = ["A", "B", "C", "D"] as const;

export function McqQuiz({ questions }: { questions: McqItem[] }) {
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [checked, setChecked] = useState(false);

  const score = questions.reduce(
    (total, question, index) =>
      total + (answers[index] === question.correct_answer ? 1 : 0),
    0
  );

  const handleCheck = () => setChecked(true);
  const handleReset = () => {
    setAnswers({});
    setChecked(false);
  };

  const allAnswered = questions.every((_, index) => answers[index]);

  return (
    <div className="space-y-4">
      {checked && (
        <Card className={cn(score === questions.length && "border-emerald-500/40")}>
          <CardContent className="flex items-center justify-between p-4">
            <p className="text-sm font-medium">
              Score: {score} / {questions.length}
            </p>
            <Button type="button" variant="outline" size="sm" onClick={handleReset}>
              <RefreshCcw className="h-4 w-4" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      )}

      {questions.map((question, index) => {
        const selected = answers[index];
        const isCorrect = checked && selected === question.correct_answer;
        const isWrong = checked && selected !== undefined && selected !== question.correct_answer;
        const unanswered = checked && selected === undefined;

        return (
          <Card key={index}>
            <CardContent className="space-y-3 p-5">
              <div className="flex items-start gap-2">
                <span className="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                  {index + 1}
                </span>
                <div className="space-y-3">
                  <p className="font-medium">{question.question_text}</p>
                  {isCorrect && (
                    <p className="flex items-center gap-1.5 text-sm font-medium text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="h-4 w-4" />
                      Correct — {question.correct_answer}
                    </p>
                  )}
                  {isWrong && (
                    <p className="flex items-center gap-1.5 text-sm font-medium text-red-600 dark:text-red-400">
                      <XCircle className="h-4 w-4" />
                      Correct answer: {question.correct_answer}
                    </p>
                  )}
                  {unanswered && (
                    <p className="text-sm text-muted-foreground">Not answered</p>
                  )}
                </div>
              </div>

              <div className="grid gap-2">
                {OPTION_KEYS.map((key) => {
                  const isSelected = selected === key;
                  const isKeyCorrect = checked && question.correct_answer === key;
                  return (
                    <button
                      key={key}
                      type="button"
                      disabled={checked}
                      onClick={() => setAnswers((prev) => ({ ...prev, [index]: key }))}
                      className={cn(
                        "flex items-start gap-2 rounded-lg border px-3 py-2 text-left text-sm transition-colors",
                        "hover:border-primary/50",
                        isSelected && "border-primary bg-primary/5",
                        isKeyCorrect && "border-emerald-500/60 bg-emerald-500/10",
                        isSelected && isKeyCorrect && "border-emerald-500/60 bg-emerald-500/10",
                        isSelected && !isKeyCorrect && checked && "border-red-500/60 bg-red-500/10",
                        checked && "cursor-default"
                      )}
                    >
                      <span className="flex size-5 shrink-0 items-center justify-center rounded-full border text-xs font-semibold">
                        {key}
                      </span>
                      <span>{question.options[key]}</span>
                    </button>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        );
      })}

      {!checked && (
        <Button type="button" size="lg" disabled={!allAnswered} onClick={handleCheck} className="w-full">
          Check Answers
        </Button>
      )}
    </div>
  );
}
