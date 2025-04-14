import React from 'react';
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-[#023E8A] text-[#CAF0F8] pt-10 pb-6 px-6 md:px-20 text-center" id='footer'>
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left ">
        {/* Logo / Nom */}
        <div>
          <h2 className="text-2xl font-bold mb-3">BEA Chatbot</h2>
          <p className="text-sm text-gray-300">Votre assistant intelligent pour des services rapides, simples et disponibles 24h/24.</p>
        </div>

        {/* Liens rapides */}
        <div>
          <h3 className="text-xl font-semibold mb-3">Navigation</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li><a href="#accueil" className="hover:underline">Accueil</a></li>
            <li><a href="#apropos" className="hover:underline">À propos</a></li>
            <li><a href="#services" className="hover:underline">Services</a></li>
            <li><a href="#contact" className="hover:underline">Contact</a></li>
          </ul>
        </div>

        {/* Réseaux sociaux */}
        <div>
          <h3 className="text-xl font-semibold mb-3">Suivez-nous</h3>
          <div className="flex justify-center md:justify-start space-x-4">
            <a href="https://www.facebook.com/BEAlgerie/?locale=fr_FR" className="hover:text-gray-300"><FaFacebookF /></a>
            {/* <a href="#" className="hover:text-gray-300"><FaTwitter /></a> */}
            <a href="https://www.instagram.com/banque_bea/" className="hover:text-gray-300"><FaInstagram /></a>
            <a href="https://dz.linkedin.com/company/banque-ext%C3%A9rieure-d-alg%C3%A9rie" className="hover:text-gray-300"><FaLinkedin /></a>
          </div>
        </div>
      </div>

      {/* Ligne séparatrice */}
      <div className="border-t border-[#CAF0F8]-500 mt-8 pt-4 text-center text-sm text-gray-300">
        © {new Date().getFullYear()} BEA Chatbot. Tous droits réservés.
      </div>
    </footer>
  );
};

export default Footer;
