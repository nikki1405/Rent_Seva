import { User, AuthResponse } from '../types/auth.types';
import axiosInstance from './axiosConfig';

interface SignupData {
  email: string;
  password: string;
  name?: string;
  mobile?: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface EstimateRecord {
  id: number;
  location: string;
  bhk: number;
  sqft: number;
  predicted_rent: number;
  created_at: string;
}

interface EstimateHistoryResponse extends Array<EstimateRecord> {}

const authService = {
  async signup(data: SignupData): Promise<AuthResponse> {
    const response = await axiosInstance.post<AuthResponse>('/api/auth/signup/', data);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async login(data: LoginData): Promise<AuthResponse> {
    const response = await axiosInstance.post<AuthResponse>('/api/auth/login/', data);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async logout(): Promise<void> {
    try {
      await axiosInstance.post('/api/auth/logout/');
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },

  async getUserProfile(): Promise<User> {
    const response = await axiosInstance.get<{ data: User }>('/api/auth/profile/');
    return response.data.data;
  },

  async getEstimatesHistory(): Promise<EstimateRecord[]> {
    const response = await axiosInstance.get<EstimateRecord[]>('/api/auth/history/');
    return response.data;
  }
};

export default authService;