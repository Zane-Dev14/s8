import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        dawn: "#ffd9b5",
        ember: "#ff6b35",
        surge: "#00c2ff",
        moss: "#58b368",
        slateglass: "#1f2937",
      },
      boxShadow: {
        surge: "0 0 0 1px rgba(0, 194, 255, 0.35), 0 16px 40px rgba(0, 0, 0, 0.35)",
      },
      backgroundImage: {
        "grid-fade": "radial-gradient(circle at top right, rgba(0,194,255,0.15), transparent 35%), radial-gradient(circle at 10% 10%, rgba(255,107,53,0.22), transparent 32%), linear-gradient(135deg, #0f172a 0%, #111827 60%, #1f2937 100%)",
      },
      fontFamily: {
        display: ["Avenir Next", "Trebuchet MS", "Segoe UI"],
        body: ["Futura", "Gill Sans", "Helvetica Neue"],
        mono: ["IBM Plex Mono", "Menlo", "Consolas"],
      },
      keyframes: {
        "rise-in": {
          "0%": { opacity: "0", transform: "translateY(18px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseedge: {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(255,107,53,0.45)" },
          "50%": { boxShadow: "0 0 0 8px rgba(255,107,53,0)" },
        },
      },
      animation: {
        "rise-in": "rise-in 0.55s ease-out both",
        pulseedge: "pulseedge 1.8s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
