import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [showPlaidModal, setShowPlaidModal] = useState(false);

  useEffect(() => {
    async function checkBankLinkStatus() {
      try {
        const res = await fetch('/api/users/should_link_bank', {
          credentials: 'include',
        });
        const data = await res.json();
        if (data.should_link_bank) {
          setShowPlaidModal(true);
        }
      } catch (error) {
        console.error('Error checking bank link status:', error);
      }
    }

    checkBankLinkStatus();
  }, []);

  const handlePlaidSuccess = async () => {
    try {
      await fetch('/api/users/update-bank-status', {
        method: 'POST',
        credentials: 'include',
      });
      setShowPlaidModal(false);
    } catch (error) {
      console.error('Error updating bank status:', error);
    }
  };

  return (
    <div className="dashboard-container">
      <h1>Welcome to Your Dashboard</h1>
      <nav>
        <Link to="/settings">Settings</Link>
        <Link to="/logout">Logout</Link>
      </nav>

      {showPlaidModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Link Your Bank Account</h2>
            <p>To get started, link your bank with Plaid.</p>
            <button onClick={handlePlaidSuccess}>Simulate Plaid Success</button>
            <button onClick={() => setShowPlaidModal(false)}>Dismiss</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
