import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [react(), tailwindcss()],
    server: {
      allowedHosts: [env.VITE_ALLOWED_HOST],
      host: `${env.VITE_HOST}`,
      port: Number(env.VITE_PORT),
      proxy: {
        "/api": {
          target: `http://api:${env.VITE_API_PORT}`, // backend server target
          changeOrigin: true,
        },
      },
    },
  };
});
