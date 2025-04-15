import React from 'react';

const DemoPage = () => {
  return (
    <div className="bg-[#90E0EF] min-h-screen w-full overflow-hidden px-4 md:px-20 lg:px-32 py-10" id='démonstration'>
      
      {/* Titre indépendant */}
      <h1 className="text-3xl sm:text-5xl font-bold text-center text-[#03045E] mb-12 mt-6" data-aos="fade-down">
        Démonstration <span className="underline underline-offset-4 decoration-1 font-light text-[#023E8A]">Interactive</span>
      </h1>
      
      {/* Contenu vidéo + démo */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-10">
        
        {/* Vidéo à gauche */}
        <div className="w-full md:w-1/2">
          <video className="rounded-lg shadow-xl w-full" controls autoPlay muted loop>
            <source src={`${import.meta.env.BASE_URL}chat.mp4`} type="video/mp4" />
            Votre navigateur ne supporte pas la vidéo.
          </video>
        </div>

        {/* Démo chatbot à droite avec animation */}
        <div className="w-full md:w-1/2 animate-fade-in-up">
          <div className="bg-[#48CAE4] rounded-xl p-6 shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">Mini Conversation</h2>
            <div className="text-sm bg-[#ADE8F4] p-3 rounded mb-2">👤 Bonjour, j’ai besoin d’aide.</div>
            <div className="text-sm bg-[#CAF0F8] p-3 rounded mb-2 text-right">🤖 Bien sûr ! Comment puis-je vous aider aujourd'hui ?</div>
            <div className="text-sm bg-[#ADE8F4] p-3 rounded mb-2">👤 Je veux ouvrir un compte.</div>
            <div className="text-sm bg-[#CAF0F8] p-3 rounded text-right">🤖 Très bien ! Voici les étapes à suivre.</div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default DemoPage;
