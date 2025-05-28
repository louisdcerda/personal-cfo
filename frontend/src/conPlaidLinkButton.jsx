import React, { useState, useEffect, useCallback } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import Button from './Button';

const PlaidLinkButton = () => {
  const [linkToken, setLinkToken] = useState(null);

  useEffect(() => {
    const createToken = async () => {
      try {
        const res = await fetch('/api/create_link_token', { method: 'POST' });
        const data = await res.json();
        setLinkToken(data.link_token);
      } catch (err) {
        console.error('Failed to create link token:', err);
      }
    };
    createToken();
  }, []);

  const onSuccess = useCallback((public_token, metadata) => {
    fetch('/api/set_access_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ public_token }),
    }).catch(console.error);
  }, []);

  const { open, ready } = usePlaidLink({ token: linkToken, onSuccess });

  if (!linkToken) return null;

  return (
    <Button onClick={() => open()} disabled={!ready}>
      Link Your Bank Account
    </Button>
  );
};

export default PlaidLinkButton;
