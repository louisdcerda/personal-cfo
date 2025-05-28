import React from 'react';

const Input = ({label, ...props}) => (
	<div className='input-group'>
	    {label && <label>{label}</label>}
    <input {...props} className="input" />
  </div>
);

export default Input;
