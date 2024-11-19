import React from 'react';

function LogoutButton() {
  const handleLogout = () => {
    fetch('http://127.0.0.1:5000/logout')
      .then(response => response.json())  
      .then(data => {
        if (data.message === "Logged out successfully") {
          // Handle frontend UI change, e.g., navigate to home page or show a message
          // console.log('Logout successful');
          window.location.href = 'http://localhost:5173/'; 
        }
      })
      .catch(error => console.error('Error during logout:', error));
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
}

export default LogoutButton;
