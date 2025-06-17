import React, { useEffect, useState } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import './Dashboard.css';

const Dashboard = () => {
  const [linkToken, setLinkToken] = useState(null);
  const [userId, setUserId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [bankLinked, setBankLinked] = useState(false);
  const [error, setError] = useState('');

  // Fetch user info and check if bank is already linked
  useEffect(() => {
    async function initDashboard() {
      try {
        const userRes = await fetch('/api/users/me', {
          credentials: 'include',
        });
        const userData = await userRes.json();
        setUserId(userData.id);

        const linkStatus = await fetch('/api/users/should_link_bank', {
          credentials: 'include',
        });
        const { should_link_bank } = await linkStatus.json();

        setBankLinked(!should_link_bank);

        if (should_link_bank) {
          const tokenRes = await fetch('/api/plaid/link-token', {
            method: 'GET',
            credentials: 'include',
          });
          const tokenData = await tokenRes.json();
          setLinkToken(tokenData.link_token);
        }
      } catch (err) {
        setError('Failed to load dashboard');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }

    initDashboard();
  }, []);

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token) => {
      try {
        await fetch('/api/plaid/exchange-public-token', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ public_token }),
        });
        setBankLinked(true);

        // update link bank in db after success
        const update_link_bank_db = await fetch("/api/users/update_link_bank", {
          method: "POST",
          credentials: "include"
        });
        console.log(update_link_bank_db);

      } catch (err) {
        console.error('Plaid exchange error:', err);
        setError('Something went wrong while linking your bank.');
      }
    },
    onExit: () => {
      console.log('User exited Plaid modal');
    },
  });

  return (
    <div className="dashboard">
      <div className="dashboard-card">
        <h1>Welcome to your Dashboard</h1>
        {isLoading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : bankLinked ? (
          <p>Your bank account is linked ✅</p>
        ) : (
          <>
            <p>Connect your bank account to get started.</p>
            <button
              onClick={open}
              disabled={!ready}
              className="link-button"
            >
              Link Bank
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
