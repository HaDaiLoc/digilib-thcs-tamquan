const DEFAULT_API_BASE_URL = 'https://digilab-thcs-tamquan.onrender.com/api';

const envApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

export const API_BASE_URL = envApiBaseUrl || DEFAULT_API_BASE_URL;

export const API_CONFIG = {
  defaultBaseUrl: DEFAULT_API_BASE_URL,
  currentBaseUrl: API_BASE_URL,
};