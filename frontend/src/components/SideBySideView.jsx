import React, { useState } from "react";
import Toast from "./Toast";

const intentIcons = {
  "Meeting Request": "📅",
  "Job Inquiry": "💼",
  Finance: "💰",
  Legal: "⚖️",
  Appreciation: "🙏",
  Complaint: "😠",
  "Technical Support": "🛠️",
  "Data Request": "📄",
  Greeting: "👋",
  Farewell: "👋",
  "Sales Inquiry": "🛒",
  "Project Update": "📈",
  Reminder: "⏰",
  "Event Planning": "🎉",
  Personal: "💌",
  "General Inquiry": "❓",
};

const intentColors = {
  "Meeting Request": "bg-blue-100 text-blue-700",
  "Job Inquiry": "bg-green-100 text-green-700",
  Finance: "bg-yellow-100 text-yellow-700",
  Legal: "bg-purple-100 text-purple-700",
  Appreciation: "bg-pink-100 text-pink-700",
  Complaint: "bg-red-100 text-red-700",
  "Technical Support": "bg-indigo-100 text-indigo-700",
  "Data Request": "bg-gray-100 text-gray-700",
  Greeting: "bg-teal-100 text-teal-700",
  Farewell: "bg-teal-100 text-teal-700",
  "Sales Inquiry": "bg-orange-100 text-orange-700",
  "Project Update": "bg-cyan-100 text-cyan-700",
  Reminder: "bg-amber-100 text-amber-700",
  "Event Planning": "bg-fuchsia-100 text-fuchsia-700",
  Personal: "bg-rose-100 text-rose-700",
  "General Inquiry": "bg-gray-100 text-gray-700",
};

function SideBySideView({ inputEmail, intent, reply, onNewEmail }) {
  const [copied, setCopied] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const icon = intentIcons[intent] || "✉️";
  const color = intentColors[intent] || "bg-gray-100 text-gray-700";

  const handleCopy = () => {
    navigator.clipboard.writeText(reply).then(() => {
      setCopied(true);
      setShowToast(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="w-full max-w-7xl mx-auto mt-8 space-y-6">
      {/* Toast notification */}
      {showToast && (
        <Toast
          message="Reply copied to clipboard!"
          type="success"
          onClose={() => setShowToast(false)}
        />
      )}

      {/* Header with intent classification */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className={`text-3xl ${color} rounded-full px-3 py-2 shadow-lg`}>
            {icon}
          </span>
          <div>
            <h2 className="text-2xl font-bold text-gray-800 tracking-tight">
              Email Classified as: {intent}
            </h2>
            <p className="text-sm text-gray-600 mt-1">AI-powered analysis and response generation</p>
          </div>
        </div>
        <button
          onClick={onNewEmail}
          className="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white px-6 py-2 rounded-lg shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 hover:scale-105"
        >
          New Email
        </button>
      </div>

      {/* Side by side layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Email Card */}
        <div className="bg-white/95 p-6 rounded-2xl shadow-xl border border-gray-100 transition-all duration-300 hover:shadow-2xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
              <span className="text-blue-600">📧</span>
              Original Email
            </h3>
            <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
              Input
            </span>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-5 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-gray-800 font-sans leading-relaxed text-sm">
              {inputEmail}
            </pre>
          </div>
        </div>

        {/* Generated Reply Card */}
        <div className="bg-white/95 p-6 rounded-2xl shadow-xl border border-gray-100 transition-all duration-300 hover:shadow-2xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
              <span className="text-green-600">🤖</span>
              AI Generated Reply
            </h3>
            <div className="flex items-center gap-2">
              <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                Output
              </span>
              <button
                onClick={handleCopy}
                className={`text-xs bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-4 py-1.5 rounded-lg shadow transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 ${
                  copied ? "scale-105" : ""
                }`}
              >
                {copied ? "✓ Copied!" : "📋 Copy"}
              </button>
            </div>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-100 rounded-xl p-5 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-gray-800 font-sans leading-relaxed text-sm">
              {reply || "Generating reply..."}
            </pre>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex justify-center mt-8">
        <div className="flex gap-4">
          <button
            onClick={handleCopy}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-3 rounded-lg shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 hover:scale-105 font-medium"
          >
            Copy Reply to Clipboard
          </button>
          <button
            onClick={() => {
              const subject = `Re: ${intent} - AI Generated Response`;
              const body = encodeURIComponent(reply);
              window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${body}`);
            }}
            className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-3 rounded-lg shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 hover:scale-105 font-medium"
          >
            Open in Email Client
          </button>
        </div>
      </div>
    </div>
  );
}

export default SideBySideView;
