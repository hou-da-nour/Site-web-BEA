package org.example.DTO;

public class QuestionResponse {
    private String question;
    private String response;

    // 🔹 Ajoute ce constructeur si nécessaire
    public QuestionResponse(String question, String response) {
        this.question = question;
        this.response = response;
    }

    // 🔹 Constructeur alternatif pour un seul argument
    public QuestionResponse(String response) {
        this.response = response;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getResponse() {
        return response;
    }

    public void setResponse(String response) {
        this.response = response;
    }
}


