/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/templates/**/*.html',
    './src/js/**/*.js',
    './node_modules/flowbite/**/*.js',
  ],
  safelist: [
    'bg-blue-200',
    'bg-gray-800',
  ],
  theme: {
    extend: {
      colors: {
        primary: "#033043",
        secondary: "#4694aa",
        medium: "#346e7f",
        accent: "#0a578b",
        darkPrimary: "#0f1a2d",
        darkSecondary: "#1e2f3f",
        darkAccent: "#1C6C83",
        darkMedium: "#2b3f50",
        darkLightAccent: "#34849B",
      }
    },
  },
  plugins: [require('flowbite/plugin')],
};
