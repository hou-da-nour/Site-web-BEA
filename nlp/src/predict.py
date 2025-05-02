import argparse
import logging
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import MODELS_DIR, DATA_DIR
from src.data_preprocessing import DataPreprocessor
from src.model import FAQClassifier
from src.utils import setup_logging

def parse_args():
    parser = argparse.ArgumentParser(description='Prédiction de catégories pour de nouvelles questions')
    parser.add_argument('--input', type=str, required=True,
                       help='Chemin vers le fichier CSV contenant les questions à classifier')
    parser.add_argument('--output', type=str, default='predictions.csv',
                       help='Chemin pour sauvegarder les prédictions')
    parser.add_argument('--show-proba', action='store_true',
                       help='Afficher les probabilités pour chaque classe')
    parser.add_argument('--confidence-threshold', type=float, default=0.75,
                       help='Seuil de confiance pour considérer une prédiction comme certaine')
    return parser.parse_args()

def main(args):
    logger = logging.getLogger(__name__)
    logger.info("Début des prédictions...")
    
    # Chargement des données
    logger.info(f"Lecture du fichier d'entrée: {args.input}")
    df = pd.read_csv(args.input)
    
    if 'question' not in df.columns:
        raise ValueError("Le fichier CSV doit contenir une colonne 'question'")
    
    # Chargement des modèles
    logger.info("Chargement du modèle...")
    classifier = FAQClassifier.load()
    preprocessor = DataPreprocessor()
    
    # Prétraitement des questions
    logger.info("Prétraitement des questions...")
    embeddings = []
    for question in df['question']:
        embedding = preprocessor.preprocess_single_text(question)
        embeddings.append(embedding)
    embeddings = np.array(embeddings)
    
    # Prédictions avec confiance
    logger.info("Prédiction des catégories...")
    predictions = classifier.predict_with_confidence(
        embeddings, 
        args.confidence_threshold,
        questions=df['question'].tolist()
    )
    
    # Préparation des résultats
    results = []
    for i, (question, pred) in enumerate(zip(df['question'], predictions)):
        # Vérification de la cohérence des probabilités
        probas = classifier.predict_proba(embeddings[i:i+1])[0]
        predicted_idx = np.argmax(probas)
        predicted_class = classifier.label_encoder.inverse_transform([predicted_idx])[0]
        
        # Vérification que la catégorie prédite correspond bien à la plus haute probabilité
        if predicted_class != pred['category']:
            logger.warning(f"Incohérence détectée pour la question: {question}")
            logger.warning(f"Catégorie prédite: {pred['category']} (confiance: {pred['confidence']:.2%})")
            logger.warning(f"Catégorie avec plus haute probabilité: {predicted_class} (confiance: {probas[predicted_idx]:.2%})")
            # Utiliser la catégorie avec la plus haute probabilité
            pred['category'] = predicted_class
            pred['confidence'] = probas[predicted_idx]
        
        result = {
            'question': question,
            'categorie_predite': pred['category'],
            'confiance': pred['confidence'],
            'est_confiant': pred['is_confiant'],
            'est_presque_ambigu': pred['is_near_ambiguous'],
            'distance_classification': pred['distance'],
            'categorie_alternative': pred['top2']['category'],
            'confiance_alternative': pred['top2']['confidence']
        }
        
        if args.show_proba:
            for idx, class_name in enumerate(classifier.label_encoder.classes_):
                result[f'proba_{class_name}'] = probas[idx]
        
        results.append(result)
    
    # Création du DataFrame
    results_df = pd.DataFrame(results)
    
    # Sauvegarde des résultats
    results_df.to_csv(args.output, index=False)
    logger.info(f"Prédictions sauvegardées dans: {args.output}")
    
    # Affichage d'un résumé
    logger.info("\nRésumé des prédictions:")
    summary = results_df['categorie_predite'].value_counts()
    for cat, count in summary.items():
        logger.info(f"{cat}: {count} questions")
    
    # Affichage des cas ambigus
    ambiguous = results_df[~results_df['est_confiant']]
    if not ambiguous.empty:
        logger.info("\nCas ambigus détectés:")
        for _, row in ambiguous.iterrows():
            logger.info(f"\nQuestion: {row['question']}")
            logger.info(f"Catégorie prédite: {row['categorie_predite']} (confiance: {row['confiance']:.2%})")
            logger.info(f"Catégorie alternative: {row['categorie_alternative']} (confiance: {row['confiance_alternative']:.2%})")
            logger.info(f"Distance de classification: {row['distance_classification']:.2%}")
            if args.show_proba:
                logger.info("Probabilités par catégorie:")
                for col in results_df.columns:
                    if col.startswith('proba_'):
                        logger.info(f"  {col[6:]}: {row[col]:.2%}")
    
    # Affichage des cas presque ambigus
    near_ambiguous = results_df[results_df['est_presque_ambigu']]
    if not near_ambiguous.empty:
        logger.info("\nCas presque ambigus (distance faible):")
        for _, row in near_ambiguous.iterrows():
            logger.info(f"\nQuestion: {row['question']}")
            logger.info(f"Catégorie prédite: {row['categorie_predite']} (confiance: {row['confiance']:.2%})")
            logger.info(f"Catégorie alternative: {row['categorie_alternative']} (confiance: {row['confiance_alternative']:.2%})")
            logger.info(f"Distance de classification: {row['distance_classification']:.2%}")

if __name__ == "__main__":
    args = parse_args()
    setup_logging()
    main(args) 