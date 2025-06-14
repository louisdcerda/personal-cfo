import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Input from '../components/Input';
import './SignInPage.css';

const SignInPage = () => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
      console.error('Signin failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signin-page">
      <h2>Welcome Back</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="signin-form">
        <Input
          label="Email"
          name="email"
          type="email"
          value={credentials.email}
          onChange={handleChange}
          required
        />
        <Input
          label="Password"
          name="password"
          type="password"
          value={credentials.password}
          onChange={handleChange}
          required
        />
        <Link to="/forgot-password" className="forgot-link">Forgot Password?</Link>
        <Button type="submit" disabled={isLoading}>
          {isLoading ? 'Signing In...' : 'Sign In'}
        </Button>
      </form>
    </div>
  );
};

export default SignInPage;
