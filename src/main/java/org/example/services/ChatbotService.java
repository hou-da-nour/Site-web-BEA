package org.example.services;

import org.example.models.Question;
import org.example.repositories.QuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ChatbotService {

    @Autowired
    private NlpClientService nlpClientService;

    public String getResponse(String questionText) {
        return nlpClientService.getAnswerFromFlask(questionText);
    }
}
