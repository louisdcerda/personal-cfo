import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';
import Input from '../components/Input';
import './SignInPage.css';

const SignInPage = () => {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const handleChange = (e) => setCredentials({ ...credentials, [e.target.name]: e.target.value });
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch('/api/signin', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(credentials) });
      // on success
    } catch (err) {
      console.error('Signin failed:', err);
    }
  };

  return (
    <div className="signin-page">
      <h2>Welcome Back</h2>
      <form onSubmit={handleSubmit} className="signin-form">
        <Input label="Email" name="email" type="email" value={credentials.email} onChange={handleChange} required />
        <Input label="Password" name="password" type="password" value={credentials.password} onChange={handleChange} required />
        <Link to="/forgot-password" className="forgot-link">Forgot Password?</Link>
        <Button type="submit">Sign In</Button>
      </form>
    </div>
  );
};

export default SignInPage;
