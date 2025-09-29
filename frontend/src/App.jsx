import React from 'react';
import './App.css';

// Import all components
import Navbar from './components/navbar/navbar';
import Hero from './components/hero/hero';
import Features from './components/features/features';
import HowItWorks from './components/howItWorks/howItWorks';
import Demo from './components/demo/demo';
import Community from './components/community/community';
import Footer from './components/footer/footer';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <Demo />
      <Community />
      <Footer />
    </div>
  );
}

export default App;
