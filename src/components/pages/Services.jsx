import React, { useState } from 'react';



const Services = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const services = [
    {
      title: "Informations Générales",
      description: "Horaires, adresses des agences, numéros utiles, et conditions d’utilisation des services BEA.",
      img: "/services/service1.jpg"
    },
    {
      title: "Ouverture de Compte",
      description: "Le chatbot vous guide sur les étapes et documents nécessaires pour ouvrir un compte bancaire BEA.",
      img: "/services/service2.jpg"
    },
    {
      title: "Prêts et Crédits",
      description: "Obtenez des informations sur les types de crédits, les taux d'intérêt, les conditions et les démarches à suivre.",
      img: "/services/service3.jpeg"
    },
    {
      title: "Assistance Client",
      description: "Posez vos questions et le chatbot vous oriente ou vous redirige vers un conseiller si besoin.",
      img: "/services/service4.jpg"
    },
    {
      title: "Sécurité & Conseils",
      description: "Recevez des conseils pour protéger votre compte et éviter les tentatives de fraude.",
      img: "/services/service5.jpg"
    }
  ];
  

  // Affiche plusieurs services en même temps
  const servicesToDisplay = [
    services[currentIndex % services.length],
    services[(currentIndex + 1) % services.length],
    services[(currentIndex + 2) % services.length]
  ];
  

const nextService = () => {
  setCurrentIndex((prevIndex) => (prevIndex + 1) % services.length);
};

const prevService = () => {
  setCurrentIndex((prevIndex) => 
    (prevIndex - 1 + services.length) % services.length
  );
};


  return (
    <div className="bg-[#ADE8F4] min-h-screen flex flex-col items-center justify-center mx-auto p-20 md:px-20 lg:px-32 w-full overflow-hidden " id='services'>
      {/* Titre en dehors de la div des services */}
      <h1 className="text-3xl sm:text-5xl font-bold text-center text-[#03045E] mb-12 mt-6" data-aos="fade-down">
        Nos <span className="underline underline-offset-4 decoration-1 font-light text-[#023E8A]">Services</span>
      </h1>

      {/* Contenu des services */}
      <div className="relative">
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
          {servicesToDisplay.map((service, index) => (
            <div key={index} className="group relative cursor-pointer items-center justify-center overflow-hidden transition-shadow hover:shadow-xl hover:shadow-bleu/30 rounded-3xl">
              <div className="h-96 w-72 ">
                <img className="h-full w-full object-cover transition-transform duration-500 group-hover:rotate-3 group-hover:scale-125 " 
                     src={service.img} 
                     alt={service.title} />
              </div>
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black group-hover:from-black/70 group-hover:via-black/60 group-hover:to-black/70"></div>
              <div className="absolute inset-0 flex translate-y-[60%] flex-col items-center justify-center px-9 text-center transition-all duration-500 group-hover:translate-y-0">
                <h1 className="font-dmserif text-3xl font-bold text-[#ADE8F4] mb-10">{service.title}</h1>
                <p className="mb-3 text-lg italic text-[#CAF0F8] opacity-0 transition-opacity duration-300 group-hover:opacity-100">{service.description}</p>

                
              </div>
            </div>
          ))}
        </div>

        {/* Flèches de navigation */}
        <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 -translate-y-[-80px] flex space-x-4  ">
          <button onClick={prevService} className="bg-[#03045E] text-[#CAF0F8] py-2 px-3 rounded-full  shadow-lg hover:bg-gray-700 cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" aria-hidden="true" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button onClick={nextService} className="bg-[#03045E] text-[#CAF0F8] py-2 px-3 rounded-full shadow-lg hover:bg-gray-700 cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" aria-hidden="true" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Services;
