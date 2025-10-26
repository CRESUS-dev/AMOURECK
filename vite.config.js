import { defineConfig } from "vite";

export default defineConfig({
  root: "frontend",
  base: "/static/vite/",
  build: {
    outDir: "../static/vite",
    emptyOutDir: true,
  },
});
