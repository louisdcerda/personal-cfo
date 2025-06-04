import React from 'react';
import { motion } from 'framer-motion';
import './AnimatedButton.css';

const AnimatedButton = ({ children, ...props }) => (
    <motion.button 
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
    className='animated-btn'
    {...props}
    >
        {children}
    </motion.button>
);

export default AnimatedButton;