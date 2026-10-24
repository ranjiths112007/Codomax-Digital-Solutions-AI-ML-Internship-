import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// GitHub Pages serves this project under the repository URL.
export default defineConfig({
  base: "/Codomax-Digital-Solutions-AI-ML-Internship-/",
  plugins: [react()],
  server: { host: "127.0.0.1", port: 5173 },
});
