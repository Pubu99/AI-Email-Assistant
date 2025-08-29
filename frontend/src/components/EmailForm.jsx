import React, { useState } from "react";

function EmailForm({ onSubmit, loading }) {
  const [emailText, setEmailText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailText.trim() === "") return;
    onSubmit(emailText);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-xl bg-white/90 p-8 rounded-2xl shadow-xl border border-gray-100 transition-all duration-300 hover:shadow-2xl"
      style={{ backdropFilter: "blur(2px)" }}
    >
      <div className="relative mb-6">
        <textarea
          id="emailText"
          rows={8}
          value={emailText}
          onChange={(e) => setEmailText(e.target.value)}
          className="peer w-full border border-gray-300 rounded-lg p-4 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50 transition shadow-sm placeholder-transparent"
          placeholder="Type or paste your email here..."
          disabled={loading}
        />
        <label
          htmlFor="emailText"
          className="absolute left-4 top-2 text-gray-500 text-base font-medium pointer-events-none transition-all duration-200 peer-focus:-top-5 peer-focus:text-sm peer-focus:text-blue-600 peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 bg-white px-1 rounded"
        >
          Paste your email text below
        </label>
      </div>
      <button
        type="submit"
        disabled={loading}
        className={`w-full py-3 rounded-lg text-lg font-bold shadow-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 ${
          loading
            ? "bg-gradient-to-r from-gray-300 to-gray-400 cursor-not-allowed text-gray-600"
            : "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white hover:scale-105"
        }`}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg
              className="animate-spin h-5 w-5 text-white"
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
            Processing...
          </span>
        ) : (
          "Generate Reply"
        )}
      </button>
    </form>
  );
}

export default EmailForm;
