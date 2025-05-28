import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';
import './LandingPage.css';

const LandingPage = () => (
  <section className="landing">
    <div className="hero">
      <h1>Welcome to Personal CFO</h1>
      <p>Your finances, managed smarter.</p>
      <Link to="/signup">
        <Button>Get Started</Button>
      </Link>
    </div>
    {/* Additional feature sections here */}
  </section>
);

export default LandingPage;

