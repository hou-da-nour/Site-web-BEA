import React, { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import building from '../../../assets/chatbot.jpg'; 
import { Link } from 'react-router-dom';


const About = () => {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);

  return (
    <div className="py-20 px-10 md:px-20 bg-[#CAF0F8]" id='apropos'>

      {/* Titre */}
      <h1 className="text-3xl sm:text-5xl font-bold text-center text-[#03045E] mb-12 mt-6"
          data-aos="fade-down">
        À propos <span className="underline underline-offset-4 decoration-1 font-light text-[#023E8A]">De Notre Chatbot</span>
      </h1>

      {/* Section principale */}
      <section className="flex flex-col md:flex-row items-center justify-between">

        {/* Image */}
        <div
          className="w-full md:w-1/2 mb-10 md:mb-0"
          data-aos="fade-right"
        >
          <img
            src={building}
            className="rounded-tl-[150px] w-full h-[500px] object-cover shadow-lg filter "
          />
        </div>

        {/* Texte */}
        <div
          className="w-full md:w-1/2 md:pl-12 text-center md:text-left"
          data-aos="fade-left"
        >
          <div className="grid grid-cols-2 gap-6 mb-8 text-[#03045E]">
            <div>
              <h3 className="text-3xl font-bold">10+</h3>
              <p className="text-sm text-[#064957]">Années d'excellence</p>
            </div>
            <div>
              <h3 className="text-3xl font-bold">12+</h3>
              <p className="text-sm text-[#064957]">Projets terminés</p>
            </div>
            <div>
              <h3 className="text-3xl font-bold">20+</h3>
              <p className="text-sm text-[#064957]">Fonctionnalités</p>
            </div>
            <div>
              <h3 className="text-3xl font-bold">25+</h3>
              <p className="text-sm text-[#064957]">Utilisateurs actifs</p>
            </div>
          </div>

          <p className="text-base text-[#064957] mb-6">
            Notre chatbot est conçu pour transformer votre expérience bancaire. Il répond à vos questions, vous oriente vers les bons services, et vous accompagne 24h/24 avec rapidité et efficacité.
          </p>

          <Link to="/description-detaillee" onClick={() => {
              setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 50);
          }}>
            <button className="bg-[#023E8A] text-[#CAF0F8] py-2 px-6 rounded hover:bg-blue-700 transition cursor-pointer">
              En savoir plus
            </button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default About;
