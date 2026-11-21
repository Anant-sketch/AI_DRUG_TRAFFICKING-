import os
import sys
import json
import joblib
import numpy as np
import pandas as pd

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

from dataset.dataset_loader import load_and_prepare_dataset
from preprocessing.preprocess import clean_text

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))

def train_and_evaluate_all():
    print("=" * 70)
    print("   AI CYBER DRUG TRAFFICKING CLASSIFIER BENCHMARK & RE-TRAINING")
    print("=" * 70)
    
    # 1. Load Balanced, Leakage-Free Dataset
    print("\n[Step 1/5] Loading clean, balanced 3-class dataset (Zero duplicate leakage)...")
    df = load_and_prepare_dataset(sample_size_per_class=400)
    
    # 2. Preprocess text using full 8-Stage NLP Pipeline
    print("\n[Step 2/5] Executing 8-Stage NLP Preprocessing Pipeline on all samples...")
    print("  -> Unescaping HTML entities, masking handles/crypto, decoding emojis, normalizing street slang...")
    df['clean_text'] = df['text'].apply(clean_text)
    
    # Filter any empty cleaned samples
    df = df[df['clean_text'].str.strip() != ''].reset_index(drop=True)
    print(f"  -> Total valid preprocessed samples: {len(df)}")
    
    X_raw = df['clean_text']
    y = df['label']
    
    # 3. Vectorization with TF-IDF (Unigram + Bigram)
    print("\n[Step 3/5] Extracting TF-IDF Features (n-gram 1-2, sublinear tf scaling)...")
    vectorizer = TfidfVectorizer(
        max_features=6000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2
    )
    X = vectorizer.fit_transform(X_raw)
    print(f"  -> TF-IDF Vocabulary size: {len(vectorizer.vocabulary_)} features")
    
    # Train-test split (80% train, 20% test) with stratified sampling
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    print(f"  -> Training samples: {X_train.shape[0]} | Unseen Testing samples: {X_test.shape[0]}")
    
    # 4. Define Candidate Classifiers
    # Note: LinearSVC is wrapped in CalibratedClassifierCV to enable predict_proba() for risk engine
    classifiers = {
        'Logistic Regression': LogisticRegression(C=2.5, max_iter=1000, random_state=42),
        'Support Vector Machine (Calibrated)': CalibratedClassifierCV(LinearSVC(C=1.2, random_state=42)),
        'Random Forest': RandomForestClassifier(n_estimators=150, max_depth=30, random_state=42),
        'Naive Bayes': MultinomialNB(alpha=0.2),
        'Neural Network (MLP)': MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=300, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.15, max_depth=4, random_state=42)
    }
    
    metrics_summary = {}
    best_f1 = -1.0
    best_acc = -1.0
    best_model_name = ""
    best_clf = None

    print("\n[Step 4/5] Training & Evaluating 6 ML Classifiers on Unseen Test Data...")
    print("-" * 75)
    print(f"{'Classifier Name':<35} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 75)
    
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        metrics_summary[name] = {
            'accuracy': round(float(acc), 4),
            'precision': round(float(prec), 4),
            'recall': round(float(rec), 4),
            'f1_score': round(float(f1), 4),
            'confusion_matrix': cm
        }
        
        print(f"{name:<35} | {acc:<10.4f} | {prec:<10.4f} | {rec:<10.4f} | {f1:<10.4f}")
        
        # Select best model based on F1-Score and Accuracy
        if f1 > best_f1 or (f1 == best_f1 and acc > best_acc):
            best_f1 = f1
            best_acc = acc
            best_model_name = name
            best_clf = clf

    print("-" * 75)
    print(f"\n🏆 Best Performing Classifier: {best_model_name}")
    print(f"   Accuracy: {best_acc:.4f} ({best_acc*100:.2f}%) | F1-Score: {best_f1:.4f}")
    
    # 5. Save Artifacts for API and Dashboard
    print("\n[Step 5/5] Saving Serialized Artifacts & Performance Metrics...")
    vectorizer_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
    model_path = os.path.join(MODELS_DIR, "best_classifier.joblib")
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(best_clf, model_path)
    
    final_output = {
        'best_model': best_model_name,
        'models': metrics_summary,
        'dataset_split': {
            'train_samples': int(X_train.shape[0]),
            'test_samples': int(X_test.shape[0]),
            'total_samples': int(len(df)),
            'classes': ['General / Benign', 'Legitimate Medical Review', 'Illicit Drug Trafficking']
        }
    }
    
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)
        
    print(f"  -> Saved Vectorizer to: {vectorizer_path}")
    print(f"  -> Saved Best Classifier to: {model_path}")
    print(f"  -> Saved Evaluation Metrics to: {metrics_path}")
    print("\nRe-training and benchmarking completed successfully!")
    return final_output

if __name__ == "__main__":
    train_and_evaluate_all()
