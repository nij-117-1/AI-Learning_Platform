// src/features/learning/projects/components/results/ProjectRecommenderResult.tsx
/**
 * Renders the Project Recommender output as a composed Markdown document: each
 * project with its description, concepts, prerequisites, deliverables, and
 * stretch goals, plus top-level advice.
 */
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { MarkdownContent } from "@/components/ui/markdown-content";
import type { ProjectRecommenderResponse } from "../../types";

function bulletList(items: string[]): string {
  return items.map((item) => `- ${item}`).join("\n");
}

export function ProjectRecommenderResult({ result }: { result: ProjectRecommenderResponse }) {
  const projectsMarkdown = result.projects
    .map((project, index) => {
      const parts: string[] = [`### ${index + 1}. ${project.title}`, project.description.trim()];
      if (typeof project.estimated_hours === "number") {
        parts.push(`**Estimated:** ${project.estimated_hours}h`);
      }
      if (project.key_concepts.length) {
        parts.push(`**Key concepts:**\n${bulletList(project.key_concepts)}`);
      }
      if (project.prerequisites.length) {
        parts.push(`**Prerequisites:**\n${bulletList(project.prerequisites)}`);
      }
      if (project.deliverables.length) {
        parts.push(`**Deliverables:**\n${bulletList(project.deliverables)}`);
      }
      if (project.stretch_goals.length) {
        parts.push(`**Stretch goals:**\n${bulletList(project.stretch_goals)}`);
      }
      return parts.join("\n\n");
    })
    .join("\n\n");

  const sections: string[] = [
    projectsMarkdown
      ? `## Recommended Projects\n\n${projectsMarkdown}`
      : "## Recommended Projects\n\n_No projects returned._",
  ];
  if (result.advice?.trim()) {
    sections.push(`## Advice\n\n${result.advice}`);
  }

  return (
    <Card>
      <CardContent className="p-5">
        <MarkdownContent content={sections.join("\n\n---\n\n")} />
      </CardContent>
    </Card>
  );
}
