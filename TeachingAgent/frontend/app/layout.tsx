import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "B2Bi Brutal Tutor",
  description: "Local-first adaptive tutor for bootcamp compression",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
