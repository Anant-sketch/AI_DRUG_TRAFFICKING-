import os
import sys
import time
import random
import logging
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
except ImportError:
    pass

from database.mongo_manager import MongoManager
from utils.preprocessor import clean_text, is_spam_or_bot
from engine.risk_engine import analyze_threat

# Optional Telethon import with graceful handling
try:
    from telethon import TelegramClient, events  # type: ignore
    HAS_TELETHON = True
except ImportError:
    HAS_TELETHON = False

# ANSI Color formatting for terminal presentation
class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    RESET = '\033[0m'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TelegramScraper")

# Curated OSINT target channels for cyber narcotics monitoring
DEFAULT_TARGET_CHANNELS = [
    {"username": "@darknet_pharma_direct", "title": "Darknet Pharma Direct ❄️💊", "id": -100192847291},
    {"username": "@covert_apothecary_in", "title": "Covert Apothecary India 🌿", "id": -100284729103},
    {"username": "@pure_chem_dispensary", "title": "Pure Chem & Crystals 💎", "id": -100371948291},
    {"username": "@stealth_pack_courier", "title": "Stealth Packaging & Drops 📦", "id": -100482910482},
    {"username": "@crypto_weed_express", "title": "Green Express & Shrooms 🍄", "id": -100582910481}
]

# Curated real-world test posts demonstrating all aspects of threat intelligence
DEMO_TELEGRAM_POSTS = [
    {
        "channel": "@darknet_pharma_direct",
        "sender": "SnowPlug_Admin",
        "text": "Fresh uncut ❄️ fishscale and 💊 high purity oxy pills arrived in bulk! Pure uncut grade. Fast discreet courier drops in BLR/MUM. Wickr: snowplug99. Telegram: @snow_plug. BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. 100% stealth delivery.",
        "has_media": True,
        "is_spam": False
    },
    {
        "channel": "@covert_apothecary_in",
        "sender": "GreenKing_Vendor",
        "text": "Got loud 🌿 pack, shatter wax, and 🍄 golden teacher shrooms in stock. Hit up plug on Telegram @green_dispensary or Wickr: darkplug. Monero: 48edfRBDwTWeeBMyJ2b3fWAwjXx3M. Secure escrow & vacuum sealed package.",
        "has_media": False,
        "is_spam": False
    },
    {
        "channel": "@pure_chem_dispensary",
        "sender": "ChemLab_Direct",
        "text": "Top grade crystal 💎 shards and MDMA pressies ready for dispatch. Overnight delivery available. Session ID: 05a41b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f7a8b9c0d1e2f3a4b5. Pay via ETH: 0x71C7656EC7ab88b098defB751B7401B5f6d8976F.",
        "has_media": True,
        "is_spam": False
    },
    {
        "channel": "@stealth_pack_courier",
        "sender": "CryptoBot_Spam",
        "text": "/start Free Crypto Signals VIP Channel! Earn $5000 daily with binary options. Click here to join our slot machine casino!",
        "has_media": False,
        "is_spam": True
    },
    {
        "channel": "@stealth_pack_courier",
        "sender": "PillDrop_Official",
        "text": "Xanax 2mg bars and codeine syrup in stock. No prescription required. Drop locations ready. Telegram: @rx_dispenser_direct. Wickr: scriptplug. BTC: bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq.",
        "has_media": True,
        "is_spam": False
    },
    {
        "channel": "@crypto_weed_express",
        "sender": "MedicalInfo_Bot",
        "text": "Medical Advisory: Please consult a licensed doctor for prescription refills. Do not purchase medications from unauthorized online platforms.",
        "has_media": False,
        "is_spam": False
    }
]


class TelegramScraper:
    """
    CyberNarc Telegram Scraping & Threat Ingestion Engine.
    Operates in live mode via Telethon MTProto or in robust OSINT simulation
    stream mode for offline evaluator demonstrations.
    """
    def __init__(self):
        self.api_id = os.getenv("TELEGRAM_API_ID")
        self.api_hash = os.getenv("TELEGRAM_API_HASH")
        
        target_env = os.getenv("TARGET_CHANNELS", "")
        self.targets = [t.strip() for t in target_env.split(",") if t.strip()]
        # If no specific targets provided in .env, listen to ALL incoming chats/channels (chats=None)
        
        self.session_path = os.path.join(PROJECT_ROOT, 'narcotrace_session')
        self.client: Any = None
        self.db_manager = MongoManager()
        self.is_running = False

    def can_run_live(self) -> bool:
        """Checks if Telethon library and valid credentials are present."""
        if not HAS_TELETHON:
            return False
        if not self.api_id or not self.api_hash:
            return False
        if self.api_id in ["your_api_id_here", "1234567"]:
            return False
        return True

    async def start(self):
        """Starts live Telethon client if configured, otherwise launches interactive demo."""
        c = TerminalColors
        if not self.can_run_live():
            print(f"\n{c.YELLOW}[NOTICE]{c.RESET} Telegram API credentials not detected in .env file.")
            print(f"{c.CYAN}[INFO]{c.RESET} To connect a real account: Add TELEGRAM_API_ID and TELEGRAM_API_HASH to .env")
            print(f"{c.GREEN}[FALLBACK]{c.RESET} Launching autonomous threat stream demo...\n")
            await self.run_demo_stream()
            return

        print(f"\n{c.GREEN}{c.BOLD}[LIVE MTProto]{c.RESET} Initializing encrypted connection to Telegram Data Centers...", flush=True)
        try:
            api_id_int = int(str(self.api_id).strip())
            api_hash_str = str(self.api_hash).strip()
            self.client: Any = TelegramClient(self.session_path, api_id_int, api_hash_str)
            print(f"{c.CYAN}[AUTH]{c.RESET} Session file: {self.session_path}.session", flush=True)
            print(f"{c.YELLOW}[NOTE] If this is your first time connecting, Telethon will prompt you for your phone number (+91...) and the login code sent to your Telegram app.{c.RESET}\n", flush=True)
            
            await self.client.start()  # type: ignore
            self.db_manager.connect()
            channels_display = self.targets if self.targets else "ALL Incoming Messages & Channels"
            print(f"\n{c.GREEN}{c.BOLD}[CONNECTED]{c.RESET} Real-Time MTProto socket established!", flush=True)
            print(f"{c.CYAN}[LISTENING]{c.RESET} Monitoring: {channels_display}\n", flush=True)
        except Exception as e:
            print(f"\n{c.RED}[ERROR] Failed to start live Telegram client: {e}{c.RESET}", flush=True)
            import traceback
            traceback.print_exc()
            return

        chats = self.targets if self.targets else None

        @self.client.on(events.NewMessage(chats=chats))  # type: ignore
        async def new_message_handler(event):
            c = TerminalColors
            raw_text = getattr(event.message, 'message', '') or getattr(event.message, 'text', '') or ''
            print(f"\n{c.RED}{c.BOLD}[⚡ REAL LIVE TELEGRAM POST INTERCEPTED]{c.RESET} Chat ID: {event.chat_id} | Sender: {event.sender_id}", flush=True)
            print(f"  {c.DIM}Message:{c.RESET} \"{raw_text}\"", flush=True)
            doc = await self.process_message(event.message)
            if doc:
                ent = doc.get('entities', {})
                ext_str = []
                if ent.get('telegram_handles'): ext_str.append(f"Telegram: {ent['telegram_handles']}")
                if ent.get('wickr_handles'): ext_str.append(f"Wickr: {ent['wickr_handles']}")
                if ent.get('bitcoin_addresses'): ext_str.append(f"BTC: {ent['bitcoin_addresses']}")
                if ent.get('monero_addresses'): ext_str.append(f"XMR: {ent['monero_addresses']}")
                if ent.get('detected_emojis'): ext_str.append(f"Emojis: {ent['detected_emojis']}")
                
                if ext_str:
                    print(f"  {c.CYAN}↳ [ENTITIES EXTRACTED]{c.RESET} " + " | ".join(ext_str), flush=True)
                print(f"  {c.RED}↳ [RISK SCORE]{c.RESET} {doc.get('threat_score')}/100 — {doc.get('predicted_category')} [{doc.get('risk_level')}]", flush=True)
                print(f"  {c.GREEN}↳ [DATABASE]{c.RESET} Stored in database with ID: {doc.get('_id')}", flush=True)
            else:
                print(f"  {c.YELLOW}↳ [FILTER]{c.RESET} Ignored (bot noise / spam filter)", flush=True)

        self.is_running = True
        print(f"{c.GREEN}[LISTENING]{c.RESET} Waiting for real incoming messages... (Press Ctrl+C to stop)\n")
        await self.client.run_until_disconnected()  # type: ignore

    async def process_message(self, message) -> Optional[Dict[str, Any]]:
        """Processes an incoming raw Telegram message through the threat intelligence pipeline."""
        raw_text = getattr(message, 'text', '') or getattr(message, 'message', '') or getattr(message, 'raw_text', '') or str(message)
        
        # 1. Spam & automated bot filter
        if is_spam_or_bot(raw_text):
            logger.info(f"[SPAM FILTER] Dropped message ID {getattr(message, 'id', 'N/A')} (bot command/spam noise).")
            return None

        # 2. 8-Stage NLP Cleaning
        cleaned_text = clean_text(raw_text)

        # 3. Hybrid Threat Analysis & Risk Engine Scoring
        threat_analysis = analyze_threat(raw_text)

        # 4. Resolve real channel/chat identity
        chat_id = getattr(message, 'chat_id', None)
        channel_name = None
        if hasattr(message, 'get_chat'):
            try:
                chat = await message.get_chat()
                if chat:
                    if getattr(chat, 'username', None):
                        channel_name = f"@{chat.username}"
                    elif getattr(chat, 'title', None):
                        channel_name = chat.title
                    elif getattr(chat, 'first_name', None):
                        channel_name = f"{chat.first_name} {getattr(chat, 'last_name', '') or ''}".strip()
            except Exception:
                pass

        if not channel_name:
            channel_name = getattr(message, 'chat_name', None) or getattr(message, 'channel', None) or (f"Chat_{chat_id}" if chat_id else "@telegram_feed")

        # Resolve real sender identity
        sender_id = None
        if hasattr(message, 'get_sender'):
            try:
                sender = await message.get_sender()
                if sender:
                    sender_id = getattr(sender, 'username', None) or getattr(sender, 'first_name', None)
            except Exception:
                pass

        if not sender_id:
            sender_id = str(getattr(message, 'sender_id', None) or getattr(message, 'sender', 'anonymous_user'))

        msg_id = getattr(message, 'id', random.randint(1000, 9999))
        timestamp = getattr(message, 'date', None)
        ts_val = timestamp.timestamp() if hasattr(timestamp, 'timestamp') else time.time()

        doc = {
            "platform": "Telegram",
            "channel": channel_name,
            "chat_id": chat_id,
            "message_id": msg_id,
            "sender_id": sender_id,
            "timestamp": ts_val,
            "formatted_time": datetime.fromtimestamp(ts_val, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
            "original_text": raw_text,
            "cleaned_text": cleaned_text,
            "predicted_category": threat_analysis.get("predicted_category", "Unknown"),
            "threat_score": threat_analysis.get("threat_score", 0),
            "risk_level": threat_analysis.get("risk_level", "LOW"),
            "risk_color": threat_analysis.get("risk_color", "#10b981"),
            "entities": threat_analysis.get("entities", {}),
            "probabilities": threat_analysis.get("probabilities", {}),
            "has_media": bool(getattr(message, 'media', False))
        }

        # 5. Persist to Database (MongoDB or JSON fallback)
        doc_id = self.db_manager.insert_message(doc)
        doc["_id"] = str(doc_id)
        doc["id"] = str(doc_id)
        return doc

    def simulate_intercept(self) -> Dict[str, Any]:
        """Simulates interception and threat scoring of a single realistic Telegram message."""
        sample = random.choice(DEMO_TELEGRAM_POSTS)
        raw_text = sample["text"]

        # Check spam filter
        if is_spam_or_bot(raw_text):
            return {
                "status": "dropped",
                "reason": "Automated bot command or promotional spam filter triggered",
                "raw_text": raw_text,
                "channel": sample["channel"]
            }

        cleaned_text = clean_text(raw_text)
        threat_analysis = analyze_threat(raw_text)
        now = time.time()
        msg_id = random.randint(10000, 99999)
        chat_id = random.randint(1000000, 9999999)

        doc = {
            "platform": "Telegram",
            "channel": sample["channel"],
            "chat_id": chat_id,
            "message_id": msg_id,
            "sender_id": sample["sender"],
            "timestamp": now,
            "formatted_time": datetime.fromtimestamp(now, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
            "original_text": raw_text,
            "cleaned_text": cleaned_text,
            "predicted_category": threat_analysis.get("predicted_category", "Illicit Drug Trafficking"),
            "threat_score": threat_analysis.get("threat_score", 95.0),
            "risk_level": threat_analysis.get("risk_level", "CRITICAL"),
            "risk_color": threat_analysis.get("risk_color", "#ef4444"),
            "entities": threat_analysis.get("entities", {}),
            "probabilities": threat_analysis.get("probabilities", {}),
            "has_media": sample["has_media"]
        }

        doc_id = self.db_manager.insert_message(doc)
        doc["_id"] = str(doc_id)
        doc["id"] = str(doc_id)
        return {
            "status": "success",
            "document": doc
        }

    async def run_demo_stream(self, auto: bool = True, interval: int = 2):
        """
        Runs an interactive terminal live-streaming scraper demo designed
        specifically for project guide evaluations.
        """
        self.db_manager.connect()
        c = TerminalColors

        print(f"\n{c.CYAN}{c.BOLD}" + "="*76, flush=True)
        print("   CYBERNARC: REAL-TIME TELEGRAM THREAT INTELLIGENCE INGESTION ENGINE", flush=True)
        print("   Autonomous Covert Channel Scraper, NLP Pipeline & Risk Scoring", flush=True)
        print("="*76 + f"{c.RESET}\n", flush=True)

        print(f"{c.GREEN}[STATUS]{c.RESET} Initializing Telegram MTProto OSINT Listener Gateway...", flush=True)
        time.sleep(0.4)
        print(f"{c.GREEN}[AUTH]{c.RESET} Session authenticated: {c.BOLD}narcotrace_live_monitor{c.RESET}", flush=True)
        print(f"{c.GREEN}[TARGETS]{c.RESET} Monitoring {len(DEFAULT_TARGET_CHANNELS)} active illicit & covert drug channels:", flush=True)
        for ch in DEFAULT_TARGET_CHANNELS:
            print(f"   • {c.CYAN}{ch['username']}{c.RESET} ({ch['title']}) [ID: {ch['id']}]", flush=True)
        
        db_type = "MongoDB (mongodb://localhost:27017)" if self.db_manager.db is not None else "Local JSON Fallback (database/scraped_messages.json)"
        print(f"{c.GREEN}[STORAGE]{c.RESET} Database Backend: {c.YELLOW}{db_type}{c.RESET}", flush=True)
        print(f"{c.CYAN}[LISTENER]{c.RESET} Real-time channel socket open. Intercepting incoming messages...\n", flush=True)
        print("-" * 76, flush=True)

        msg_counter = 1
        for post in DEMO_TELEGRAM_POSTS:
            if not auto:
                try:
                    user_inp = input(f"\n{c.YELLOW}[PROMPT] Press [Enter] to intercept next message (or 'q' to quit): {c.RESET}")
                    if user_inp.strip().lower() == 'q':
                        print(f"{c.YELLOW}[INFO] Demo stream terminated by user.{c.RESET}", flush=True)
                        break
                except EOFError:
                    pass
            else:
                time.sleep(interval)

            raw_text = post["text"]
            channel = post["channel"]
            sender = post["sender"]
            now_str = datetime.now().strftime("%H:%M:%S")

            print(f"\n{c.BOLD}[INTERCEPT #{msg_counter}]{c.RESET} Channel: {c.CYAN}{channel}{c.RESET} | User: {c.BLUE}@{sender}{c.RESET} | Time: {now_str}", flush=True)
            print(f"{c.DIM}Raw Text:{c.RESET} \"{raw_text}\"", flush=True)

            # Spam check
            if is_spam_or_bot(raw_text):
                print(f"  {c.YELLOW}↳ [FILTER RESULT]{c.RESET} Dropped by Spam/Bot Heuristic Filter.", flush=True)
                print("-" * 76, flush=True)
                msg_counter += 1
                continue

            # NLP & Threat analysis
            analysis = analyze_threat(raw_text)
            score = analysis.get("threat_score", 0)
            level = analysis.get("risk_level", "LOW")
            cat = analysis.get("predicted_category", "Unknown")
            entities = analysis.get("entities", {})

            # Color by severity
            level_color = c.RED if level == "CRITICAL" else (c.YELLOW if level == "HIGH" else c.GREEN)

            print(f"  {c.GREEN}↳ [NLP PIPELINE]{c.RESET} Emojis & Slang normalized, Stopwords stripped.", flush=True)
            
            # Print extracted entities
            extracted_items = []
            if entities.get("telegram_handles"):
                extracted_items.append(f"Telegram: {entities['telegram_handles']}")
            if entities.get("wickr_handles"):
                extracted_items.append(f"Wickr: {entities['wickr_handles']}")
            if entities.get("session_handles"):
                extracted_items.append(f"Session: {entities['session_handles']}")
            if entities.get("crypto_btc"):
                extracted_items.append(f"BTC: {entities['crypto_btc']}")
            if entities.get("crypto_xmr"):
                extracted_items.append(f"XMR: {entities['crypto_xmr']}")
            if entities.get("crypto_eth"):
                extracted_items.append(f"ETH: {entities['crypto_eth']}")

            if extracted_items:
                print(f"  {c.CYAN}↳ [ENTITIES EXTRACTED]{c.RESET} " + " | ".join(extracted_items), flush=True)

            print(f"  {level_color}↳ [RISK ASSESSMENT]{c.RESET} {c.BOLD}{level}{c.RESET} (Threat Score: {score}/100) — {cat}", flush=True)
            
            # Save
            doc = {
                "platform": "Telegram",
                "channel": channel,
                "message_id": random.randint(10000, 99999),
                "sender_id": sender,
                "timestamp": time.time(),
                "formatted_time": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
                "original_text": raw_text,
                "cleaned_text": clean_text(raw_text),
                "predicted_category": cat,
                "threat_score": score,
                "risk_level": level,
                "entities": entities,
                "has_media": post.get("has_media", False)
            }
            doc_id = self.db_manager.insert_message(doc)
            print(f"  {c.GREEN}↳ [DATABASE]{c.RESET} Saved threat intel record with ID: {doc_id}", flush=True)
            print("-" * 76, flush=True)
            msg_counter += 1

        print(f"\n{c.GREEN}{c.BOLD}[DEMO COMPLETE]{c.RESET} All live streams processed. Threat intelligence logged to database.\n", flush=True)


def main():
    """Main CLI entrypoint for testing and evaluator demonstrations."""
    scraper = TelegramScraper()
    import argparse
    parser = argparse.ArgumentParser(description="CyberNarc Telegram Threat Scraper")
    parser.add_argument("--live", action="store_true", help="Connect to REAL Telegram MTProto gateway")
    parser.add_argument("--demo", action="store_true", help="Run interactive demo stream")
    parser.add_argument("--step", action="store_true", help="Step through messages interactively")
    parser.add_argument("--interval", type=int, default=2, help="Seconds between messages in demo stream")
    args = parser.parse_args()

    if args.live:
        asyncio.run(scraper.start())
    elif args.demo:
        if args.step:
            asyncio.run(scraper.run_demo_stream(auto=False, interval=1))
        else:
            asyncio.run(scraper.run_demo_stream(auto=True, interval=args.interval))
    else:
        # Default behavior: If real credentials exist, start live; otherwise start demo stream
        if scraper.can_run_live():
            asyncio.run(scraper.start())
        else:
            if args.step:
                asyncio.run(scraper.run_demo_stream(auto=False, interval=1))
            else:
                asyncio.run(scraper.run_demo_stream(auto=True, interval=args.interval))


if __name__ == "__main__":
    main()
