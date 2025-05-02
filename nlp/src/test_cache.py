import pandas as pd
import time
import logging
from pathlib import Path
from tqdm import tqdm
from src.answer_finder import AnswerFinder
from src.config import DATA_DIR

logger = logging.getLogger(__name__)

def test_cache_performance():
    """Teste les performances du cache avec différentes configurations."""
    # Charger les questions
    df = pd.read_csv(DATA_DIR / "faqs_clean.csv")
    questions = df['question'].tolist()
    print(f"Nombre de questions chargées: {len(questions)}")
    
    # Initialiser AnswerFinder
    finder = AnswerFinder()
    
    # Test 1: Sans cache
    print("\n=== Test sans cache ===")
    finder.clear_cache()  # Vider le cache
    start_time = time.time()
    
    for question in tqdm(questions[:100], desc="Test sans cache"):
        _ = finder.find_best_answer(question, "Générale")
    
    without_cache_time = time.time() - start_time
    print(f"Temps sans cache: {without_cache_time:.2f} secondes")
    
    # Test 2: Avec cache
    print("\n=== Test avec cache ===")
    start_time = time.time()
    
    for question in tqdm(questions[:100], desc="Test avec cache"):
        _ = finder.find_best_answer(question, "Générale")
    
    with_cache_time = time.time() - start_time
    print(f"Temps avec cache: {with_cache_time:.2f} secondes")
    
    # Test 3: Questions répétées
    print("\n=== Test avec questions répétées ===")
    repeated_questions = questions[:10] * 10  # Répéter 10 questions 10 fois
    start_time = time.time()
    
    for question in tqdm(repeated_questions, desc="Test questions répétées"):
        _ = finder.find_best_answer(question, "Générale")
    
    repeated_time = time.time() - start_time
    print(f"Temps avec questions répétées: {repeated_time:.2f} secondes")
    
    # Calculer les métriques
    speedup = without_cache_time / with_cache_time
    repeated_speedup = (without_cache_time * len(repeated_questions)) / repeated_time
    
    print("\n=== Résultats ===")
    print(f"Accélération moyenne: {speedup:.2f}x")
    print(f"Accélération avec questions répétées: {repeated_speedup:.2f}x")
    
    # Afficher les statistiques du cache
    cache_stats = finder.preprocessor.get_cache_stats()
    print("\n=== Statistiques du Cache ===")
    print(f"Taille du cache: {cache_stats['size']}")
    print(f"Taille maximale: {cache_stats['max_size']}")
    print(f"TTL: {cache_stats['ttl']} secondes")

def optimize_cache():
    """Suggère des optimisations pour le cache."""
    print("\n=== Suggestions d'Optimisation ===")
    
    # 1. Ajuster la taille du cache
    print("\n1. Ajustement de la taille du cache:")
    print("- Augmenter CACHE_SIZE si vous avez beaucoup de RAM")
    print("- Réduire CACHE_SIZE si vous avez des problèmes de mémoire")
    print("- Recommandation: CACHE_SIZE = nombre de questions fréquentes * 1.5")
    
    # 2. Ajuster le TTL
    print("\n2. Ajustement du TTL (Time To Live):")
    print("- Augmenter TTL pour les questions qui changent rarement")
    print("- Réduire TTL pour les questions qui changent souvent")
    print("- Recommandation: TTL = 3600 (1 heure) pour les FAQ statiques")
    
    # 3. Optimisations FAISS
    print("\n3. Optimisations FAISS:")
    print("- Utiliser GPU si disponible")
    print("- Ajuster le nombre de clusters pour l'index")
    print("- Utiliser des index quantifiés pour réduire la mémoire")
    
    # 4. Stratégies de cache
    print("\n4. Stratégies de cache avancées:")
    print("- Implémenter un cache à deux niveaux (mémoire + disque)")
    print("- Utiliser un cache distribué pour les déploiements multiples")
    print("- Mettre en cache les résultats par catégorie")

if __name__ == "__main__":
    print("=== Test des Performances du Cache ===")
    test_cache_performance()
    optimize_cache() 