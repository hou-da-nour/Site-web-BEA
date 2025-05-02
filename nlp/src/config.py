import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models" / "saved_models"
EMBEDDINGS_DIR = MODELS_DIR / "embeddings"
COMPARISON_RESULTS_DIR = MODELS_DIR / "comparison_results"
FAISS_INDICES_DIR = MODELS_DIR / "faiss_indices"

# Paramètres du modèle
MODEL_NAME = "camembert-base"  # Modèle de base
DISTIL_MODEL_NAME = "camembert-base"  # Utiliser le même modèle pour la comparaison
USE_DISTIL = False  # Désactiver Distil pour l'instant
MAX_LENGTH = 128
RANDOM_STATE = 42
TEST_SIZE = 0.2
BATCH_SIZE = 64  # Augmenté pour de meilleures performances

# Paramètres d'augmentation de données
AUGMENTATION_ENABLED = True
NUM_AUGMENTATIONS = 3
AUGMENTATION_METHODS = ['synonym', 'keyboard', 'formulation']

# Paramètres de prétraitement
CLEAN_TEXT = True
REMOVE_DUPLICATES = True
NORMALIZE_QUESTIONS = True

# Paramètres du classifieur
HIDDEN_LAYERS = (200, 100, 50)
LEARNING_RATE = 'adaptive'
MAX_ITER = 5000
EARLY_STOPPING = True
VALIDATION_FRACTION = 0.2
N_ITER_NO_CHANGE = 50

# Seuils de confiance
DEFAULT_THRESHOLD = 0.80
DISTANCE_THRESHOLD = 0.15
NEAR_AMBIGUOUS_THRESHOLD = 0.05

# Paramètres de cache
CACHE_SIZE = 1000  # Nombre d'embeddings en cache
CACHE_TTL = 3600  # Durée de vie du cache en secondes

# Paramètres de performance
USE_GPU = True  # Utiliser GPU si disponible
NUM_THREADS = 4  # Nombre de threads pour le traitement

# Création des répertoires nécessaires
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
os.makedirs(COMPARISON_RESULTS_DIR, exist_ok=True)
os.makedirs(FAISS_INDICES_DIR, exist_ok=True)
