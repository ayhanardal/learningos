import os
import yaml
import random
import math
import json
from pathlib import Path
from datetime import datetime, timedelta
from app.services.data import CURRICULUM_DIR, get_progress_raw, slugify

EXACT_ALLOCATIONS = {
    "Paragrafta Anlam": 19,
    "Sözel Mantık": 7,
    "Sözcükte ve Cümlede Anlam": 5,
    "Dil Bilgisi ve Ses Olayları": 6,
    "İslamiyet Öncesi Türk Tarihi": 1,
    "İlk Türk-İslam Devletleri": 2,
    "Osmanlı Devleti Siyasi Tarihi": 4,
    "Osmanlı Kültür ve Medeniyeti": 3,
    "XX. Yüzyıl Osmanlı ve İnkılap Tarihine Giriş": 3,
    "Milli Mücadele Dönemi": 5,
    "Atatürk Dönemi ve İnkılaplar": 4,
    "Atatürk Dönemi Dış Politika ve Çağdaş": 3,
    "Temel Kavramlar ve Sayılar": 8,
    "Cebirsel İfadeler ve Denklemler": 8,
    "Oran - Orantı": 2,
    "Problemler": 13,
    "Kümeler ve Fonksiyonlar": 3,
    "P.K.O. (Saymanın Kuralları)": 3,
    "Sayısal Mantık": 4,
    "Geometri": 0,
    "Hukukun Temel Kavramları": 2,
    "Devlet Biçimleri ve Anayasa Tarihi": 1,
    "Temel Hak ve Hürriyetler": 1,
    "Yasama": 1,
    "Yürütme": 1,
    "Yargı": 1,
    "İdare Hukuku": 2,
    "Uluslararası Kuruluşlar ve Güncel Olaylar": 2,
    "Fiziki Coğrafya ve Su Örtüsü": 5,
    "Sanayi, Ulaşım, Ticaret ve Turizm": 2,
    "Madenler ve Enerji Kaynakları": 2,
    "Nüfus ve Yerleşme": 3,
    "İklim ve Bitki Örtüsü": 2,
    "Tarım, Hayvancılık ve Ormancılık": 2,
    "Türkiye'nin Coğrafi Konumu": 2,
    "Olasılık ve Stokastik Süreçler": 9,
    "Matematiksel İstatistik": 6,
    "Örnekleme": 4,
    "Uygulamalı İstatistik": 6,
    "Varyans Analizi (ANOVA)": 4,
    "Parametrik Olmayan Testler": 2,
    "Regresyon Analizi": 6,
    "Zaman Serileri": 4,
    "Çok Değişkenli Analizler": 5,
    "Yöneylem Araştırması": 0
}

FROZEN_SCHEDULE_PATH = CURRICULUM_DIR.parent / "study-plans" / "frozen-schedule.json"

GYGK_SUBJECTS = ["Matematik", "Türkçe", "Tarih", "Coğrafya", "Vatandaşlık"]
ALAN_SUBJECTS = ["İstatistik"]

def _get_subject_session_totals():
    totals = {}
    for t_name, count in EXACT_ALLOCATIONS.items():
        subj = _find_subject_for_topic(t_name)
        totals[subj] = totals.get(subj, 0) + count
    return totals

def _find_subject_for_topic(topic_name):
    for root, _, files in os.walk(CURRICULUM_DIR):
        for f in files:
            if not f.endswith(".yaml"):
                continue
            try:
                with open(Path(root) / f, encoding="utf-8") as fh:
                    subj = yaml.safe_load(fh)
            except Exception:
                continue
            if not subj or not isinstance(subj, dict):
                continue
            for t in subj.get("topics", []):
                if t.get("name") == topic_name:
                    return subj.get("subject", "")
    return ""

def _parse_all_topics():
    all_topics = {}
    for root, _, files in os.walk(CURRICULUM_DIR):
        for f in files:
            if not f.endswith(".yaml"):
                continue
            try:
                with open(Path(root) / f, encoding="utf-8") as fh:
                    subj = yaml.safe_load(fh)
            except Exception:
                continue
            if not subj or not isinstance(subj, dict):
                continue
            subject_name = subj.get("subject", "")
            topics = []
            for t in subj.get("topics", []):
                topics.append({
                    "name": t.get("name", ""),
                    "subject": subject_name,
                    "chronologicalIndex": t.get("chronologicalIndex"),
                    "isRoutine": t.get("isRoutine", False),
                    "avg_questions": t.get("avg_questions", 0),
                    "target_net": t.get("target_net", 0),
                    "allocated": EXACT_ALLOCATIONS.get(t.get("name", ""), 0)
                })
            all_topics[subject_name] = topics
    return all_topics

def _generate_frozen_schedule():
    if FROZEN_SCHEDULE_PATH.exists():
        return json.loads(FROZEN_SCHEDULE_PATH.read_text(encoding="utf-8"))

    start = datetime(2026, 7, 4)
    subject_allocations = _get_subject_session_totals()

    gygk_sequence = []
    remaining = {s: subject_allocations.get(s, 0) for s in GYGK_SUBJECTS}
    while any(remaining.values()):
        for subj in GYGK_SUBJECTS:
            amount = 2 if (subj in ["Matematik", "Türkçe"] and remaining.get(subj, 0) >= 2) else 1
            if remaining.get(subj, 0) >= amount:
                for _ in range(amount):
                    gygk_sequence.append(subj)
                remaining[subj] -= amount
            elif remaining.get(subj, 0) > 0:
                gygk_sequence.append(subj)
                remaining[subj] -= 1

    alan_total = subject_allocations.get("İstatistik", 0)

    frozen = []
    gygk_idx = 0
    alan_remaining = alan_total
    for day_idx in range(60):
        current_date = start + timedelta(days=day_idx)
        date_str = current_date.strftime("%Y-%m-%d")
        dow = current_date.weekday()
        is_alan_day = dow in [1, 3, 5]

        genel_slots = {}
        alan_slots = {}

        if is_alan_day and alan_remaining >= 2:
            alan_slots["İstatistik"] = 2
            alan_remaining -= 2
        elif is_alan_day and alan_remaining == 1:
            alan_slots["İstatistik"] = 1
            alan_remaining -= 1

        max_genel_slots = max(0, 3 - sum(alan_slots.values()))
        
        remaining_gygk = len(gygk_sequence) - gygk_idx
        remaining_days = 60 - day_idx
        
        genel_today = math.ceil(remaining_gygk / remaining_days) if remaining_days > 0 else 0
        genel_today = min(max_genel_slots, genel_today)
        if remaining_gygk > 0 and genel_today == 0 and max_genel_slots > 0:
            genel_today = 1

        count = 0
        day_subjects = []
        while count < genel_today and gygk_idx < len(gygk_sequence):
            subj = gygk_sequence[gygk_idx]
            if subj in ["Matematik", "Türkçe"] and gygk_idx + 1 < len(gygk_sequence) and gygk_sequence[gygk_idx+1] == subj:
                if count + 2 <= genel_today:
                    day_subjects.extend([subj, subj])
                    gygk_idx += 2
                    count += 2
                else:
                    day_subjects.append(subj)
                    gygk_idx += 1
                    count += 1
            else:
                day_subjects.append(subj)
                gygk_idx += 1
                count += 1
                
        for subj in day_subjects:
            genel_slots[subj] = genel_slots.get(subj, 0) + 1

        total_sessions = sum(genel_slots.values()) + sum(alan_slots.values())

        frozen.append({
            "date": date_str,
            "phase": "calisma",
            "genel_slots": genel_slots,
            "alan_slots": alan_slots,
            "total_hours": total_sessions * 1.5
        })

    FROZEN_SCHEDULE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FROZEN_SCHEDULE_PATH.write_text(json.dumps(frozen, indent=2, ensure_ascii=False))
    return frozen

def _get_target_questions(subject, topic_name, topic_data):
    avg_q = topic_data.get("avg_questions", 0)
    target_net = topic_data.get("target_net", 0)
    if subject == "Türkçe":
        target_q = int(avg_q * 3.5) if avg_q > 0 else 45
        if target_q < 45:
            target_q = 45
    else:
        target_q = int(target_net * 45) if target_net > 0 else 30
        if target_q < 15:
            target_q = 15
    return target_q

def _build_topic_queues(all_topics, raw_progress):
    queues = {}
    for subj, topics in all_topics.items():
        seq = [t for t in topics if not t["isRoutine"]]
        seq.sort(key=lambda x: x["chronologicalIndex"] if x["chronologicalIndex"] is not None else 9999)
        routines = [t for t in topics if t["isRoutine"]]

        seq_queue = []
        for t in seq:
            count = t["allocated"]
            if count > 0:
                topic_slug = f"{slugify(subj)}-{slugify(t['name'])}"
                prog = raw_progress.get(topic_slug, {})
                comp_h = prog.get("completed", 0.0)
                solved_q = prog.get("solved_questions", 0)
                target_q = _get_target_questions(subj, t["name"], t)
                total_hours = 8.0
                completed_count = max(int(comp_h / 1.5), int(solved_q / max(target_q, 1) * count)) if target_q > 0 else 0
                remaining = max(0, count - completed_count)
                seq_queue.extend([t] * remaining)

        routine_pool = []
        for t in routines:
            count = t["allocated"]
            if count > 0:
                routine_pool.extend([t] * count)

        queues[subj] = {
            "sequential": seq_queue,
            "routines": routine_pool if routine_pool else seq_queue[:1] if seq_queue else []
        }
    return queues

def _assign_topics_to_day(genel_slots, alan_slots, queues):
    genel_tasks = []
    alan_tasks = []
    used_today = set()

    for subj, count in genel_slots.items():
        q = queues.get(subj, {"sequential": [], "routines": []})
        
        topics_to_process = []
        for _ in range(count):
            has_seq = len(q["sequential"]) > 0
            has_rout = len(q["routines"]) > 0
            types_picked_today = [t.get("isRoutine", False) for t in topics_to_process if t]
            
            if has_seq and has_rout:
                if True in types_picked_today and False not in types_picked_today:
                    t = q["sequential"].pop(0)
                elif False in types_picked_today and True not in types_picked_today:
                    t = q["routines"].pop(0)
                else:
                    # Pick based on pacing (whichever has more remaining sessions to be scheduled)
                    if len(q["sequential"]) >= len(q["routines"]):
                        t = q["sequential"].pop(0)
                    else:
                        t = q["routines"].pop(0)
            elif has_seq:
                t = q["sequential"].pop(0)
            elif has_rout:
                t = q["routines"].pop(0)
            else:
                t = None
                
            topics_to_process.append(t)

        for topic in topics_to_process:
            if topic:
                topic_name = topic["name"]
                topic_slug = f"{slugify(subj)}-{slugify(topic_name)}"
                target_q = _get_target_questions(subj, topic_name, topic)
                genel_tasks.append({
                    "subject": subj,
                    "topic": topic_name,
                    "hours": 1.5,
                    "target_questions": target_q,
                    "topic_slug": topic_slug
                })
                used_today.add(topic_name)
            else:
                genel_tasks.append({
                    "subject": subj,
                    "topic": "Genel Tekrar",
                    "hours": 1.5,
                    "target_questions": 30,
                    "topic_slug": f"{slugify(subj)}-genel-tekrar"
                })

    for subj, count in alan_slots.items():
        q = queues.get(subj, {"sequential": [], "routines": []})
        
        topics_to_process = []
        for _ in range(count):
            has_seq = len(q["sequential"]) > 0
            has_rout = len(q["routines"]) > 0
            types_picked_today = [t.get("isRoutine", False) for t in topics_to_process if t]
            
            if has_seq and has_rout:
                if True in types_picked_today and False not in types_picked_today:
                    t = q["sequential"].pop(0)
                elif False in types_picked_today and True not in types_picked_today:
                    t = q["routines"].pop(0)
                else:
                    if len(q["sequential"]) >= len(q["routines"]):
                        t = q["sequential"].pop(0)
                    else:
                        t = q["routines"].pop(0)
            elif has_seq:
                t = q["sequential"].pop(0)
            elif has_rout:
                t = q["routines"].pop(0)
            else:
                t = None
                
            topics_to_process.append(t)

        for topic in topics_to_process:
            if topic:
                topic_name = topic["name"]
                topic_slug = f"{slugify(subj)}-{slugify(topic_name)}"
                target_q = _get_target_questions(subj, topic_name, topic)
                alan_tasks.append({
                    "subject": subj,
                    "topic": topic_name,
                    "hours": 1.5,
                    "target_questions": target_q,
                    "topic_slug": topic_slug
                })
            else:
                alan_tasks.append({
                    "subject": subj,
                    "topic": "Genel Tekrar",
                    "hours": 1.5,
                    "target_questions": 45,
                    "topic_slug": f"{slugify(subj)}-genel-tekrar"
                })

    return genel_tasks, alan_tasks

def generate_roadmap_projection():
    frozen = _generate_frozen_schedule()
    all_topics = _parse_all_topics()
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}

    queues = _build_topic_queues(all_topics, raw_progress)

    weeks_data = {}
    total_gygk_hours = 0.0
    total_gygk_questions = 0
    total_alan_hours = 0.0
    total_alan_questions = 0
    subject_efforts = {}

    for day_idx, day_entry in enumerate(frozen):
        genel_tasks, alan_tasks = _assign_topics_to_day(
            day_entry["genel_slots"], day_entry["alan_slots"], queues
        )

        total_hours = sum(t["hours"] for t in genel_tasks + alan_tasks)
        day_plan = {
            "date": day_entry["date"],
            "phase": day_entry.get("phase", "calisma"),
            "note": "Frozen schedule + chronologicalIndex assignment",
            "genel": genel_tasks,
            "alan": alan_tasks,
            "total_hours": round(total_hours, 2)
        }

        week_num = (day_idx // 7) + 1
        week_key = f"Hafta {week_num}"
        if week_key not in weeks_data:
            weeks_data[week_key] = {
                "days": [],
                "stats": {
                    "total_hours": 0.0,
                    "total_questions": 0,
                    "distribution": {},
                    "gygk_hours": 0.0,
                    "alan_hours": 0.0,
                    "gygk_pct": 0.0,
                    "alan_pct": 0.0,
                    "top_subjects": []
                }
            }

        weeks_data[week_key]["days"].append(day_plan)
        w_stats = weeks_data[week_key]["stats"]
        w_stats["gygk_hours"] += sum(t.get("hours", 0.0) for t in genel_tasks)
        w_stats["alan_hours"] += sum(t.get("hours", 0.0) for t in alan_tasks)
        w_stats["total_hours"] += day_plan["total_hours"]

        all_tasks = genel_tasks + alan_tasks
        for task in all_tasks:
            w_stats["total_questions"] += task.get("target_questions", 0)
            subj = task.get("subject", "Diğer")
            h = task.get("hours", 0.0)
            w_stats["distribution"][subj] = w_stats["distribution"].get(subj, 0.0) + h

        for task in genel_tasks:
            h = task.get("hours", 0.0)
            q = task.get("target_questions", 0)
            total_gygk_hours += h
            total_gygk_questions += q
            subj = task.get("subject", "Diğer")
            if subj not in subject_efforts:
                subject_efforts[subj] = {"hours": 0.0, "questions": 0}
            subject_efforts[subj]["hours"] += h
            subject_efforts[subj]["questions"] += q

        for task in alan_tasks:
            h = task.get("hours", 0.0)
            q = task.get("target_questions", 0)
            total_alan_hours += h
            total_alan_questions += q
            subj = task.get("subject", "İstatistik")
            if subj not in subject_efforts:
                subject_efforts[subj] = {"hours": 0.0, "questions": 0}
            subject_efforts[subj]["hours"] += h
            subject_efforts[subj]["questions"] += q

    for week_key, w_val in weeks_data.items():
        w_stats = w_val["stats"]
        w_stats["total_hours"] = round(w_stats["total_hours"], 2)
        w_stats["gygk_hours"] = round(w_stats["gygk_hours"], 2)
        w_stats["alan_hours"] = round(w_stats["alan_hours"], 2)
        tot = w_stats["total_hours"]
        w_stats["gygk_pct"] = round((w_stats["gygk_hours"] / tot * 100), 1) if tot > 0 else 0
        w_stats["alan_pct"] = round((w_stats["alan_hours"] / tot * 100), 1) if tot > 0 else 0

        sorted_dist = sorted(w_stats["distribution"].items(), key=lambda x: x[1], reverse=True)
        w_stats["top_subjects"] = [item[0] for item in sorted_dist[:2]]
        for subj in w_stats["distribution"]:
            w_stats["distribution"][subj] = round(w_stats["distribution"][subj], 2)

        w_val["weekly_distribution"] = {}
        for subj, h in w_stats["distribution"].items():
            q_count = 0
            for day in w_val["days"]:
                all_tasks = day.get("genel", []) + day.get("alan", [])
                for t in all_tasks:
                    if t["subject"] == subj:
                        q_count += t.get("target_questions", 0)
            pct = round((h / tot * 100), 1) if tot > 0 else 0
            w_val["weekly_distribution"][subj] = {
                "hours": h,
                "questions": q_count,
                "pct": pct
            }

    sprint_1_hours = 0.0
    sprint_1_questions = 0
    sprint_2_hours = 0.0
    sprint_2_questions = 0
    for week_key, w_val in weeks_data.items():
        week_num = int(week_key.replace("Hafta ", ""))
        if week_num <= 4:
            sprint_1_hours += w_val["stats"]["total_hours"]
            sprint_1_questions += w_val["stats"]["total_questions"]
        else:
            sprint_2_hours += w_val["stats"]["total_hours"]
            sprint_2_questions += w_val["stats"]["total_questions"]

    monthly_stats = {
        "sprint_1": {
            "name": "1. Ay (Sprint 1)",
            "weeks_range": "Hafta 1 - 4",
            "total_hours": round(sprint_1_hours, 1),
            "total_questions": sprint_1_questions
        },
        "sprint_2": {
            "name": "2. Ay (Sprint 2)",
            "weeks_range": "Hafta 5 - 9",
            "total_hours": round(sprint_2_hours, 1),
            "total_questions": sprint_2_questions
        }
    }

    total_hours = total_gygk_hours + total_alan_hours
    gygk_pct = (total_gygk_hours / total_hours * 100) if total_hours > 0 else 0
    alan_pct = (total_alan_hours / total_hours * 100) if total_hours > 0 else 0

    category_distribution = {
        "gygk": {
            "hours": round(total_gygk_hours, 1),
            "questions": total_gygk_questions,
            "pct": round(gygk_pct, 1)
        },
        "alan": {
            "hours": round(total_alan_hours, 1),
            "questions": total_alan_questions,
            "pct": round(alan_pct, 1)
        }
    }

    subject_distribution = []
    for subj, data in subject_efforts.items():
        pct = (data["hours"] / total_hours * 100) if total_hours > 0 else 0
        subject_distribution.append({
            "subject": subj,
            "hours": round(data["hours"], 1),
            "questions": data["questions"],
            "pct": round(pct, 1)
        })
    subject_distribution.sort(key=lambda x: x["hours"], reverse=True)

    return {
        "monthly_stats": monthly_stats,
        "weeks": weeks_data,
        "distribution": {
            "category": category_distribution,
            "subject": subject_distribution
        }
    }

def get_adequacy_report():
    all_topics = _parse_all_topics()
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}

    total_available = 180
    total_required = 0
    subject_requirements = {}
    bottlenecks = {}

    for subj, topics in all_topics.items():
        needed = 0
        for t in topics:
            count = t["allocated"]
            slug = f"{slugify(subj)}-{slugify(t['name'])}"
            prog = raw_progress.get(slug, {})
            comp_h = prog.get("completed", 0.0)
            solved_q = prog.get("solved_questions", 0)
            completed_count = max(int(comp_h / 1.5), int(solved_q / 45)) if solved_q > 0 else 0
            remaining = max(0, count - completed_count)
            needed += remaining
        subject_requirements[subj] = needed
        total_required += needed

    for subj, needed in subject_requirements.items():
        alloc = max(1, int(needed * (total_available / max(total_required, 1))))
        diff = needed - alloc
        if diff > 0:
            bottlenecks[subj] = diff

    adequacy_score = round((total_available / max(total_required, 1) * 100), 1) if total_required > 0 else 100.0

    return {
        "total_available_sessions": total_available,
        "total_required_sessions": total_required,
        "adequacy_score": adequacy_score,
        "subject_requirements": subject_requirements,
        "bottlenecks": bottlenecks
    }

def get_macro_sprint():
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}

    total_hours = 0.0
    completed_hours = 0.0
    total_questions = 0
    completed_questions = 0
    focus_topics = []

    for root, _, files in os.walk(CURRICULUM_DIR):
        for f in files:
            if not f.endswith(".yaml"):
                continue
            try:
                with open(Path(root) / f, encoding="utf-8") as fh:
                    subj = yaml.safe_load(fh)
            except Exception:
                continue
            if not subj or not isinstance(subj, dict):
                continue

            subject_name = subj.get("subject", "")
            for t in subj.get("topics", []):
                topic_name = t.get("name", "")
                topic_slug = f"{slugify(subject_name)}-{slugify(topic_name)}"
                chrono = t.get("chronologicalIndex")
                is_routine = t.get("isRoutine", False)

                prog = raw_progress.get(topic_slug, {})
                comp_h = prog.get("completed", 0.0)
                solved_q = prog.get("solved_questions", 0)

                avg_q = t.get("avg_questions", 0)
                target_net = t.get("target_net", 0)

                if subject_name == "Türkçe":
                    target_q = int(avg_q * 3.5) if avg_q > 0 else 45
                    if target_q < 45:
                        target_q = 45
                else:
                    target_q = int(target_net * 45) if target_net > 0 else 30
                    if target_q < 15:
                        target_q = 15

                total_hours_target = t.get("estimated_hours") or t.get("hours", 0) or 8.0
                total_hours += total_hours_target
                completed_hours += min(comp_h, total_hours_target)
                total_questions += target_q
                completed_questions += min(solved_q, target_q)

                if chrono is not None and chrono <= 5 and not is_routine:
                    focus_topics.append({
                        "subject": subject_name,
                        "topic": topic_name
                    })

    completion_pct = (completed_hours / total_hours * 100) if total_hours > 0 else 0
    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    current_month = months[datetime.now().month - 1]

    return {
        "sprint_name": f"{current_month} Sprint'i",
        "total_hours": round(total_hours, 1),
        "completed_hours": round(completed_hours, 1),
        "total_questions": total_questions,
        "completed_questions": completed_questions,
        "completion_pct": round(completion_pct, 1),
        "focus_topics": focus_topics
    }