/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      animation: {
        "loop-scroll": "loop-scroll 10s linear infinite"
      },
      keyframes: {
        "loop-scroll": {
          from: {
            transform: "translateX(0%)"
          },
          to: {
            transform: "translateX(calc(-50% - 10px))"
          }
        }
      }
    },
  },
  plugins: [],
}

