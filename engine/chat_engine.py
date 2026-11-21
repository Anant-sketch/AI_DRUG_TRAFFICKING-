"""
Project AI Knowledge & Conversational Assistant Engine for
AI-Powered Cyber Drug Trafficking Detection & Threat Intelligence Platform
"""

import re
from typing import Dict, Any, List, Optional
from engine.risk_engine import analyze_threat

# ==============================================================================
# COMPREHENSIVE PROJECT KNOWLEDGE BASE (TECHNICAL, ARCHITECTURAL & VIVA-READY)
# ==============================================================================

KNOWLEDGE_BASE = {
    "project_overview": {
        "title": "Project Overview & Problem Statement",
        "keywords": ["overview", "about", "project", "what is this", "introduction", "problem statement", "objective", "goal"],
        "answer": """**CyberNarc: AI Cyber Illicit Trafficking Detection & Intelligence Platform**

* **Domain Background**: Illicit drug traffickers have transitioned from physical streets to encrypted digital channels (**Telegram, Wickr, Session**) and darknet TOR markets.
* **Evasion Tactics**: Traffickers bypass automated keyword filters using **drug emoji ciphers** (❄️ for cocaine, 💊 for pills, 🌿 for cannabis), **street slang** (*loud pack*, *uncut fish scale*), and **cryptocurrency wallets** (Bitcoin, Monero).
* **Core Solution**: An end-to-end multi-modular threat intelligence platform that:
  1. Executes an **8-Stage NLP Preprocessing Pipeline** to decode emojis, expand slang, and mask cyber entities.
  2. Performs **3-Class Machine Learning Classification** (Benign vs Medical vs Illicit Drug Trade).
  3. Extracts **Covert Law Enforcement Artifacts** (Telegram handles, Wickr IDs, Session IDs, BTC/XMR wallets).
  4. Computes a **Hybrid Risk Severity Score (0–100%)** with Explainable AI (XAI) token attribution.
  5. Generates formal **Law Enforcement Evidence Case Reports** for legal prosecution."""
    },

    "preprocessing": {
        "title": "8-Stage NLP Preprocessing Pipeline",
        "keywords": ["preprocessing", "preprocess", "pipeline", "8-stage", "clean_text", "nlp pipeline", "clean text", "stages"],
        "answer": """**The 8-Stage NLP Preprocessing Pipeline (`preprocessing/preprocess.py`)**

1. **Stage 1: HTML Entity Unescaping & Web Noise Stripping**: Decodes web-escaped characters (e.g., `&#039;` &rarr; `'`, `&amp;` &rarr; `&`) and removes HTML tags (`<p>`, `<span>`).
2. **Stage 2: Covert Cyber Entity Canonical Masking**: Replaces Telegram handles, Wickr IDs, Session IDs, `.onion` darknet domains, and crypto addresses (BTC, ETH, XMR) with canonical tokens like `token_telegram_contact`, `token_crypto_btc`, etc.
3. **Stage 3: Illicit Drug Emoji Cipher Decoding**: Translates street emoji ciphers into semantic tokens (e.g., ❄️ &rarr; `drug_cocaine`, 💊 &rarr; `drug_prescription_pills`, 🌿 &rarr; `drug_cannabis_weed`, 💉 &rarr; `drug_heroin_needle`).
4. **Stage 4: English Contraction Expansion**: Expands contractions (e.g., *don't* &rarr; *do not*, *can't* &rarr; *cannot*) to preserve syntactic negation cues.
5. **Stage 5: Street Slang & Darknet Jargon Normalization**: Replaces multi-word phrases (*loud pack* &rarr; `potent_cannabis`, *stealth shipping* &rarr; `covert_delivery`) and single-word jargon (*plug* &rarr; `dealer_supplier`, *uncut* &rarr; `pure_quality`).
6. **Stage 6: Token-Safe Punctuation Cleaning**: Strips special punctuation while strictly preserving intra-token underscores (`_`) ensuring canonical tags remain intact.
7. **Stage 7: Stopword Filtering (Retaining Negations)**: Removes English stopwords while strictly retaining critical negation words (`no`, `not`, `nor`, `none`, `neither`, `never`, `without`).
8. **Stage 8: Morphological Lemmatization**: WordNet and rule-based morphological normalization reducing inflected tokens to canonical base lemmas."""
    },

    "machine_learning": {
        "title": "Machine Learning Models & Evaluation Benchmarks",
        "keywords": ["model", "models", "accuracy", "f1", "machine learning", "classifier", "best model", "logistic regression", "random forest", "naive bayes", "gradient boosting", "svm", "support vector machine"],
        "answer": """**Machine Learning Classifiers & Benchmark Results (`models/train_models.py`)**

We evaluated 6 diverse algorithms on 6,000-dimensional TF-IDF unigram + bigram feature matrices on unseen test data ($N = 240$):

| Model Architecture | Test Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Support Vector Machine (Calibrated)** | **98.33%** | **0.9841** | **0.9833** | **0.9833** | 🏆 **Production Model** |
| **Random Forest Classifier** | **97.92%** | **0.9797** | **0.9792** | **0.9793** | Validated Ensemble |
| **Logistic Regression (L2)** | **97.92%** | **0.9804** | **0.9792** | **0.9791** | Linear Baseline |
| **Neural Network (MLP: 128x64)** | **97.92%** | **0.9804** | **0.9792** | **0.9791** | Deep Learning Benchmark |
| **Multinomial Naive Bayes** | **97.50%** | **0.9763** | **0.9750** | **0.9748** | Fast Baseline |
| **Gradient Boosting** | **97.08%** | **0.9713** | **0.9708** | **0.9708** | Boosted Trees |

* **Why Support Vector Machine (Calibrated) as Production Model?**
  1. Highest overall F1-score (**98.33%**) on unseen test data with optimal maximum-margin separation in high-dimensional TF-IDF space.
  2. **100% recall on illicit narcotics** with zero false negatives (detected all 80/80 illicit test posts).
  3. Probability calibration via Platt scaling provides exact posterior probabilities required by the Hybrid Risk Engine.
  4. Ultra-fast inference (<2ms per post) on commodity CPU hardware."""
    },

    "dataset": {
        "title": "Dataset Construction & 3-Class Strategy",
        "keywords": ["dataset", "data", "classes", "three class", "3-class", "medical", "uci", "drugscom", "adversarial"],
        "answer": """**Dataset Architecture & 3-Class Taxonomy (`dataset/dataset_loader.py`)**

Rather than naive binary classification, our platform implements a balanced **3-Class Taxonomy**:

1. **Class 0: General / Benign Everyday Posts**:
   - Everyday conversational comments, tech discussions, academic chats, and sports forum posts.
   - Includes **Adversarial Traps** (e.g., *"remember to take blood pressure pill"*, *"winter snow blizzard"*, *"looking for tech vendor plug"*) to prevent false positives.
2. **Class 1: Legitimate Medical Reviews**:
   - Extracted from the **UCI / Drugs.com dataset** (`drugsComTrain_raw.csv`).
   - Genuine patient experiences with prescription drugs (e.g., Lisinopril, Sertraline, Metformin, Adderall).
   - Critical for training the model to distinguish legal healthcare discussions from illicit narcotic sales.
3. **Class 2: Illicit Drug Trafficking / Distribution**:
   - Real-world and synthetically augmented darknet marketplace listings and encrypted channel posts.
   - Features covert handles (Telegram `@coke_vendor`, Wickr), cryptocurrency addresses (BTC, XMR), stealth packaging terms, and emoji ciphers."""
    },

    "risk_scoring": {
        "title": "Hybrid Threat Risk Scoring Mathematical Formulation",
        "keywords": ["risk", "threat score", "formula", "scoring", "risk score", "calculation", "math", "equation"],
        "answer": """**Hybrid Threat Risk Scoring Formula (`engine/risk_engine.py`)**

The platform combines machine learning probability with cyber entity density:

$$\\text{Threat Score (\\%)} = \\min\\left(100.0, \\; \\left(P_{\\text{illicit}} \\times 0.70 + \\text{EntityBonus} \\times 0.30\\right) \\times 100\\right)$$

$$\\text{where } \\text{EntityBonus} = \\min\\left(0.40, \\; N_{\\text{entities}} \\times 0.15 + N_{\\text{keywords}} \\times 0.05\\right)$$

* **Risk Level Thresholds**:
  - 🔴 **CRITICAL (80% – 100%)**: Confirmed commercial trafficking with active contact/payment channels.
  - 🟠 **HIGH (60% – 79%)**: Explicit illicit narcotic offering or bulk solicitation.
  - 🟡 **MEDIUM (35% – 59%)**: Ambiguous slang, suspicious peer inquiries, or partial handles.
  - 🟢 **LOW (0% – 34%)**: Benign conversation or legitimate medical prescription review.
* **Critical Override Rule**: If explicit drug emojis AND an active Telegram/Crypto handle are detected simultaneously, the threat score is automatically enforced to a minimum of **88.0% (CRITICAL)**."""
    },

    "entity_extractor": {
        "title": "Covert Entity Extractor & Pattern Recognition",
        "keywords": ["entity", "extractor", "telegram", "wickr", "session", "crypto", "bitcoin", "monero", "onion", "darknet", "regex"],
        "answer": """**Covert Entity Extraction Engine (`extractors/entity_extractor.py`)**

Extracts actionable digital evidentiary artifacts via compiled Deterministic Finite Automata (DFA regex):

* **Telegram Handles**: `(?:@|t\\.me\\/|telegram\\.me\\/)([a-zA-Z0-9_]{5,32})`
* **Wickr Usernames**: `(?:wickr|wickrme)[\\s:]*([a-zA-Z0-9_]{3,32})`
* **Session IDs**: `(?:session|session id)[\\s:]*([a-fA-F0-9]{20,66})`
* **Darknet Tor Markets**: `\\b([a-z2-7]{16,56}\\.onion)\\b`
* **Bitcoin (BTC) Wallets**: SegWit (`bc1...`) and Legacy (`1...`, `3...`) regex validators.
* **Monero (XMR) Wallets**: Privacy-coin addresses starting with `4` or `8` (`[48][0-9a-zA-Z]{20,94}`).
* **Illicit Emoji Ciphers**: Unicode scanning for `❄️`, `💊`, `🌿`, `💉`, `🧪`, `🍬`, `🍯`, `🧊`."""
    },

    "explainable_ai": {
        "title": "Explainable AI (XAI) & Token Keyword Attribution",
        "keywords": ["xai", "explainable", "explainable ai", "highlight", "tokens", "token highlight", "interpretability"],
        "answer": """**Explainable AI (XAI) Token Attribution Module**

* **The Problem**: Machine learning classifiers are often "black boxes", which is unacceptable in criminal prosecution where digital forensics must be audit-proof.
* **Our XAI Mechanism**:
  - The system analyzes token-level contributions against known danger dictionaries and extracted cyber entities.
  - Danger tokens (drug emojis, contact handles, crypto wallets, street slang) are highlighted with high-contrast red tags (`danger`).
  - Contextual benign tokens are labeled as `normal`.
* **Law Enforcement Value**: Officers and forensic evaluators can immediately see **why** the AI made the decision without inspecting high-dimensional matrix mathematics."""
    },

    "case_reporting": {
        "title": "Automated Cyber Threat Intelligence Case Report Generator",
        "keywords": ["report", "case report", "pdf", "export", "law enforcement", "dossier", "summary"],
        "answer": """**Automated Case Dossier Generator (`engine/report_generator.py`)**

Generates court-ready evidentiary dossiers with a single click:

* **Official Case Reference**: e.g., `CASE-INTEL-849201` with automated timestamp.
* **Threat Verdict & Probability Breakdown**: Classification, Risk Score, and ML confidence.
* **Forensic Evidence Log**: Formatted list of all discovered Telegram handles, Wickr IDs, and crypto wallet hashes.
* **Chain of Custody Notice**: Verifies automated digital processing compliance.
* **Print & Export Capability**: Instant PDF export and CSV case audit logging."""
    },

    "tech_stack": {
        "title": "Technology Stack & Architecture",
        "keywords": ["tech stack", "technology", "python", "fastapi", "libraries", "tools", "architecture"],
        "answer": """**Full System Technology Stack**

* **Backend & NLP Engine**:
  - Python 3.14 / 3.13
  - **FastAPI**: Asynchronous high-speed REST API microframework.
  - **Uvicorn**: Lightning-fast ASGI web server.
  - **Scikit-Learn**: TF-IDF feature extraction, Logistic Regression, Random Forest, Naive Bayes.
  - **NLTK**: Stopword tokenization and morphological lemmatization.
  - **Joblib**: Serialized model deployment.
* **Frontend Dashboard**:
  - Modern Glassmorphism CSS UI system (dark slate palette, neon cyan/purple accents).
  - Responsive vanilla JavaScript (zero external CDN dependency required).
  - Live WebSocket / REST asynchronous communication."""
    },

    "viva_questions": {
        "title": "Top Evaluator / Viva Questions & Answers",
        "keywords": ["viva", "evaluator", "questions", "interview", "review", "marks", "rubric", "bmsce"],
        "answer": """**Top Viva & Project Review Defense Questions**

1. **Q: Why not use binary classification (Illicit vs Non-Illicit)?**
   * *A*: Binary models suffer massive false positives on medical reviews mentioning opioids or painkillers. Adding a dedicated "Legitimate Medical Review" class forces the model to learn the context of doctor prescriptions vs darknet sales.
2. **Q: How do you handle new unseen street drug slang?**
   * *A*: Multi-word n-gram TF-IDF $(1,2)$ captures contextual associations even if an individual slang word evolves, while the modular slang dictionary in `preprocess.py` allows updating slang terms without retraining.
3. **Q: What is the computational complexity of the preprocessing pipeline?**
   * *A*: $\\mathcal{O}(N)$ linear scan per document using pre-compiled regex automata and $\\mathcal{O}(1)$ dictionary hash table lookups.
4. **Q: Why is Monero (XMR) detection especially important?**
   * *A*: Monero is an untraceable privacy coin heavily favored on darknet markets. Detecting Monero addresses provides an immediate boost to the risk score."""
    }
}

# ==============================================================================
# INTENT MATCHING & INTELLIGENT CONVERSATIONAL RESPONSE ENGINE
# ==============================================================================

SUGGESTED_PROMPTS = [
    "Explain the 8-Stage NLP Preprocessing Pipeline",
    "Which ML model is the best and why?",
    "How is the Hybrid Threat Risk Score calculated?",
    "Why does the system use 3 classes instead of binary?",
    "What entities and crypto wallets are extracted?",
    "Can you analyze this post: 'Fresh ❄️ on Telegram @coke_king'?"
]

def format_bot_response(content: str, suggestions: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "status": "success",
        "response": content,
        "suggested_questions": suggestions or SUGGESTED_PROMPTS[:4]
    }

def get_chat_response(user_message: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    Main dialogue router:
    1. Checks if the user is asking to analyze a sample post.
    2. Matches semantic intents against the project knowledge base.
    3. Handles greetings and conversational inquiries.
    4. Provides comprehensive viva-ready project explanations.
    """
    if not user_message or not user_message.strip():
        return format_bot_response("Please enter a question or topic about the project!")

    query = user_message.strip()
    query_lower = query.lower()

    # 1. Live text analysis trigger in chat
    analyze_triggers = ["analyze this", "analyze post", "scan this", "test this", "is this illicit", "check this post"]
    contains_trigger = any(t in query_lower for t in analyze_triggers)
    is_sample_post = ("❄" in query or "💊" in query or "@" in query or "wickr" in query_lower or "btc" in query_lower or "plug" in query_lower) and len(query.split()) > 4

    if contains_trigger or is_sample_post:
        # Strip trigger prefix if present
        clean_target = query
        for t in analyze_triggers:
            if t in clean_target.lower():
                idx = clean_target.lower().find(t) + len(t)
                clean_target = clean_target[idx:].strip(" :-\"'")
                break

        if len(clean_target) > 5:
            analysis = analyze_threat(clean_target)
            cat = analysis['predicted_category']
            score = analysis['threat_score']
            level = analysis['risk_level']
            tg = ", ".join(analysis['entities']['telegram_handles']) or "None"
            crypto = ", ".join(analysis['entities']['bitcoin_addresses'] + analysis['entities']['monero_addresses']) or "None"
            emojis = ", ".join(analysis['entities']['detected_emojis']) or "None"

            response = f"""**🔍 Real-Time Threat Intelligence Analysis:**

* **Input Analyzed**: *"{clean_target}"*
* **Classification Verdict**: **{cat}**
* **Threat Severity Score**: **{score}%** ({level})
* **Extracted Telegram Handles**: `{tg}`
* **Extracted Crypto Wallets**: `{crypto}`
* **Detected Drug Emojis**: `{emojis}`
* **8-Stage Cleaned Input**:
  `{analysis['cleaned_text']}`

💡 *You can also test this in the Live Text Scanner tab!*"""
            return format_bot_response(response, [
                "How was this Threat Score calculated?",
                "Explain the 8-Stage NLP pipeline",
                "Which ML model made this prediction?"
            ])

    # 2. Greetings & general identity
    if query_lower in ["hi", "hello", "hey", "help", "who are you", "what can you do"]:
        greeting = """👋 **Hello! I am CyberNarc AI — the Project Intelligence Assistant.**

I have complete knowledge of the **AI-Powered Cyber Drug Trafficking Detection Platform**. You can ask me anything about:

* 🔬 **The 8-Stage NLP Preprocessing Pipeline** (Emoji translation, Slang normalization, Cyber masking)
* 📊 **Machine Learning Classifiers** (Logistic Regression, Random Forest, Benchmark results)
* 🎯 **Hybrid Risk Engine Formula** (How the 0–100% Threat Score is mathematically derived)
* 📂 **Dataset & 3-Class Strategy** (UCI medical reviews, illicit trafficking, adversarial traps)
* 🔎 **Covert Entity Extraction** (Telegram, Wickr, Session, Bitcoin, Monero)
* 🎓 **Viva & Evaluator FAQs** (Rubric alignment for 20/20 review marks)
* ⚡ **Live Analysis**: Paste any text and ask me to analyze it!

*What would you like to explore?*"""
        return format_bot_response(greeting, SUGGESTED_PROMPTS)

    # 3. Knowledge base scoring & best-match retrieval
    best_match_key = None
    best_score = 0

    for key, item in KNOWLEDGE_BASE.items():
        score = 0
        for kw in item["keywords"]:
            if kw in query_lower:
                score += len(kw) * 2
        if score > best_score:
            best_score = score
            best_match_key = key

    if best_match_key and best_score >= 4:
        item = KNOWLEDGE_BASE[best_match_key]
        return format_bot_response(item["answer"])

    # 4. Fallback contextual guidance
    fallback_text = f"""I understand you're asking about: **"{query}"**.

Here are the key technical areas of our project you might be interested in:

* 🔬 **NLP Pipeline**: Type *"Explain 8-stage preprocessing"* to see how raw posts are cleaned.
* 📊 **Model Benchmarks**: Type *"Which ML model is best?"* to see accuracy and comparison tables.
* 🧮 **Mathematical Formulation**: Type *"How is the risk score calculated?"* to view the hybrid scoring equation.
* 📁 **Datasets**: Type *"What dataset is used?"* to learn about the 3-class design.
* 🚨 **Direct Analysis**: Type *"Analyze: [your post text]"* to test threat scoring live.

Feel free to pick one of the quick options below!"""
    return format_bot_response(fallback_text, SUGGESTED_PROMPTS)
