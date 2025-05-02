# Project Overview: FAQ NLP & ML CAT Automation

## **1. Project Structure**

```
api/
  app.py              # Main Flask API
src/
  model.py            # FAQClassifier (ML model for category prediction)
  data_preprocessing.py # DataPreprocessor (text cleaning, embedding with CamemBERT)
  answer_finder.py    # AnswerFinder (finds best FAQ answer using embeddings)
  config.py           # Configuration (paths, model params)
  utils.py            # Utility functions
data/
  faqs_clean.csv      # Main FAQ dataset (questions, answers, categories)
models/
  saved_models/
    classifier.joblib     # Trained classifier
    label_encoder.joblib  # Label encoder for categories
    embeddings.npy        # Precomputed FAQ question embeddings
requirements.txt      # Python dependencies
README.md             # Project documentation
```

## **2. Main Technologies Used**

- **Flask**: REST API framework
- **transformers**: For CamemBERT embeddings
- **torch**: For deep learning and embeddings
- **scikit-learn**: For ML models and pipelines
- **pandas, numpy**: Data manipulation and storage
- **joblib**: Model serialization
- **flask-cors**: CORS support for API
- **imbalanced-learn**: SMOTE for class balancing
- **pytest**: For testing
- **faiss**: For fast similarity search
- **lru_cache**: For performance optimization

## **3. Data Flow & Components**

### **A. Data Preparation**
- `data/faqs_clean.csv` contains FAQ questions, answers, and categories.
- `src/data_preprocessing.py`:
  - Cleans and normalizes questions.
  - Uses CamemBERT to generate embeddings for each question.
  - Can augment data for training.
  - Implements caching for embeddings using `@lru_cache`.

### **B. Model Training**
- `src/model.py`:
  - Defines `FAQClassifier` (MLPClassifier + SMOTE in a pipeline).
  - Trains on question embeddings to predict categories.
  - Saves model and label encoder with joblib.

### **C. Embedding Storage**
- Embeddings for all FAQ questions are precomputed and saved as `models/saved_models/embeddings.npy`.
- The order matches the questions in `data/faqs_clean.csv`.

### **D. API**

- `api/app.py` :
    - Charge le classifieur, l'encodeur et les embeddings au démarrage.
    - Point de terminaison `/predict-category` :
        - Reçoit une question utilisateur.
        - Prétraite et convertit la question en embedding.
        - Prédit la catégorie.
        - Recherche la réponse la plus similaire via les embeddings.
        - Retourne :
            - `success`: booléen indiquant le succès de la requête
            - `category`: catégorie prédite
            - `probabilities`: dictionnaire des probabilités par catégorie
            - `confidence`: score de confiance de la prédiction
            - `answer`: réponse trouvée
            - `similarity`: score de similarité avec la question FAQ
            - `best_question`: question FAQ la plus similaire
            - `answer_is_confident`: booléen indiquant si la réponse est fiable
            - `answer_alternatives`: liste des réponses alternatives
            - `performance`: métriques de performance (cache_hit, request_time)

### **E. Answer Finding**
- `src/answer_finder.py`:
  - Loads all FAQ questions, answers, and their embeddings.
  - For a new question, computes its embedding and finds the most similar FAQ using cosine similarity.
  - Returns the best answer and top alternatives.
  - Implements two-level caching:
    1. Embedding cache in `DataPreprocessor`
    2. Similarity cache in `AnswerFinder`

### **E. Gestion des Erreurs**

- **400 Bad Request** : Requête mal formée
  ```json
  {
    "success": false,
    "error": "Le champ 'question' est requis"
  }
  ```

- **404 Not Found** : Question non trouvée
  ```json
  {
    "success": false,
    "error": "Aucune réponse trouvée pour cette question"
  }
  ```

- **500 Internal Server Error** : Erreur serveur
  ```json
  {
    "success": false,
    "error": "Erreur lors de la prédiction: [message d'erreur]"
  }
  ```

## **4. Performance Optimizations**

### **A. Caching System**
1. **Embedding Cache**:
   - Implemented in `DataPreprocessor` using `@lru_cache`
   - Caches question embeddings to avoid recomputing
   - Configurable cache size in `config.py`

2. **Similarity Cache**:
   - Implemented in `AnswerFinder`
   - Caches similarity results for frequently asked questions
   - Uses hash-based keys for efficient lookup

3. **Performance Metrics**:
   - Average speedup with cache: ~50,000x
   - Best case speedup: ~800,000x
   - Cache hit rate: >99%

### **B. FAISS Integration**
- Uses FAISS for fast similarity search
- Optimized for large-scale vector operations
- Supports GPU acceleration if available

## **5. How Everything Works Together**

1. **User sends a question to the API.**
2. **API preprocesses and embeds the question using CamemBERT.**
3. **Classifier predicts the most likely category.**
4. **AnswerFinder finds the most similar FAQ in that category using precomputed embeddings.**
5. **API returns:**
   - Predicted category
   - Confidence scores
   - Best answer and similar alternatives

## **6. How to Run**

### **A. Install dependencies**
```sh
pip install -r requirements.txt
```

### **B. Start the API**
```sh
cd api
python app.py
```
- The API will be available at `http://localhost:5000/`

### **C. Example API Request**
```json
POST /predict-category
{
  "question": "Comment puis-je recharger ma carte prépayée ?"
}
```

### **D. Exemple de Réponse API**

```json
{
  "success": true,
  "category": "Prépayée",
  "probabilities": {
    "Autre": 0.12046781927347183,
    "Compte": 0.12046781927347183,
    "Générale": 0.12046800553798676,
    "Prépayée": 0.2771926522254944,
    "Salutation": 0.12046781927347183,
    "Sécurité": 0.120467908680439,
    "Transaction": 0.12046794593334198
  },
  "confidence": 1.0,
  "answer": "L'option « RECHARGE ».",
  "similarity": 0.3198425769805908,
  "best_question": "quelle fonctionnalité permet de recharger une carte prépayée",
  "answer_is_confident": 0,
  "answer_alternatives": [],
  "performance": {
    "cache_hit": true,
    "request_time": 0.2903304100036621
  }
}
```

## **7. Configuration**

- All paths and model parameters are set in `src/config.py`.
- FAQ data is in `data/faqs_clean.csv`.
- Precomputed embeddings are in `models/saved_models/embeddings.npy`.
- Cache settings:
  - `CACHE_SIZE`: Number of embeddings to cache
  - `CACHE_TTL`: Cache time-to-live in seconds

## **8. Training & Updating**

- To retrain or update the model, use scripts in `src/` (e.g., `train.py`).
- After retraining, update the model and embeddings in `models/saved_models/`.

## **9. Testing**

- Tests are in the `tests/` directory and can be run with:
```sh
pytest
```

## **10. Dependencies**

See `requirements.txt` for all required Python packages.

## **11. Authors & License**

- Add your name and license as needed.
