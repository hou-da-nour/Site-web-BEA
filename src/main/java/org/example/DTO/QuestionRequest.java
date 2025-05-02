package org.example.DTO;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class QuestionRequest {
    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    private String question;
}
