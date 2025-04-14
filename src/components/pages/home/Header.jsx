import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import ButtonHome from './ButtonHome';
import { motion } from 'framer-motion'; 

const Header = () => {
  const images = [
    '/home/chat.jpg',
    '/home/chat3.jpg',
    '/home/chat4.jpg' 
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div 
      className="min-h-screen bg-cover bg-center flex items-center justify-center w-full overflow-hidden transition-all duration-500 relative " id='accueil'
      style={{ backgroundImage: `url(${images[currentIndex]})` }}
    >
      {/* Overlay sombre */}
      <div className="absolute inset-0 bg-black opacity-50"></div>

      {/* Flou */}
      <div className="absolute inset-0 blur-lg"></div> 

      <div className="relative z-10 text-center text-[#CAF0F8] px-6 md:px-12">
        <Navbar />

        <motion.h2
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="text-4xl md:text-5xl font-extrabold mb-4"
        >
          Votre assistant bancaire intelligent toujours à votre service !
        </motion.h2>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2, ease: "easeOut", delay: 0.3 }}
          className="text-lg md:text-xl mb-6 max-w-2xl mx-auto"
        >
          Discutez avec notre chatbot et obtenez des réponses instantanées sur vos comptes, 
          transactions et services bancaires, 24h/24 et 7j/7.
        </motion.p>
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2, ease: "easeOut", delay: 0.3 }}
          className="text-lg md:text-xl mb-6 max-w-2xl mx-auto"
        >
          <ButtonHome />
        </motion.p>
      </div>
    </div>
  );
};

export default Header;
