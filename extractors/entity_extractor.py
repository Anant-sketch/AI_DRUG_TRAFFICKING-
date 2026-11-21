import re
from typing import Dict, List, Any

# Regex patterns for intelligence extraction
PATTERNS = {
    'telegram_handle': r'(?:@|t\.me\/|telegram\.me\/)([a-zA-Z0-9_]{5,32})',
    'wickr_handle': r'(?:wickr|wickrme|wickr me)[\s:]*([a-zA-Z0-9_]{3,32})',
    'session_handle': r'(?:session|session id)[\s:]*([a-fA-F0-9]{20,66})',
    'bitcoin_address': r'\b(bc1[a-zA-Z0-9]{25,39}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b',
    'ethereum_address': r'\b(0x[a-fA-F0-9]{40})\b',
    'monero_address': r'\b([48][0-9a-zA-Z]{20,94})\b',
    'darknet_onion': r'\b([a-z2-7]{16,56}\.onion)\b',
    'phone_number': r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
}

DRUG_EMOJIS = ['❄️', '❄', '💊', '🌿', '🍁', '🍃', '🔌', '🍄', '💉', '🧪', '🍬', '🧊', '💨', '🍫', '💎']

SUSPICIOUS_KEYWORD_LIST = [
    'plug', 'coke', 'cocaine', 'heroin', 'meth', 'ice', 'weed', 'cannabis', 'hash', 'shrooms',
    'xanax', 'bars', 'pills', 'percocet', 'oxy', 'fentanyl', 'lsd', 'acid', 'ecstasy', 'mdma',
    'uncut', 'stealth', 'discreet shipping', 'darknet', 'tor', 'escrow', 'telegram', 'wickr',
    'crypto', 'bitcoin', 'monero', 'btc', 'xmr', 'cashapp', 'zelle', 'venmo', 'pack', 'loud', 'pure'
]

def extract_entities(text: str) -> Dict[str, Any]:
    """
    Scans raw text and extracts law-enforcement intelligence artifacts:
    Telegram/Wickr/Session handles, Crypto addresses, Onion links, and suspicious emojis.
    """
    if not isinstance(text, str):
        return {
            'telegram_handles': [],
            'wickr_handles': [],
            'session_handles': [],
            'bitcoin_addresses': [],
            'ethereum_addresses': [],
            'monero_addresses': [],
            'darknet_links': [],
            'phone_numbers': [],
            'detected_emojis': [],
            'suspicious_keywords': [],
            'entity_count': 0
        }

    results = {}

    # Extract regex entities
    results['telegram_handles'] = list(set(re.findall(PATTERNS['telegram_handle'], text, re.IGNORECASE)))
    results['wickr_handles'] = list(set(re.findall(PATTERNS['wickr_handle'], text, re.IGNORECASE)))
    results['session_handles'] = list(set(re.findall(PATTERNS['session_handle'], text, re.IGNORECASE)))
    results['bitcoin_addresses'] = list(set(re.findall(PATTERNS['bitcoin_address'], text)))
    results['ethereum_addresses'] = list(set(re.findall(PATTERNS['ethereum_address'], text)))
    results['monero_addresses'] = list(set(re.findall(PATTERNS['monero_address'], text)))
    results['darknet_links'] = list(set(re.findall(PATTERNS['darknet_onion'], text, re.IGNORECASE)))
    results['phone_numbers'] = list(set(re.findall(PATTERNS['phone_number'], text)))

    # Extract drug emojis
    found_emojis = [char for char in DRUG_EMOJIS if char in text]
    results['detected_emojis'] = list(set(found_emojis))

    # Extract suspicious keyword hits
    text_lower = text.lower()
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORD_LIST if kw in text_lower]
    results['suspicious_keywords'] = list(set(found_keywords))

    # Calculate total entity count
    total_entities = (
        len(results['telegram_handles']) +
        len(results['wickr_handles']) +
        len(results['bitcoin_addresses']) +
        len(results['ethereum_addresses']) +
        len(results['monero_addresses']) +
        len(results['darknet_links']) +
        len(results['detected_emojis'])
    )
    results['entity_count'] = total_entities

    return results

if __name__ == "__main__":
    sample = "Darknet vendor 🔌 DM on Telegram @dark_plug99 or Wickr: drugking. Pay BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa or Monero. ❄️ and 💊 available."
    extracted = extract_entities(sample)
    import json
    print(json.dumps(extracted, indent=2))
