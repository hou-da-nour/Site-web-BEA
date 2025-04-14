package org.example.controllers;

import org.example.models.Question;
import org.example.repositories.QuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.example.DTO.QuestionResponse;
import org.example.DTO.QuestionRequest;

import java.util.List;

@RestController
@RequestMapping("/chatbot")
public class ChatbotController {

    @Autowired
    private QuestionRepository questionRepository;

    // 🔹 L'utilisateur envoie une question en JSON et reçoit une réponse en JSON
    @PostMapping
    public QuestionResponse askQuestion(@RequestBody QuestionRequest request) {
        return questionRepository.findByQuestiontextIgnoreCase(request.getQuestion())
                .map(q -> new QuestionResponse(q.getAnswertext()))
                .orElseGet(() -> new QuestionResponse("Je ne connais pas encore la réponse à cette question."));
    }

    // 🔹 Ajout d'une nouvelle question avec réponse (JSON)
    @PostMapping("/add")
    public String addQuestion(@RequestBody Question newQuestion) {
        questionRepository.save(newQuestion);
        return "Question ajoutée avec succès !";
    }

    // 🔹 Récupérer toutes les questions enregistrées
    @GetMapping("/questions")
    public List<Question> getAllQuestions() {
        return questionRepository.findAll();
    }

    // 🔹 Vérification si le chatbot est en ligne
    @GetMapping
    public String testChatbot() {
        System.out.println("🔥 Endpoint /chatbot GET a été appelé !");
        return "L'API Chatbot est en ligne 🚀";
    }
}
