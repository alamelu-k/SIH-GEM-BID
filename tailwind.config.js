/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gem: {
          dark: '#0f172a',      // Primary deep slate
          navy: '#1e293b',      // Secondary slate
          accent: '#1d4ed8',    // Official institutional blue
          light: '#f8fafc',     // Clean background
          border: '#e2e8f0',    // Clean subtle dividers
        },
        status: {
          pass: '#15803d',       // Emerald 700
          'pass-bg': '#f0fdf4',  // Emerald 50
          fail: '#b91c1c',       // Red 700
          'fail-bg': '#fef2f2',  // Red 50
          missing: '#b45309',    // Amber 700
          'missing-bg': '#fffbeb',
          mismatch: '#c2410c',   // Orange 700
          'mismatch-bg': '#fff7ed',
          review: '#6b21a8',     // Purple 700
          'review-bg': '#faf5ff',
          unavailable: '#475569',
          'unavailable-bg': '#f1f5f9'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      }
    },
  },
  plugins: [],
}
