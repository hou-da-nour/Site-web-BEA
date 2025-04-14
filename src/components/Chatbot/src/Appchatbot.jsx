import { useState, useEffect, useRef } from "react";
import ChatbotIcon from "./components/ChatbotIcon";
import { ChatForm } from "./components/ChatForm";
import { ChatMessage } from "./components/ChatMessage";
import chatbotImage from "./assets/images/chatbot-icon.jpg";

const App = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [showChatbot, setShowChatbot] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isKeyboardOpen, setIsKeyboardOpen] = useState(false);
  const chatBodyRef = useRef(null);
  

  // connection avec le backend 
  const askBackendChatbot = async (userMessage) => {
    
  try {
    const response = await fetch("http://localhost:8080/api/questions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        questiontext: userMessage, // ✅ Utilise le bon champ
        answertext: "" // Laisse vide si ce n'est pas requis
      }),
      mode: "cors"
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP : ${response.status}`);
    }

    const data = await response.json();
    console.log("Réponse API :", data); // Ajoute ceci pour voir ce que ton backend renvoie
    return data.answertext || "Réponse non disponible"; 
  } catch (error) {
    console.error("Erreur lors de la communication avec le chatbot :", error);
    return "Désolé, une erreur s'est produite. Veuillez réessayer.";
  }
};
  //  Détecter si le clavier est ouvert
  useEffect(() => {
    const handleResize = () => {
      if (window.innerHeight < 500) {
        setIsKeyboardOpen(true);
      } else {
        setIsKeyboardOpen(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  //  Scroll automatique en bas à chaque mise à jour du chat ou quand l'utilisateur tape un message
  useEffect(() => {
    if (chatBodyRef.current) {
      setTimeout(() => {
        chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
      }, 300);
    }
  }, [chatHistory, isKeyboardOpen]);

  //  Fonction pour gérer l'envoi de message
  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    setChatHistory(prevHistory => [...prevHistory, { role: "user", text: message }]);
    setIsLoading(true);

    const botResponse = await askBackendChatbot(message);
    console.log("Réponse reçue :", botResponse); // 🔹 DEBUG

    setChatHistory(prevHistory => [
      ...prevHistory,
      { role: "bot", text: botResponse || "Désolé, pas de réponse du serveur." }
    ]);

    setIsLoading(false);
  };
  return (
    <div className={`container ${showChatbot ? "show-chatbot" : ""}`}>
      <button onClick={() => setShowChatbot(prev => !prev)} id="chatbot-toggler">
        {showChatbot ? <span className="material-symbols-rounded">close</span> : <img src={chatbotImage} className="chatbot-icon" alt="Chatbot Icon" />}
      </button>

      {showChatbot && (
        <div className={`chatbot-popup ${isKeyboardOpen ? "keyboard-open" : ""}`}>
          <div className="chat-header">
            <div className="header-info">
              <ChatbotIcon />
              <div className="intro-text">
                <h2 className="logo-text">Chatbot Assistant</h2>
                <p> ● En ligne </p>
              </div>
            </div>
            <button onClick={() => setShowChatbot(prev => !prev)} className="material-symbols-rounded">Keyboard_arrow_down</button>
          </div>

          <div className="chat-body" ref={chatBodyRef}>
            <div className="message bot-message">
              <ChatbotIcon />
              <p className="message-text">
                Bonjour ! 👋<br /> Je suis votre assistant virtuel BEA. Comment puis-je vous aider aujourd’hui ?
              </p>
            </div>

            {chatHistory.map((chat, index) => (
              <ChatMessage key={index} chat={chat} />
            ))}

            {isLoading && (
              <div className="message bot-message">
                <ChatbotIcon />
                <p className="message-text typing-animation">...</p>
              </div>
            )}
          </div>

          <div className="chat-footer">
            <ChatForm 
              chatHistory={chatHistory} 
              setChatHistory={setChatHistory} 
              generateBotResponse={handleSendMessage} 
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;