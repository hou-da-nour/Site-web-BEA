package org.example.services;
import org.example.exceptions.ResourceNotFoundException;
import org.example.models.Question;
import org.example.repositories.QuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class QuestionService {

    @Autowired
    private QuestionRepository questionRepository;

    // Ajouter une question
    public Question addQuestion(Question question) {
        return questionRepository.save(question);
    }

    // Récupérer toutes les questions
    public List<Question> getAllQuestions() {
        return questionRepository.findAll();
    }

    // Récupérer une question par ID
    public Question getQuestionById(Long id) {
        return questionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Question non trouvée avec l'ID : " + id));
    }


    // Modifier une question
    public Question updateQuestion(Long id, Question newQuestion) {
        Question question = questionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Impossible de modifier : Question non trouvée avec l'ID : " + id));

        question.setQuestiontext(newQuestion.getQuestiontext());
        question.setAnswertext(newQuestion.getAnswertext());

        return questionRepository.save(question);
    }


    // Supprimer une question
    public void deleteQuestion(Long id) {
        Question question = questionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Impossible de supprimer : Question non trouvée avec l'ID : " + id));

        questionRepository.delete(question);
    }

}
