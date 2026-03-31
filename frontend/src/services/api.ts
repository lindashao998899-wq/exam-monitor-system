import axios from "axios";

const apiBase = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "/api";

export const api = axios.create({
  baseURL: apiBase,
});
