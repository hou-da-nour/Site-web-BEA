import React from 'react';

const Demo = () => {
  return (
    <div className="bg-[#CAF0F8] min-h-screen flex flex-col items-center" id='démonstration'>
      {/* Titre  */}
      <h1 className="text-3xl sm:text-5xl font-bold text-center text-[#03045E] mb-12 mt-6" data-aos="fade-down">
        Demonstration <span className="underline underline-offset-4 decoration-1 font-light text-[#023E8A]">De Chatbot</span>
      </h1>
      
      <main className="flex flex-col items-center  mt-10">
        <section className="max-w-4xl w-full p-6 bg-white rounded-lg shadow-lg ">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">Comment fonctionne le Chatbot ?</h2>
          
          <div className="relative pb-9/16 mb-6">
            <iframe
              className="absolute top-0 left-0 w-full h-full "
              src="/1.mp4" // Remplacez "votre-video-id" par l'ID de votre vidéo YouTube
              title="Démonstration Chatbot"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>

          <p className="text-lg text-gray-700">
            Découvrez comment notre chatbot intelligent fonctionne, avec une démonstration détaillée de ses fonctionnalités.
          </p>
        </section>

        <section className="mt-10 w-full max-w-4xl p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Pourquoi utiliser ce Chatbot ?</h3>
          <ul className="list-disc pl-5 space-y-2 text-lg text-gray-700">
            <li>Répondre instantanément à toutes vos questions financières.</li>
            <li>Améliorer l'expérience utilisateur avec des interactions intelligentes.</li>
            <li>Optimiser les services clients en fournissant une assistance 24/7.</li>
            <li>Des réponses précises basées sur une analyse intelligente des données.</li>
          </ul>
        </section>
      </main>

    </div>
  );
};

export default Demo;
