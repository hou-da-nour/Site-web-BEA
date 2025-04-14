import React from 'react';

const ButtonHome = () => {
  return (
    <div className="relative inline-block ">
      <button className=" cursor-pointer relative inline-block px-4 py-1 rounded-full bg-gradient-to-b from-blue-800 via-blue-600 to-blue-400 text-white font-medium text-sm shadow-lg hover:scale-105 transform transition-all duration-300">
        <span className="relative z-10 inline-block px-6 py-3 rounded-full overflow-hidden">
          <a href='https://www.bea.dz/' className='font-bold font-mono'>Visiter Notre Siteweb</a>
        </span>
        <div className="absolute inset-0 bg-gradient-to-b from-blue-400 to-blue-600 opacity-60 filter blur-sm transition-all duration-500"></div>
        <div className="absolute left-1/2 transform -translate-x-1/2 top-1 -z-10 bg-blue-500 w-24 h-2 rounded-full opacity-50 blur-lg"></div>
        <div className="absolute inset-0 bg-blue-700 opacity-10 mix-blend-overlay"></div>
      </button>
    </div>
  );
};

export default ButtonHome;
