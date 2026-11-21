import os
import sys
import joblib
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from preprocessing.preprocess import clean_text, get_preprocessing_stages_breakdown
from extractors.entity_extractor import extract_entities, SUSPICIOUS_KEYWORD_LIST, DRUG_EMOJIS

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))

# Global lazy-loaded artifacts
VECTORIZER = None
MODEL = None

def get_model_and_vectorizer():
    global VECTORIZER, MODEL
    if VECTORIZER is None or MODEL is None:
        vec_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
        model_path = os.path.join(MODELS_DIR, "best_classifier.joblib")
        
        if os.path.exists(vec_path) and os.path.exists(model_path):
            VECTORIZER = joblib.load(vec_path)
            MODEL = joblib.load(model_path)
        else:
            # Fallback: train on the fly if model files do not exist yet
            from models.train_models import train_and_evaluate_all
            train_and_evaluate_all()
            VECTORIZER = joblib.load(vec_path)
            MODEL = joblib.load(model_path)
            
    return VECTORIZER, MODEL

def analyze_threat(text: str) -> Dict[str, Any]:
    """
    Performs comprehensive threat intelligence analysis on input text:
    - ML Classification (Illicit vs Medical vs General)
    - Entity Extraction (Telegram, Crypto, Emojis)
    - Risk Scoring Engine (0 - 100%)
    - Explainable AI (Keyword Highlighting)
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'status': 'error',
            'message': 'Empty or invalid text provided.'
        }

    vec, clf = get_model_and_vectorizer()
    
    # 1. Preprocess & Vectorize
    cleaned = clean_text(text)
    stages = get_preprocessing_stages_breakdown(text)
    features = vec.transform([cleaned])
    
    # 2. Get Model Probabilities
    probs = clf.predict_proba(features)[0]
    classes = ['General / Benign', 'Legitimate Medical Review', 'Illicit Drug Trafficking']
    
    prob_dict = {
        classes[i]: round(float(probs[i]), 4) for i in range(len(classes))
    }
    
    predicted_class_idx = int(clf.predict(features)[0])
    predicted_category = classes[predicted_class_idx]
    
    # 3. Extract Entities
    entities = extract_entities(text)
    
    # 4. Compute Threat Score & Risk Level
    illicit_ml_prob = prob_dict['Illicit Drug Trafficking']
    entity_count = entities['entity_count']
    keyword_count = len(entities['suspicious_keywords'])
    
    # Entity bonus factor (up to 40% boost for explicit handles/wallets/emojis)
    entity_factor = min(0.40, (entity_count * 0.15 + keyword_count * 0.05))
    
    # Combined score
    raw_threat_score = (illicit_ml_prob * 0.70) + (entity_factor * 0.30)
    
    # Override: If explicit drug emojis AND (Telegram/Crypto handle) are present, enforce critical risk
    if len(entities['detected_emojis']) > 0 and (len(entities['telegram_handles']) > 0 or len(entities['bitcoin_addresses']) > 0):
        raw_threat_score = max(raw_threat_score, 0.88)
        
    threat_score_pct = round(min(100.0, raw_threat_score * 100.0), 1)
    
    if threat_score_pct >= 80.0:
        risk_level = 'CRITICAL'
        risk_color = '#ef4444' # Vibrant red
    elif threat_score_pct >= 60.0:
        risk_level = 'HIGH'
        risk_color = '#f97316' # Bright orange
    elif threat_score_pct >= 35.0:
        risk_level = 'MEDIUM'
        risk_color = '#eab308' # Amber yellow
    else:
        risk_level = 'LOW'
        risk_color = '#22c55e' # Soft emerald green

    # 5. Generate Explainable AI (XAI) Token Badges
    tokens = text.split()
    highlighted_tokens = []
    
    for token in tokens:
        clean_token = token.lower().strip(",.!?\"'()")
        is_emoji = any(e in token for e in DRUG_EMOJIS)
        is_handle = token.startswith('@') or 't.me/' in clean_token or 'wickr' in clean_token
        is_crypto = any(crypto in token for crypto in (entities['bitcoin_addresses'] + entities['ethereum_addresses'] + entities['monero_addresses']))
        is_suspicious_kw = clean_token in SUSPICIOUS_KEYWORD_LIST
        
        if is_emoji or is_handle or is_crypto or is_suspicious_kw:
            tag = 'danger'
        else:
            tag = 'normal'
            
        highlighted_tokens.append({'token': token, 'tag': tag})

    return {
        'status': 'success',
        'raw_text': text,
        'cleaned_text': cleaned,
        'preprocessing_stages': stages,
        'predicted_category': predicted_category,
        'probabilities': prob_dict,
        'threat_score': threat_score_pct,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'entities': entities,
        'xai_highlights': highlighted_tokens
    }

if __name__ == "__main__":
    sample = "Fresh stock ❄️ and 💊! DM plug @coke_king_99 or Wickr: darkplug. Pay BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    result = analyze_threat(sample)
    import json
    print(json.dumps(result, indent=2))
