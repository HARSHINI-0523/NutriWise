import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/UserLoginContext.jsx';
import { useSidebar } from '../../contexts/SidebarContext'; // NEW
import './header.css';

const Header = () => {
    const { isAuthenticated, currentUser, logOut } = useAuth();
    const { setSidebarMode } = useSidebar(); // Use sidebar context
    const navigate = useNavigate();

    // NOTE: scrollToSection logic is likely not needed anymore if you are using React Router links

    const handleLogout = () => {
        logOut();
        navigate('/login');
    };

    // Helper function to handle navigation and setting sidebar mode
    const handleNavClick = (mode, defaultPath) => {
        setSidebarMode(mode);
        navigate(defaultPath); // Navigate to the default path for the section
    };

    const userName = currentUser?.displayName || currentUser?.email || 'User Profile';

    return (
        <nav className="navbar">
            <div className="nav-container">
                <div className="nav-logo">
                    <div className="logo-icon">
                        <img src="/nutriwise.jpg" alt="NutriWise Logo" />
                    </div>
                    <span className="logo-text">NutriWise</span>
                </div>
                
                <div className="nav-links">
                    <Link 
                        to="/reports/my"
                        onClick={() => handleNavClick('Reports', '/reports/my')}
                    >
                        Reports
                    </Link>
                    <Link 
                        to="/diet-plans/generate"
                        onClick={() => handleNavClick('DietPlans', '/diet-plans/generate')}
                    >
                        Diet Plans
                    </Link>
                    <Link to="/challenges">Challenges</Link>
                    <Link to="/community">Community</Link>
                </div>
                
                <div className="nav-actions">
                    {isAuthenticated ? (
                        <>
                            <Link 
                                to="/profile" 
                                className="nav-profile-link" 
                                title={userName}
                            >
                                {userName}
                            </Link>
                            <button 
                                onClick={handleLogout} 
                                className="nav-btn nav-btn-primary"
                            >
                                Log Out
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="nav-btn nav-btn-secondary">
                                Sign In
                            </Link>
                            <Link to="/login" className="nav-btn nav-btn-primary">
                                Get Started
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Header;
