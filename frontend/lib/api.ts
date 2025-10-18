import axios from "axios";

// Django backend URL - change this to your production URL
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;

// API endpoints
export const authAPI = {
  login: (email: string, password: string) =>
    api.post("/auth/login/", { email, password }),

  signup: (email: string, password: string, name: string) =>
    api.post("/auth/register/", { email, password, name }),

  logout: () => api.post("/auth/logout/"),

  getProfile: () => api.get("/auth/user/"),
};

export const accountsAPI = {
  list: () => api.get("/accounts/"),

  create: (data: { email: string; password: string }) =>
    api.post("/accounts/", data),

  addWithLogin: (data: { email: string; password: string }) =>
    api.post("/accounts/add-with-login/", data),

  updateSession: (id: number) => api.post(`/accounts/${id}/update-session/`),

  delete: (id: number) => api.delete(`/accounts/${id}/`),

  bulkUpload: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/accounts/bulk-upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export const postsAPI = {
  list: () => api.get("/posts/"),

  create: (data: FormData) =>
    api.post("/posts/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    }),

  update: (id: number, data: FormData) =>
    api.put(`/posts/${id}/`, data, {
      headers: { "Content-Type": "multipart/form-data" },
    }),

  delete: (id: number) => api.delete(`/posts/${id}/`),

  bulkUpload: (file: File, accountIds: number[]) => {
    const formData = new FormData();
    formData.append("csv_file", file);
    accountIds.forEach((id) => {
      formData.append("accounts[]", id.toString());
    });
    return api.post("/posts/bulk-upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export const statsAPI = {
  getDashboard: () => api.get("/stats/dashboard/"),
};
