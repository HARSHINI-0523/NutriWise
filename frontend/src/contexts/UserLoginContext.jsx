import React, { createContext, useContext, useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5000/api/auth';

// Creating context
const AuthContext = createContext();

// Custom hook to use the Auth context
export const useAuth = () => {
    return useContext(AuthContext);
};

// Auth Provider Component
export const UserLoginProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);
    // Note: useNavigate must be used in components rendered inside the Router (like Login.jsx), not here.

    // Initial load: Check localStorage for existing session/token
    useEffect(() => {
        const token = localStorage.getItem('userToken');
        const user = localStorage.getItem('userProfile');

        if (token && user) {
            try {
                // Restore user session from localStorage
                setCurrentUser(JSON.parse(user));
            } catch (e) {
                // If parsing fails, clear bad data
                localStorage.removeItem('userToken');
                localStorage.removeItem('userProfile');
                console.error("Failed to parse user profile from localStorage:", e);
            }
        }
        setLoading(false);
    }, []);

    // Helper function for API calls
    const makeAuthRequest = async (endpoint, payload) => {
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            // Throw the error message provided by the Express backend
            throw new Error(data.message || `${endpoint} failed.`);
        }
        return data;
    };

    // 1. Email/Password Sign Up
    const signUp = async (email, password, name) => {
        const data = await makeAuthRequest('signup', { email, password, name });
        
        // Store token and user data on successful sign up
        const userProfile = { 
            uid: data._id, 
            displayName: data.name, 
            email: data.email, 
            token: data.token 
        };
        localStorage.setItem('userToken', data.token);
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        setCurrentUser(userProfile);
        
        // Note: Navigation must happen in the component calling this (Login.jsx)
    };

    // 2. Email/Password Sign In
    const signIn = async (email, password) => {
        const data = await makeAuthRequest('login', { email, password });
        
        // Store token and user data on successful sign in
        const userProfile = { 
            uid: data._id, 
            displayName: data.name, 
            email: data.email, 
            token: data.token 
        };
        localStorage.setItem('userToken', data.token);
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        setCurrentUser(userProfile);

        // Note: Navigation must happen in the component calling this (Login.jsx)
    };

    // 3. Sign Out
    const logOut = () => {
        // Clear all session data
        localStorage.removeItem('userToken');
        localStorage.removeItem('userProfile');
        setCurrentUser(null);
        // Note: Navigation must happen in the component calling this (e.g., Navbar.jsx)
    };

    // Google Sign-in is disabled since it requires complex OAuth implementation on a custom backend
    const signInWithGoogle = () => {
        console.warn("Google Sign-in not implemented on custom API.");
        throw new Error("Google Sign-in not implemented on custom API.");
    };

    // The value exposed by the context provider
    const value = {
        currentUser,
        loading,
        signUp,
        signIn,
        signInWithGoogle,
        logOut,
        userId: currentUser?.uid, 
        isAuthenticated: !!currentUser, // Convenience flag
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading ? children : <div className="flex items-center justify-center min-h-screen text-lg text-green-600">Loading Session...</div>}
        </AuthContext.Provider>
    );
};
