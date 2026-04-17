/** @type {import('tailwindcss').Config} */
module.exports = {
  // 👇 C'est ICI le problème. Copie-colle cette ligne :
  content: ["./templates/**/*.html", "./static/**/*.js"],
  
  theme: {
    extend: {},
  },
  plugins: [],
}