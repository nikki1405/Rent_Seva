import axios from 'axios';

const API_URL = process.env.NODE_ENV === 'production' 
    ? 'https://api.example.com'
    : 'http://localhost:8000';

const axiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Enhanced request interceptor with detailed logging
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        
        // Detailed request logging
        const requestData = typeof config.data === 'string' ? config.data : JSON.stringify(config.data);
        console.log('Full Request Details:', {
            url: `${config.baseURL}${config.url}`,
            method: config.method,
            headers: config.headers,
            data: requestData,
            parsedData: typeof config.data === 'string' ? JSON.parse(config.data) : config.data
        });
        
        return config;
    },
    (error) => {
        console.error('Request Error:', error);
        return Promise.reject(error);
    }
);

// Enhanced response interceptor with detailed error logging
axiosInstance.interceptors.response.use(
    (response) => {
        console.log('Response Success:', {
            status: response.status,
            data: response.data
        });
        return response;
    },
    async (error) => {
        console.error('Response Error Details:', {
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            request: {
                url: error.config?.url,
                method: error.config?.method,
                data: error.config?.data ? (
                    typeof error.config.data === 'string' ? 
                        JSON.parse(error.config.data) : 
                        error.config.data
                ) : {}
            }
        });
        
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;