import React, { useState } from 'react';
import { Link } from 'react-router-dom';


const Dashboard = () => {
    useEffect(() => {
        async function checkBankLinkStatus() {
          const res = await fetch('/api/users/should_link_bank', { credentials: 'include' });
          const data = await res.json();
          if (data.should_link_bank) {
            // 👉 show Plaid modal
          }
        }
      
        checkBankLinkStatus();
      }, []);
      
}