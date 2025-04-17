import React from 'react';
import './Loader.css'; // 🔥 On importe le CSS personnalisé

const Loader = () => {
  return (
    <div className="flex justify-center items-center h-screen bg-white">
      <div className="boxes">
        <div className="box">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div className="box">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div className="box">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div className="box">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>
    </div>
  );
};

export default Loader;


// import React from 'react';


// const Loader = () => {
//   return (
//     <div className="fixed inset-0 bg-white flex items-center justify-center z-50">
//       <div className="w-12 h-12 border-4 border-blue-300 border-t-blue-700 rounded-full animate-spin"></div>
//     </div>
//   );
// };

// export default Loader;


