package org.example.models;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import java.util.List;

@Entity
@Table(name = "admins")
@Getter
@Setter
@NoArgsConstructor
public class Admin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;  // Il faudra le chiffrer plus tard !




    @OneToMany(mappedBy = "admin", fetch = FetchType.LAZY)
    @JsonIgnore  // ⬅️ Ignore cette relation lors de la conversion en JSON
    private List<Question> questions;  // ⚠️ Une liste de questions
}
