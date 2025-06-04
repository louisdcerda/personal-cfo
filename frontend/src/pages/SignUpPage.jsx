import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './SignUpPage.css';

const SignUpPage = () => {
  const [form, setForm] = useState({ name: '', email: '', password: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // ...your signup logic
  };

  return (
    <div className="signup-page">
      {/* OPTIONAL NAVBAR AT TOP */}
      <div className="navbar">
        <Link to="/">Home</Link>
        <Link to="/signup">Sign Up</Link>
        <Link to="/signin">Sign In</Link>
      </div>

      {/* SIGN UP FORM PANEL */}
      <form onSubmit={handleSubmit} className="signup-form">
        <h2>Create Your Account</h2>
        <div className="input-group">
          <label>Name</label>
          <input
            name="name"
            type="text"
            placeholder="Enter your name"
            value={form.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="input-group">
          <label>Email</label>
          <input
            name="email"
            type="email"
            placeholder="you@example.com"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="input-group">
          <label>Password</label>
          <input
            name="password"
            type="password"
            placeholder="••••••••"
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Sign Up</button>

        {/* OPTIONAL SOCIAL SIGNUP */}
        <div className="social-signup">
          <button className="social-btn">Sign up with Google</button>
          <button className="social-btn">Sign up with Facebook</button>
        </div>

        {/* OPTIONAL “LINK YOUR BANK” HEADING */}
        <div className="link-wrapper">
          <h3>Link Your Bank</h3>
          {/* Insert PlaidLinkButton here if desired */}
        </div>
      </form>
    </div>
  );
};

export default SignUpPage;
