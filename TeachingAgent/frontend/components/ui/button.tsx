import * as React from "react";

import { cn } from "@/lib/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost" | "danger";
};

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-xl px-4 py-2.5 text-sm font-semibold tracking-wide transition",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-surge/80 disabled:cursor-not-allowed disabled:opacity-50",
        variant === "primary" && "bg-ember text-white hover:bg-ember/90",
        variant === "ghost" && "bg-white/5 text-dawn hover:bg-white/10",
        variant === "danger" && "bg-red-500 text-white hover:bg-red-400",
        className,
      )}
      {...props}
    />
  );
}
