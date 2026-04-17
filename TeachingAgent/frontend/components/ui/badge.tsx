import * as React from "react";

import { cn } from "@/lib/utils";

type BadgeProps = React.HTMLAttributes<HTMLSpanElement> & {
  tone?: "neutral" | "success" | "warning" | "danger";
};

export function Badge({ className, tone = "neutral", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold uppercase tracking-wide",
        tone === "neutral" && "bg-white/10 text-slate-200",
        tone === "success" && "bg-moss/25 text-moss",
        tone === "warning" && "bg-ember/20 text-ember",
        tone === "danger" && "bg-red-500/20 text-red-300",
        className,
      )}
      {...props}
    />
  );
}
