// src/features/learning/tutor-chat/types/index.ts
/**
 * Zod schemas + TypeScript types for the Tutor Chat API
 * (Backend/learning/tutor_chat/api.md).
 */
import { z } from "zod";

export const ChatMessageSchema = z.object({
  role: z.string(),
  content: z.string(),
});
export type ChatMessage = z.infer<typeof ChatMessageSchema>;

export const EducationalBreakdownSchema = z.object({
  title: z.string(),
  description: z.string(),
});
export type EducationalBreakdown = z.infer<typeof EducationalBreakdownSchema>;

export const ChatRoleSchema = z.enum(["user", "assistant"]);

/** A chat turn as stored in the UI (adds the per-turn concept breakdown). */
export const UiChatMessageSchema = ChatMessageSchema.extend({
  role: ChatRoleSchema,
  breakdown: z.array(EducationalBreakdownSchema).default([]),
});
export type UiChatMessage = z.infer<typeof UiChatMessageSchema>;

export const TutorChatFormSchema = z.object({
  master_topic: z
    .string()
    .trim()
    .min(2, "Master topic is required")
    .max(300),
  additional_context: z.string().trim().max(2000).default(""),
});
export type TutorChatFormValues = z.infer<typeof TutorChatFormSchema>;

export const TutorChatRequestSchema = z.object({
  master_topic: z.string().trim().min(2),
  additional_context: z.string().trim().optional(),
  chat_history: z.array(ChatMessageSchema).default([]),
  user_input: z.string().trim().min(1),
});
export type TutorChatRequest = z.infer<typeof TutorChatRequestSchema>;

export const TutorChatResponseSchema = z.object({
  tutor_response: z.string(),
  educational_breakdown: z.array(EducationalBreakdownSchema).default([]),
  status: z.string().optional(),
});
export type TutorChatResponse = z.infer<typeof TutorChatResponseSchema>;
