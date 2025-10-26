import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
  root: "frontend",
  base: "/static/vite/",
  build: {
    outDir: "../static/vite",
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, "frontend/main.js"), // <= important
    },
  },
});
