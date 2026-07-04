from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services import data, notes, pinned

router = APIRouter()


class LogEntry(BaseModel):
    subject: str = Field(..., description="Ders adı")
    hours: float = Field(..., gt=0, description="Çalışılan saat")
    solved_questions: int = Field(..., description="Çözülen soru sayısı")
    topic_slug: str = Field(..., description="Konu slug ID'si")


class NoteEntry(BaseModel):
    type: str = Field(..., description="Soru tipi / Taktik")
    content: str = Field(..., description="Not içeriği")
    solution: str = Field(default="", description="Çözüm / Açıklama")


def sync_wrap(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"[api] Error in {fn.__name__}: {e}")
            return {"error": str(e), "data": []}
    return wrapper


@router.get("/curriculum/all")
async def get_curriculum_all():
    return sync_wrap(data.get_curriculum_all)()


@router.get("/curriculum/summary")
async def get_curriculum_summary():
    return sync_wrap(data.get_curriculum_summary)()


@router.get("/plan")
async def get_plan():
    return sync_wrap(data.get_plan)()


@router.get("/today")
async def get_today():
    return sync_wrap(data.get_today)()


@router.get("/progress")
async def get_progress():
    return sync_wrap(data.get_progress)()


@router.get("/logs")
async def get_logs():
    return sync_wrap(data.get_logs)()


@router.get("/stats")
async def get_stats():
    return sync_wrap(data.get_stats)()


@router.post("/log")
async def log_study(entry: LogEntry):
    try:
        data.log_study(entry.subject, entry.hours, entry.solved_questions, entry.topic_slug)
        return {"ok": True, "subject": entry.subject, "hours": entry.hours, "solved_questions": entry.solved_questions}
    except Exception as e:
        print(f"[api] Error in log_study: {e}")
        return {"ok": False, "error": str(e)}


@router.get("/notes/{subject}/{topic}")
async def get_notes(subject: str, topic: str):
    try:
        return notes.get_notes(subject, topic)
    except Exception as e:
        print(f"[api] Error in get_notes: {e}")
        return {"error": str(e), "data": []}


@router.post("/notes/{subject}/{topic}")
async def add_note(subject: str, topic: str, entry: NoteEntry):
    try:
        result = notes.add_note(subject, topic, entry.type, entry.content, entry.solution)
        return {"ok": True, "notes": result}
    except Exception as e:
        print(f"[api] Error in add_note: {e}")
        return {"ok": False, "error": str(e)}


@router.get("/notes/{subject}/{topic}/{subtopic}")
async def get_notes_st(subject: str, topic: str, subtopic: str):
    try:
        return notes.get_notes(subject, topic, subtopic)
    except Exception as e:
        print(f"[api] Error in get_notes_st: {e}")
        return {"error": str(e), "data": []}


@router.post("/notes/{subject}/{topic}/{subtopic}")
async def add_note_st(subject: str, topic: str, subtopic: str, entry: NoteEntry):
    try:
        result = notes.add_note(subject, topic, entry.type, entry.content, entry.solution, subtopic)
        return {"ok": True, "notes": result}
    except Exception as e:
        print(f"[api] Error in add_note_st: {e}")
        return {"ok": False, "error": str(e)}


@router.get("/pinned")
async def get_pinned():
    try:
        return pinned.get_all()
    except Exception as e:
        print(f"[api] Error in get_pinned: {e}")
        return {"error": str(e), "data": []}


@router.post("/pin/{subject}/{topic}")
async def toggle_pin(subject: str, topic: str, subtopic: str = ""):
    try:
        return pinned.toggle(subject, topic, subtopic or None)
    except Exception as e:
        print(f"[api] Error in toggle_pin: {e}")
        return {"ok": False, "error": str(e)}


@router.get("/plan/week")
async def get_plan_week():
    return sync_wrap(data.get_plan_week)()


@router.get("/plan/macro")
async def get_plan_macro():
    return sync_wrap(data.get_plan_macro)()

