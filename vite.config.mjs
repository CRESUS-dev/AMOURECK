import { defineConfig } from "vite";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  root: path.resolve(__dirname, "frontend"),
  base: "/static/vite/",
  build: {
    outDir: path.resolve(__dirname, "static/vite"),
    emptyOutDir: true,
    manifest: "manifest.json", // ← forcer la création du manifest
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "frontend/main-ticket.js"),
        packages: path.resolve(__dirname, "frontend/main-packages.js"),
      },
      output: {
        entryFileNames: "assets/[name]-[hash].js",
        chunkFileNames: "assets/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash][extname]",
      },
    },
  },
});
