import React from 'react';
import './HeroWave.css';

const HeroWave = () => (
  <svg className="hero-wave" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
    <path fill="var(--color-accent)" d="M0,48L48,58.7C96,69,192,91,288,96C384,101,480,91,576,85.3C672,80,768,80,864,96C960,112,1056,144,1152,154.7C1248,165,1344,155,1392,149.3L1440,144L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z" />
  </svg>
);

export default HeroWave;