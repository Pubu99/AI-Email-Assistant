import React, { useState } from 'react';
import EmailForm from './components/EmailForm';
import ResultCard from './components/ResultCard';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Send email text to backend
  const handleSubmit = async (emailText) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailText }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to fetch reply. Try again.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">AI Email Assistant</h1>
      <EmailForm onSubmit={handleSubmit} loading={loading} />
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {result && <ResultCard intent={result[0]} reply={result[1]} />}
    </div>
  );
}

export default App;
