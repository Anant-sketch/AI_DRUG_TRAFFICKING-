"""
CyberNarc - Real-Time Telegram Ingestion Demo Runner
Usage:
    python run_telegram_demo.py          # Auto-streams intercepted messages every 2 seconds
    python run_telegram_demo.py --step   # Step through messages interactively with Enter key
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.telegram_scraper import main

if __name__ == "__main__":
    main()

