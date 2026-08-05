// src/features/learning/tutor-chat/components/pages/TutorChatPage.tsx
/**
 * Tutor Chat page: a topic-scoped, multi-turn chatbot. Settings (master topic +
 * context) live in the left column, the conversation (persisted to localStorage,
 * passed back to the backend each turn) in the right.
 */
"use client";

import { useCallback, useState, useTransition } from "react";
import { MessagesSquare } from "lucide-react";
import { usePersistedState } from "@/features/learning/explainer/hooks/usePersistedState";
import { ExplainerPageShell } from "@/features/learning/explainer/components/ExplainerPageShell";
import { DraftStatus } from "@/features/learning/explainer/components/DraftStatus";
import { EmptyResult } from "@/features/learning/explainer/components/EmptyResult";
import { InputField, TextareaField } from "@/features/learning/explainer/components/fields";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Eraser } from "lucide-react";
import { tutorChatAction } from "../../actions/chat";
import type { UiChatMessage } from "../../types";
import { ChatTranscript } from "../chat/ChatTranscript";
import { ChatComposer } from "../chat/ChatComposer";

const SETTINGS_KEY = "learning.tutor-chat.settings.v1";
const HISTORY_KEY = "learning.tutor-chat.history.v1";
const DRAFT_KEY = "learning.tutor-chat.draft.v1";

interface ChatSettings {
  master_topic: string;
  additional_context: string;
}

const DEFAULT_SETTINGS: ChatSettings = {
  master_topic: "Quantum Physics",
  additional_context: "I am a high school student with a basic understanding of classical mechanics. Use analogies.",
};

export function TutorChatPage() {
  const settings = usePersistedState<ChatSettings>({
    key: SETTINGS_KEY,
    initialValue: DEFAULT_SETTINGS,
  });
  const history = usePersistedState<UiChatMessage[]>({
    key: HISTORY_KEY,
    initialValue: [],
  });
  const draft = usePersistedState<string>({
    key: DRAFT_KEY,
    initialValue: "",
  });

  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const handleSend = useCallback(() => {
    const userInput = draft.value.trim();
    if (!userInput || isPending) return;
    if (!settings.value.master_topic.trim()) {
      setError("Set a master topic before starting the conversation.");
      return;
    }

    const userMessage: UiChatMessage = { role: "user", content: userInput, breakdown: [] };
    const historyWithUser = [...history.value, userMessage];
    history.setValue(historyWithUser);
    draft.setValue("");
    setError(null);

    startTransition(async () => {
      try {
        const response = await tutorChatAction({
          master_topic: settings.value.master_topic.trim(),
          additional_context: settings.value.additional_context.trim() || undefined,
          chat_history: historyWithUser.map((message) => ({
            role: message.role,
            content: message.content,
          })),
          user_input: userInput,
        });
        const assistantMessage: UiChatMessage = {
          role: "assistant",
          content: response.tutor_response,
          breakdown: response.educational_breakdown,
        };
        history.setValue((current) => [...current, assistantMessage]);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Something went wrong. Please try again."
        );
      }
    });
  }, [draft, history, isPending, settings.value]);

  const handleNewConversation = useCallback(() => {
    history.setValue([]);
    draft.setValue("");
    setError(null);
  }, [history, draft]);

  return (
    <ExplainerPageShell
      title="Tutor Chat"
      description="A topic-scoped tutor that keeps your context and previous turns in mind, replying with a personalized explanation and a concept breakdown each time."
      headerAction={
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleNewConversation}
            disabled={isPending || history.value.length === 0}
            className="gap-1.5"
          >
            <Eraser className="h-3.5 w-3.5" />
            New Conversation
          </Button>
          <DraftStatus
            status={history.status}
            onReset={handleNewConversation}
            onClear={handleNewConversation}
            disabled={isPending}
          />
        </div>
      }
      form={
        <div className="space-y-4">
          <InputField
            label="Master Topic"
            htmlFor="master_topic"
            placeholder="e.g. Quantum Physics"
            value={settings.value.master_topic}
            onChange={(event) =>
              settings.setValue((current) => ({ ...current, master_topic: event.target.value }))
            }
            disabled={isPending}
          />
          <TextareaField
            label="Your Background & Context"
            htmlFor="additional_context"
            placeholder="Optional — background, goals, or learning style…"
            hint="Optional. Saved locally and included with every turn."
            value={settings.value.additional_context}
            onChange={(event) =>
              settings.setValue((current) => ({
                ...current,
                additional_context: event.target.value,
              }))
            }
            disabled={isPending}
          />
        </div>
      }
      result={
        <Card>
          <CardContent className="p-0">
            {history.value.length === 0 && !isPending ? (
              <div className="p-5">
                <EmptyResult
                  icon={MessagesSquare}
                  title="Start a conversation"
                  description="Set a master topic, then ask your first question to begin chatting with your personal tutor."
                />
              </div>
            ) : (
              <div>
                <ChatTranscript messages={history.value} isPending={isPending} />
                {error && (
                  <div
                    role="alert"
                    className="mx-3 mb-1 flex items-start gap-2 rounded-lg border border-destructive/30 bg-destructive/5 p-3 text-sm text-destructive"
                  >
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                    <span>{error}</span>
                  </div>
                )}
                <ChatComposer
                  value={draft.value}
                  onChange={draft.setValue}
                  onSubmit={handleSend}
                  isPending={isPending}
                  placeholder="Ask a follow-up question…"
                />
              </div>
            )}
          </CardContent>
        </Card>
      }
    />
  );
}
