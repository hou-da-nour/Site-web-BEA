import requests
import time
import json
from tqdm import tqdm

def test_api_performance():
    """Teste les performances de l'API avec et sans cache."""
    # URL de l'API
    api_url = "http://localhost:5000/predict-category"
    
    # Questions de test
    test_questions = [
        "Comment recharger ma carte prépayée ?",
        "Quelles sont les étapes pour ouvrir un compte ?",
        "Comment contacter le service client ?",
        "Quels sont les frais de transaction ?",
        "Comment bloquer ma carte en cas de perte ?"
    ]
    
    # Test 1: Sans cache
    print("\n=== Test sans cache ===")
    # Vider le cache via l'API
    requests.post("http://localhost:5000/clear-cache")
    
    start_time = time.time()
    for question in tqdm(test_questions, desc="Test sans cache"):
        response = requests.post(api_url, json={"question": question})
        if response.status_code != 200:
            print(f"Erreur: {response.text}")
    without_cache_time = time.time() - start_time
    
    # Test 2: Avec cache
    print("\n=== Test avec cache ===")
    start_time = time.time()
    for question in tqdm(test_questions, desc="Test avec cache"):
        response = requests.post(api_url, json={"question": question})
        if response.status_code != 200:
            print(f"Erreur: {response.text}")
    with_cache_time = time.time() - start_time
    
    # Test 3: Questions répétées
    print("\n=== Test avec questions répétées ===")
    repeated_questions = test_questions * 3  # Répéter 3 fois
    start_time = time.time()
    for question in tqdm(repeated_questions, desc="Test questions répétées"):
        response = requests.post(api_url, json={"question": question})
        if response.status_code != 200:
            print(f"Erreur: {response.text}")
    repeated_time = time.time() - start_time
    
    # Afficher les résultats
    print("\n=== Résultats ===")
    print(f"Temps sans cache: {without_cache_time:.2f} secondes")
    print(f"Temps avec cache: {with_cache_time:.2f} secondes")
    print(f"Temps avec questions répétées: {repeated_time:.2f} secondes")
    
    # Calculer les accélérations
    speedup = without_cache_time / with_cache_time
    repeated_speedup = (without_cache_time * len(repeated_questions)) / repeated_time
    
    print(f"\nAccélération moyenne: {speedup:.2f}x")
    print(f"Accélération avec questions répétées: {repeated_speedup:.2f}x")

if __name__ == "__main__":
    print("=== Test des Performances de l'API ===")
    test_api_performance() 