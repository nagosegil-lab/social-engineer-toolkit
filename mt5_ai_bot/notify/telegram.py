from __future__ import annotations

import json
import time
from typing import Optional

import requests


def send_message(bot_token: str, chat_id: str, text: str, parse_mode: Optional[str] = None) -> bool:
    if not bot_token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text[:4000],  # Telegram message limit safety
        "disable_web_page_preview": True,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if not resp.ok:
            return False
        data = resp.json()
        return bool(data.get("ok"))
    except Exception:
        return False
