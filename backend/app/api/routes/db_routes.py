from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import UserNote, UserRoadmap
from app.schemas import NoteCreate, RoadmapCreate

router = APIRouter()

@router.post("/notes")
def save_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(UserNote).filter(UserNote.subject == note.subject, UserNote.topic == note.topic).first()
    content_str = json.dumps(note.content)
    if db_note:
        db_note.content = content_str
    else:
        db_note = UserNote(subject=note.subject, topic=note.topic, content=content_str)
        db.add(db_note)
    db.commit()
    return {"status": "success", "message": "Not başarıyla kaydedildi."}

@router.get("/notes")
def get_note(subject: str, topic: str, db: Session = Depends(get_db)):
    db_note = db.query(UserNote).filter(UserNote.subject == subject, UserNote.topic == topic).first()
    if db_note:
        return {"status": "success", "content": json.loads(db_note.content)}
    raise HTTPException(status_code=404, detail="Not bulunamadı")

@router.post("/plan/roadmap/save")
def save_roadmap(roadmap: RoadmapCreate, db: Session = Depends(get_db)):
    db_roadmap = db.query(UserRoadmap).filter(UserRoadmap.sprint_start_date == roadmap.sprint_start_date).first()
    if db_roadmap:
        db_roadmap.roadmap_json = roadmap.roadmap_json
    else:
        db_roadmap = UserRoadmap(sprint_start_date=roadmap.sprint_start_date, roadmap_json=roadmap.roadmap_json)
        db.add(db_roadmap)
    db.commit()
    return {"status": "success", "message": "Yol haritası kaydedildi."}

@router.get("/plan/roadmap/load")
def load_roadmap(sprint_start_date: str, db: Session = Depends(get_db)):
    db_roadmap = db.query(UserRoadmap).filter(str(UserRoadmap.sprint_start_date) == sprint_start_date).first()
    if db_roadmap:
        return {"status": "success", "roadmap_json": db_roadmap.roadmap_json}
    raise HTTPException(status_code=404, detail="Yol haritası bulunamadı")
