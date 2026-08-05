// src/features/tools/vision-converter/components/results/VisionConverterResult.tsx
/**
 * Renders the Vision Converter output: the AI-generated Markdown in a
 * card so tables, headers, and lists render faithfully.
 */
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { MarkdownContent } from "@/components/ui/markdown-content";
import type { VisionConversionResponse } from "../../types";

export function VisionConverterResult({ result }: { result: VisionConversionResponse }) {
  return (
    <Card>
      <CardContent className="p-5">
        <MarkdownContent content={result.markdown_output} />
      </CardContent>
    </Card>
  );
}
