// File: ProtectedRoute.jsx

import React, { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../contexts/UserLoginContext";

const ProtectedRoute = () => {
  const { currentUser, isAuthenticated, logOut } = useAuth();
  const [isVerifying, setIsVerifying] = useState(true);
  const [isValidSession, setIsValidSession] = useState(false);

  useEffect(() => {
    const validateSession = async () => {
      const sessionToken = currentUser?.token;

      if (!sessionToken) {
        setIsValidSession(false);
        setIsVerifying(false);
        return;
      }

      try {
        // Change this URL to your local backend's validation endpoint
        const response = await fetch(
          "http://localhost:5000/api/auth/validate-session",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${sessionToken}`,
            },
          }
        );

        if (response.ok) {
          setIsValidSession(true);
        } else {
          console.warn("Session validation failed:", response.status);
          logOut();
          setIsValidSession(false);
        }
      } catch (error) {
        console.error("Error validating session:", error);
        logOut();
        setIsValidSession(false);
      } finally {
        setIsVerifying(false);
      }
    };

    validateSession();
  }, [currentUser, logOut]);

  if (isVerifying) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          backgroundColor: "#1a1a2e",
          color: "#e0e0e0",
        }}
      >
        <h2>Verifying session...</h2>
      </div>
    );
  }

  if (!isAuthenticated || !isValidSession) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
