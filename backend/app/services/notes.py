import json
from pathlib import Path
from app.services.data import BASE_DIR, slugify

NOTES_DIR = BASE_DIR / "data"
NOTES_FILE = NOTES_DIR / "user_notes.json"

NOTES_DIR.mkdir(parents=True, exist_ok=True)
if not NOTES_FILE.exists():
    NOTES_FILE.write_text("{}")


def _load():
    try:
        raw = NOTES_FILE.read_text().strip()
        return json.loads(raw) if raw else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data):
    NOTES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def _key(subject, topic, subtopic=""):
    s_slug = slugify(subject)
    t_slug = slugify(topic)
    if subtopic:
        st_slug = slugify(subtopic)
        return f"{s_slug}-{t_slug}-{st_slug}"
    return f"{s_slug}-{t_slug}"



def get_notes(subject, topic, subtopic=""):
    db = _load()
    k = _key(subject, topic, subtopic)
    return db.get(k, [])


def add_note(subject, topic, note_type, content, solution="", subtopic=""):
    db = _load()
    k = _key(subject, topic, subtopic)
    if k not in db:
        db[k] = []
    db[k].append({
        "type": note_type,
        "content": content,
        "solution": solution,
        "id": len(db[k]) + 1,
    })
    _save(db)
    return db[k]
