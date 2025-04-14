// Loader.jsx
import React from 'react';

const Loader = () => {
  return (
    <div className="flex items-center justify-center h-screen bg-white">
      <div className="relative w-12 h-12 animate-spin-custom">
        <div className="absolute w-3 h-3 bg-blue-600 rounded-full top-0 left-0" />
        <div className="absolute w-3 h-3 bg-blue-600 rounded-full top-0 right-0" />
        <div className="absolute w-3 h-3 bg-blue-600 rounded-full bottom-0 left-0" />
        <div className="absolute w-3 h-3 bg-blue-600 rounded-full bottom-0 right-0" />
      </div>
    </div>
  );
};

export default Loader;
