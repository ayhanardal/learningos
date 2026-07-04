import json
from pathlib import Path
from app.services.data import BASE_DIR

PINNED_FILE = BASE_DIR / "data" / "pinned.json"

PINNED_FILE.parent.mkdir(parents=True, exist_ok=True)
if not PINNED_FILE.exists():
    PINNED_FILE.write_text("[]")


def _load():
    try:
        raw = PINNED_FILE.read_text().strip()
        return json.loads(raw) if raw else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(data):
    PINNED_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def get_all():
    return _load()


def toggle(subject, topic, subtopic=None):
    items = _load()
    key = subject + "::" + topic + ("::" + subtopic if subtopic else "")
    existing = None
    for item in items:
        item_key = item["subject"] + "::" + item["topic"] + ("::" + item.get("subtopic", "") if item.get("subtopic") else "")
        if item_key == key:
            existing = item
            break
    if existing:
        items = [i for i in items if i is not existing]
        _save(items)
        return {"pinned": False, "items": items}
    items.append({"subject": subject, "topic": topic, "subtopic": subtopic or ""})
    _save(items)
    return {"pinned": True, "items": items}
