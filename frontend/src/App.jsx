import React, { useState, useEffect } from "react";
import EmailForm from "./components/EmailForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);
  const [typedReply, setTypedReply] = useState(""); // for typing effect
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Typing effect logic
  useEffect(() => {
    if (result?.reply) {
      setTypedReply(""); // reset typed reply
      let i = 0;
      const fullText = result.reply;
      const interval = setInterval(() => {
        setTypedReply((prev) => prev + fullText.charAt(i));
        i++;
        if (i >= fullText.length) clearInterval(interval);
      }, 30); // 30ms per character typing speed
      return () => clearInterval(interval);
    }
  }, [result]);

  // Send email text to backend
  const handleSubmit = async (emailText) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setTypedReply(""); // clear typed reply before new request
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: emailText }),
        mode: "cors",
      });

      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to fetch reply. Try again.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-50 to-indigo-50 flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        AI-Powered Email Categorizer & Reply Generator
      </h1>
      <EmailForm onSubmit={handleSubmit} loading={loading} />
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {result && (
        <ResultCard
          intent={result.intent}
          reply={typedReply} // show the typed reply here
        />
      )}
    </div>
  );
}

export default App;
