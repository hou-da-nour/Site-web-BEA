import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion'; 

const AboutDetails = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }} 
      animate={{ opacity: 1, y: 0 }}   
      transition={{ duration: 0.8, ease: 'easeOut' }}
      className="min-h-screen px-6 py-20 lg:px-24 bg-[#E0F7FA] text-[#03045E]"
    >
      <h1 className="text-4xl font-bold text-center mb-10">
        Détails sur le <span className="text-[#0077B6]">Chatbot BEA</span>
      </h1>

      <div className="flex flex-col lg:flex-row items-center gap-10">
        <img
          src="/home/chat2.jpg"
          alt="Chatbot"
          className="w-full lg:w-1/2 rounded-xl shadow-xl"
        />

        <div className="lg:w-1/2 space-y-4">
          <p>
            Le <strong>Chatbot BEA</strong> est un assistant virtuel conçu pour répondre aux questions fréquentes des clients de la Banque Extérieure d’Algérie. Accessible 24h/24, il facilite la navigation sur le site et oriente les utilisateurs vers les services bancaires adaptés.
          </p>

          <ul className="list-disc list-inside text-[#023E8A]">
            <li>Informations générales : horaires, agences, documents requis</li>
            <li>Ouverture de compte : conditions, étapes et formulaires</li>
            <li>Demandes de prêts : types, taux d’intérêt, éligibilité</li>
            <li>Conseils de sécurité bancaire</li>
            <li>Redirection vers un conseiller humain si nécessaire</li>
          </ul>

          <p className="pt-4">
            Le chatbot ne gère pas de données personnelles sensibles. Les opérations comme la consultation de solde ou les virements restent accessibles via l’application mobile sécurisée de la BEA.
          </p>

          <Link to="/">
            <button className="mt-6 px-6 py-2 bg-[#03045E] text-white rounded-full hover:bg-[#0077B6] cursor-pointer">
              Retour à l'accueil
            </button>
          </Link>
        </div>
      </div>
    </motion.div>
  );
};

export default AboutDetails;
