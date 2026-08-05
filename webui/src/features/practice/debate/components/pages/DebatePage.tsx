// src/features/practice/debate/components/pages/DebatePage.tsx
/**
 * Debate Engine page: build a persona, debate it turn by turn, and get the
 * judge's verdict.
 */
"use client";

import { Swords } from "lucide-react";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { FormActions } from "@/features/learning/explainer/components/FormActions";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import {
  InputField,
  SelectField,
  SliderField,
} from "@/features/learning/explainer/components/fields";
import { usePersistedForm } from "@/features/learning/explainer/hooks/usePersistedForm";
import { usePersistedState } from "@/features/learning/explainer/hooks/usePersistedState";
import { useToolRequest } from "@/features/learning/explainer/hooks/useToolRequest";
import { createPersonaAction, debateTurnAction, judgeDebateAction } from "../../actions";
import {
  PersonaFormSchema,
  type DebateSession,
  type PersonaFormValues,
  type PersonaResponse,
  type TurnStrategy,
  type DebateTurnResponse,
  type JudgeResponse,
} from "../../types";
import { sideOptions } from "../../lib/options";
import { DebateBoard } from "../results/DebateBoard";

const STORAGE_KEY = "practice.debate.form.v1";
const SESSION_KEY = "practice.debate.session.v1";

const DEFAULTS: PersonaFormValues = {
  archetype: "Cynical Academic",
  style: "data-driven",
  intensity: 7,
  influences: "Keynes, Behavioral Economics",
  topic: "Universal Basic Income",
  side: "con",
};

export function DebatePage() {
  const persisted = usePersistedForm<PersonaFormValues, PersonaResponse>({
    schema: PersonaFormSchema,
    storageKey: STORAGE_KEY,
    defaults: DEFAULTS,
  });
  const session = usePersistedState<DebateSession | null>({
    key: SESSION_KEY,
    initialValue: null,
  });

  const start = useToolRequest<PersonaFormValues, PersonaResponse>({
    run: createPersonaAction,
    onSuccess: (result) => {
      const values = persisted.form.getValues();
      session.setValue({
        topic: values.topic,
        persona: result.persona,
        side: values.side,
        history: [],
        log: [
          {
            role: "assistant",
            content: `**${result.persona.persona_name}** (${values.side === "con" ? "against" : "for"} "${values.topic}") is ready. Their stance: ${result.persona.overall_stance}.\n\nMake your opening argument.`,
          },
        ],
        lastTurn: null,
        proTranscript: "",
        conTranscript: "",
        complete: false,
        verdict: null,
      });
    },
  });

  const turn = useToolRequest<
    {
      session: DebateSession;
      argument: string;
      strategy: TurnStrategy;
      evidence: string;
    },
    { response: DebateTurnResponse; argument: string; session: DebateSession }
  >({
    run: async ({ session: current, argument, strategy, evidence }) => {
      const response = await debateTurnAction({
        system_prompt: current.persona.system_prompt,
        topic: current.topic,
        history: current.history,
        strategy,
        evidence: evidence || undefined,
        instructions: "Keep the spoken argument concise.",
      });
      return { response, argument, session: current };
    },
    onSuccess: ({ response, argument, session: prev }) => {
      const current = session.value;
      if (!current) return;
      const userTranscript = `${current.side === "pro" ? "CON" : "PRO"}: ${argument}\n\n`;
      const personaTranscript = `${current.side === "pro" ? "PRO" : "CON"}: ${response.spoken_argument}\n\n`;
      session.setValue({
        ...current,
        history: [
          ...current.history,
          { role: "user", content: argument },
          { role: "assistant", content: response.spoken_argument },
        ],
        log: [
          ...current.log,
          { role: "user", content: argument },
          { role: "assistant", content: response.spoken_argument },
        ],
        lastTurn: response,
        proTranscript:
          current.side === "pro" ? current.proTranscript + personaTranscript : current.proTranscript + userTranscript,
        conTranscript:
          current.side === "con" ? current.conTranscript + personaTranscript : current.conTranscript + userTranscript,
      });
    },
  });

  const judge = useToolRequest<{ session: DebateSession }, JudgeResponse>({
    run: async ({ session: current }) =>
      judgeDebateAction({
        topic: current.topic,
        pro_transcript: current.proTranscript,
        con_transcript: current.conTranscript,
      }),
    onSuccess: (result) => {
      const current = session.value;
      if (!current) return;
      session.setValue({ ...current, complete: true, verdict: result });
    },
  });

  const errors = persisted.form.formState.errors;
  const isPending = start.isPending || turn.isPending || judge.isPending;

  const handleNewDebate = () => {
    session.setValue(null);
    persisted.resetDraft();
  };

  const handleTurn = (argument: string, strategy: TurnStrategy, evidence: string) => {
    const current = session.value;
    if (current) turn.execute({ session: current, argument, strategy, evidence });
  };

  const handleJudge = () => {
    const current = session.value;
    if (current) judge.execute({ session: current });
  };

  return (
    <ExplainerPageShell
      title="Debate Engine"
      description="Build a character-driven debate persona with real strategic priorities, go head-to-head turn by turn, and get a judge's verdict."
      headerAction={
        <DraftStatus
          status={persisted.status}
          onReset={handleNewDebate}
          onClear={handleNewDebate}
          disabled={isPending}
        />
      }
      form={
        <form onSubmit={persisted.form.handleSubmit(start.execute)} className="space-y-4">
          <InputField
            label="Archetype"
            htmlFor="debate_archetype"
            placeholder="e.g. Cynical Academic, Aggressive Trial Lawyer"
            disabled={start.isPending}
            {...persisted.form.register("archetype")}
            error={errors.archetype?.message}
          />
          <InputField
            label="Speech Style"
            htmlFor="debate_style"
            placeholder="e.g. sesquipedalian, punchy and short, data-driven"
            disabled={start.isPending}
            {...persisted.form.register("style")}
            error={errors.style?.message}
          />
          <SliderField
            label="Rhetorical Intensity"
            name="intensity"
            htmlFor="debate_intensity"
            control={persisted.form.control}
            min={1}
            max={10}
            formatValue={(value) => `${value}/10`}
            disabled={start.isPending}
          />
          <InputField
            label="Influences"
            htmlFor="debate_influences"
            placeholder="Comma-separated, e.g. Sartre, Game Theory"
            disabled={start.isPending}
            {...persisted.form.register("influences")}
            error={errors.influences?.message}
          />
          <InputField
            label="Debate Topic"
            htmlFor="debate_topic"
            placeholder="e.g. Universal Basic Income"
            disabled={start.isPending}
            {...persisted.form.register("topic")}
            error={errors.topic?.message}
          />
          <SelectField
            label="Persona Side"
            name="side"
            htmlFor="debate_side"
            control={persisted.form.control}
            options={sideOptions}
            disabled={start.isPending}
            error={errors.side?.message}
          />
          <InputField
            label="Custom Constraints (optional)"
            htmlFor="debate_constraints"
            placeholder="e.g. Never uses emojis"
            disabled={start.isPending}
            {...persisted.form.register("custom_constraints")}
            error={errors.custom_constraints?.message}
          />
          <FormActions
            isPending={start.isPending}
            error={start.error}
            submitLabel={session.value ? "Build a new persona" : "Build persona"}
            submitPendingLabel="Crafting the persona…"
          />
        </form>
      }
      result={
        session.value ? (
          <DebateBoard
            session={session.value}
            isPending={isPending}
            error={turn.error ?? judge.error}
            onTurn={handleTurn}
            onJudge={handleJudge}
          />
        ) : (
          <EmptyResult
            icon={Swords}
            title="No persona yet"
            description="Define an archetype, style, and topic, then face your opponent."
          />
        )
      }
    />
  );
}
