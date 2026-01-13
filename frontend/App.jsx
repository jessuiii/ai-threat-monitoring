import React, { useState } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';
import jwtDecode from 'jwt-decode';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  const handleSetToken = (tok) => {
    setToken(tok);
    localStorage.setItem('token', tok);
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
  };

  let user = null;
  try {
    if (token) user = jwtDecode(token);
  } catch (e) { user = null; }

  if (!token || !user) {
    return <Login setToken={handleSetToken} />;
  }

  return <Dashboard token={token} user={user} onLogout={handleLogout} />;
}

export default App;
