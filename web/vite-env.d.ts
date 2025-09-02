/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PORT: string;
  readonly VITE_API_PORT: string;
  readonly VITE_ALLOWED_HOST: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
