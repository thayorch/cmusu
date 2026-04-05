/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        kanit: ['Kanit', 'Noto Sans Thai', 'sans-serif'],
        mono: ['Space Mono', 'monospace'],
      },
      colors: {
        bg: '#F0EFFF',
        purple: { DEFAULT: '#A259FF', soft: '#EDE0FF', light: '#F5EEFF' },
        blue:   { DEFAULT: '#5BC8FF', soft: '#DBF3FF', light: '#EFF9FF' },
        pink:   { DEFAULT: '#FF6EC7', soft: '#FFD6F0', light: '#FFF0F9' },
        yellow: { DEFAULT: '#FFD166', soft: '#FFF3D0', light: '#FFFBEE' },
        mint:   { DEFAULT: '#06D6A0', soft: '#D0FAF0', light: '#EDFDF8' },
        orange: { DEFAULT: '#FF9A5C', soft: '#FFE5D3', light: '#FFF5EF' },
        dark:   '#1A1040',
        muted:  '#8B7BAE',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      animation: {
        'float-blob': 'floatBlob 10s ease-in-out infinite',
        'bounce-in': 'bounceIn 0.7s cubic-bezier(0.34,1.56,0.64,1) both',
        'slide-up': 'slideUp 0.6s ease both',
        wiggle: 'wiggle 3s ease-in-out infinite',
        ticker: 'ticker 28s linear infinite',
        'spin-slow': 'spinSlow 20s linear infinite',
        'pulse-dot': 'pulseDot 1.5s ease infinite',
      },
    },
  },
  plugins: [],
}
