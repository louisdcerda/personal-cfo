import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // send email to your signup API or redirect to /signup?email=…
    console.log('Submitted email:', email);
  };

  return (
    <div className="landing-netflix">
      {/* HERO (full-screen background) */}
      <div className="hero-section">
        <div className="hero-overlay" />
        <div className="hero-content">
          <h1 className="hero-title">Take Control of Your Money</h1>
          <p className="hero-subtitle">
            Every tool you need—budget tracking, insights, and more. All in one place.
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
              Get Started &rarr;
            </button>
          </form>
          <p className="hero-note">
            Ready in seconds. No credit card required.
          </p>
        </div>
      </div>

      {/* FEATURE ROW 1 */}
      <div className="feature-row">
        <div className="feature-text">
          <h2>Smart Budget Tracking</h2>
          <p>
            Visualize your spending in real time, set custom alerts, and never
            wonder where your money went. Our sleek, interactive charts help
            you stay on top of every dollar.
          </p>
        </div>
        <div className="feature-image">
          <img
            src="/images/business-man-thinking-of-several-options-svgrepo-com.svg"
            alt="Budget Charts"
            loading="lazy"
          />
        </div>
      </div>

      {/* FEATURE ROW 2 (image left, text right) */}
      <div className="feature-row alt">
        <div className="feature-image">
          <img
            src="/images/data-analysis-svgrepo-com.svg"
            alt="Investment Dashboard"
            loading="lazy"
          />
        </div>
        <div className="feature-text">
          <h2>Data-Driven Investment Insights</h2>
          <p>
            Use AI-powered analysis to optimize your portfolio. Track risk
            metrics, compare performance, and get tailored recommendations that
            adapt as markets change.
          </p>
        </div>
      </div>

      {/* FEATURE ROW 3 */}
      <div className="feature-row">
        <div className="feature-text">
          <h2>Personalized Financial Reports</h2>
          <p>
            Receive monthly reports that break down your net worth, expenses,
            and growth opportunities. Everything is designed to help you plan
            ahead with confidence.
          </p>
        </div>
        <div className="feature-image">
          <img
            src="/images/financial-report-svgrepo-com.svg"
            alt="Financial Report"
            loading="lazy"
          />
        </div>
      </div>

      {/* FINAL CTA BANNER */}
      <div className="final-cta">
        <div className="cta-content">
          <h2>Ready to master your finances?</h2>
          <Link to="/signup">
            <button className="cta-button">Create Free Account</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
