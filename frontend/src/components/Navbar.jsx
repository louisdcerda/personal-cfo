// src/components/Navbar.jsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();
  const current = (path) => location.pathname === path ? 'active' : '';

  return (
    <div className="navbar">
      <div className="logo">
        <span className="brand-primary">Personal</span><br />
        <span className="brand-secondary">CFO</span>
      </div>
      <div className="nav-links">
        <Link className={current('/')} to="/">Home</Link>
        <Link className={current('/signup')} to="/signup">Sign Up</Link>
        <Link className={current('/signin')} to="/signin">Sign In</Link>
      </div>
    </div>
  );
};

export default Navbar;
