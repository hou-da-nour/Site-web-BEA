// import { useRef } from "react";


// export const ChatForm = ({chatHistory , setChatHistory , generateBotResponse}) => {
//     const inputRef = useRef();

//     const handleFormSubmit = (e) => {
//         e.preventDefault();
//         const userMessage = inputRef.current.value.trim();   //Getting the input value and removing whitespaces
//         if(!userMessage) return;
//         inputRef.current.value = "";   // Cleaning the message input after getting the value

        
//         // Update chat history with the user's message
//         setChatHistory(history => [...history , { role: "user" , text : userMessage}]);

//         //  Delay 600 ms before showing "..." and generating
//         setTimeout(() => {
//             // Add a " ..." placeholder for the bot's mssage
//             setChatHistory((history) => [
//               ...history,
//               { role: "model", text :"Thinking ..." } // Utilisation d'une propriété spéciale pour l'animation
//             ]);
//             // setChatHistory((history) => [
//             //   ...history,
//             //   { role: "model", isTyping: true } // Utilisation d'une propriété spéciale pour l'animation
//             // ]);

//             // Call the Function to generate the Bot's response
//             generateBotResponse([...chatHistory,{ role: "user" , text : userMessage}]);
//         } , 600 );

//     };
    
//   return (
//     <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
//         <input ref={inputRef} type="text" placeholder="Message..." className="message-input" required />
//         <button className="material-symbols-rounded">arrow_upward</button>
//     </form>
//   );
// };



// import { useRef } from "react";

// export const ChatForm = ({ generateBotResponse }) => {
//   const inputRef = useRef();

//   const handleFormSubmit = (e) => {
//     e.preventDefault();
//     const userMessage = inputRef.current.value.trim();
    
//     if (!userMessage) return;
    
//     inputRef.current.value = "";
//     generateBotResponse(userMessage); // 🔹 Envoie le message au backend
//   };

//   return (
//     <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
//       <input ref={inputRef} type="text" placeholder="Message..." className="message-input" required />
//       <button className="material-symbols-rounded">arrow_upward</button>
//     </form>
//   );
// };

// chatpbt
import { useRef } from "react";

export const ChatForm = ({ chatHistory, setChatHistory, generateBotResponse }) => {
  const inputRef = useRef();

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const userMessage = inputRef.current.value.trim();  

    if (!userMessage) return;
    inputRef.current.value = "";  

    // Ajouter le message utilisateur dans l'historique
    setChatHistory(history => [...history, { role: "user", text: userMessage }]);

    // Ajouter un message de "chargement" du bot
    setTimeout(() => {
      setChatHistory(history => [...history, { role: "bot", text: "Thinking ..." }]);

      // Appeler la fonction pour obtenir la réponse du bot
      generateBotResponse([...chatHistory, { role: "user", text: userMessage }]);
    }, 600);
  };

  return (
    <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
      <input ref={inputRef} type="text" placeholder="Poser une question" className="message-input" required />
      <button className="material-symbols-rounded">arrow_upward</button>
    </form>
  );
};



