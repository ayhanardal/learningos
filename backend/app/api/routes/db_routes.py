from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import json
import uuid
import os

from app.database import get_db
from app.models import UserNote, UserRoadmap
from app.schemas import NoteCreate, RoadmapCreate

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@router.post("/notes/upload")
async def upload_note_image(file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        raise HTTPException(status_code=400, detail="Geçersiz dosya formatı!")
    
    filename = f"{uuid.uuid4()}{ext.lower()}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya kaydedilemedi: {str(e)}")
        
    return {"status": "success", "url": f"/static/uploads/{filename}"}
