from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from src.data_preprocessing import DataPreprocessor
from src.model import FAQClassifier
from src.answer_finder import AnswerFinder
import threading
import time
from collections import deque
import statistics
import os
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bool):
            return int(obj)
        return super().default(obj)

app = Flask(__name__)
CORS(app)
app.json_encoder = CustomJSONEncoder

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales pour les modèles
preprocessor = None
classifier = None
answer_finder = None
models_loaded = False
loading_error = None

# Statistiques de performance
performance_stats = {
    'request_times': deque(maxlen=100),  # Garde les 100 derniers temps
    'cache_hits': 0,
    'total_requests': 0,
    'start_time': None
}

def load_models():
    """Charge les modèles en arrière-plan."""
    global preprocessor, classifier, answer_finder, models_loaded, loading_error
    try:
        logger.info("Début du chargement des modèles...")
        start_time = time.time()
        
        # Charger les modèles
        preprocessor = DataPreprocessor()
        classifier = FAQClassifier.load()
        answer_finder = AnswerFinder()
        
        # Vérifier que tout est chargé
        if preprocessor and classifier and answer_finder:
            models_loaded = True
            load_time = time.time() - start_time
            logger.info(f"Modèles chargés avec succès en {load_time:.2f} secondes")
            performance_stats['start_time'] = time.time()
        else:
            loading_error = "Erreur lors du chargement des modèles"
            logger.error(loading_error)
    except Exception as e:
        loading_error = str(e)
        logger.error(f"Erreur lors du chargement des modèles: {e}")

# Ne charger les modèles que dans le processus principal
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logger.info("Chargement des modèles dans le processus principal...")
    load_models()
else:
    logger.info("Processus de rechargement Flask détecté, pas de chargement des modèles")

@app.route('/predict-category', methods=['POST'])
def predict_category():
    """Endpoint pour prédire la catégorie d'une question."""
    if not models_loaded:
        if loading_error:
            return jsonify({
                "success": False,
                "error": f"Erreur de chargement des modèles: {loading_error}"
            }), 500
        return jsonify({
            "success": False,
            "error": "Les modèles sont en cours de chargement. Veuillez réessayer dans quelques secondes."
        }), 503
    
    try:
        start_time = time.time()
        performance_stats['total_requests'] += 1
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "Question manquante dans la requête"
            }), 400
 
        question = data['question']

        # Prétraiter la question
        embedding = preprocessor.preprocess_single_text(question)
        # Reshape l'embedding en 2D (1, n_features)
        embedding = embedding.reshape(1, -1)
        
        # Prédire la catégorie
        prediction = classifier.predict_with_confidence(embedding, questions=[question])
        
        # Trouver la meilleure réponse
        answer = answer_finder.find_best_answer(
            question,
            prediction[0]['category'],
            min_similarity=0.7
        )
        
        # Mettre à jour les statistiques
        request_time = time.time() - start_time
        performance_stats['request_times'].append(request_time)
        
        # Vérifier si le cache a été utilisé
        cache_stats = preprocessor.get_cache_stats()
        if cache_stats['size'] > 0:
            performance_stats['cache_hits'] += 1

        return jsonify({
            "success": True,
            "category": prediction[0]['category'],
            "probabilities": prediction[0]['probabilities'],
            "confidence": prediction[0]['confidence'],
            "answer": answer['answer'],
            "similarity": answer['similarity'],
            "best_question": answer['best_question'],
            "answer_is_confident": answer['is_confident'],
            "answer_alternatives": answer['alternatives'],
            "performance": {
                "request_time": request_time,
                "cache_hit": cache_stats['size'] > 0
            }
        })
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Erreur lors de la prédiction: {str(e)}"
        }), 500

@app.route('/performance', methods=['GET'])
def get_performance():
    """Endpoint pour obtenir les statistiques de performance."""
    if not models_loaded:
        return jsonify({
            "success": False,
            "error": "Les modèles ne sont pas encore chargés"
        }), 503
    
    times = list(performance_stats['request_times'])
    if not times:
        return jsonify({
            "success": True,
            "message": "Pas encore de requêtes traitées"
        })
    
    return jsonify({
        "success": True,
        "stats": {
            "total_requests": performance_stats['total_requests'],
            "cache_hits": performance_stats['cache_hits'],
            "cache_hit_rate": performance_stats['cache_hits'] / performance_stats['total_requests'] if performance_stats['total_requests'] > 0 else 0,
            "average_time": statistics.mean(times),
            "min_time": min(times),
            "max_time": max(times),
            "median_time": statistics.median(times),
            "uptime": time.time() - performance_stats['start_time'] if performance_stats['start_time'] else 0
        }
    })

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    """Endpoint pour vider le cache."""
    if not models_loaded:
        return jsonify({
            "success": False,
            "error": "Les modèles ne sont pas encore chargés"
        }), 503
    
    try:
        preprocessor.clear_cache()
        answer_finder.clear_cache()
        return jsonify({
            "success": True,
            "message": "Cache vidé avec succès"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erreur lors du vidage du cache: {str(e)}"
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Endpoint pour vérifier l'état des modèles."""
    return jsonify({
        "success": True,
        "models_loaded": models_loaded,
        "loading_error": loading_error
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)