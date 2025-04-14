package org.example.services;

import org.example.models.Question;
import org.example.repositories.QuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class ChatbotService {

    @Autowired
    private QuestionRepository questionRepository;

    /**
     * Trouve une réponse à une question posée par un client.
     */
    public String getResponse(String questionText) {
        Optional<Question> question = questionRepository.findByQuestiontextIgnoreCase(questionText);
        return question.map(Question::getAnswertext)
                .orElse("Désolé, je ne connais pas la réponse à cette question.");
    }
}