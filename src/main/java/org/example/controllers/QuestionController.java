package org.example.controllers;

import org.example.DTO.QuestionResponse;
import org.example.DTO.QuestionRequest;
import org.example.models.Question;
import org.example.services.QuestionService;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/questions")
@AllArgsConstructor
public class QuestionController {

    private final QuestionService questionService;

    @PostMapping
    public ResponseEntity<Question> createQuestion(@RequestBody Question question) {
        // Vérifier si la question existe déjà
        List<Question> existingQuestions = questionService.findByText(question.getQuestiontext());

        if (!existingQuestions.isEmpty()) {
            return ResponseEntity.ok(existingQuestions.get(0)); // Retourne la première question trouvée
        }

        // Générer une réponse si elle n'existe pas encore
        String generatedAnswer = findAnswer(question.getQuestiontext());
        question.setAnswertext(generatedAnswer);

        // Sauvegarder la nouvelle question
        Question savedQuestion = questionService.addQuestion(question);
        return ResponseEntity.ok(savedQuestion);
    }

    private String findAnswer(String questiontext) {
        List<Question> existingQuestions = questionService.findByText(questiontext);
        return !existingQuestions.isEmpty() ? existingQuestions.get(0).getAnswertext() : "Réponse non disponible";
    }

    @GetMapping
    public ResponseEntity<List<Question>> getAllQuestions() {
        return ResponseEntity.ok(questionService.getAllQuestions());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Question> getQuestionById(@PathVariable Long id) {
        return ResponseEntity.ok(questionService.getQuestionById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Question> updateQuestion(@PathVariable Long id, @RequestBody Question question) {
        return ResponseEntity.ok(questionService.updateQuestion(id, question));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteQuestion(@PathVariable Long id) {
        questionService.deleteQuestion(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/test")
    public String testEndpoint() {
        return "Le contrôleur fonctionne !";
    }

    @PostMapping("/chatbot")
    public ResponseEntity<QuestionResponse> chatbotResponse(@RequestBody QuestionRequest questionRequest) {
        // Vérifier si la question existe déjà
        List<Question> existingQuestions = questionService.findByText(questionRequest.getQuestion());

        if (!existingQuestions.isEmpty()) {
            // Retourner la première réponse trouvée
            return ResponseEntity.ok(new QuestionResponse(
                    existingQuestions.get(0).getQuestiontext(),
                    existingQuestions.get(0).getAnswertext()
            ));
        }

        // 🔹 Si la question est nouvelle, enregistrer avec "Désolé..."
        Question newQuestion = new Question();
        newQuestion.setQuestiontext(questionRequest.getQuestion());
        newQuestion.setAnswertext("Désolé, je ne connais pas la réponse.");
        questionService.addQuestion(newQuestion);

        return ResponseEntity.ok(new QuestionResponse(newQuestion.getAnswertext()));

    }
}
