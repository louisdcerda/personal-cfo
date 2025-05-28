import React from 'react';

const Button = ({ children, onClick, type = 'button', disabled }) => (
  <button type={type} onClick={onClick} disabled={disabled} className="btn">
    {children}
  </button>
);

export default Button;
