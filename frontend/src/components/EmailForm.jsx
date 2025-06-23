import React, { useState } from 'react';

function EmailForm({ onSubmit, loading }) {
  const [emailText, setEmailText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailText.trim() === '') return;
    onSubmit(emailText);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-xl bg-white p-6 rounded shadow"
    >
      <label htmlFor="emailText" className="block text-gray-700 font-semibold mb-2">
        Paste your email text below:
      </label>
      <textarea
        id="emailText"
        rows={8}
        value={emailText}
        onChange={(e) => setEmailText(e.target.value)}
        className="w-full border border-gray-300 rounded p-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Type or paste your email here..."
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading}
        className={`mt-4 px-6 py-2 rounded text-white font-semibold ${
          loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? 'Processing...' : 'Generate Reply'}
      </button>
    </form>
  );
}

export default EmailForm;
