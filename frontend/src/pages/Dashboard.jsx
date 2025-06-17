import React, { useEffect, useState } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import './Dashboard.css';

const Dashboard = () => {
  const [linkToken, setLinkToken] = useState(null);
  const [bankLinked, setBankLinked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch whether we need to link bank and, if so, get a linkToken
  useEffect(() => {
    const init = async () => {
      try {
        const statusRes = await fetch('/api/users/should_link_bank', { credentials: 'include' });
        if (!statusRes.ok) throw new Error('Status check failed');
        const { should_link_bank } = await statusRes.json();
        setBankLinked(!should_link_bank);

        if (should_link_bank) {
          const tokenRes = await fetch('/api/plaid/link-token', { credentials: 'include' });
          if (!tokenRes.ok) throw new Error('Failed to fetch link token');
          const { link_token } = await tokenRes.json();
          setLinkToken(link_token);
        }
      } catch (err) {
        console.error(err);
        setError(err.message || 'Unknown error');
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  // Configure Plaid Link once we have a linkToken
  const { open, ready } = usePlaidLink({
    token: linkToken || '',
    onSuccess: async (public_token, metadata) => {
      try {
        // Exchange the public_token for an access token
        const exchangeRes = await fetch('/api/plaid/exchange-public-token', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ public_token }),
        });
        if (!exchangeRes.ok) throw new Error('Exchange failed');
        setBankLinked(true);

        // Mark in our DB that the user has linked their bank
        const updateRes = await fetch('/api/users/update_link_bank', {
          method: 'POST',
          credentials: 'include',
        });
        const updateJson = await updateRes.json();
        if (!updateRes.ok || updateJson.error) {
          console.warn('Backend update error', updateJson);
        }
      } catch (err) {
        console.error('Plaid onSuccess error:', err);
        setError('Something went wrong during bank link.');
      }
    },
    onExit: (err) => {
      if (err) console.warn('User exited Plaid Link with error:', err);
    },
  });

  // Loading / error states
  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard-card">
          <p>Loading your dashboard…</p>
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="dashboard">
        <div className="dashboard-card">
          <p className="error-message">Error: {error}</p>
        </div>
      </div>
    );
  }

  // Main UI
  return (
    <div className="dashboard">
      <div className="dashboard-card">
        <h1>Welcome to your Dashboard</h1>
        {bankLinked ? (
          <p>Your bank account is linked ✅</p>
        ) : (
          <>
            <p>Connect your bank account to get started.</p>
            <button
              className="link-button"
              onClick={open}
              disabled={!ready}
            >
              {ready ? 'Link Bank' : 'Preparing…'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
