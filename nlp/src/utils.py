import logging
import json
from pathlib import Path
from typing import Dict, Any
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

def setup_logging(level=logging.INFO):
    """Configure le logging pour le projet."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def save_metrics(metrics: Dict[str, Any], filepath: Path):
    """Sauvegarde les métriques d'évaluation au format JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

def calculate_metrics(y_true, y_pred, labels=None):
    """Calcule les métriques détaillées de classification."""
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None
    )
    
    return {
        'precision': precision.tolist(),
        'recall': recall.tolist(),
        'f1': f1.tolist(),
        'support': support.tolist()
    }

class NumpyEncoder(json.JSONEncoder):
    """Encoder personnalisé pour sérialiser les types numpy."""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super().default(obj)
