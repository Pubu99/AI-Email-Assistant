import React, { useState } from "react";

function ResultCard({ intent, reply }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(reply).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // Reset after 2 sec
    });
  };

  return (
    <div className="w-full max-w-xl bg-white p-6 mt-8 rounded-lg shadow-md border border-gray-200">
      <h2 className="text-xl font-semibold mb-3 text-gray-900">Predicted Intent:</h2>
      <p className="mb-6 text-gray-700">{intent}</p>

      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-semibold text-gray-900">Generated Reply:</h2>
        <button
          onClick={handleCopy}
          className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded transition"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>

      <pre
        className="whitespace-pre-wrap bg-gray-50 border border-gray-300 rounded p-4 text-gray-900 font-sans leading-relaxed"
        style={{ minHeight: "100px" }}
      >
        {reply || "Generating reply..."}
      </pre>
    </div>
  );
}

export default ResultCard;
