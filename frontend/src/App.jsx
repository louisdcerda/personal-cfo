import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';
import SignUpPage from './pages/SignUpPage';
import SignInPage from './pages/SignInPage';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Layout><LandingPage /></Layout>} />
      <Route path="/signup" element={<Layout><SignUpPage /></Layout>} />
      <Route path="/signin" element={<Layout><SignInPage /></Layout>} />
    </Routes>
  </Router>
);

export default App;
