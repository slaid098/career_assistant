// This file is for custom environment variable type declarations.
// It allows for type-safe access to process.env in a Next.js project.

declare namespace NodeJS {
  interface ProcessEnv {
    readonly NEXT_PUBLIC_API_BASE_URL: string;
    // Add other environment variables here
  }
} 