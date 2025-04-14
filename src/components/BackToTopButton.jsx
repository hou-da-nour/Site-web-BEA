import React from 'react';

const BackToTopButton = () => {
  // Fonction pour faire défiler la page en haut
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <button
      onClick={scrollToTop}
      className="fixed  bottom-10 h-[50px] w-[50px] left-4 p-3 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-all duration-200 cursor-pointer"
    >
      <span className="text-xl"> ^ </span>
    </button>
  );
};

export default BackToTopButton;
