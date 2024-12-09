import React from 'react';

function LoginButton() {
  const handleLogin = () => {
    // Simply redirect the user to the backend /login route
    window.location.href = 'http://127.0.0.1:5000/login';
    window.location.href = 'http://localhost:5173/';
  };

  return (
    <button onClick={handleLogin}>
      Login with Spotify
    </button>
  );
}

export default LoginButton;


// const LoginButton = () => {
//   const [message, setMessage] = useState('');

//   // Function to call the /test route and update the message state
//   const testRoute = async () => {
//     try {
//       const response = await fetch('http://127.0.0.1:5000/login');
//       const data = await response.json(); // Parse the JSON response
//       setMessage(data.message); // Access the message from the JSON object
//     } catch (error) {
//       console.error('Error fetching the test message:', error);
//       setMessage('Failed to fetch test message.');
//     }
//   };

//   return (
//     <div>
//       <h1>Test the Flask Route</h1>
//       <button onClick={testRoute}>Click to Test</button>
//       <p>{message}</p>
//     </div>
//   );
// };