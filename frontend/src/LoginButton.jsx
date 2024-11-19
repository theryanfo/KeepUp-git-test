import React from 'react';

function LoginButton() {
  const handleLogin = () => {
    // Simply redirect the user to the backend /login route
    window.location.href = 'http://127.0.0.1:5000/login';
  };

  return (
    <button onClick={handleLogin}>
      Login with Spotify
    </button>
  );
}

export default LoginButton;
