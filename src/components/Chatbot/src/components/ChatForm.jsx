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

// 
import { useRef } from "react";

export const ChatForm = ({ chatHistory, setChatHistory, generateBotResponse }) => {
  const inputRef = useRef();

  const handleFormSubmit = (e) => {
    e.preventDefault();

    const userMessage = String(inputRef.current.value).trim();
    console.log("Input message:", inputRef.current.value);


    if (!userMessage) return;

    // Nettoyer le champ input
    inputRef.current.value = "";

    // Nouveau tableau d'historique avec le message de l'utilisateur
    const updatedHistory = [...chatHistory, { role: "user", text: userMessage }];
    setChatHistory(updatedHistory);

    // Ajouter un message "bot typing..." puis appeler generateBotResponse
    // setTimeout(() => {
    //   setChatHistory(prev => [...prev, { role: "bot", text: "Thinking ..." }]);

    //   // Appeler le backend ou générer une réponse fictive
    //   generateBotResponse(updatedHistory);
    // }, 600);
    setTimeout(() => {
      // Affiche un message temporaire "Thinking..."
      setChatHistory((prev) => [...prev, { role: "bot", text: "Thinking ..." }]);
    
      // Appelle la fonction de génération
      generateBotResponse([...chatHistory, { role: "user", text: userMessage }]);
    }, 600);
    
  };

  return (
    <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
      <input
        ref={inputRef}
        type="text"
        placeholder="Poser une question"
        className="message-input"
        required
      />
      <button className="material-symbols-rounded">arrow_upward</button>
    </form>
  );
};



