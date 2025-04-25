import React, { createContext, useState } from 'react';

export interface User {
  email: string;
  uid: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  token?: string;
}

export interface AuthError {
  error: string;
}

interface AuthContextType {
  user: User | null;
  logout: () => Promise<void>;
  isAuthenticated: boolean; // Add this property
  // other properties
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Example: Ensure isAuthenticated is set based on user
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const isAuthenticated = !!user;

  const logout = async () => {
    // logout logic
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};