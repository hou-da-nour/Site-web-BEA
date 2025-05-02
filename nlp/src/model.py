import logging
import joblib
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from collections import Counter
from src.config import *
from typing import Dict, List, Any, Optional, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

logger = logging.getLogger(__name__)

class FAQDataset(Dataset):
    """Dataset personnalisé pour les questions FAQ."""
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.FloatTensor(X)
        self.y = torch.LongTensor(y.to_numpy() if hasattr(y, 'to_numpy') else y)
    
    def __len__(self) -> int:
        return len(self.X)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.X[idx], self.y[idx]

class FAQClassifier:
    def __init__(self):
        """Initialise le classifieur avec un pipeline plus sophistiqué."""
        # Configuration de SMOTE avec une stratégie personnalisée
        smote = SMOTE(
            sampling_strategy={
                0: 100,  # Augmenter à 100 exemples
                1: 100,  # Augmenter à 100 exemples
                2: 200,  # Augmenter à 200 exemples
                3: 385,  # Garder le même nombre
                4: 50,   # Augmenter à 50 exemples
                5: 150,  # Augmenter à 150 exemples
                6: 230   # Garder le même nombre
            },
            random_state=RANDOM_STATE
        )
        
        # Création du pipeline avec SMOTE et MLPClassifier
        self.model = Pipeline([
            ('smote', smote),
            ('classifier', MLPClassifier(
                hidden_layer_sizes=HIDDEN_LAYERS,
                learning_rate=LEARNING_RATE,
                max_iter=MAX_ITER,
                early_stopping=EARLY_STOPPING,
                validation_fraction=VALIDATION_FRACTION,
                n_iter_no_change=N_ITER_NO_CHANGE,
                random_state=RANDOM_STATE
            ))
        ])
        self.label_encoder = None
        
        # Seuils de confiance par catégorie (ajustés)
        self.category_thresholds = {
            'Sécurité': 0.95,
            'Transaction': 0.90,
            'Compte': 0.85,
            'Prépayée': 0.85,
            'Générale': 0.75,  # Seuil abaissé pour plus de flexibilité
            'Autre': 0.75,
            'Salutation': 0.75
        }
        self.default_threshold = 0.85
        self.distance_threshold = 0.20
        self.near_ambiguous_threshold = 0.10
        
        # Nouveaux paramètres
        self.temperature = 1.2  # Température pour le softmax
        self.alternative_threshold = 0.6
        
        # Règles de détection par mot-clé (déjà améliorées)
        self.keyword_rules = {
            'Salutation': [
                # Salutations de base
                'salut', 'bonjour', 'bonsoir', 'bonne journée', 'bonne soirée', 'salutations',
                # Variations formelles
                'cher', 'madame', 'monsieur', 'messieurs', 'mesdames',
                # Expressions de politesse
                'merci', 'au revoir', 'cordialement', 'bien à vous', 'sincèrement',
                # Expressions de demande
                'pouvez-vous', 'pourriez-vous', 'auriez-vous', 'serait-il possible',
                # Expressions de souhait
                'je souhaite', 'je voudrais', 'j\'aimerais', 'je désire'
            ],
            'Sécurité': [
                # Vol et perte
                'vol', 'perdu', 'égaré', 'disparu', 'manquant', 'trouvé',
                # Piratage et fraude
                'piratage', 'fraude', 'arnaque', 'escroquerie', 'usurpation',
                # Blocage et déblocage
                'bloquer', 'débloquer', 'verrouiller', 'déverrouiller', 'activer', 'désactiver',
                # Codes et sécurité
                'code', 'cvv', 'cvc', 'pin', 'mot de passe', 'identifiant',
                # Alertes et notifications
                'alerte', 'notification', 'suspicion', 'anomalie', 'douteux',
                # Protection
                'protection', 'sécuriser', 'sécurité', 'confidentiel', 'privé'
            ],
            'Transaction': [
                # Types de transactions
                'paiement', 'achat', 'transaction', 'dépense', 'retrait', 'virement', 'transfert',
                # Opérations spécifiques
                'achat en ligne', 'paiement en ligne', 'retrait d\'argent', 'virement bancaire',
                # États des transactions
                'échoué', 'refusé', 'accepté', 'validé', 'annulé', 'en cours',
                # Montants et limites
                'montant', 'plafond', 'limite', 'seuil', 'maximum', 'minimum',
                # Détails transactionnels
                'date', 'heure', 'lieu', 'commerçant', 'marchand', 'boutique'
            ],
            'Compte': [
                # Types de comptes
                'compte', 'compte bancaire', 'compte courant', 'compte épargne',
                # Opérations sur compte
                'solde', 'relevé', 'historique', 'débit', 'crédit', 'opération',
                # Informations de compte
                'rib', 'iban', 'numéro de compte', 'titulaire', 'propriétaire',
                # Gestion de compte
                'ouvrir', 'fermer', 'modifier', 'changer', 'mettre à jour',
                # Services bancaires
                'conseiller', 'service client'
            ],
            'Prépayée': [
                # Types de cartes
                'carte prépayée', 'carte rechargeable', 'carte à recharger',
                # Opérations de recharge
                'recharger', 'recharge', 'crédit', 'solde', 'recharge',
                # Gestion de carte
                'activer', 'désactiver', 'bloquer', 'débloquer', 'perdu',
                # Limites et plafonds
                'plafond', 'limite', 'maximum', 'seuil', 'restriction',
                # Services associés
                'recharge en ligne', 'recharge en agence', 'recharge automatique'
            ],
            'Générale': [
                # Questions de base
                'comment', 'où', 'quand', 'pourquoi', 'quel', 'quelle', 'quels', 'quelles',
                # Expressions de demande
                'pouvez-vous', 'pourriez-vous', 'auriez-vous', 'serait-il possible',
                # Expressions de souhait
                'je souhaite', 'je voudrais', 'j\'aimerais', 'je désire',
                # Expressions de besoin
                'j\'ai besoin', 'il me faut', 'je cherche', 'je recherche',
                # Expressions de compréhension
                'je ne comprends pas', 'je ne sais pas', 'je suis perdu',
                # Informations générales
                'agence', 'banque', 'horaires', 'ouverture', 'fermeture', 'heures', 'jours'
            ],
            'Autre': []  # Catégorie par défaut
        }
    
    def _check_keyword_rules(self, question: str) -> Optional[str]:
        """Vérifie si la question correspond à une règle de mot-clé."""
        question_lower = question.lower()
        for category, keywords in self.keyword_rules.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        return None
    
    def train(self, X: np.ndarray, y: np.ndarray, label_encoder: LabelEncoder) -> None:
        """Entraîne le modèle avec gestion avancée du déséquilibre des classes."""
        self.label_encoder = label_encoder
        
        # Vérifier la distribution des classes
        class_counts = Counter(y)
        logger.info(f"Distribution des classes avant SMOTE: {class_counts}")
        
        # Calculer les poids des classes pour l'entraînement
        total = len(y)
        class_weights = {
            label: total / (len(class_counts) * count)
            for label, count in class_counts.items()
        }
        logger.info(f"Poids des classes: {class_weights}")
        
        # Ajuster les paramètres SMOTE en fonction de la distribution
        min_samples = min(class_counts.values())
        if min_samples <= 2:
            logger.warning(f"Classe avec très peu d'échantillons ({min_samples}). Désactivation de SMOTE pour ces classes.")
            sampling_strategy = {
                label: count for label, count in class_counts.items()
            }
            self.model.named_steps['smote'].set_params(
                k_neighbors=1,
                sampling_strategy=sampling_strategy
            )
        elif min_samples <= 5:
            logger.warning(f"Classe avec peu d'échantillons ({min_samples}). Ajustement des paramètres SMOTE.")
            sampling_strategy = {
                label: 5 if count < 5 else count
                for label, count in class_counts.items()
            }
            self.model.named_steps['smote'].set_params(
                k_neighbors=min(2, min_samples - 1),
                sampling_strategy=sampling_strategy
            )
        
        # Créer le dataset PyTorch
        dataset = FAQDataset(X, y)
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
        
        logger.info("Entraînement du modèle avec SMOTE et MLPClassifier...")
        self.model.fit(X, y)
        
        # Vérifier la nouvelle distribution après SMOTE
        y_resampled = self.model.named_steps['smote'].fit_resample(X, y)[1]
        new_counts = Counter(y_resampled)
        logger.info(f"Distribution des classes après SMOTE: {new_counts}")
        
        logger.info("Entraînement terminé!")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Prédit les classes pour de nouvelles données."""
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Retourne les probabilités de prédiction."""
        return self.model.predict_proba(X)
    
    def _apply_temperature_scaling(self, probas: np.ndarray) -> np.ndarray:
        """Applique la température scaling aux probabilités."""
        scaled_probas = probas / self.temperature
        return np.exp(scaled_probas) / np.sum(np.exp(scaled_probas), axis=1, keepdims=True)

    def predict_with_confidence(self, X: np.ndarray, threshold: Optional[float] = None, questions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Prédit les classes avec gestion avancée de la confiance et des cas ambigus."""
        probas = self.predict_proba(X)
        # Appliquer la température scaling
        probas = self._apply_temperature_scaling(probas)
        predictions = []
        
        for i, proba in enumerate(probas):
            # Vérifier d'abord les règles de mot-clé si une question est fournie
            if questions is not None:
                keyword_category = self._check_keyword_rules(questions[i])
                if keyword_category is not None:
                    predictions.append({
                        'category': keyword_category,
                        'confidence': 1.0,
                        'is_confiant': 1,  # Convertir en int pour JSON
                        'is_near_ambiguous': 0,  # Convertir en int pour JSON
                        'distance': 1.0,
                        'entropy': 0.0,
                        'probabilities': {self.label_encoder.inverse_transform([j])[0]: float(p) for j, p in enumerate(proba)},
                        'top2': {
                            'category': self.label_encoder.inverse_transform([np.argmax(proba)])[0],
                            'confidence': float(np.max(proba))
                        }
                    })
                    continue
            
            # Trouver les indices des deux meilleures prédictions
            top2_idx = np.argsort(proba)[-2:][::-1]
            max_proba = proba[top2_idx[0]]
            second_proba = proba[top2_idx[1]]
            
            # Éviter les égalités exactes
            if abs(max_proba - second_proba) < 1e-6:
                second_proba = max_proba - 1e-6
            
            # Convertir les indices en catégories
            predicted_class = self.label_encoder.inverse_transform([top2_idx[0]])[0]
            second_class = self.label_encoder.inverse_transform([top2_idx[1]])[0]
            
            # Calculer la distance de classification
            distance = max_proba - second_proba
            
            # Calculer l'entropie pour mesurer l'incertitude
            entropy = -np.sum(proba * np.log(proba + 1e-10))
            
            # Vérifier si le cas est presque ambigu
            is_near_ambiguous = int(distance < self.near_ambiguous_threshold)  # Convertir en int
            
            # Utiliser le seuil spécifique à la catégorie ou le seuil par défaut
            category_threshold = self.category_thresholds.get(predicted_class, self.default_threshold)
            if threshold is not None:
                category_threshold = threshold
            
            # Un cas est ambigu si la confiance est faible OU la distance est faible OU l'entropie est élevée
            is_ambiguous = int(
                int(max_proba < category_threshold) or 
                int(distance < self.distance_threshold) or
                int(entropy > 0.5)
            )  # Convertir en int
            
            # Obtenir les catégories alternatives si :
            # 1. Le cas est ambigu OU
            # 2. La deuxième meilleure prédiction est suffisamment confiante
            alternatives = []
            if is_ambiguous or int(second_proba > self.alternative_threshold):  # Convertir en int
                alternatives = self.get_alternative_categories(proba)
            
            # Convertir tous les booléens en entiers dans les alternatives
            for alt in alternatives:
                if 'is_confident' in alt:
                    alt['is_confident'] = int(alt['is_confident'])
            
            predictions.append({
                'category': predicted_class,
                'confidence': float(max_proba),
                'is_confiant': int(not is_ambiguous),  # Convertir en int pour JSON
                'is_near_ambiguous': is_near_ambiguous,  # Déjà converti en int
                'distance': float(distance),
                'entropy': float(entropy),
                'probabilities': {self.label_encoder.inverse_transform([j])[0]: float(p) for j, p in enumerate(proba)},
                'top2': {
                    'category': second_class,
                    'confidence': float(second_proba)
                },
                'alternatives': alternatives
            })
        
        return predictions
    
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> str:
        """Évalue le modèle et retourne un rapport détaillé."""
        y_pred = self.predict(X)
        
        # Matrice de confusion
        cm = confusion_matrix(y, y_pred)
        logger.info("\nMatrice de confusion:")
        logger.info(cm)
        
        # Rapport de classification
        report = classification_report(y, y_pred, zero_division=0)
        logger.info("\nRapport de classification:")
        logger.info(report)
        
        return report
    
    def save(self) -> None:
        """Sauvegarde le modèle entraîné."""
        joblib.dump(self.model, MODELS_DIR / "classifier.joblib")
        joblib.dump(self.label_encoder, MODELS_DIR / "label_encoder.joblib")
        logger.info("Modèles sauvegardés")
    
    @classmethod
    def load(cls) -> 'FAQClassifier':
        """Charge un modèle sauvegardé."""
        classifier = cls()
        classifier.model = joblib.load(MODELS_DIR / "classifier.joblib")
        classifier.label_encoder = joblib.load(MODELS_DIR / "label_encoder.joblib")
        return classifier

    def analyze_errors(self, X: np.ndarray, y: np.ndarray, questions: List[str]) -> Dict[str, Any]:
        """Analyse les erreurs de classification pour comprendre les confusions."""
        predictions = self.predict_with_confidence(X, questions=questions)
        errors = []
        
        for i, (true_label, pred) in enumerate(zip(y, predictions)):
            if true_label != pred['category']:
                errors.append({
                    'question': questions[i],
                    'true_category': self.label_encoder.inverse_transform([true_label])[0],
                    'predicted_category': pred['category'],
                    'confidence': float(pred['confidence']),  # Convertir en float
                    'distance': float(pred['distance']),  # Convertir en float
                    'top2': {
                        'category': pred['top2']['category'],
                        'confidence': float(pred['top2']['confidence'])  # Convertir en float
                    }
                })
        
        # Analyse des erreurs par catégorie
        error_analysis = {
            'total_errors': len(errors),
            'error_rate': float(len(errors) / len(y)),  # Convertir en float
            'confusion_matrix': {},
            'common_errors': []
        }
        
        # Construire la matrice de confusion des erreurs
        for error in errors:
            true_cat = error['true_category']
            pred_cat = error['predicted_category']
            key = f"{true_cat}->{pred_cat}"
            error_analysis['confusion_matrix'][key] = error_analysis['confusion_matrix'].get(key, 0) + 1
        
        # Identifier les erreurs les plus fréquentes
        sorted_errors = sorted(error_analysis['confusion_matrix'].items(), 
                             key=lambda x: x[1], reverse=True)
        error_analysis['common_errors'] = sorted_errors[:5]  # Top 5 des erreurs
        
        # Log des résultats
        logger.info("\nAnalyse des erreurs :")
        logger.info(f"Nombre total d'erreurs : {error_analysis['total_errors']}")
        logger.info(f"Taux d'erreur : {error_analysis['error_rate']:.2%}")
        logger.info("\nMatrice de confusion des erreurs :")
        for (true_cat, pred_cat), count in sorted_errors:
            logger.info(f"{true_cat} -> {pred_cat} : {count} erreurs")
        
        return error_analysis

    def analyze_ambiguity(self, X: np.ndarray, questions: Optional[List[str]] = None) -> Dict[str, float]:
        """Analyse l'ambiguïté globale du modèle."""
        predictions = self.predict_with_confidence(X, questions=questions)
        
        metrics = {
            'mean_distance': float(np.mean([p['distance'] for p in predictions])),
            'mean_entropy': float(np.mean([p['entropy'] for p in predictions])),
            'ambiguous_rate': float(np.mean([1 - p['is_confiant'] for p in predictions])),  # Convertir en int
            'near_ambiguous_rate': float(np.mean([p['is_near_ambiguous'] for p in predictions]))
        }
        
        # Log des métriques
        logger.info("\nAnalyse de l'ambiguïté :")
        logger.info(f"Distance moyenne : {metrics['mean_distance']:.4f}")
        logger.info(f"Entropie moyenne : {metrics['mean_entropy']:.4f}")
        logger.info(f"Taux de cas ambigus : {metrics['ambiguous_rate']:.2%}")
        logger.info(f"Taux de cas presque ambigus : {metrics['near_ambiguous_rate']:.2%}")
        
        return metrics

    def get_alternative_categories(self, proba: np.ndarray, threshold: float = 0.1) -> List[Dict[str, Any]]:
        """Retourne les catégories alternatives dont la probabilité est proche de la meilleure prédiction."""
        best_idx = np.argmax(proba)
        best_proba = proba[best_idx]
        
        alternatives = []
        for idx, p in enumerate(proba):
            if idx != best_idx and int((best_proba - p) < threshold):  # Convertir en int
                alternatives.append({
                    'category': self.label_encoder.inverse_transform([idx])[0],
                    'confidence': float(p)  # Convertir en float pour JSON
                })
        
        return sorted(alternatives, key=lambda x: x['confidence'], reverse=True)
