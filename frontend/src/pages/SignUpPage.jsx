import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './SignUpPage.css';

const SignUpPage = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError(''); // Clear error when user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/users/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Signup failed');
      }

      // Store token and redirect to dashboard
      localStorage.setItem('token', data.token);
      navigate('/dashboard');

    } catch (error) {
      setError(error.message || 'Something went wrong. Please try again later.');
      console.error("Signup error:", error);
    } finally {
      setIsLoading(false);
    }
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
      <h2>Create Account</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="signup-form">
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
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>
      <p className="login-link">
        Already have an account? <Link to="/signin">Sign In</Link>
      </p>

      {/* OPTIONAL SOCIAL SIGNUP */}
      <div className="social-signup">
        <button className="social-btn">Sign up with Google</button>
        <button className="social-btn">Sign up with Facebook</button>
      </div>

      {/* OPTIONAL "LINK YOUR BANK" HEADING */}
      <div className="link-wrapper">
        <h3>Link Your Bank</h3>
        {/* Insert PlaidLinkButton here if desired */}
      </div>
    </div>
  );
};

export default SignUpPage;
