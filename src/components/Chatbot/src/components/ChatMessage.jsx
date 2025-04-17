// import React from 'react'
// import ChatbotIcon from './ChatbotIcon';

// export const ChatMessage = ({ chat }) => {
//   return (
//     // Ajout de la gestion de l'animation lorsque le chatbot est en train de répondre
//     <div className={`message ${chat.role === "model" ? "bot" : "user"}-message`}> 
      
//       {/* Affichage de l'icône du chatbot uniquement pour les messages du bot */}
//       {chat.role === "model" && <ChatbotIcon />}

//       {/* Vérification si le chatbot est en train de taper (animation "…") */}
//       {chat.isTyping ? (
//         <div className="typing-dots">
//           <span></span>
//           <span></span>
//           <span></span>
//         </div>
//       ) : (
//         <p className="message-text">{chat.text}</p>
//       )}
//     </div>
//   );
// };

// 
import React from 'react';
import ChatbotIcon from './ChatbotIcon';

export const ChatMessage = ({ chat }) => {
  console.log("Message reçu :", chat);

  return (
    <div className={`message ${chat.role === "bot" ? "bot-message" : "user-message"}`}> 
      {/* Icône du chatbot seulement si c'est un message du bot */}
      {chat.role === "bot" && <ChatbotIcon />}

      {/* Message ou animation */}
      {chat.isTyping ? (
        <div className="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      ) : (
        <p className="message-text">{chat.text}</p>
      )}
    </div>
  );
};

// youtube
// import React from 'react'
// import ChatbotIcon from './ChatbotIcon';

// export const ChatMessage = ({ chat }) => {
//   return (
//     <div className={`message ${chat.role === "model" ? "bot" : "user"}-message`}> 
      
      
//       {chat.role === "model" && <ChatbotIcon />}

//       <p className="message-text">{chat.text}</p>
//     </div>
//   );
// };