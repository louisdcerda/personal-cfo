import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { usePlaidLink } from 'react-plaid-link';
import './AuthStyling.css';

const SignInPage = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [linkToken, setLinkToken] = useState(null);
  const [shouldShowPlaid, setShouldShowPlaid] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
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
        body: JSON.stringify(form),
        credentials: 'include',
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Login failed');

      // Check bank link status
      const res = await fetch('/api/users/should_link_bank', {
        credentials: 'include',
      });
      const { should_link_bank } = await res.json();

      if (should_link_bank) {
        setShouldShowPlaid(true);
        const linkRes = await fetch('/api/plaid/link-token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_user_id: form.email,
            language: 'en',
          }),
        });
        const linkData = await linkRes.json();
        setLinkToken(linkData.link_token);
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Something went wrong.');
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token, metadata) => {
      await fetch('/api/plaid/exchange-public-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ public_token }),
      });
      navigate('/dashboard');
    },
    onExit: () => {
      navigate('/dashboard');
    },
  });

  useEffect(() => {
    if (shouldShowPlaid && ready && linkToken) {
      open();
    }
  }, [shouldShowPlaid, ready, linkToken]);

  return (
    <div className="signin-page">
      <div className="form-container">
        <h2>Welcome Back</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <label>
            Email
            <input
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              required
              style={{ color: 'black' }}
            />
          </label>
          <label>
            Password
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              required
              style={{ color: 'black' }}
            />
          </label>
          <div className="form-footer">
            <Link to="/forgot-password" className="forgot-link">Forgot Password?</Link>
          </div>
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <p>
          Don’t have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default SignInPage;
