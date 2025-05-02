import numpy as np
import pandas as pd
from pathlib import Path
import logging
import faiss
import os
from .data_preprocessing import DataPreprocessor
from .config import DATA_DIR, MODELS_DIR
from .model_singleton import ModelSingleton

logger = logging.getLogger(__name__)

class AnswerFinder:
    def __init__(self, faq_data_path=None):
        """
        Initialise le chercheur de réponses avec FAISS pour une recherche rapide.
        
        Args:
            faq_data_path (str, optional): Chemin vers le fichier CSV des FAQ
        """
        # Utiliser le singleton pour le modèle
        model_singleton = ModelSingleton()
        self.preprocessor = DataPreprocessor()
        self.question_embeddings = {}
        self.faiss_indices = {}
        self.similarity_cache = {}  # Cache pour les similarités
        
        try:
            # Charger les données FAQ
            if faq_data_path:
                self.faq_data = pd.read_csv(faq_data_path)
            else:
                self.faq_data = pd.read_csv(DATA_DIR / "faqs_clean.csv")
            
            # Vérifier si les indices FAISS existent déjà
            if self._check_faiss_indices():
                self._load_faiss_indices()
            else:
                self._prepare_embeddings()
                self._save_faiss_indices()
            
            logger.info(f"Base de connaissances chargée avec {len(self.faq_data)} questions/réponses")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {str(e)}")
            raise
    
    def _check_faiss_indices(self) -> bool:
        """Vérifie si les indices FAISS existent déjà."""
        index_dir = MODELS_DIR / "faiss_indices"
        if not index_dir.exists():
            return False
        
        # Vérifier que tous les indices nécessaires existent
        for category in self.faq_data['Categorie'].unique():
            index_path = index_dir / f"{category}.index"
            if not index_path.exists():
                return False
        
        return True
    
    def _load_faiss_indices(self):
        """Charge les indices FAISS pré-calculés."""
        index_dir = MODELS_DIR / "faiss_indices"
        logger.info("Chargement des indices FAISS pré-calculés...")
        
        for category in self.faq_data['Categorie'].unique():
            try:
                # Charger l'index
                index_path = index_dir / f"{category}.index"
                index = faiss.read_index(str(index_path))
                
                # Charger les données associées
                data_path = index_dir / f"{category}_data.npz"
                data = np.load(data_path, allow_pickle=True)
                
                self.question_embeddings[category] = {
                    'questions': data['questions'].tolist(),
                    'answers': data['answers'].tolist(),
                    'embeddings': data['embeddings']
                }
                self.faiss_indices[category] = index
                
                logger.debug(f"Index FAISS chargé pour la catégorie {category}")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de l'index pour {category}: {str(e)}")
                raise
    
    def _save_faiss_indices(self):
        """Sauvegarde les indices FAISS et les données associées."""
        index_dir = MODELS_DIR / "faiss_indices"
        index_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Sauvegarde des indices FAISS...")
        
        for category in self.faq_data['Categorie'].unique():
            try:
                # Sauvegarder l'index
                index_path = index_dir / f"{category}.index"
                faiss.write_index(self.faiss_indices[category], str(index_path))
                
                # Sauvegarder les données associées
                data_path = index_dir / f"{category}_data.npz"
                np.savez(
                    data_path,
                    questions=self.question_embeddings[category]['questions'],
                    answers=self.question_embeddings[category]['answers'],
                    embeddings=self.question_embeddings[category]['embeddings']
                )
                
                logger.debug(f"Index FAISS sauvegardé pour la catégorie {category}")
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde de l'index pour {category}: {str(e)}")
                raise
    
    def _prepare_embeddings(self):
        """Prépare les embeddings et les indices FAISS pour toutes les questions par catégorie."""
        for category in self.faq_data['Categorie'].unique():
            try:
                category_data = self.faq_data[self.faq_data['Categorie'] == category]
                
                # Préparer les embeddings
                embeddings = []
                for question in category_data['question']:
                    embedding = self.preprocessor.preprocess_single_text(question)
                    embeddings.append(embedding)
                
                embeddings = np.array(embeddings).astype('float32')
                
                # Créer l'index FAISS
                index = faiss.IndexFlatL2(embeddings.shape[1])
                index.add(embeddings)
                
                # Stocker les données par catégorie
                self.question_embeddings[category] = {
                    'questions': category_data['question'].tolist(),
                    'answers': category_data['Réponse'].tolist(),
                    'embeddings': embeddings
                }
                self.faiss_indices[category] = index
                
                logger.debug(f"Préparé {len(embeddings)} embeddings pour la catégorie {category}")
            except Exception as e:
                logger.error(f"Erreur lors de la préparation des embeddings pour {category}: {str(e)}")
                raise
    
    def _compute_similarities(self, question_embedding: np.ndarray, category: str, k: int = 3) -> tuple:
        """
        Calcule les similarités entre une question et les FAQs d'une catégorie.
        
        Args:
            question_embedding: L'embedding de la question
            category: La catégorie à chercher
            k: Nombre de résultats à retourner
        
        Returns:
            tuple: (distances, indices, similarities)
        """
        try:
            # Vérifier le cache
            cache_key = f"{category}_{hash(question_embedding.tobytes())}"
            if cache_key in self.similarity_cache:
                return self.similarity_cache[cache_key]
            
            index = self.faiss_indices[category]
            distances, indices = index.search(question_embedding, k)
            
            # Convertir les distances en similarités (1 - distance normalisée)
            max_distance = np.max(distances)
            similarities = 1 - (distances / (max_distance + 1e-8))  # Éviter division par zéro
            
            # Mettre en cache
            result = (distances, indices, similarities)
            self.similarity_cache[cache_key] = result
            
            return result
        except Exception as e:
            logger.error(f"Erreur lors du calcul des similarités: {str(e)}")
            raise
    
    def find_best_answer(self, question: str, predicted_category: str, min_similarity: float = 0.7) -> dict:
        """
        Trouve la meilleure réponse pour une question dans une catégorie en utilisant FAISS.
        
        Args:
            question (str): La question à répondre
            predicted_category (str): La catégorie prédite
            min_similarity (float): Seuil minimum de similarité (0-1)
        
        Returns:
            dict: {
                'answer': str,  # La réponse trouvée
                'similarity': float,  # Score de similarité (0-1)
                'best_question': str,  # Question la plus similaire
                'is_confident': int,  # Si la similarité est suffisante (0 ou 1)
                'alternatives': list  # Autres réponses similaires
            }
        """
        if predicted_category not in self.question_embeddings:
            return {
                'answer': "Désolé, je n'ai pas de réponse dans cette catégorie.",
                'similarity': 0.0,
                'best_question': "",
                'is_confident': 0,  # Convertir en int
                'alternatives': []
            }
        
        try:
            # Préparer l'embedding de la question
            question_embedding = self.preprocessor.preprocess_single_text(question)
            question_embedding = question_embedding.reshape(1, -1).astype('float32')
            
            # Calculer les similarités
            distances, indices, similarities = self._compute_similarities(question_embedding, predicted_category)
            
            # Trouver la meilleure correspondance
            best_idx = indices[0][0]
            best_similarity = float(similarities[0][0])  # Convertir en float
            
            # Vérifier si la similarité est suffisante
            is_confident = int(best_similarity >= min_similarity)  # Convertir en int
            
            # Préparer les alternatives
            alternatives = []
            for i in range(1, len(indices[0])):
                if similarities[0][i] >= min_similarity:
                    alternatives.append({
                        'question': self.question_embeddings[predicted_category]['questions'][indices[0][i]],
                        'answer': self.question_embeddings[predicted_category]['answers'][indices[0][i]],
                        'similarity': float(similarities[0][i])  # Convertir en float
                    })
            
            return {
                'answer': self.question_embeddings[predicted_category]['answers'][best_idx],
                'similarity': best_similarity,
                'best_question': self.question_embeddings[predicted_category]['questions'][best_idx],
                'is_confident': is_confident,  # Déjà converti en int
                'alternatives': alternatives
            }
        except Exception as e:
            logger.error(f"Erreur lors de la recherche de réponse: {str(e)}")
            return {
                'answer': "Désolé, une erreur s'est produite lors de la recherche de réponse.",
                'similarity': 0.0,
                'best_question': "",
                'is_confident': 0,  # Convertir en int
                'alternatives': []
            }
    
    def find_answers_in_category(self, question: str, category: str, min_similarity: float = 0.7) -> list:
        """
        Trouve toutes les réponses similaires dans une catégorie en utilisant FAISS.
        
        Args:
            question (str): La question à répondre
            category (str): La catégorie à chercher
            min_similarity (float): Seuil minimum de similarité
        
        Returns:
            list: Liste des réponses avec leurs similarités
        """
        if category not in self.question_embeddings:
            return []
        
        try:
            # Prétraiter la question
            question_embedding = self.preprocessor.preprocess_single_text(question)
            question_embedding = question_embedding.reshape(1, -1).astype('float32')
            
            # Calculer les similarités
            _, indices, similarities = self._compute_similarities(
                question_embedding, 
                category, 
                k=len(self.question_embeddings[category]['questions'])
            )
            
            # Trouver toutes les réponses au-dessus du seuil
            answers = []
            for i in range(len(indices[0])):
                if similarities[0][i] >= min_similarity:
                    answers.append({
                        'question': self.question_embeddings[category]['questions'][indices[0][i]],
                        'answer': self.question_embeddings[category]['answers'][indices[0][i]],
                        'similarity': similarities[0][i]
                    })
            
            return answers
        except Exception as e:
            logger.error(f"Erreur lors de la recherche dans la catégorie {category}: {str(e)}")
            return []

    def find_top3_answers(self, question: str, category: str) -> list:
        """
        Trouve les 3 meilleures réponses similaires pour une question dans une catégorie en utilisant FAISS.
        
        Args:
            question (str): La question à répondre
            category (str): La catégorie à chercher
        
        Returns:
            list: Liste des 3 meilleures réponses avec leurs similarités
        """
        if category not in self.question_embeddings:
            return []
        
        try:
            # Prétraiter la question
            question_embedding = self.preprocessor.preprocess_single_text(question)
            question_embedding = question_embedding.reshape(1, -1).astype('float32')
            
            # Calculer les similarités
            _, indices, similarities = self._compute_similarities(question_embedding, category, k=3)
            
            # Créer la liste des résultats
            results = []
            for i in range(len(indices[0])):
                results.append({
                    'question': self.question_embeddings[category]['questions'][indices[0][i]],
                    'answer': self.question_embeddings[category]['answers'][indices[0][i]],
                    'similarity': similarities[0][i]
                })
            
            return results
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des top 3 réponses: {str(e)}")
            return []

    def clear_cache(self):
        """Vide le cache des similarités."""
        self.similarity_cache.clear()
        self.preprocessor.clear_cache() 