/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        coursera: {
          blue: '#0056D2',
          dark: '#00419E',
          light: '#F0F5FF',
          subtleDark: '#0D1B36',
        },
        zinc: {
          925: '#121215',
          950: '#09090B',
        },
      },
    },
  },
  plugins: [],
}
