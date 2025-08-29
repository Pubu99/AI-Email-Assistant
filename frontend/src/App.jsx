import React, { useState, useEffect } from "react";
import EmailForm from "./components/EmailForm";
import ResultCard from "./components/ResultCard";

function Spinner() {
  return (
    <div className="flex justify-center items-center mt-8">
      <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-blue-600"></div>
    </div>
  );
}

function Footer() {
  return (
    <footer className="w-full text-center py-6 mt-12 text-gray-500 text-sm opacity-80">
      <span>
        Made with <span className="text-pink-500">♥</span> by Pro UI/UX Engineer
        &mdash; 2025
      </span>
    </footer>
  );
}

function App() {
  const [result, setResult] = useState(null);
  const [typedReply, setTypedReply] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (result?.reply) {
      setTypedReply("");
      let i = 0;
      const fullText = result.reply;
      const interval = setInterval(() => {
        setTypedReply((prev) => prev + fullText.charAt(i));
        i++;
        if (i >= fullText.length) clearInterval(interval);
      }, 18);
      return () => clearInterval(interval);
    }
  }, [result]);

  const handleSubmit = async (emailText) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setTypedReply("");
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
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 flex flex-col items-center px-2 py-8">
      <header className="w-full max-w-2xl flex flex-col items-center mb-8">
        <div className="flex items-center gap-3 mb-2">
          <img
            src="/icons8-email-32.png"
            alt="Email Icon"
            className="h-8 w-8 animate-bounce"
          />
          <h1 className="text-4xl font-extrabold text-gray-800 tracking-tight drop-shadow-sm bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-500 bg-clip-text text-transparent">
            AI Email Assistant
          </h1>
        </div>
        <p className="text-lg text-gray-600 font-medium text-center max-w-xl">
          Paste your email below and get a smart, context-aware reply instantly.
          Powered by AI.
        </p>
      </header>
      <main className="w-full flex flex-col items-center">
        <EmailForm onSubmit={handleSubmit} loading={loading} />
        {loading && <Spinner />}
        {error && <p className="text-red-500 mt-4">{error}</p>}
        {result && <ResultCard intent={result.intent} reply={typedReply} />}
      </main>
      <Footer />
    </div>
  );
}

export default App;
