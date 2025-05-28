import React from 'react';
import { Link } from 'react-router-dom';
import './Layout.css';

const Layout = ({ children }) => (
  <div className="app-container">
    <header className="header">
      <Link to="/" className="logo">Personal CFO</Link>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/signup">Sign Up</Link>
        <Link to="/signin">Sign In</Link>
      </nav>
    </header>
    <main className="main-content">
      {children}
    </main>
    <footer className="footer">
      &copy; {new Date().getFullYear()} Personal CFO. All rights reserved.
    </footer>
  </div>
);

export default Layout;