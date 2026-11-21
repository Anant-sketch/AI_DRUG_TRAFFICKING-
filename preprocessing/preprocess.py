import re
import html
import sys

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# Pre-compiled regex patterns for maximum efficiency
CYBER_PATTERNS = {
    'telegram': re.compile(r'(?:@|t\.me\/|telegram\.me\/)([a-zA-Z0-9_]{5,32})', re.IGNORECASE),
    'wickr': re.compile(r'(?:wickr|wickrme|wickr me)[\s:]*([a-zA-Z0-9_]{3,32})', re.IGNORECASE),
    'session': re.compile(r'(?:session|session id)[\s:]*([a-fA-F0-9]{20,66})', re.IGNORECASE),
    'crypto_btc': re.compile(r'\b(bc1[a-zA-Z0-9]{25,39}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b'),
    'crypto_eth': re.compile(r'\b(0x[a-fA-F0-9]{40})\b'),
    'crypto_xmr': re.compile(r'\b([48][0-9a-zA-Z]{20,94})\b'),
    'darknet_onion': re.compile(r'\b([a-z2-7]{16,56}\.onion)\b', re.IGNORECASE),
}

# Illicit drug emoji cipher dictionary
EMOJI_DRUG_MAP = {
    '❄️': ' drug_cocaine ',
    '❄': ' drug_cocaine ',
    '💊': ' drug_prescription_pills ',
    '🌿': ' drug_cannabis_weed ',
    '🍁': ' drug_cannabis_weed ',
    '🍃': ' drug_cannabis_weed ',
    '🔌': ' drug_dealer_plug ',
    '🍄': ' drug_shrooms_psychedelic ',
    '💉': ' drug_heroin_needle ',
    '🧪': ' drug_meth_chemical ',
    '🍬': ' drug_ecstasy_mdma ',
    '🧊': ' drug_ice_crystal_meth ',
    '🍫': ' drug_thc_edibles ',
    '💎': ' drug_pure_crystals ',
    '🍯': ' drug_thc_wax_dab ',
    '💨': ' drug_vape_smoke ',
    '🚀': ' drug_euphoria_high ',
    '🔥': ' fire_potent_quality ',
}

# Standard English contractions expansion map
CONTRACTIONS_MAP = {
    r"\bcan't\b": "cannot",
    r"\bwon't\b": "will not",
    r"\bshan't\b": "shall not",
    r"\bn't\b": " not",
    r"\b're\b": " are",
    r"\b's\b": " is",
    r"\b'd\b": " would",
    r"\b'll\b": " will",
    r"\b't\b": " not",
    r"\b've\b": " have",
    r"\b'm\b": " am",
}

# Multi-word street slang and darknet trade terms
MULTI_WORD_SLANG = {
    'loud pack': 'potent_cannabis',
    'pure uncut': 'pure_unadulterated',
    'uncut pure': 'pure_unadulterated',
    'stealth shipping': 'covert_delivery',
    'discreet shipping': 'covert_delivery',
    'stealth packaging': 'hidden_packaging',
    'discreet delivery': 'covert_delivery',
    'no prescription': 'illicit_no_rx',
    'overnight delivery': 'rapid_courier_shipping',
    'bulk order': 'wholesale_quantity',
    'fish scale': 'pure_cocaine_fishscale',
    'brown sugar': 'afghan_heroin',
    'crystal meth': 'methamphetamine',
    'gel tabs': 'lsd_tabs',
}

# Single-word street drug slang mapping
SINGLE_WORD_SLANG = {
    'plug': 'dealer_supplier',
    'score': 'purchase_illicit_drugs',
    'uncut': 'pure_quality',
    'pack': 'drug_package',
    'loud': 'strong_marijuana',
    'gear': 'illicit_narcotics',
    'tabs': 'acid_lsd_tabs',
    'bars': 'xanax_alprazolam_bars',
    'pressies': 'counterfeit_pills',
    'vendor': 'darknet_seller',
    'escrow': 'darknet_crypto_escrow',
    'fishscale': 'pure_cocaine',
    'shards': 'crystal_meth',
    'speed': 'amphetamine_paste',
    'dabs': 'concentrated_thc',
    'lean': 'codeine_syrup',
    'dope': 'illicit_heroin',
    'blow': 'cocaine_powder',
    'snow': 'cocaine_powder',
    'coke': 'cocaine',
    'shrooms': 'psychedelic_mushrooms',
    'mdma': 'ecstasy_mdma',
    'fent': 'lethal_fentanyl',
}

# Complete standard English stop words (zero external network dependency)
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y'
}

# Negation words to explicitly retain for threat & medical context integrity
NEGATION_WHITELIST = {'no', 'not', 'nor', 'none', 'neither', 'never', 'without'}
STOP_WORDS = STOP_WORDS - NEGATION_WHITELIST

# Safe Lemmatizer check without downloading over the internet
HAS_WORDNET = False
lemmatizer_obj = None
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    # Test if WordNet corpora is already cached locally
    test_lem = WordNetLemmatizer()
    _ = test_lem.lemmatize('test')
    lemmatizer_obj = test_lem
    HAS_WORDNET = True
except Exception:
    HAS_WORDNET = False


# ==========================================
# MODULAR 8-STAGE PREPROCESSING FUNCTIONS
# ==========================================

def stage1_html_unescape_and_clean(text: str) -> str:
    """Stage 1: Decodes HTML entities (&#039; -> ', &amp; -> &) and strips HTML tags."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    return text

def stage2_mask_cyber_entities(text: str) -> str:
    """Stage 2: Detects covert handles & crypto wallets, transforming into canonical features."""
    text = CYBER_PATTERNS['telegram'].sub(' token_telegram_contact ', text)
    text = CYBER_PATTERNS['wickr'].sub(' token_wickr_handle ', text)
    text = CYBER_PATTERNS['session'].sub(' token_session_handle ', text)
    text = CYBER_PATTERNS['darknet_onion'].sub(' token_darknet_onion ', text)
    text = CYBER_PATTERNS['crypto_btc'].sub(' token_crypto_btc ', text)
    text = CYBER_PATTERNS['crypto_eth'].sub(' token_crypto_eth ', text)
    text = CYBER_PATTERNS['crypto_xmr'].sub(' token_crypto_xmr ', text)
    return text

def stage3_decode_emojis(text: str) -> str:
    """Stage 3: Translates illicit emoji ciphers into standardized semantic tokens."""
    for emoji_char, token in EMOJI_DRUG_MAP.items():
        text = text.replace(emoji_char, token)
    return text

def stage4_expand_contractions(text: str) -> str:
    """Stage 4: Expands English contractions (don't -> do not) for uniform representation."""
    for pattern, replacement in CONTRACTIONS_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def stage5_normalize_slang(text: str) -> str:
    """Stage 5: Expands street slang, dealer jargon, and darknet idioms."""
    text_lower = text.lower()
    for phrase, replacement in MULTI_WORD_SLANG.items():
        text_lower = text_lower.replace(phrase, f" {replacement} ")

    tokens = text_lower.split()
    normalized = [SINGLE_WORD_SLANG.get(w, w) for w in tokens]
    return " ".join(normalized)

def stage6_clean_punctuation(text: str) -> str:
    """Stage 6: Removes special characters and punctuation while preserving token underscores."""
    text = re.sub(r'[^a-zA-Z0-9_\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def stage7_tokenize_and_filter_stopwords(text: str) -> list:
    """Stage 7: Splits text into tokens and filters stopwords while preserving negations."""
    tokens = text.split()
    filtered = [w for w in tokens if w not in STOP_WORDS and len(w) > 1]
    return filtered

def stage8_lemmatize_tokens(tokens: list) -> list:
    """Stage 8: Morphological lemmatization to reduce words to root grammatical forms."""
    if HAS_WORDNET and lemmatizer_obj:
        try:
            return [lemmatizer_obj.lemmatize(w) for w in tokens]
        except Exception:
            pass

    # Robust rule-based morphological normalization fallback
    lemmatized = []
    for w in tokens:
        if w.startswith(('drug_', 'token_')):
            lemmatized.append(w)
        elif w.endswith('ies') and len(w) > 5:
            lemmatized.append(w[:-3] + 'y')
        elif w.endswith('es') and len(w) > 4:
            lemmatized.append(w[:-2])
        elif w.endswith('s') and not w.endswith('ss') and len(w) > 3:
            lemmatized.append(w[:-1])
        elif w.endswith('ing') and len(w) > 5:
            lemmatized.append(w[:-3])
        elif w.endswith('ed') and len(w) > 4:
            lemmatized.append(w[:-2])
        else:
            lemmatized.append(w)
    return lemmatized

def clean_text(text: str) -> str:
    """
    Full 8-Stage NLP Preprocessing Pipeline:
    1. HTML entity unescaping & web noise removal
    2. Covert cyber entity detection & canonical tokenization
    3. Illicit emoji cipher decoding
    4. English contraction expansion
    5. Street slang & darknet jargon normalization
    6. Token-safe punctuation filtering (preserving underscores)
    7. Stopword filtering with negation retention
    8. Morphological lemmatization
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    s1 = stage1_html_unescape_and_clean(text)
    s2 = stage2_mask_cyber_entities(s1)
    s3 = stage3_decode_emojis(s2)
    s4 = stage4_expand_contractions(s3)
    s5 = stage5_normalize_slang(s4)
    s6 = stage6_clean_punctuation(s5)
    s7 = stage7_tokenize_and_filter_stopwords(s6)
    s8 = stage8_lemmatize_tokens(s7)

    return " ".join(s8)

def get_preprocessing_stages_breakdown(text: str) -> dict:
    """Returns intermediate representations at each stage for explainability & evaluations."""
    s1 = stage1_html_unescape_and_clean(text)
    s2 = stage2_mask_cyber_entities(s1)
    s3 = stage3_decode_emojis(s2)
    s4 = stage4_expand_contractions(s3)
    s5 = stage5_normalize_slang(s4)
    s6 = stage6_clean_punctuation(s5)
    s7 = stage7_tokenize_and_filter_stopwords(s6)
    s8 = stage8_lemmatize_tokens(s7)

    return {
        'stage1_html_clean': s1,
        'stage2_cyber_masked': s2,
        'stage3_emoji_decoded': s3,
        'stage4_contractions_expanded': s4,
        'stage5_slang_normalized': s5,
        'stage6_punctuation_cleaned': s6,
        'stage7_tokens_filtered': s7,
        'stage8_lemmatized_output': " ".join(s8)
    }

if __name__ == "__main__":
    test_sample = "Hey guys! Don&#039;t sleep on this ❄️ and 💊 available! DM plug on Telegram @coke_plug99 for loud pack discreet shipping. BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    print("=== Testing 8-Stage NLP Preprocessing Pipeline ===")
    print("Input Text:\n", test_sample)
    print("\nProcessed Output:\n", clean_text(test_sample))