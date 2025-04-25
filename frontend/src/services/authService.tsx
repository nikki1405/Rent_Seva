import { User, AuthResponse } from '../types/auth.types';
import axiosInstance from './axiosConfig';

const authService = {
    async login(credentials: { email: string; password: string }) {
        const response = await axiosInstance.post<AuthResponse>('/api/auth/login/', credentials);
        const data = response.data;
        if (data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
        }
        return data;
    },

    async logout() {
        try {
            await axiosInstance.post('/api/auth/logout/');
        } finally {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        }
    },

    async signup(email: string, password: string) {
        const response = await axiosInstance.post<AuthResponse>('/api/auth/signup/', { email, password });
        const data = response.data;
        if (data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
        }
        return data;
    },

    async getUserProfile() {
        const response = await axiosInstance.get<{ data: User }>('/api/auth/profile/');
        return response.data.data;
    }
};

export default authService;