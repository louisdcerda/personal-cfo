import React from 'react';
import { motion } from 'framer-motion';
import './AnimatedFeatureCard.css';

const AnimatedFeatureCard = ({ title, children }) => (
  <motion.div
    className="feature-card"
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
    viewport={{ once: true }}
  >
    <h3>{title}</h3>
    <p>{children}</p>
  </motion.div>
);

export default AnimatedFeatureCard;