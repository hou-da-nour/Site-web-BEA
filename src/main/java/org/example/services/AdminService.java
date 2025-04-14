package org.example.services;

import org.example.models.Admin;
import org.example.DTO.AdminDTO;
import org.example.exceptions.ResourceNotFoundException;
import org.example.repositories.AdminRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AdminService {

    @Autowired
    private AdminRepository adminRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    /**
     * Crée un nouvel administrateur.
     */
    public Admin createAdmin(AdminDTO adminDTO) {
        Admin admin = new Admin();
        admin.setUsername(adminDTO.getUsername());
        admin.setPassword(passwordEncoder.encode(adminDTO.getPassword())); // Hash du mot de passe
        return adminRepository.save(admin);
    }

    /**
     * Authentifie un administrateur sans JWT (pour tests).
     */
    public String authenticate(String username, String password) {
        Admin admin = adminRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("Identifiants invalides"));

        if (!passwordEncoder.matches(password, admin.getPassword())) {
            throw new ResourceNotFoundException("Mot de passe incorrect !");
        }

        return "Authentification réussie"; // ✅ On retourne juste un message pour tester sans JWT
    }
}

