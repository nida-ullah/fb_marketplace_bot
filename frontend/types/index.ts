export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export interface FacebookAccount {
  id: number;
  email: string;
  password?: string;
  session_cookie?: string;
  created_at: string;
}

export interface MarketplacePost {
  id: number;
  account: FacebookAccount;
  title: string;
  description: string;
  price: number;
  image?: string;
  scheduled_time: string;
  posted: boolean;
  created_at?: string;
}

export interface DashboardStats {
  total_accounts: number;
  active_accounts: number;
  total_posts: number;
  pending_posts: number;
  posted_today: number;
  success_rate: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}
