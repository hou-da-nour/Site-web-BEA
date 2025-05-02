import time
import torch
from tqdm import tqdm
from src.data_preprocessing import DataPreprocessor
from src.config import MODEL_NAME

def benchmark_model():
    """Mesure les performances du modèle avec différentes configurations."""
    print("=== Benchmark du Modèle ===")
    
    # 1. Test de chargement
    print("\n1. Test de chargement du modèle")
    start_time = time.time()
    preprocessor = DataPreprocessor(model_name=MODEL_NAME)
    load_time = time.time() - start_time
    print(f"Temps de chargement: {load_time:.2f} secondes")
    print(f"Device utilisé: {preprocessor.device}")
    
    # 2. Test de prédiction
    print("\n2. Test de prédiction")
    test_questions = [
        "Comment recharger ma carte prépayée ?",
        "Quelles sont les étapes pour ouvrir un compte ?",
        "Comment contacter le service client ?",
        "Quels sont les frais de transaction ?",
        "Comment bloquer ma carte en cas de perte ?"
    ]
    
    # Test sans cache
    print("\nTest sans cache:")
    preprocessor.clear_cache()
    times = []
    for question in tqdm(test_questions, desc="Prédictions sans cache"):
        start = time.time()
        _ = preprocessor.preprocess_single_text(question)
        times.append(time.time() - start)
    avg_time_no_cache = sum(times) / len(times)
    print(f"Temps moyen sans cache: {avg_time_no_cache:.4f} secondes")
    
    # Test avec cache
    print("\nTest avec cache:")
    times = []
    for question in tqdm(test_questions, desc="Prédictions avec cache"):
        start = time.time()
        _ = preprocessor.preprocess_single_text(question)
        times.append(time.time() - start)
    avg_time_with_cache = sum(times) / len(times)
    print(f"Temps moyen avec cache: {avg_time_with_cache:.4f} secondes")
    
    # Test avec questions répétées
    print("\nTest avec questions répétées:")
    repeated_questions = test_questions * 3
    times = []
    for question in tqdm(repeated_questions, desc="Prédictions répétées"):
        start = time.time()
        _ = preprocessor.preprocess_single_text(question)
        times.append(time.time() - start)
    avg_time_repeated = sum(times) / len(times)
    print(f"Temps moyen avec questions répétées: {avg_time_repeated:.4f} secondes")
    
    # Calculer les accélérations
    speedup = avg_time_no_cache / avg_time_with_cache
    repeated_speedup = (avg_time_no_cache * len(repeated_questions)) / (avg_time_repeated * len(repeated_questions))
    
    print("\n=== Résultats ===")
    print(f"Temps de chargement: {load_time:.2f} secondes")
    print(f"Temps moyen sans cache: {avg_time_no_cache:.4f} secondes")
    print(f"Temps moyen avec cache: {avg_time_with_cache:.4f} secondes")
    print(f"Temps moyen avec questions répétées: {avg_time_repeated:.4f} secondes")
    print(f"\nAccélération moyenne: {speedup:.2f}x")
    print(f"Accélération avec questions répétées: {repeated_speedup:.2f}x")
    
    # Afficher les statistiques du cache
    cache_stats = preprocessor.get_cache_stats()
    print("\n=== Statistiques du Cache ===")
    print(f"Taille du cache: {cache_stats['size']}")
    print(f"Taille maximale: {cache_stats['max_size']}")
    print(f"TTL: {cache_stats['ttl']} secondes")

if __name__ == "__main__":
    benchmark_model() 