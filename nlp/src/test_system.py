import pandas as pd
import logging
from pathlib import Path
from src.config import DATA_DIR, MODELS_DIR
from src.data_preprocessing import DataPreprocessor
from src.model import FAQClassifier
from src.answer_finder import AnswerFinder
from src.utils import setup_logging

def test_system():
    """Teste le système complet de prédiction et recherche de réponses."""
    logger = logging.getLogger(__name__)
    logger.info("Début du test du système...")

    # Chargement des données de test
    logger.info("Chargement des données de test...")
    test_df = pd.read_csv(DATA_DIR / "test_questions.csv")
    
    # Initialisation des composants
    logger.info("Initialisation des composants...")
    preprocessor = DataPreprocessor()
    classifier = FAQClassifier.load()
    answer_finder = AnswerFinder()
    
    # Préparation des données
    logger.info("Préparation des données...")
    X_test, _ = preprocessor.prepare_data(test_df, augment=False)
    
    # Prédictions
    logger.info("Génération des prédictions...")
    predictions = classifier.predict_with_confidence(X_test, questions=test_df['question'].tolist())
    
    # Recherche des réponses
    logger.info("Recherche des réponses...")
    results = []
    for i, (question, pred) in enumerate(zip(test_df['question'], predictions)):
        # Recherche de la meilleure réponse
        answer_result = answer_finder.find_best_answer(
            question=question,
            predicted_category=pred['category'],
            min_similarity=0.7
        )
        
        # Préparation du résultat
        result = {
            'Question': question,
            'Catégorie Prédite': pred['category'],
            'Confiance Catégorie': f"{pred['confidence']:.6f}",
            'Est Confiant': pred['is_confiant'],
            'Distance': f"{pred['distance']:.6f}",
            'Entropie': f"{pred['entropy']:.6f}",
            'Réponse': answer_result['answer'],
            'Similarité Réponse': f"{answer_result['similarity']:.6f}",
            'Question Similaire': answer_result['best_question'],
            'Est Confiant Réponse': answer_result['is_confident']
        }
        
        # Ajout des alternatives si disponibles
        if answer_result['alternatives']:
            result['Alternatives'] = " | ".join([
                f"{alt['question']} ({alt['similarity']:.6f})"
                for alt in answer_result['alternatives']
            ])
        else:
            result['Alternatives'] = "Aucune"
        
        results.append(result)
    
    # Création du DataFrame des résultats
    results_df = pd.DataFrame(results)
    
    # Sauvegarde des résultats
    results_df.to_csv(MODELS_DIR / "system_test_results.csv", index=False)
    logger.info(f"Résultats sauvegardés dans {MODELS_DIR / 'system_test_results.csv'}")
    
    # Affichage des résultats
    logger.info("\nRésultats du système :")
    for result in results:
        logger.info(f"\nQuestion : {result['Question']}")
        logger.info(f"Catégorie prédite : {result['Catégorie Prédite']} (confiance: {result['Confiance Catégorie']})")
        logger.info(f"Réponse : {result['Réponse']}")
        logger.info(f"Similarité : {result['Similarité Réponse']}")
        logger.info(f"Question similaire : {result['Question Similaire']}")
        if result['Alternatives'] != "Aucune":
            logger.info(f"Alternatives : {result['Alternatives']}")
    
    # Statistiques globales
    logger.info("\nStatistiques globales :")
    logger.info(f"Nombre total de questions : {len(results)}")
    logger.info(f"Nombre de prédictions confiantes : {sum(1 for r in results if r['Est Confiant'])}")
    logger.info(f"Nombre de réponses confiantes : {sum(1 for r in results if r['Est Confiant Réponse'])}")
    
    logger.info("\nTest terminé!")

if __name__ == "__main__":
    setup_logging()
    test_system() 