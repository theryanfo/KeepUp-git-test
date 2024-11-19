import React, { useState } from 'react';

const TestButton = () => {
  const [message, setMessage] = useState('');

  // Function to call the /test route and update the message state
  const testRoute = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/test');
      const data = await response.json(); // Parse the JSON response
      setMessage(data.message); // Access the message from the JSON object
    } catch (error) {
      console.error('Error fetching the test message:', error);
      setMessage('Failed to fetch test message.');
    }
  };

  return (
    <div>
      <h1>Test the Flask Route</h1>
      <button onClick={testRoute}>Click to Test</button>
      <p>{message}</p>
    </div>
  );
};

export default TestButton;
