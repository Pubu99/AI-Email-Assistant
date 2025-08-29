import React, { useState } from "react";

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

function ResultCard({ intent, reply }) {
  const [copied, setCopied] = useState(false);
  const icon = intentIcons[intent] || "✉️";
  const color = intentColors[intent] || "bg-gray-100 text-gray-700";

  const handleCopy = () => {
    navigator.clipboard.writeText(reply).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="w-full max-w-xl bg-white/95 p-8 mt-10 rounded-2xl shadow-2xl border border-gray-100 transition-all duration-300 hover:shadow-3xl">
      <div className="flex items-center gap-3 mb-4">
        <span className={`text-3xl ${color} rounded-full px-3 py-1 shadow-sm`}>
          {icon}
        </span>
        <h2 className="text-2xl font-bold text-gray-800 tracking-tight">
          {intent}
        </h2>
      </div>

      <div className="flex items-center justify-between mb-2">
        <h2 className="text-lg font-semibold text-gray-700">Generated Reply</h2>
        <button
          onClick={handleCopy}
          className={`text-xs bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-4 py-1.5 rounded shadow transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 ${
            copied ? "scale-105" : ""
          }`}
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>

      <pre
        className="whitespace-pre-wrap bg-gradient-to-br from-gray-50 to-blue-50 border border-blue-100 rounded-xl p-5 text-gray-900 font-sans leading-relaxed text-base shadow-inner transition-all duration-200 hover:bg-blue-50"
        style={{ minHeight: "110px", fontSize: "1.08rem" }}
      >
        {reply || "Generating reply..."}
      </pre>
    </div>
  );
}

export default ResultCard;
