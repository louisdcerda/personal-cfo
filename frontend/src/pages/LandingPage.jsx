import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: connect to signup flow or capture email
    console.log('Submitted email:', email);
  };

  return (
    <div className="landing-container">
      {/* HERO SECTION */}
      <section className="hero-section">
        <div className="hero-inner">
          <h1 className="hero-title">Take Control of Your Money</h1>
          <p className="hero-subtitle">
            All your finances—budget tracking, reports, and AI-powered insights—in one place.
          </p>
          <form className="email-form" onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Enter your email"
              className="email-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit" className="email-button">
              Get Started →
            </button>
          </form>
          <p className="hero-note">No credit card required. Ready in seconds.</p>
        </div>
      </section>

      {/* FEATURES */}
      <section className="features">
        <div className="feature-row">
          <div className="feature-text">
            <h2>Smart Budget Tracking</h2>
            <p>
              Visualize spending in real time, set alerts, and stay on top of your financial goals.
            </p>
          </div>
          <div className="feature-image">
            <img
              src="/images/business-man-thinking-of-several-options-svgrepo-com.svg"
              alt="Budget Tracking"
              loading="lazy"
            />
          </div>
        </div>

        <div className="feature-row alt">
          <div className="feature-image">
            <img
              src="/images/data-analysis-svgrepo-com.svg"
              alt="Investment Insights"
              loading="lazy"
            />
          </div>
          <div className="feature-text">
            <h2>Data-Driven Investment Insights</h2>
            <p>
              Use AI to optimize your portfolio with adaptive recommendations and real-time metrics.
            </p>
          </div>
        </div>

        <div className="feature-row">
          <div className="feature-text">
            <h2>Personalized Reports</h2>
            <p>
              Get monthly summaries of your net worth, spending habits, and opportunities to grow.
            </p>
          </div>
          <div className="feature-image">
            <img
              src="/images/financial-report-svgrepo-com.svg"
              alt="Financial Reports"
              loading="lazy"
            />
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="final-cta">
        <div className="cta-content">
          <h2>Ready to master your finances?</h2>
          <Link to="/signup">
            <button className="cta-button">Create Free Account</button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
