import React from 'react';
import './navbar.css';

const Navbar = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  };

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
          <a 
            href="#home" 
            className="nav-link"
            onClick={(e) => {
              e.preventDefault();
              scrollToSection('home');
            }}
          >
            Home
          </a>
          <a 
            href="#features" 
            className="nav-link"
            onClick={(e) => {
              e.preventDefault();
              scrollToSection('features');
            }}
          >
            Features
          </a>
          <a 
            href="#how-it-works" 
            className="nav-link"
            onClick={(e) => {
              e.preventDefault();
              scrollToSection('how-it-works');
            }}
          >
            How It Works
          </a>
          <a 
            href="#demo" 
            className="nav-link"
            onClick={(e) => {
              e.preventDefault();
              scrollToSection('demo');
            }}
          >
            Demo
          </a>
          <a 
            href="#community" 
            className="nav-link"
            onClick={(e) => {
              e.preventDefault();
              scrollToSection('community');
            }}
          >
            Community
          </a>
        </div>
        
        <div className="nav-actions">
          <button className="nav-btn nav-btn-secondary">Sign In</button>
          <button className="nav-btn nav-btn-primary">Get Started</button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
