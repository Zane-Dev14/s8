import * as React from "react";

import { cn } from "@/lib/utils";

type ProgressProps = {
  value: number;
  className?: string;
};

export function Progress({ value, className }: ProgressProps) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("h-2 w-full rounded-full bg-white/10", className)}>
      <div
        className="h-full rounded-full bg-gradient-to-r from-surge via-moss to-ember transition-all"
        style={{ width: `${clamped}%` }}
      />
    </div>
  );
}
