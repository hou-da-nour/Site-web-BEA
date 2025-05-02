package org.example.services;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class NlpClientService {

    private final RestTemplate restTemplate = new RestTemplate();

    public String getAnswerFromFlask(String question) {
        String flaskUrl = "http://localhost:5000/predict-category";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // Corps JSON à envoyer
        Map<String, String> payload = Map.of("question", question);
        HttpEntity<Map<String, String>> request = new HttpEntity<>(payload, headers);

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(flaskUrl, request, Map.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                Map<String, Object> body = response.getBody();

                if (body != null && Boolean.TRUE.equals(body.get("success"))) {
                    String answer = (String) body.get("answer");
                    String category = (String) body.get("category");
                    double confidence = (double) body.get("confidence");

                    return String.format("Catégorie : %s\nRéponse : %s\nConfiance : %.2f",
                            category, answer, confidence);
                } else {
                    return "Aucune réponse NLP disponible.";
                }
            }
            return "Erreur : NLP non disponible.";

        } catch (Exception e) {
            return "Erreur de communication avec le service NLP : " + e.getMessage();
        }
    }
}
