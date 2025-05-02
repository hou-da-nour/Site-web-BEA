import torch
from transformers import AutoTokenizer, AutoModel
import logging
import time
from .config import MODEL_NAME, DISTIL_MODEL_NAME, USE_DISTIL, USE_GPU, NUM_THREADS

logger = logging.getLogger(__name__)

class ModelSingleton:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelSingleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._load_model()
    
    def _load_model(self):
        """Charge le modèle CamemBERT une seule fois."""
        model_name = DISTIL_MODEL_NAME if USE_DISTIL else MODEL_NAME
        logger.info(f"Chargement du modèle {model_name}...")
        start_time = time.time()
        
        try:
            # Optimisations pour le chargement
            self.device = torch.device("cuda" if USE_GPU and torch.cuda.is_available() else "cpu")
            
            # Charger le tokenizer et le modèle en mode évaluation avec optimisations
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                local_files_only=False,
                trust_remote_code=True,
                use_fast=True  # Utiliser le tokenizer rapide
            )
            
            # Charger le modèle avec optimisations
            self.model = AutoModel.from_pretrained(
                model_name,
                local_files_only=False,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
                device_map="auto" if self.device.type == "cuda" else None
            )
            
            # Optimisations supplémentaires
            self.model.eval()
            if self.device.type == "cuda":
                self.model = self.model.cuda()
                torch.backends.cudnn.benchmark = True
                logger.info("Modèle déplacé sur GPU avec optimisations")
            
            # Configurer le nombre de threads
            torch.set_num_threads(NUM_THREADS)
            
            logger.info(f"Modèle chargé en {time.time() - start_time:.2f} secondes")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle {model_name}: {str(e)}")
            raise RuntimeError(f"Impossible de charger le modèle {model_name}. Erreur: {str(e)}")
    
    def get_model(self):
        """Retourne le modèle et le tokenizer."""
        return self.model, self.tokenizer
    
    def get_device(self):
        """Retourne le device utilisé."""
        return self.device 