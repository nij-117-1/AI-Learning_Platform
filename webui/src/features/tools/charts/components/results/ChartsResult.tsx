// src/features/tools/charts/components/results/ChartsResult.tsx
/**
 * Renders the Chart.js Generator output: the explanation message and the
 * generated HTML/JS code block, ready to copy into a frontend.
 */
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { CodeBlock } from "@/components/ui/code-block";
import { MarkdownContent } from "@/components/ui/markdown-content";
import type { ChartResponse } from "../../types";

export function ChartsResult({ result }: { result: ChartResponse }) {
  return (
    <div className="space-y-4">
      {result.answer_message.trim() && (
        <Card>
          <CardContent className="p-5">
            <MarkdownContent content={result.answer_message} />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="space-y-3 p-5">
          <h3 className="text-sm font-semibold">Chart.js code</h3>
          <CodeBlock
            code={result.chart_div_code}
            language="javascript"
            filename="chart.html"
          />
        </CardContent>
      </Card>
    </div>
  );
}
