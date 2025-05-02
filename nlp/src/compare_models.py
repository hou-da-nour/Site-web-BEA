import pandas as pd
from pathlib import Path
import logging
from tqdm import tqdm
from src.model_comparison import ModelComparison
from src.config import DATA_DIR, MODEL_NAME

logger = logging.getLogger(__name__)

def load_test_questions():
    """Charge les questions de test depuis le fichier CSV."""
    try:
        df = pd.read_csv(DATA_DIR / "faqs_clean.csv")
        logger.info(f"Chargement de {len(df)} questions depuis {DATA_DIR / 'faqs_clean.csv'}")
        return df['question'].tolist()
    except Exception as e:
        logger.error(f"Erreur lors du chargement des questions: {e}")
        raise

def main():
    """Fonction principale pour comparer les performances avec et sans cache."""
    try:
        # Charger les questions
        questions = load_test_questions()
        print(f"Nombre de questions chargées: {len(questions)}")
        
        # Utiliser toutes les questions
        print(f"Test avec toutes les questions ({len(questions)} questions)")
        
        # Comparer les performances avec et sans cache
        print("\n=== Test de Performance ===")
        try:
            comparison = ModelComparison(model_name=MODEL_NAME)
            results = comparison.compare_performance(questions)
            report = comparison.generate_report(results)
            print("Test terminé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du test: {e}")
            report = "Erreur lors du test"
        
        # Générer le rapport
        print("\n" + "="*80)
        print("=== Rapport de Performance ===")
        print(f"\nModèle: {MODEL_NAME}")
        print(report)
        print("="*80)
        
        # Sauvegarder le rapport
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        with open(reports_dir / f"performance_report_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write(report)
            
        print(f"\nRapport sauvegardé dans le dossier 'reports/'")
        print("Visualisations générées dans le dossier 'models/saved_models/comparison_results/'")
        
    except Exception as e:
        logger.error(f"Erreur lors de la comparaison: {e}")
        raise

if __name__ == "__main__":
    main() 