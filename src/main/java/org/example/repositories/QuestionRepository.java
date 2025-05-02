package org.example.repositories;

import org.example.models.Question;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;
@Repository
public interface QuestionRepository extends JpaRepository<Question, Long> {
    List<Question> findByQuestiontextIgnoreCase(String questiontext);
}
