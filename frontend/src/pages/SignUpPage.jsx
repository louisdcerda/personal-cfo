import React, { useState } from 'react';
import Button from '../components/Button';
import Input from '../components/Input';
import SocialButton from '../components/SocialButton';
import PlaidLinkButton from '../components/PlaidLinkButton';
import './SignUpPage.css';

const SignUpPage = () => {
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch('/api/signup', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
      // on success
    } catch (err) {
      console.error('Signup failed:', err);
    }
  };

  return (
    <div className="signup-page">
      <h2>Create Your Account</h2>
      <form onSubmit={handleSubmit} className="signup-form">
        <Input label="Name" name="name" value={form.name} onChange={handleChange} required />
        <Input label="Email" name="email" type="email" value={form.email} onChange={handleChange} required />
        <Input label="Password" name="password" type="password" value={form.password} onChange={handleChange} required />
        <Button type="submit">Sign Up</Button>
      </form>
      <div className="social-signup">
        <SocialButton provider="google" onClick={() => {/* handle OAuth */}} />
        <SocialButton provider="facebook" onClick={() => {/* handle OAuth */}} />
      </div>
      <h3>Link Your Bank</h3>
      <PlaidLinkButton />
    </div>
  );
};

export default SignUpPage;