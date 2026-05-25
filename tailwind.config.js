/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  // Theme switching is driven by a `dark` class on <html>. See src/lib/theme.tsx.
  darkMode: "class",
  theme: { extend: {} },
  plugins: []
};
