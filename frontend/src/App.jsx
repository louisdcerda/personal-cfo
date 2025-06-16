import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';
import SignUpPage from './pages/SignUpPage';
import SignInPage from './pages/SignInPage';
import Dashboard from './pages/Dashboard';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Layout><LandingPage /></Layout>} />
      <Route path="/signup" element={<Layout><SignUpPage /></Layout>} />
      <Route path="/signin" element={<Layout><SignInPage /></Layout>} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  </Router>
);

export default App;
