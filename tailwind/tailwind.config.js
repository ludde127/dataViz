/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../**/*.{html,js}"
  ],
  darkMode: "class",
  safelist: ["dark"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
  },
  daisyui: { themes: true },
  plugins: [require("@tailwindcss/typography"), require("daisyui")]
}