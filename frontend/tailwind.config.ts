import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: "#0f1117",
          raised: "#161921",
          overlay: "#1c1f2b",
        },
        accent: {
          DEFAULT: "#6366f1",
          hover: "#818cf8",
        },
        border: {
          DEFAULT: "#2a2d3a",
        },
      },
    },
  },
  plugins: [],
};
export default config;
