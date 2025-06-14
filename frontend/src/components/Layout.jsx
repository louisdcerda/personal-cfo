import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Layout.css';

const Layout = ({ children }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => setMenuOpen(!menuOpen);
  const closeMenu = () => setMenuOpen(false);

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo">
          <Link to="/" className="logo-text" onClick={closeMenu}>
            Personal <strong>CFO</strong>
          </Link>
        </div>

        <button className="menu-toggle" onClick={toggleMenu} aria-label="Toggle navigation">
          ☰
        </button>

        <nav className={`nav-links ${menuOpen ? 'open' : ''}`}>
          <Link to="/" onClick={closeMenu} className={location.pathname === '/' ? 'active' : ''}>Home</Link>
          <Link to="/signup" onClick={closeMenu} className={location.pathname === '/signup' ? 'active' : ''}>Sign Up</Link>
          <Link to="/signin" onClick={closeMenu} className={location.pathname === '/signin' ? 'active' : ''}>Sign In</Link>
        </nav>
      </header>

      <main className="main-content">{children}</main>

      <footer className="footer">
        &copy; {new Date().getFullYear()} Personal CFO. All rights reserved.
      </footer>
    </div>
  );
};

export default Layout;
