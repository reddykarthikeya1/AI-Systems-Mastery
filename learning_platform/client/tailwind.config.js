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
        academy: {
          blue: '#0056D2',
          dark: '#00419E',
          light: '#F0F5FF',
          subtleDark: '#0D1B36',
        },
        zinc: {
          925: '#121215',
          950: '#09090B',
        },
        bg: {
          DEFAULT: 'var(--bg)',
          subtle: 'var(--bg-subtle)',
        },
        surface: {
          DEFAULT: 'var(--surface)',
          raised: 'var(--surface-raised)',
          overlay: 'var(--surface-overlay)',
        },
        fg: {
          DEFAULT: 'var(--fg)',
          muted: 'var(--fg-muted)',
          subtle: 'var(--fg-subtle)',
        },
        border: {
          DEFAULT: 'var(--border)',
          subtle: 'var(--border-subtle)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          hover: 'var(--accent-hover)',
          subtle: 'var(--accent-subtle)',
          fg: 'var(--accent-fg)',
        },
        success: {
          DEFAULT: 'var(--success)',
          subtle: 'var(--success-subtle)',
        },
        warning: {
          DEFAULT: 'var(--warning)',
          subtle: 'var(--warning-subtle)',
        },
        danger: {
          DEFAULT: 'var(--danger)',
          subtle: 'var(--danger-subtle)',
        },
      },
    },
  },
  plugins: [],
}
