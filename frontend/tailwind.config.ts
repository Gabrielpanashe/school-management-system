import type { Config } from "tailwindcss";

export default {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                foreground: "var(--foreground)",
                brand: {
                    green: {
                        light: "#f0fdf4",
                        DEFAULT: "#22c55e",
                        dark: "#16a34a",
                    },
                    navy: {
                        DEFAULT: "#1e3a8a",
                        dark: "#172554",
                    },
                },
            },
        },
    },
    plugins: [],
} satisfies Config;
