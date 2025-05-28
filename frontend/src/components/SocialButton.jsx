import React from 'react';

const SocialButton = ({ provider, onClick }) => (
  <button className={`social-btn social-btn--${provider}`} onClick={onClick}>
    Sign up with {provider.charAt(0).toUpperCase() + provider.slice(1)}
  </button>
);

export default SocialButton;
