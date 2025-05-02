import argparse
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from collections import Counter

from src.config import *
from src.data_preprocessing import DataPreprocessor
from src.model import FAQClassifier
from src.utils import setup_logging, save_metrics, calculate_metrics

def parse_args():
    parser = argparse.ArgumentParser(description='Entraînement du modèle de classification FAQ')
    parser.add_argument('--data', type=str, default=str(DATA_DIR / "faqs_clean.csv"),
                       help='Chemin vers le fichier CSV des données')
    parser.add_argument('--test-size', type=float, default=TEST_SIZE,
                       help='Proportion du jeu de test')
    parser.add_argument('--random-state', type=int, default=RANDOM_STATE,
                       help='Graine aléatoire pour la reproductibilité')
    parser.add_argument('--save-embeddings', action='store_true',
                       help='Sauvegarder les embeddings')
    parser.add_argument('--cv-folds', type=int, default=5,
                       help='Nombre de folds pour la validation croisée')
    return parser.parse_args()

def train_model(args):
    logger = logging.getLogger(__name__)
    logger.info("Début de l'entraînement...")

    # Chargement des données
    logger.info(f"Chargement des données depuis {args.data}")
    df = pd.read_csv(args.data)
    
    # Préparation des données
    logger.info("Préparation des données...")
    preprocessor = DataPreprocessor()
    X, y = preprocessor.prepare_data(df)
    
    if args.save_embeddings:
        np.save(MODELS_DIR / "embeddings.npy", X)
        logger.info("Embeddings sauvegardés")
    
    # Split train/test avec stratification
    logger.info(f"Split des données (test_size={args.test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=args.test_size, 
        random_state=args.random_state,
        stratify=y
    )
    
    # Vérifier la distribution des classes
    class_counts = Counter(y_train)
    logger.info(f"Distribution des classes dans le jeu d'entraînement: {class_counts}")
    
    # Ajuster le nombre de folds en fonction de la plus petite classe
    min_samples = min(class_counts.values())
    n_folds = min(3, min_samples)
    if n_folds < 2:
        logger.warning("Trop peu d'échantillons pour la validation croisée. Utilisation d'un seul fold.")
        n_folds = 1
    
    logger.info(f"Validation croisée ({n_folds} folds)...")
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=args.random_state)
    classifier = FAQClassifier()
    
    try:
        # Scores de validation croisée
        cv_scores = cross_val_score(
            classifier.model, X_train, y_train, 
            cv=cv, scoring='f1_weighted',
            error_score='raise'
        )
        logger.info(f"Scores de validation croisée: {cv_scores}")
        logger.info(f"Moyenne des scores CV: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    except Exception as e:
        logger.warning(f"Erreur lors de la validation croisée: {str(e)}")
        logger.info("Continuation avec l'entraînement direct...")
    
    # Entraînement final
    logger.info("Entraînement du modèle final...")
    classifier.train(X_train, y_train, preprocessor.label_encoder)
    
    # Évaluation sur le test set
    logger.info("Évaluation sur le jeu de test...")
    y_pred = classifier.predict(X_test)
    metrics = calculate_metrics(y_test, y_pred)
    save_metrics(metrics, MODELS_DIR / "metrics.json")
    
    eval_report = classifier.evaluate(X_test, y_test)
    logger.info("\nRapport de classification :\n" + eval_report)
    
    # Matrice de confusion
    logger.info("Génération de la matrice de confusion...")
    cm = confusion_matrix(y_test, y_pred)
    
    # Récupérer les noms des catégories
    labels = preprocessor.label_encoder.classes_
    
    # Tracer la matrice de confusion
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.xlabel('Prédit')
    plt.ylabel('Réel')
    plt.title('Matrice de confusion')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Sauvegarder la figure
    plt.savefig(MODELS_DIR / "confusion_matrix.png")
    logger.info("Matrice de confusion sauvegardée dans models/saved_models/confusion_matrix.png")
    
    # Sauvegarde
    logger.info("Sauvegarde des modèles...")
    classifier.save()
    
    logger.info("Entraînement terminé avec succès!")

if __name__ == "__main__":
    args = parse_args()
    setup_logging()
    train_model(args)
