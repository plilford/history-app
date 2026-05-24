import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      // Make updates take effect on the very next reload rather than
      // requiring all open tabs/instances to close first. Important for
      // the TWA case where the app may stay alive in background indefinitely.
      workbox: { clientsClaim: true, skipWaiting: true },
      manifest: {
        name: "Ever-When",
        short_name: "Ever-When",
        description: "Explore historical timelines side by side.",
        theme_color: "#0f172a",
        background_color: "#0f172a",
        display: "standalone",
        start_url: "/",
        icons: [
          { src: "icon-192.png",          sizes: "192x192", type: "image/png" },
          { src: "icon-512.png",          sizes: "512x512", type: "image/png" },
          { src: "icon-512-maskable.png", sizes: "512x512", type: "image/png", purpose: "maskable" }
        ]
      }
    })
  ],
  server: { port: 5173 }
});
