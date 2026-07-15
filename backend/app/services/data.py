import json, os, yaml, re
from datetime import datetime
from pathlib import Path

_container = Path("/workspace/projects/learningos")
if _container.exists():
    BASE_DIR = _container
else:
    _self = Path(os.path.abspath(__file__))
    BASE_DIR = _self.parent.parent.parent.parent
CURRICULUM_DIR = BASE_DIR / "curriculum"
PLAN_FILE = BASE_DIR / "study-plans" / "60-gunluk-plan.json"
TRACKER_DIR = BASE_DIR / ".tracker"
TRACKER_LOG = TRACKER_DIR / "log.json"
TRACKER_TOPICS = TRACKER_DIR / "topics_status.json"
TRACKER_SUBQUESTS = TRACKER_DIR / "session_subquests.json"

TRACKER_DIR.mkdir(parents=True, exist_ok=True)
for _f in [TRACKER_LOG, TRACKER_TOPICS, TRACKER_SUBQUESTS]:
    if not _f.exists():
        _f.write_text("{}" if _f in [TRACKER_TOPICS, TRACKER_SUBQUESTS] else "[]")


def slugify(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    mapping = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'â': 'a', 'î': 'i', 'û': 'u', 'I': 'i', 'İ': 'i'
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text).strip('-')
    return text


def load_json(path, default=None):
    if path.exists():
        try:
            raw = path.read_text().strip()
            if not raw:
                return default if default is not None else {}
            return json.loads(raw)
        except (json.JSONDecodeError, OSError):
            return default if default is not None else {}
    return default if default is not None else {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def safe_call(fn, default=None):
    try:
        return fn()
    except Exception as e:
        print(f"[data] Error in {fn.__name__}: {e}")
        return default


def get_plan():
    return load_json(PLAN_FILE, default={})


def get_today():
    from app.services.plan_generator import generate_roadmap_projection
    roadmap = generate_roadmap_projection()
    weeks = roadmap.get("weeks", {})
    if not weeks:
        return {"genel": [], "alan": []}
    today_str = datetime.now().strftime("%Y-%m-%d")
    sorted_keys = sorted(weeks.keys(), key=lambda x: int(x.replace("Hafta ", "")))
    for wk in sorted_keys:
        for day in weeks[wk]["days"]:
            if day["date"] == today_str:
                return day
    first_key = sorted_keys[0]
    days = weeks[first_key]["days"]
    return days[0] if days else {"genel": [], "alan": []}


def get_progress():
    raw_progress = load_json(TRACKER_TOPICS, default={})
    
    mapping = {"Türkçe": "turkce", "Matematik": "matematik", "Tarih": "tarih",
               "Coğrafya": "cografya", "Vatandaşlık": "vatandaslik", "İstatistik": "istatistik"}
               
    result = {}
    for lesson_name, lesson_slug in mapping.items():
        result[lesson_slug] = {
            "done": 0.0,
            "total": 0.0,
            "solved_questions": 0,
            "target_questions": 0
        }
        
    summary = get_curriculum_summary()
    for cat in summary:
        for s in cat["subjects"]:
            lesson_slug = mapping.get(s["name"])
            if lesson_slug:
                result[lesson_slug]["total"] = s["total_hours"]
                result[lesson_slug]["target_questions"] = s["total_questions"] or 0
                
    for topic_slug, data in raw_progress.items():
        matched_slug = None
        for lesson_slug in mapping.values():
            if topic_slug.startswith(lesson_slug + "-"):
                matched_slug = lesson_slug
                break
        
        if matched_slug:
            result[matched_slug]["done"] += data.get("completed", 0.0)
            result[matched_slug]["solved_questions"] += data.get("solved_questions", 0)
            
    return result


def get_logs():
    return load_json(TRACKER_LOG, default=[])


def log_study(subject, hours, solved_questions=0, topic_slug=""):
    logs = get_logs()
    if not isinstance(logs, list):
        logs = []
        
    efficiency = solved_questions / hours if hours > 0 else 0
    logs.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "subject": subject,
        "hours": hours,
        "solved_questions": solved_questions,
        "topic_slug": topic_slug,
        "efficiency": round(efficiency, 2)
    })
    save_json(TRACKER_LOG, logs)

    topics = get_progress_raw()
    if not isinstance(topics, dict):
        topics = {}
        
    target_q = 0
    curriculum = get_curriculum_all()
    found = False
    for exam in curriculum:
        for test in exam["tests"]:
            for s in test["subjects"]:
                if s["subject"] == subject:
                    for t in s["topics"]:
                        if t["id"] == topic_slug:
                            target_q = t["avg_questions"]
                            found = True
                            break
                if found: break
            if found: break
        if found: break

    topics.setdefault(topic_slug, {
        "completed": 0.0,
        "total": 0.0,
        "solved_questions": 0,
        "target_questions": target_q
    })
    
    topics[topic_slug]["completed"] = topics[topic_slug].get("completed", 0.0) + hours
    topics[topic_slug]["solved_questions"] = topics[topic_slug].get("solved_questions", 0) + solved_questions
    topics[topic_slug]["target_questions"] = target_q
    
    save_json(TRACKER_TOPICS, topics)
    return True


def get_progress_raw():
    return load_json(TRACKER_TOPICS, default={})


def get_session_subquests_raw():
    return load_json(TRACKER_SUBQUESTS, default={})


def get_completed_sessions_count(topic_slug):
    data = get_session_subquests_raw()
    topic_data = data.get(topic_slug, {})
    sessions = topic_data.get("sessions", [])
    count = 0
    for session in sessions:
        subquests = session.get("subquests", [])
        if subquests and all(sq.get("is_completed", False) for sq in subquests):
            count += 1
    return count


def get_subquests(topic_slug: str):
    data = get_session_subquests_raw()
    return data.get(topic_slug, {"sessions": []})


def save_session_subquests(topic_slug: str, session_index: int, subquests: list):
    data = get_session_subquests_raw()
    if topic_slug not in data:
        data[topic_slug] = {"sessions": []}
    
    sessions = data[topic_slug]["sessions"]
    session = next((s for s in sessions if s.get("session_index") == session_index), None)
    if session:
        session["subquests"] = subquests
    else:
        sessions.append({
            "session_index": session_index,
            "subquests": subquests
        })
    
    save_json(TRACKER_SUBQUESTS, data)
    return True


def toggle_subquest(topic_slug: str, session_index: int, subquest_id: str, is_completed: bool):
    data = get_session_subquests_raw()
    if topic_slug not in data:
        return False
    
    sessions = data[topic_slug]["sessions"]
    session = next((s for s in sessions if s.get("session_index") == session_index), None)
    if not session:
        return False
        
    sq = next((q for q in session.get("subquests", []) if q.get("id") == subquest_id), None)
    if not sq:
        return False
        
    sq["is_completed"] = is_completed
    from datetime import datetime
    if is_completed:
        sq["completed_at"] = datetime.now().strftime("%Y-%m-%d")
    else:
        sq["completed_at"] = None
        
    save_json(TRACKER_SUBQUESTS, data)
    return True


def get_dynamic_subtopics(subject_name, topic_name):
    tracker_subquests = {}
    if TRACKER_SUBQUESTS.exists():
        try:
            with open(TRACKER_SUBQUESTS, "r", encoding="utf-8") as f:
                tracker_subquests = json.load(f)
        except Exception:
            pass

    slug = f"{slugify(subject_name)}-{slugify(topic_name)}"
    topic_data = tracker_subquests.get(slug, {})
    sessions = topic_data.get("sessions", [])
    
    dynamic_subtopics = []
    seen = set()
    for session in sessions:
        for sq in session.get("subquests", []):
            if sq.get("label") == "alt konu" and sq.get("title"):
                title = sq.get("title")
                if title not in seen:
                    seen.add(title)
                    dynamic_subtopics.append(title)
    return dynamic_subtopics


def get_curriculum_summary():
    progress = get_progress_raw()
    if not isinstance(progress, dict):
        progress = {}

    categories = {}
    if not CURRICULUM_DIR.exists():
        return []
    for root, _, files in os.walk(CURRICULUM_DIR):
        for f in files:
            if not f.endswith(".yaml"):
                continue
            try:
                with open(Path(root) / f, encoding="utf-8") as fh:
                    subj = yaml.safe_load(fh)
            except (yaml.YAMLError, OSError):
                continue
            if not subj:
                continue
            
            subject_name = subj["subject"]
            cat = subj.get("category", "Diğer")
            
            total_hours = subj.get("total_estimated_hours") or sum(
                (t.get("estimated_hours") or t.get("hours", 0) or 0) for t in subj.get("topics", [])
            ) or 1
            
            done_hours = 0.0
            for t in subj.get("topics", []):
                t_slug = f"{slugify(subject_name)}-{slugify(t['name'])}"
                done_hours += progress.get(t_slug, {}).get("completed", 0.0)
                
            pct = round((done_hours / total_hours * 100) if total_hours else 0, 1)
            categories.setdefault(cat, []).append({
                "name": subject_name,
                "total_questions": subj.get("total_questions"),
                "target_correct": subj.get("target_correct") or subj.get("target_net"),
                "total_hours": total_hours,
                "completed_hours": done_hours,
                "completion_pct": pct,
                "topics": [{
                    "id": f"{slugify(subject_name)}-{slugify(t['name'])}",
                    "name": t["name"],
                    "hours": t.get("estimated_hours") or t.get("hours", 0),
                    "avg_questions": t.get("avg_questions", 0),
                    "subtopics": [{
                        "id": f"{slugify(subject_name)}-{slugify(t['name'])}-{slugify(st)}",
                        "name": st
                    } for st in get_dynamic_subtopics(subject_name, t['name'])]
                } for t in subj.get("topics", [])],
            })
    return [{"name": cat, "subjects": categories[cat]} for cat in ["Genel Yetenek", "Genel Kültür", "Alan Bilgisi"] if cat in categories]


EXAM_MAP = {
    "genel-yetenek": {"exam": "2026 KPSS Lisans", "exam_id": "lisans", "test": "Genel Yetenek (GY)", "test_id": "gy"},
    "genel-kultur": {"exam": "2026 KPSS Lisans", "exam_id": "lisans", "test": "Genel Kültür (GK)", "test_id": "gk"},
    "alan": {"exam": "2026 KPSS Alan Bilgisi", "exam_id": "alan", "test": "Alan Bilgisi", "test_id": "alan"},
}


def get_curriculum_all():
    if not CURRICULUM_DIR.exists():
        return []
    
    from app.services.plan_generator import EXACT_ALLOCATIONS
        
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}
        
    exams = {}
    for root, _, files in os.walk(CURRICULUM_DIR):
        for f in files:
            if not f.endswith(".yaml"):
                continue
            try:
                with open(Path(root) / f, encoding="utf-8") as fh:
                    subj = yaml.safe_load(fh)
            except (yaml.YAMLError, OSError):
                continue
            if not subj or not isinstance(subj, dict):
                continue
            meta = EXAM_MAP.get(subj.get("exam", ""))
            if not meta:
                continue
            exam_id = meta["exam_id"]
            test_id = meta["test_id"]
            subject_name = subj.get("subject", "")
            
            topics_list = []
            for t in subj.get("topics", []):
                t_name = t.get("name", "")
                t_slug = f"{slugify(subject_name)}-{slugify(t_name)}"
                
                allocated = EXACT_ALLOCATIONS.get(t_name, 0)
                
                prog = raw_progress.get(t_slug, {})
                comp_h = prog.get("completed", 0.0)
                solved_q = prog.get("solved_questions", 0)
                
                completed = get_completed_sessions_count(t_slug)
                
                topics_list.append({
                    "id": t_slug,
                    "name": t_name,
                    "avg_questions": t.get("avg_questions", 0),
                    "target_net": t.get("target_net", 0),
                    "allocated_sessions": allocated,
                    "completed_sessions": completed,
                    "chronologicalIndex": t.get("chronologicalIndex"),
                    "isRoutine": t.get("isRoutine", False),
                    "subtopics": [{
                        "id": f"{t_slug}-{slugify(st)}",
                        "name": st
                    } for st in get_dynamic_subtopics(subject_name, t_name)]
                })

            subject_data = {
                "subject": subject_name,
                "total_questions": subj.get("total_questions", 0),
                "target_correct": subj.get("target_correct") or subj.get("target_net", 0),
                "topics": topics_list,
            }
            exams.setdefault(exam_id, {"exam": meta["exam"], "exam_id": exam_id, "tests": {}})
            exams[exam_id]["tests"].setdefault(test_id, {"test": meta["test"], "test_id": test_id, "subjects": []})
            exams[exam_id]["tests"][test_id]["subjects"].append(subject_data)
    result = []
    for eid in ["lisans", "alan"]:
        if eid not in exams:
            continue
        tests = []
        for tid in (["gy", "gk"] if eid == "lisans" else ["alan"]):
            if tid in exams[eid]["tests"]:
                tests.append(exams[eid]["tests"][tid])
        result.append({"exam": exams[eid]["exam"], "exam_id": eid, "tests": tests})
    return result


def get_stats():
    plan = get_plan() or {}
    topics = get_progress()
    logs = get_logs()
    today_str = datetime.now().strftime("%Y-%m-%d")

    if not isinstance(logs, list):
        logs = []
    if not isinstance(topics, dict):
        topics = {}

    total_logged = sum(e.get("hours", 0) for e in logs) if logs else 0
    today_hours = sum(e.get("hours", 0) for e in logs if e.get("date") == today_str) if logs else 0
    week_hours = 0
    if logs:
        now = datetime.now()
        week_hours = sum(
            e.get("hours", 0) for e in logs
            if (now - datetime.strptime(e.get("date"), "%Y-%m-%d")).days < 7
        )

    # Toplam çözülen soru
    total_questions = sum(e.get("solved_questions", 0) for e in logs) if logs else 0
    # Genel verimlilik
    avg_efficiency = total_questions / total_logged if total_logged > 0 else 0

    subject_stats = {}
    for key, data in topics.items():
        if not isinstance(data, dict):
            continue
        total = data.get("total", 0) or 1
        done = data.get("done", 0)
        pct = round((done / total * 100) if total else 0, 1)
        names = {"turkce": "Türkçe", "matematik": "Matematik", "tarih": "Tarih",
                 "cografya": "Coğrafya", "vatandaslik": "Vatandaşlık", "istatistik": "İstatistik"}
        subject_stats[names.get(key, key)] = {"done": done, "total": total, "pct": pct, "completed_sessions": 0}

    curriculum = get_curriculum_summary()
    for cat in curriculum:
        for subj in cat.get("subjects", []):
            subj_name = subj.get("name")
            if subj_name not in subject_stats:
                subject_stats[subj_name] = {"done": 0, "total": 1, "pct": 0, "completed_sessions": 0}
            for topic in subj.get("topics", []):
                topic_slug = topic.get("id")
                if topic_slug:
                    subject_stats[subj_name]["completed_sessions"] += get_completed_sessions_count(topic_slug)

    genel_exam = datetime(2026, 9, 6)
    alan_exam = datetime(2026, 9, 12)
    now = datetime.now()

    return {
        "total_hours": total_logged,
        "today_hours": today_hours,
        "week_hours": week_hours,
        "plan_total": (plan.get("stats") or {}).get("total_hours", 0),
        "subjects": subject_stats,
        "total_questions": total_questions,
        "avg_efficiency": round(avg_efficiency, 2),
        "countdown": {
            "genel": (genel_exam - now).days,
            "alan": (alan_exam - now).days,
        },
    }


def get_plan_week():
    from app.services.plan_generator import generate_roadmap_projection
    roadmap = generate_roadmap_projection()
    weeks = roadmap.get("weeks", {})
    if not weeks:
        return {"days": []}
    today_str = datetime.now().strftime("%Y-%m-%d")
    sorted_keys = sorted(weeks.keys(), key=lambda x: int(x.replace("Hafta ", "")))
    for wk in sorted_keys:
        for day in weeks[wk]["days"]:
            if day["date"] == today_str:
                return weeks[wk]
    first_key = sorted_keys[0]
    return weeks[first_key]


def get_plan_macro():
    from app.services.plan_generator import get_macro_sprint
    return get_macro_sprint()


def get_plan_roadmap():
    from app.services.plan_generator import generate_roadmap_projection
    return generate_roadmap_projection()
def get_dashboard_today_progress():
    from datetime import datetime
    
    day_plan = get_today()
    tasks = day_plan.get("genel", []) + day_plan.get("alan", [])
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    tracker_data = get_session_subquests_raw()
    from app.services.plan_generator import generate_roadmap_projection, EXACT_ALLOCATIONS
    
    roadmap = generate_roadmap_projection()
    weeks = roadmap.get("weeks", {})
    sorted_weeks = sorted(weeks.keys(), key=lambda x: int(x.replace("Hafta ", "")))
    
    calendar_counts = {}
    found_today = False
    task_calendar_indices = []
    
    for wk in sorted_weeks:
        if found_today: break
        for day in weeks[wk]["days"]:
            day_tasks = day.get("genel", []) + day.get("alan", [])
            is_today = (day["date"] == today_str)
            for dt in day_tasks:
                d_slug = f"{slugify(dt['subject'])}-{slugify(dt['topic'])}"
                calendar_counts[d_slug] = calendar_counts.get(d_slug, 0) + 1
                if is_today:
                    task_calendar_indices.append(calendar_counts[d_slug])
            if is_today:
                found_today = True
                break

    daily_sessions = []
    for i, t in enumerate(tasks):
        slug = f"{slugify(t['subject'])}-{slugify(t['topic'])}"
        overall_idx = task_calendar_indices[i] if i < len(task_calendar_indices) else 1
        
        topic_data = tracker_data.get(slug, {"sessions": []})
        sessions = topic_data.get("sessions", [])
        
        session_data = next((s for s in sessions if s.get("session_index") == overall_idx), None)
        
        is_completed = False
        if session_data and session_data.get("subquests"):
            if all(sq.get("is_completed") for sq in session_data["subquests"]):
                is_completed = True
                
        daily_sessions.append({
            "daily_index": i + 1,
            "subject": t["subject"],
            "topic": t["topic"],
            "topic_slug": slug,
            "topic_expected": EXACT_ALLOCATIONS.get(t["topic"], 0),
            "topic_completed": get_completed_sessions_count(slug),
            "overall_session_index": overall_idx,
            "is_completed": is_completed,
            "subquests": session_data["subquests"] if session_data else []
        })
        
    return daily_sessions
