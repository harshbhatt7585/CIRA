/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0B3C5D',
          hover: '#082d47',
        },
        secondary: {
          DEFAULT: '#328CC1',
          hover: '#27709b',
        },
        appBg: '#F0F2F5',
        surface: '#FFFFFF',
        textDark: '#1D2731',
        alertRed: '#DC2626',
      }
    },
  },
  plugins: [],
}
