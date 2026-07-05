from pydantic import BaseModel
from typing import Dict, Any
from datetime import date

class NoteCreate(BaseModel):
    subject: str
    topic: str
    content: Dict[str, Any]

class RoadmapCreate(BaseModel):
    sprint_start_date: date
    roadmap_json: Dict[str, Any]
