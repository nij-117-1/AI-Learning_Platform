// src/features/tools/diagram/components/results/DiagramResult.tsx
/**
 * Renders the Diagram Generator output: the explanation message and the
 * generated diagram code in a copyable code block.
 */
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { CodeBlock } from "@/components/ui/code-block";
import { MarkdownContent } from "@/components/ui/markdown-content";
import type { DiagramResponse } from "../../types";

export function DiagramResult({ result }: { result: DiagramResponse }) {
  const filename = result.format === "mermaid" ? "diagram.mmd" : "diagram.drawio.xml";

  return (
    <div className="space-y-4">
      {result.message.trim() && (
        <Card>
          <CardContent className="p-5">
            <MarkdownContent content={result.message} />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="space-y-3 p-5">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">Diagram code</h3>
            <span className="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              {result.format}
            </span>
          </div>
          <CodeBlock code={result.code} language="text" filename={filename} />
        </CardContent>
      </Card>
    </div>
  );
}
