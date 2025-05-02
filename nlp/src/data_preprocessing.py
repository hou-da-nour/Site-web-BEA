import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import LabelEncoder
import re
import logging
import torch
from src.config import (
    MODEL_NAME, DISTIL_MODEL_NAME, USE_DISTIL, MAX_LENGTH,
    CACHE_SIZE, CACHE_TTL, USE_GPU, NUM_THREADS
)
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
from typing import List, Dict, Any
from functools import lru_cache
import time
from contextlib import nullcontext
from .model_singleton import ModelSingleton

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Nettoie le texte en supprimant la ponctuation et en mettant en minuscules."""
    if not isinstance(text, str):
        logger.warning(f"Texte non valide reçu : {text}")
        return ""
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_question(question: str) -> str:
    """Normalise les variations de formulation des questions."""
    # Supprimer les expressions de demande courantes
    patterns = [
        r'^(quels sont|quelle est|comment|où|que faire|pourriez-vous|je souhaiterais|à propos de)\s+',
        r'^(pouvez-vous|pourriez-vous|auriez-vous|serait-il possible)\s+',
        r'^(je souhaite|je voudrais|j\'aimerais|je désire)\s+',
        r'^(j\'ai besoin|il me faut|je cherche|je recherche)\s+',
        r'^(je ne comprends pas|je ne sais pas|je suis perdu)\s+'
    ]
    
    for pattern in patterns:
        question = re.sub(pattern, '', question.lower())
    
    return clean_text(question)

def augment_text(text: str, num_aug: int = 3) -> List[str]:
    """Génère des variations de la question pour l'augmentation de données."""
    augmented = []
    
    # Augmentation par synonymes
    aug_synonym = naw.SynonymAug(aug_src='wordnet', lang='fra')
    augmented.extend(aug_synonym.augment(text, n=num_aug))
    
    # Augmentation par caractères
    aug_char = nac.KeyboardAug()
    augmented.extend(aug_char.augment(text, n=num_aug))
    
    # Variations de formulation
    variations = [
        f"Comment {text}",
        f"Quelle est la procédure pour {text}",
        f"Je souhaite savoir {text}",
        f"Pouvez-vous m'expliquer {text}",
        f"J'aimerais comprendre {text}",
        f"Pourriez-vous me dire {text}",
        f"Quelle est la méthode pour {text}",
        f"Quels sont les étapes pour {text}"
    ]
    augmented.extend(variations)
    
    return list(set(augmented))  # Supprimer les doublons

class DataPreprocessor:
    def __init__(self, model_name=None):
        """Initialise le prétraitement avec le modèle CamemBERT ou DistilCamemBERT."""
        # Utiliser le singleton pour le modèle
        model_singleton = ModelSingleton()
        self.model, self.tokenizer = model_singleton.get_model()
        self.device = model_singleton.get_device()
        
        # Initialiser le label encoder
        self.label_encoder = LabelEncoder()
        
        # Cache pour les embeddings
        self._embedding_cache = {}
        
        logger.info("DataPreprocessor initialisé avec le modèle singleton")
    
    @lru_cache(maxsize=CACHE_SIZE)
    def preprocess_single_text(self, text: str) -> np.ndarray:
        """
        Prétraite un seul texte pour la prédiction avec mise en cache.
        
        Args:
            text (str): Le texte à prétraiter
        
        Returns:
            np.ndarray: L'embedding du texte
        """
        # Vérifier le cache
        if text in self._embedding_cache:
            return self._embedding_cache[text]
        
        # Nettoyer et normaliser le texte
        cleaned_text = normalize_question(text)
        
        # Tokenizer et embedding avec optimisations
        inputs = self.tokenizer(
            cleaned_text,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )
        
        # Déplacer les inputs sur le bon device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Calculer l'embedding avec optimisations
        with torch.no_grad(), torch.cuda.amp.autocast() if self.device.type == "cuda" else nullcontext():
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]
        
        # Mettre en cache
        self._embedding_cache[text] = embedding
        
        return embedding
    
    def prepare_data(self, df: pd.DataFrame, augment: bool = False) -> tuple:
        """Prépare les données pour l'entraînement."""
        logger.info("Nettoyage des questions...")
        df['question_clean'] = df['question'].apply(normalize_question)
        
        # Supprimer les doublons après nettoyage
        df = df.drop_duplicates(subset=['question_clean'])
        
        if augment:
            logger.info("Augmentation des données...")
            augmented_data = []
            for _, row in df.iterrows():
                variations = augment_text(row['question_clean'])
                for var in variations:
                    augmented_data.append({
                        'question': var,
                        'Réponse': row['Réponse'],
                        'Categorie': row['Categorie']
                    })
            df = pd.concat([df, pd.DataFrame(augmented_data)])
        
        logger.info("Encodage des catégories...")
        if 'Categorie' in df.columns:
            df['category_encoded'] = self.label_encoder.fit_transform(df['Categorie'])
            y = df['category_encoded']
        else:
            y = None
        
        logger.info("Création des embeddings...")
        embeddings = []
        batch_size = 32
        
        for i in range(0, len(df), batch_size):
            batch_texts = df['question_clean'].iloc[i:i+batch_size].tolist()
            inputs = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt"
            )
            
            # Déplacer les inputs sur GPU si disponible
            if USE_GPU and torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
                embeddings.extend(batch_embeddings)
            
            logger.info(f"Traitement des questions {i+1} à {min(i+batch_size, len(df))}")
        
        return np.array(embeddings), y
    
    def clear_cache(self):
        """Vide le cache des embeddings."""
        self._embedding_cache.clear()
        self.preprocess_single_text.cache_clear()
    
    def get_cache_stats(self) -> dict:
        """Retourne les statistiques du cache."""
        return {
            'size': len(self._embedding_cache),
            'max_size': CACHE_SIZE,
            'ttl': CACHE_TTL
        } 