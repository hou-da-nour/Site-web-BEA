package org.example.models;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import java.time.LocalDateTime;

@Entity
@Table(name = "questions")
@Getter
@Setter
@NoArgsConstructor
public class Question {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 500)
    private String questiontext;

    @Column(nullable = false, length = 500)
    private String answertext;

    @Column(nullable = false)
    private LocalDateTime created_at = LocalDateTime.now();



    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getQuestiontext() {
        return questiontext;
    }

    public void setQuestiontext(String questiontext) {
        this.questiontext = questiontext;
    }

    public String getAnswertext() {
        return answertext;
    }

    public void setAnswertext(String answertext) {
        this.answertext = answertext;
    }

    public LocalDateTime getCreated_at() {
        return created_at;
    }

    public void setCreated_at(LocalDateTime created_at) {
        this.created_at = created_at;
    }

    public Admin getAdmin() {
        return admin;
    }

    public void setAdmin(Admin admin) {
        this.admin = admin;
    }

    // Une question est créée par un seul admin
    @ManyToOne
    @JoinColumn(name = "admin_id", nullable = true)
    private Admin admin;
}
