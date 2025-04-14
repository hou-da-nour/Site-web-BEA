// tailwind.config.js
module.exports = {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}", // assure-toi que tes fichiers React sont inclus
    ],
    theme: {
      extend: {
        animation: {
          'spin-custom': 'spin988 2s linear infinite',
        },
        keyframes: {
          spin988: {
            '0%': { transform: 'scale(1) rotate(0deg)' },
            '20%, 25%': { transform: 'scale(1.3) rotate(90deg)' },
            '45%, 50%': { transform: 'scale(1) rotate(180deg)' },
            '70%, 75%': { transform: 'scale(1.3) rotate(270deg)' },
            '95%, 100%': { transform: 'scale(1) rotate(360deg)' },
          },
        },
      },
    },
    plugins: [],
  }
  