import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import logo from '/BEA.png';
import { navigation } from '../../../constants';
import ButtonNavbar from '../home/ButtonNavbar';
import MenuSvg from '../../../assets/MenuSvg'; // Assure-toi que le chemin est correct
import { HamburgerMenu } from '../../design/Header';
import { motion } from 'framer-motion';



const Navbar = () => {
  const pathname = useLocation();
  const [openNavigation, setOpenNavigation] = useState(false); // Menu initialement fermé
  const toggleNavigation = () => setOpenNavigation(!openNavigation); // Bascule l'état du menu

  const handleClick = () => {
    setOpenNavigation(false); // Ferme la navigation après un clic
  };

  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 500) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.div
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className={`fixed top-0 left-0 w-full z-50 
        ${isScrolled ? 'bg-[#03045E]' : 'backdrop-blur-2xl border-b border-n-6'}
        transition-all duration-500 ease-in-out`}
    >
      <div className="flex items-center px-5 lg:px-7.5 xl:px-10 max-lg:py-4 sm:text-[#03045E]">
        <a className="py-3 block w-[12rem] xl:mr-8" href="#hero">
          <img src={logo} className="w-[50px] h-[45px] mb-[-10px] pb-2" />
          <p className="text-[0.8rem] font-bold text-[#90E0EF]">Banque Exterieur D’Algerie</p>
        </a>
        <nav
          className={`${openNavigation ? 'flex' : 'hidden'} fixed top-0 left-0 right-0 bg-[#040432] backdrop-blur-2xl lg:static text-[#90E0EF] lg:flex lg:mx-auto lg:bg-transparent py-4 mt-24 sm:py-0 sm:mt-0 sm:mb[10px]`}
        >
          <div className="relative z-2 flex flex-col items-center justify-center m-auto lg:flex-row">
            {navigation.map((item) => (
              <a
                key={item.id}
                href={item.url}
                className={`block relative font-code lg:text-[1rem] sm:text-1.5xl sm:font-bold transition-colors hover:text-[#0096C7] ${item.onlyMobile ? 'lg:hidden' : ''} 
                px-6 py-6 md:py-8 lg:-mr-0.25 lg:text-xs lg:font-semibold ${item.url === pathname.hash ? 'z-2 ' : ' '}
                lg:leading-5 xl:px-12`}
                onClick={handleClick} // Ferme la navigation lorsque l'on clique sur un lien
              >
                {item.title}
              </a>
            ))}
          </div>
          <HamburgerMenu />
        </nav>
        <a>
          <ButtonNavbar />
        </a>
        <button className="ml-auto lg:hidden">
          <MenuSvg openNavigation={openNavigation} toggleNavigation={toggleNavigation} /> {/* Passer l'état et la fonction ici */}
        </button>
      </div>
    </motion.div>
  );
};

export default Navbar;
