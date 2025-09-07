import React, { useState, useEffect } from "react";
import EmailForm from "./components/EmailForm";
import ResultCard from "./components/ResultCard";
import SideBySideView from "./components/SideBySideView";

function Spinner() {
  return (
    <div className="flex flex-col justify-center items-center mt-12 space-y-4">
      <div className="relative">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600"></div>
        <div className="animate-ping rounded-full h-16 w-16 border-2 border-blue-300 absolute top-0 left-0"></div>
      </div>
      <div className="text-center">
        <p className="text-lg font-semibold text-gray-700 animate-pulse">
          Processing your email...
        </p>
        <p className="text-sm text-gray-500 mt-1">
          Our AI is analyzing and generating a response
        </p>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <footer className="w-full text-center py-6 mt-12 text-gray-500 text-sm opacity-80">
      <span>
        AI-Powered Email Categorizer & Reply Generator
      </span>
    </footer>
  );
}

function App() {
  const [result, setResult] = useState(null);
  const [typedReply, setTypedReply] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputEmail, setInputEmail] = useState("");
  const [showResults, setShowResults] = useState(false);

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
    setInputEmail(emailText);
    setShowResults(false);
    
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
      setShowResults(true);
    } catch (err) {
      setError("Failed to fetch reply. Please check your connection and try again.");
    }
    setLoading(false);
  };

  const handleNewEmail = () => {
    setResult(null);
    setTypedReply("");
    setInputEmail("");
    setShowResults(false);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex flex-col px-4 py-8">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 left-1/2 w-80 h-80 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
      </div>

      <div className="relative z-10 flex flex-col items-center">
        {/* Header */}
        <header className="w-full max-w-4xl flex flex-col items-center mb-12">
          <div className="flex items-center gap-4 mb-4">
            <div className="relative">
              <img
                src="/icons8-email-32.png"
                alt="Email Icon"
                className="h-12 w-12 animate-bounce drop-shadow-lg"
              />
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-5xl font-extrabold text-gray-800 tracking-tight drop-shadow-lg bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
              AI Email Assistant
            </h1>
          </div>
          <p className="text-xl text-gray-600 font-medium text-center max-w-2xl leading-relaxed">
            Harness the power of AI to categorize emails and generate intelligent, 
            context-aware responses instantly. Transform your email workflow today.
          </p>
          <div className="flex items-center gap-6 mt-6 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              <span>AI-Powered Analysis</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
              <span>Smart Categorization</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></span>
              <span>Instant Replies</span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="w-full flex flex-col items-center">
          {!showResults ? (
            <div className="w-full max-w-2xl">
              <EmailForm onSubmit={handleSubmit} loading={loading} />
              {loading && <Spinner />}
              {error && (
                <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center gap-3">
                    <span className="text-red-500 text-xl">⚠️</span>
                    <p className="text-red-700 font-medium">{error}</p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <SideBySideView
              inputEmail={inputEmail}
              intent={result?.intent}
              reply={typedReply}
              onNewEmail={handleNewEmail}
            />
          )}
        </main>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  );
}

export default App;
