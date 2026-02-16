import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        finny: {
          primary: "#6C5CE7",
          secondary: "#00CEC9",
          accent: "#FDCB6E",
          dark: "#2D3436",
          light: "#F8F9FA",
          success: "#00B894",
          warning: "#E17055",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
