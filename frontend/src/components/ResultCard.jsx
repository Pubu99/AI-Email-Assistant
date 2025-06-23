import React from 'react';

function ResultCard({ intent, reply }) {
  return (
    <div className="w-full max-w-xl bg-white p-6 mt-8 rounded shadow">
      <h2 className="text-xl font-bold mb-3 text-gray-800">Predicted Intent:</h2>
      <p className="mb-6 text-gray-700">{intent}</p>

      <h2 className="text-xl font-bold mb-3 text-gray-800">Generated Reply:</h2>
      <p className="whitespace-pre-line text-gray-900">{reply}</p>
    </div>
  );
}

export default ResultCard;
