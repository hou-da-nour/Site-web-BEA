package org.example.controllers;

import org.example.models.Question;
import org.example.repositories.QuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    private QuestionRepository questionRepository;

    // 🔹 Ajouter une question
    @PostMapping("/questions")
    public Question addQuestion(@RequestBody Question question) {
        return questionRepository.save(question);
    }

    // 🔹 Modifier une question
    @PutMapping("/questions/{id}")
    public Question updateQuestion(@PathVariable Long id, @RequestBody Question questionDetails) {
        Optional<Question> questionOptional = questionRepository.findById(id);
        if (questionOptional.isPresent()) {
            Question question = questionOptional.get();
            question.setQuestiontext(questionDetails.getQuestiontext());  // Correction de "setQuestion" → "setTexte"
            question.setAnswertext(questionDetails.getAnswertext());
            return questionRepository.save(question);
        } else {
            throw new RuntimeException("Question non trouvée");
        }
    }

    // 🔹 Supprimer une question
    @DeleteMapping("/questions/{id}")
    public void deleteQuestion(@PathVariable Long id) {
        questionRepository.deleteById(id);
    }

    // 🔹 Lister toutes les questions
    @GetMapping("/questions")
    public List<Question> getAllQuestions() {
        return questionRepository.findAll();
    }
}
