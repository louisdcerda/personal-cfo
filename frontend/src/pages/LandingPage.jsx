import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';
import TestimonialCarousel from '../components/TestimonialCarousel';
import './LandingPage.css';

const LandingPage = () => (
  <section className="landing">
    <div className="hero">
      <h1>Take Control of Your Financial Future</h1>
      <p>Smart budgeting • Investment insights • Personalized reports</p>
      <Link to="/signup">
        <Button>Get Started</Button>
      </Link>
    </div>
    <div className="features">
      <div className="feature-item">
        <h3>Budget Tracking</h3>
        <p>Monitor your spending in real-time.</p>
      </div>
      <div className="feature-item">
        <h3>Investment Insights</h3>
        <p>Get data-driven recommendations.</p>
      </div>
      <div className="feature-item">
        <h3>Personalized Reports</h3>
        <p>Understand your financial health.</p>
      </div>
    </div>
    <div className="testimonials">
      <h2>What Our Users Say</h2>
      <TestimonialCarousel />
    </div>
  </section>
);

export default LandingPage;