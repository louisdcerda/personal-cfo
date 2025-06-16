// src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [showPlaid, setShowPlaid] = useState(false);
  const [linkToken, setLinkToken] = useState(null);

  useEffect(() => {
    async function checkBankStatus() {
      const res = await fetch("/api/users/should_link_bank", { credentials: "include" });
      const data = await res.json();

      if (data.should_link_bank) {
        const tokenRes = await fetch("/plaid/link-token", {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            client_user_id: "placeholder", // Replace with actual user ID
            language: "en"
          }),
        });

        const tokenData = await tokenRes.json();
        setLinkToken(tokenData.link_token);
        setShowPlaid(true);
      }
    }

    checkBankStatus();
  }, []);

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token, metadata) => {
      await fetch("/plaid/exchange-public-token", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ public_token }),
      });
      setShowPlaid(false);
    },
  });

  useEffect(() => {
    if (showPlaid && ready) open();
  }, [showPlaid, ready]);

  return (
    <div className="dashboard">
      <div className="dashboard-card">
        <h1>Welcome to your Dashboard</h1>
        <p>Monitor your financial data here. Link a bank account to get started.</p>
      </div>
    </div>
  );
};

export default Dashboard;
