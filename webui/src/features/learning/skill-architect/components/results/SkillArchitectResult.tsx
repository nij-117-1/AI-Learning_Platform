// src/features/learning/skill-architect/components/results/SkillArchitectResult.tsx
/**
 * Renders the Skill Architect output as a composed Markdown document: the core
 * philosophy, the level-wise skill tree, the critical bottleneck, and tactical
 * navigation advice.
 */
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { MarkdownContent } from "@/components/ui/markdown-content";
import type { SkillArchitectResponse } from "../../types";

function bulletList(items: string[]): string {
  return items.map((item) => `- ${item}`).join("\n");
}

export function SkillArchitectResult({ result }: { result: SkillArchitectResponse }) {
  const treeMarkdown = result.skill_tree_levels
    .map((level, index) => {
      const parts: string[] = [`### ${index + 1}. ${level.level_name}`];
      if (level.root_skills.length) {
        parts.push(`**Root skills:**\n${bulletList(level.root_skills)}`);
      }
      if (level.how_it_works.trim()) {
        parts.push(level.how_it_works.trim());
      }
      if (level.proof_of_mastery.trim()) {
        parts.push(`- **Proof of mastery:** ${level.proof_of_mastery.trim()}`);
      }
      if (level.unlock_condition.trim()) {
        parts.push(`- **Unlock condition:** ${level.unlock_condition.trim()}`);
      }
      return parts.join("\n\n");
    })
    .join("\n\n");

  const sections: string[] = [];
  if (result.core_philosophy.trim()) {
    sections.push(`## Core Philosophy\n\n${result.core_philosophy.trim()}`);
  }
  sections.push(
    treeMarkdown
      ? `## The Skill Tree\n\n${treeMarkdown}`
      : "## The Skill Tree\n\n_No skill tree levels returned._"
  );
  if (result.critical_bottleneck.trim()) {
    sections.push(`## Critical Bottleneck\n\n${result.critical_bottleneck.trim()}`);
  }
  if (result.strategic_navigation.trim()) {
    sections.push(`## Strategic Navigation\n\n${result.strategic_navigation.trim()}`);
  }

  return (
    <Card>
      <CardContent className="p-5">
        <MarkdownContent content={sections.join("\n\n---\n\n")} />
      </CardContent>
    </Card>
  );
}
