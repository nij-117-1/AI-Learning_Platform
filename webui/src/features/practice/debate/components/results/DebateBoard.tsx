// src/features/practice/debate/components/results/DebateBoard.tsx
/**
 * The in-progress debate board: persona profile, transcript of exchanges, a
 * turn composer (argument + strategy + evidence), and an end-and-judge flow.
 */
"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Loader2, Gavel, Crosshair, MessageSquareQuote } from "lucide-react";
import { ChatTranscript } from "@/features/practice/components/chat/ChatTranscript";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import type { DebateSession, TurnStrategy } from "../../types";
import { strategyOptions } from "../../lib/options";
import { DebateVerdict } from "./DebateVerdict";

interface DebateBoardProps {
  session: DebateSession;
  isPending: boolean;
  error: string | null;
  onTurn: (argument: string, strategy: TurnStrategy, evidence: string) => void;
  onJudge: () => void;
}

export function DebateBoard({ session, isPending, error, onTurn, onJudge }: DebateBoardProps) {
  const [argument, setArgument] = useState("");
  const [strategy, setStrategy] = useState<TurnStrategy>("counter");
  const [evidence, setEvidence] = useState("");

  const { persona } = session;
  const canSubmit = argument.trim().length > 0 && !isPending;

  const submit = () => {
    if (!canSubmit) return;
    onTurn(argument.trim(), strategy, evidence.trim());
    setArgument("");
    setEvidence("");
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2 text-sm">
          <Badge>{persona.persona_name}</Badge>
          <span
            className={cn(
              "rounded-full border px-2.5 py-0.5 font-medium capitalize",
              session.side === "con"
                ? "border-rose-500/30 text-rose-600 dark:text-rose-400"
                : "border-emerald-500/30 text-emerald-600 dark:text-emerald-400"
            )}
          >
            {session.side === "con" ? "Against" : "For"}: {session.topic}
          </span>
        </div>
        {!session.complete && (
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="gap-1.5"
            disabled={isPending}
            onClick={onJudge}
          >
            <Gavel className="h-4 w-4" />
            End &amp; judge
          </Button>
        )}
      </div>

      <Card>
        <CardContent className="grid gap-3 p-4 text-sm sm:grid-cols-3">
          <div className="space-y-1">
            <p className="text-xs font-semibold text-muted-foreground">Stance</p>
            <p className="capitalize">{persona.overall_stance}</p>
          </div>
          <div className="space-y-1">
            <p className="text-xs font-semibold text-muted-foreground">Strategic priorities</p>
            <ul className="list-inside list-disc text-muted-foreground">
              {persona.strategic_priorities.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="space-y-1">
            <p className="text-xs font-semibold text-muted-foreground">Quirks</p>
            <ul className="list-inside list-disc text-muted-foreground">
              {persona.linguistic_quirks.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>

      {session.verdict && <DebateVerdict verdict={session.verdict} />}

      {session.lastTurn && !session.complete && (
        <Card>
          <CardContent className="space-y-3 p-4">
            <p className="flex items-center gap-1.5 text-sm font-semibold">
              <Crosshair className="h-4 w-4 text-primary" />
              Turn breakdown
            </p>
            <div className="grid gap-3 text-sm sm:grid-cols-2">
              <div className="rounded-lg bg-muted/50 p-3">
                <p className="text-xs font-medium text-muted-foreground">Opponent analysis</p>
                <p className="mt-0.5">{session.lastTurn.opponent_analysis}</p>
              </div>
              <div className="rounded-lg bg-muted/50 p-3">
                <p className="text-xs font-medium text-muted-foreground">Core claim</p>
                <p className="mt-0.5">{session.lastTurn.core_claim}</p>
              </div>
              <div className="rounded-lg bg-muted/50 p-3 sm:col-span-2">
                <p className="text-xs font-medium text-muted-foreground">Reasoning &amp; evidence</p>
                <p className="mt-0.5">{session.lastTurn.reasoning_and_evidence}</p>
              </div>
              <div className="flex flex-wrap gap-1.5 sm:col-span-2">
                {session.lastTurn.rhetorical_devices.map((device) => (
                  <Badge key={device} variant="outline">
                    {device}
                  </Badge>
                ))}
              </div>
              <div className="rounded-lg border border-primary/20 bg-primary/5 p-3 sm:col-span-2">
                <p className="flex items-center gap-1.5 text-xs font-medium text-primary">
                  <MessageSquareQuote className="h-3.5 w-3.5" />
                  Closing question
                </p>
                <p className="mt-0.5">{session.lastTurn.closing_question}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="p-0">
          <ChatTranscript
            messages={session.log}
            isPending={isPending}
            emptyTitle="Debate started"
            emptyDescription={`${persona.persona_name} is waiting for your opening argument.`}
          />

          {!session.complete && (
            <div className="space-y-3 border-t p-3">
              <div className="flex items-end gap-2">
                <Input
                  value={evidence}
                  onChange={(event) => setEvidence(event.target.value)}
                  placeholder="Optional evidence / facts to anchor this turn"
                  disabled={isPending}
                  className="flex-1 bg-transparent"
                />
              </div>
              <Textarea
                value={argument}
                onChange={(event) => setArgument(event.target.value)}
                placeholder="Make your argument to the opponent…"
                disabled={isPending}
                className="min-h-24 resize-none bg-transparent"
              />
              <div className="flex items-center gap-2">
                <div className="w-44">
                  <Select value={strategy} onValueChange={(value) => setStrategy(value as TurnStrategy)} disabled={isPending}>
                    <SelectTrigger id="debate_strategy" className="w-full">
                      <SelectValue placeholder="Strategy" />
                    </SelectTrigger>
                    <SelectContent>
                      {strategyOptions.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <Button
                  type="button"
                  onClick={submit}
                  disabled={!canSubmit}
                  className="gap-1.5"
                >
                  {isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Gavel className="h-4 w-4" />
                  )}
                  Deliver argument
                </Button>
              </div>
              {error && (
                <p role="alert" className="text-sm text-destructive">
                  {error}
                </p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
