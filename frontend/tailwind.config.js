/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        blue: {
          500: "#5D9CEC", // Azul claro para links e botões
          600: "#4A8BC2", // Azul para hover
        },
        gray: {
          100: "#F0F3F4", // Fundo da sidebar
          600: "#7F8C8D", // Texto secundário
        },
        green: {
          400: "#34B9A1", // Verde claro para botões
        },
        white: "#FFFFFF", // Branco
      },
    },
  },
  plugins: [
    require('flowbite/plugin'), // Adicione o Flowbite como plugin
  ],
};
