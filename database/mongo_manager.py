import os
import json
import logging
import uuid
import time
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Check if pymongo is installed
try:
    from pymongo import MongoClient  # type: ignore
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False
    logger.warning("pymongo is not installed. MongoManager will use local JSON persistence fallback.")


class MongoManager:
    """
    Robust Database Manager for Scraped Telegram Threat Intelligence.
    Supports MongoDB natively when available, with automatic zero-configuration
    fallback to local JSON database (database/scraped_messages.json) to ensure
    demos and offline evaluations never crash.
    """
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("MONGODB_DATABASE", "narcotrace")
        self.client = None
        self.db = None
        self.is_connected = False
        
        # Local JSON database fallback path
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.fallback_file = os.path.join(self.base_dir, "scraped_messages.json")

    def connect(self) -> bool:
        """Attempts connection to MongoDB; enables fallback mode on failure."""
        if not HAS_PYMONGO:
            logger.info(f"Using local JSON database fallback at: {self.fallback_file}")
            self.is_connected = True
            return True

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            self.db = self.client[self.db_name]
            self.client.admin.command('ping')
            self.is_connected = True
            logger.info(f"Successfully connected to MongoDB at {self.uri}")
            return True
        except Exception as e:
            logger.warning(f"MongoDB not reachable ({e}). Switching to local JSON storage fallback.")
            self.client = None
            self.db = None
            self.is_connected = True
            return True

    def _read_fallback(self) -> List[Dict[str, Any]]:
        """Reads stored messages from local JSON fallback file safely."""
        if not os.path.exists(self.fallback_file):
            return []
        try:
            with open(self.fallback_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except Exception as e:
            logger.error(f"Error reading JSON fallback database: {e}")
            return []

    def _write_fallback(self, data: List[Dict[str, Any]]) -> bool:
        """Writes messages to local JSON fallback file safely using atomic swap."""
        temp_file = self.fallback_file + ".tmp"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(temp_file):
                # Atomic replace on Windows/Linux
                if os.path.exists(self.fallback_file):
                    os.replace(temp_file, self.fallback_file)
                else:
                    os.rename(temp_file, self.fallback_file)
            return True
        except Exception as e:
            logger.error(f"Error writing to JSON fallback database: {e}")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass
            return False

    def insert_message(self, message_data: Dict[str, Any]) -> str:
        """Inserts a scraped message into MongoDB or local JSON fallback."""
        if not self.is_connected:
            self.connect()

        # Generate a clean string ID if not present
        doc_id = str(message_data.get("id") or message_data.get("_id") or f"doc_{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}")
        message_data["id"] = doc_id
        message_data["_id"] = doc_id

        # If MongoDB is active
        if self.db is not None:
            try:
                collection = self.db['messages']
                db_doc = dict(message_data)
                result = collection.insert_one(db_doc)
                obj_id = str(result.inserted_id)
                # Keep _id as clean string to prevent JSON serialization crashes
                message_data["_id"] = obj_id
                message_data["id"] = obj_id
                logger.info(f"MongoDB: Inserted new message ID: {obj_id}")
                return obj_id
            except Exception as e:
                logger.warning(f"MongoDB insert failed ({e}). Falling back to local storage.")

        # Local JSON Fallback
        doc = dict(message_data)
        doc["_id"] = doc_id
        doc["id"] = doc_id

        existing = self._read_fallback()
        
        # Deduplication check
        chat_id = doc.get("chat_id")
        msg_id = doc.get("message_id")
        channel = doc.get("channel")

        def is_duplicate(m: Dict[str, Any]) -> bool:
            if m.get("_id") == doc_id or m.get("id") == doc_id:
                return True
            if msg_id and m.get("message_id") == msg_id:
                if chat_id and m.get("chat_id") == chat_id:
                    return True
                if channel and m.get("channel") == channel:
                    return True
            return False

        existing = [m for m in existing if not is_duplicate(m)]
        existing.insert(0, doc)  # Prepend newest first
        existing = existing[:200]  # Retain latest 200 records
        self._write_fallback(existing)
        logger.info(f"Local DB: Saved scraped message {doc_id}")
        return doc_id

    def get_messages(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves recent scraped messages."""
        if not self.is_connected:
            self.connect()

        if self.db is not None:
            try:
                collection = self.db['messages']
                records = list(collection.find().sort("_id", -1).limit(limit))
                clean_records = []
                for r in records:
                    item = dict(r)
                    if "_id" in item:
                        item["_id"] = str(item["_id"])
                    if "id" not in item:
                        item["id"] = str(item.get("_id", ""))
                    clean_records.append(item)
                return clean_records
            except Exception as e:
                logger.warning(f"Failed to query MongoDB ({e}). Falling back to local JSON.")

        messages = self._read_fallback()
        return messages[:limit]

    def count_messages(self) -> int:
        """Returns total messages count."""
        if not self.is_connected:
            self.connect()

        if self.db is not None:
            try:
                return self.db['messages'].count_documents({})
            except Exception:
                pass

        return len(self._read_fallback())

    def clear_messages(self) -> bool:
        """Clears stored messages for clean demo restarts."""
        if self.db is not None:
            try:
                self.db['messages'].delete_many({})
            except Exception:
                pass
        return self._write_fallback([])
