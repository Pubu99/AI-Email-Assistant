import React, { useState } from "react";

function EmailForm({ onSubmit, loading }) {
  const [emailText, setEmailText] = useState("");
  const [charCount, setCharCount] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailText.trim() === "") return;
    onSubmit(emailText);
  };

  const handleChange = (e) => {
    const text = e.target.value;
    setEmailText(text);
    setCharCount(text.length);
  };

  return (
    <div className="w-full space-y-6">
      {/* Main Form */}
      <form
        onSubmit={handleSubmit}
        className="w-full bg-white/90 p-8 rounded-2xl shadow-xl border border-gray-100 transition-all duration-300 hover:shadow-2xl"
        style={{ backdropFilter: "blur(10px)" }}
      >
        <div className="relative mb-6">
          <textarea
            id="emailText"
            rows={10}
            value={emailText}
            onChange={handleChange}
            className="peer w-full border-2 border-gray-300 rounded-xl p-6 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-gray-50 transition-all duration-200 shadow-sm placeholder-transparent resize-none"
            placeholder="Type or paste your email here..."
            disabled={loading}
            maxLength={5000}
          />
          <label
            htmlFor="emailText"
            className="absolute left-6 top-4 text-gray-500 text-base font-medium pointer-events-none transition-all duration-200 peer-focus:-top-3 peer-focus:left-4 peer-focus:text-sm peer-focus:text-blue-600 peer-placeholder-shown:top-6 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 bg-white px-2 rounded"
          >
            Paste your email text here
          </label>
          
          {/* Character counter */}
          <div className="absolute bottom-3 right-3 text-xs text-gray-500">
            {charCount}/5000
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <button
            type="submit"
            disabled={loading || emailText.trim() === ""}
            className={`flex-1 py-4 rounded-xl text-lg font-bold shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 ${
              loading || emailText.trim() === ""
                ? "bg-gradient-to-r from-gray-300 to-gray-400 cursor-not-allowed text-gray-600"
                : "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white hover:scale-105 hover:shadow-xl"
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-3">
                <svg
                  className="animate-spin h-6 w-6 text-white"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v8z"
                  />
                </svg>
                Processing Email...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <span>🤖</span>
                Generate AI Reply
              </span>
            )}
          </button>
          
          {emailText && !loading && (
            <button
              type="button"
              onClick={() => {
                setEmailText("");
                setCharCount(0);
              }}
              className="px-6 py-4 bg-gray-500 hover:bg-gray-600 text-white rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 hover:scale-105"
            >
              Clear
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default EmailForm;
