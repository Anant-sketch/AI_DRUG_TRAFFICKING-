import re
import os
import sys

# Ensure root directory is on path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from preprocessing.preprocess import clean_text as core_clean_text, CYBER_PATTERNS

# Regex for common bot commands and non-threat spam advertising
BOT_COMMAND_PATTERN = re.compile(r'^\s*/(start|help|settings|rules|id|info|menu|lang|subscribe|unsubscribe)\b', re.IGNORECASE)

SPAM_KEYWORDS = [
    r'\b(crypto signals|binary options|earn \$?\d+ daily|forex trading|guaranteed returns|free spins|online casino|slot machine|porn|viagra|cialis)\b'
]
SPAM_PATTERN = re.compile('|'.join(SPAM_KEYWORDS), re.IGNORECASE)


def is_spam_or_bot(text: str) -> bool:
    """
    Evaluates whether an incoming raw Telegram message is automated bot noise
    or generic marketing spam rather than potential threat activity.
    """
    if not text or not isinstance(text, str):
        return True

    text_stripped = text.strip()
    if len(text_stripped) < 5:
        return True

    # Filter out direct bot commands (/start, /help, etc.)
    if BOT_COMMAND_PATTERN.match(text_stripped):
        return True

    # Filter out generic commercial spam unrelated to narcotics / threat ops
    if SPAM_PATTERN.search(text_stripped):
        return True

    return False


def clean_text(text: str) -> str:
    """
    Delegates to the 8-Stage NLP Preprocessing Pipeline for token normalization,
    emoji decoding, slang expansion, and cyber entity masking.
    """
    return core_clean_text(text)

