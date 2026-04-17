"use client";

import { useEffect, useState } from "react";

import type { InteractiveTeachDiagram } from "@/lib/types";
import { resolveApiUrl } from "@/lib/api";

export function DiagramViewer({ diagrams }: { diagrams: InteractiveTeachDiagram[] }) {
  const [renderedMermaid, setRenderedMermaid] = useState<Record<string, string>>({});

  useEffect(() => {
    let active = true;

    async function renderMermaidDiagrams() {
      const items = diagrams
        .map((diagram, index) => ({ diagram, index }))
        .filter(({ diagram }) => Boolean(diagram.mermaid_code?.trim()));

      if (!items.length) {
        setRenderedMermaid({});
        return;
      }

      const mermaid = (await import("mermaid")).default;
      mermaid.initialize({ startOnLoad: false, securityLevel: "loose", theme: "default" });

      const nextState: Record<string, string> = {};
      for (const { diagram, index } of items) {
        const key = `${diagram.title}-${index}`;
        try {
          const { svg } = await mermaid.render(`teach-diagram-${index}-${Date.now()}`, diagram.mermaid_code ?? "");
          nextState[key] = svg;
        } catch {
          nextState[key] = "";
        }
      }

      if (active) {
        setRenderedMermaid(nextState);
      }
    }

    void renderMermaidDiagrams();
    return () => {
      active = false;
    };
  }, [diagrams]);

  if (!diagrams.length) {
    return (
      <div className="rounded-xl border border-dashed border-white/20 bg-ink/40 p-4 text-sm text-slate-300">
        No diagram found for this concept yet. Uploading more visuals in your ZIP improves this section.
      </div>
    );
  }

  return (
    <div className="grid gap-3 md:grid-cols-2">
      {diagrams.map((diagram, index) => {
        const key = `${diagram.title}-${index}`;
        const svg = renderedMermaid[key];
        const hasMermaid = Boolean(diagram.mermaid_code?.trim());

        return (
          <figure key={`${diagram.image_url}-${diagram.title}-${index}`} className="overflow-hidden rounded-xl border border-white/10 bg-ink/40">
            {hasMermaid ? (
              <div className="h-48 w-full overflow-auto bg-white p-3">
                {svg ? (
                  <div dangerouslySetInnerHTML={{ __html: svg }} />
                ) : (
                  <pre className="text-xs text-slate-700 whitespace-pre-wrap">{diagram.mermaid_code}</pre>
                )}
              </div>
            ) : (
              <img
                src={resolveApiUrl(diagram.image_url)}
                alt={diagram.title}
                className="h-48 w-full object-cover"
                loading="lazy"
              />
            )}
            <figcaption className="space-y-1 p-3">
              <p className="text-sm font-semibold text-dawn">{diagram.title}</p>
              <p className="text-xs text-slate-300">{diagram.description}</p>
              <p className="text-[11px] text-slate-400">{diagram.source_path}</p>
            </figcaption>
          </figure>
        );
      })}
    </div>
  );
}
