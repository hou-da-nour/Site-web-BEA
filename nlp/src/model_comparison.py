import pandas as pd
import numpy as np
import json
from pathlib import Path
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_preprocessing import DataPreprocessor
from src.config import MODEL_NAME, MODELS_DIR

logger = logging.getLogger(__name__)

class ModelComparison:
    def __init__(self, model_name=None):
        """Initialise la comparaison des modèles."""
        self.results_dir = MODELS_DIR / "comparison_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialiser le modèle avec le nom spécifié
        self.model = DataPreprocessor(model_name=model_name)
    
    def compare_performance(self, questions: list, save_results: bool = True) -> dict:
        """
        Compare les performances avec et sans cache.
        
        Args:
            questions (list): Liste de questions à tester
            save_results (bool): Sauvegarder les résultats
        
        Returns:
            dict: Résultats de la comparaison
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'questions': [],
            'metrics': {
                'with_cache': {'total_time': 0},
                'without_cache': {'total_time': 0}
            }
        }
        
        # Statistiques pour les visualisations
        with_cache_times = []
        without_cache_times = []
        
        for question in questions:
            # Test sans cache
            self.model.clear_cache()
            start_time = datetime.now()
            _ = self.model.preprocess_single_text(question)
            without_cache_time = (datetime.now() - start_time).total_seconds()
            
            # Test avec cache
            start_time = datetime.now()
            _ = self.model.preprocess_single_text(question)
            with_cache_time = (datetime.now() - start_time).total_seconds()
            
            # Stocker les résultats
            question_result = {
                'question': question,
                'with_cache': {
                    'time': with_cache_time
                },
                'without_cache': {
                    'time': without_cache_time
                }
            }
            
            results['questions'].append(question_result)
            
            # Mettre à jour les métriques
            results['metrics']['with_cache']['total_time'] += with_cache_time
            results['metrics']['without_cache']['total_time'] += without_cache_time
            
            # Collecter les données pour les visualisations
            with_cache_times.append(with_cache_time)
            without_cache_times.append(without_cache_time)
        
        # Calculer les moyennes
        num_questions = len(questions)
        results['metrics']['with_cache']['avg_time'] = results['metrics']['with_cache']['total_time'] / num_questions
        results['metrics']['without_cache']['avg_time'] = results['metrics']['without_cache']['total_time'] / num_questions
        
        # Calculer le gain de performance
        results['metrics']['speedup'] = results['metrics']['without_cache']['avg_time'] / results['metrics']['with_cache']['avg_time']
        
        # Sauvegarder les résultats
        if save_results:
            self._save_results(results)
            self._generate_visualizations(with_cache_times, without_cache_times)
        
        return results
    
    def _save_results(self, results: dict):
        """Sauvegarde les résultats dans un fichier JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.results_dir / f"comparison_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Résultats sauvegardés dans {filename}")
    
    def _generate_visualizations(self, with_cache_times, without_cache_times):
        """Génère les visualisations des résultats."""
        # Utiliser un style matplotlib valide
        plt.style.use('seaborn-v0_8')
        
        # Créer le graphique
        plt.figure(figsize=(10, 6))
        plt.hist([with_cache_times, without_cache_times], 
                label=['Avec cache', 'Sans cache'],
                bins=30, alpha=0.7)
        plt.xlabel('Temps de traitement (secondes)')
        plt.ylabel('Nombre de questions')
        plt.title('Distribution des temps de traitement')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Sauvegarder le graphique
        plt.savefig(self.results_dir / "performance_comparison.png")
        plt.close()
    
    def generate_report(self, results: dict) -> str:
        """Génère un rapport détaillé des résultats."""
        report = [
            "=== Rapport Détaillé de Performance ===",
            f"Date: {results['timestamp']}",
            "\n1. Métriques Globales:",
            f"- Nombre de questions testées: {len(results['questions'])}",
            f"- Temps moyen sans cache: {results['metrics']['without_cache']['avg_time']:.3f}s",
            f"- Temps moyen avec cache: {results['metrics']['with_cache']['avg_time']:.3f}s",
            f"- Accélération: {results['metrics']['speedup']:.2f}x",
            "\n2. Détails par Question:"
        ]
        
        # Trier les questions par gain de performance
        sorted_questions = sorted(
            results['questions'],
            key=lambda x: x['without_cache']['time'] / x['with_cache']['time'],
            reverse=True
        )
        
        # Ajouter les questions avec le meilleur gain
        report.append("\nQuestions avec le meilleur gain de performance:")
        for q in sorted_questions[:5]:
            speedup = q['without_cache']['time'] / q['with_cache']['time']
            report.extend([
                f"\nQuestion: {q['question']}",
                f"- Temps sans cache: {q['without_cache']['time']:.3f}s",
                f"- Temps avec cache: {q['with_cache']['time']:.3f}s",
                f"- Accélération: {speedup:.2f}x"
            ])
        
        # Conclusion
        report.extend([
            "\n3. Conclusion:",
            f"- Le cache améliore les performances de {results['metrics']['speedup']:.2f}x en moyenne",
            f"- {len([q for q in results['questions'] if q['with_cache']['time'] < q['without_cache']['time']])} questions bénéficient du cache",
            f"- Le gain de performance est plus important pour les questions répétées"
        ])
        
        return "\n".join(report)

def main():
    """Fonction principale pour exécuter la comparaison."""
    # Exemple de questions à tester
    test_questions = [
        "Comment recharger ma carte prépayée ?",
        "Quelles sont les étapes pour ouvrir un compte ?",
        "Comment contacter le service client ?",
        "Quels sont les frais de transaction ?",
        "Comment bloquer ma carte en cas de perte ?"
    ]
    
    # Créer et exécuter la comparaison
    comparison = ModelComparison()
    results = comparison.compare_performance(test_questions)
    
    # Générer et afficher le rapport
    report = comparison.generate_report(results)
    print(report)

if __name__ == "__main__":
    main() 