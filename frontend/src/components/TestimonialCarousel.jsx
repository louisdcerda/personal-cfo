import React, { useState } from 'react';

const testimonials = [
  { text: "wtf do i put in here. later issue", author: "— louis" },
  { text: "I love the intuitive budgeting features.", author: "— Jamie" },
  { text: "Their investment insights are spot on.", author: "— Morgan" }
];

const TestimonialCarousel = () => {
  const [index, setIndex] = useState(0);
  const next = () => setIndex((i) => (i + 1) % testimonials.length);
  const prev = () => setIndex((i) => (i - 1 + testimonials.length) % testimonials.length);

  return (
    <div className="testimonial-carousel">
      <button onClick={prev}>‹</button>
      <blockquote>{testimonials[index].text}</blockquote>
      <cite>{testimonials[index].author}</cite>
      <button onClick={next}>›</button>
    </div>
  );
};

export default TestimonialCarousel;
