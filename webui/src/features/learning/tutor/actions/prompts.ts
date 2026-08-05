// src/features/learning/tutor/actions/prompts.ts
/**
 * Server Actions for the Adaptive Tutor prompt-template CRUD endpoints
 * (POST/GET /learning/tutor/prompts, GET/DELETE /learning/tutor/prompts/{name}).
 */
"use server";

import {
  PromptActionResponseSchema,
  PromptListResponseSchema,
  PromptResponseSchema,
  PromptSaveSchema,
  type PromptActionResponse,
  type PromptResponse,
  type PromptSaveValues,
} from "../types";
import { deleteJson, getJson, postJson, safeParse, tutorApiUrl } from "../lib/api";

function promptNameUrl(name: string): string {
  return tutorApiUrl(`prompts/${encodeURIComponent(name)}`);
}

export async function listPromptsAction(): Promise<string[]> {
  const raw = await getJson<unknown>(tutorApiUrl("prompts"));
  return safeParse(PromptListResponseSchema, raw, "Invalid prompts list");
}

export async function getPromptAction(name: string): Promise<PromptResponse> {
  const raw = await getJson<unknown>(promptNameUrl(name));
  return safeParse(PromptResponseSchema, raw, "Invalid prompt response");
}

export async function savePromptAction(
  input: PromptSaveValues
): Promise<PromptActionResponse> {
  safeParse(PromptSaveSchema, input, "Invalid prompt payload");
  const raw = await postJson<unknown>(tutorApiUrl("prompts"), {
    name: input.name,
    content: input.content,
  });
  return safeParse(PromptActionResponseSchema, raw, "Invalid prompt save response");
}

export async function deletePromptAction(name: string): Promise<void> {
  await deleteJson<void>(promptNameUrl(name));
}
