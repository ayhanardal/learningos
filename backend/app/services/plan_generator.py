import os
import yaml
import random
import math
from pathlib import Path
from datetime import datetime
from app.services.data import CURRICULUM_DIR, get_progress_raw, slugify

EXACT_ALLOCATIONS = {
    # TÜRKÇE (Toplam 34 Oturum)
    "Paragrafta Anlam": 20,
    "Sözel Mantık": 7,
    "Sözcükte ve Cümlede Anlam": 5,
    "Dil Bilgisi ve Ses Olayları": 2,
    
    # TARİH (Toplam 25 Oturum)
    "İnkılap Tarihi": 15,
    "Osmanlı Devleti": 7,
    "Çağdaş Türk ve Dünya Tarihi": 2,
    "İlk Türk-İslam Devletleri": 1,
    "İslamiyet Öncesi Türk Tarihi": 0,
    
    # MATEMATİK (Toplam 38 Oturum)
    "Problemler": 13,
    "Cebir (Üslü, Köklü, Çarpanlara Ayırma)": 8,
    "Temel Kavramlar ve Rasyonel Sayılar": 8,
    "Sayısal Mantık": 6,
    "Olasılık ve İstatistik": 3,
    "Geometri": 0,
    "Kümeler ve Fonksiyonlar": 0,
    
    # VATANDAŞLIK (Toplam 11 Oturum)
    "Yasama, Yürütme ve Yargı": 5,
    "Uluslararası Kuruluşlar ve Güncel Olaylar": 4,
    "Hukukun Temel Kavramları": 2,
    "İdare Hukuku": 0,
    "Devlet Biçimleri ve Anayasa Tarihi": 0,
    
    # COĞRAFYA (Toplam 18 Oturum)
    "Fiziki Coğrafya ve Su Örtüsü": 6,
    "Sanayi, Ulaşım, Ticaret ve Turizm": 3,
    "Madenler ve Enerji Kaynakları": 3,
    "Nüfus ve Yerleşme": 2,
    "İklim ve Bitki Örtüsü": 2,
    "Tarım, Hayvancılık ve Ormancılık": 2,
    "Türkiye'nin Coğrafi Konumu": 0,
    
    # İSTATİSTİK (Toplam 52 Oturum)
    "Olasılık ve Stokastik Süreçler": 11,
    "Uygulamalı İstatistik": 8,
    "Regresyon Analizi": 8,
    "Matematiksel İstatistik": 5,
    "Varyans Analizi (ANOVA)": 5,
    "Çok Değişkenli Analizler": 5,
    "Örnekleme": 5,
    "Zaman Serileri": 5,
    "Yöneylem Araştırması": 0,
    "Parametrik Olmayan Testler": 0
}

SUBJECT_OF_TOPIC = {
    "Paragrafta Anlam": "Türkçe", "Sözel Mantık": "Türkçe", "Sözcükte ve Cümlede Anlam": "Türkçe", "Dil Bilgisi ve Ses Olayları": "Türkçe",
    "İnkılap Tarihi": "Tarih", "Osmanlı Devleti": "Tarih", "Çağdaş Türk ve Dünya Tarihi": "Tarih", "İlk Türk-İslam Devletleri": "Tarih", "İslamiyet Öncesi Türk Tarihi": "Tarih",
    "Problemler": "Matematik", "Cebir (Üslü, Köklü, Çarpanlara Ayırma)": "Matematik", "Temel Kavramlar ve Rasyonel Sayılar": "Matematik", "Sayısal Mantık": "Matematik", "Olasılık ve İstatistik": "Matematik", "Geometri": "Matematik", "Kümeler ve Fonksiyonlar": "Matematik",
    "Yasama, Yürütme ve Yargı": "Vatandaşlık", "Uluslararası Kuruluşlar ve Güncel Olaylar": "Vatandaşlık", "Hukukun Temel Kavramları": "Vatandaşlık", "İdare Hukuku": "Vatandaşlık", "Devlet Biçimleri ve Anayasa Tarihi": "Vatandaşlık",
    "Fiziki Coğrafya ve Su Örtüsü": "Coğrafya", "Sanayi, Ulaşım, Ticaret ve Turizm": "Coğrafya", "Madenler ve Enerji Kaynakları": "Coğrafya", "Nüfus ve Yerleşme": "Coğrafya", "İklim ve Bitki Örtüsü": "Coğrafya", "Tarım, Hayvancılık ve Ormancılık": "Coğrafya", "Türkiye'nin Coğrafi Konumu": "Coğrafya",
    "Olasılık ve Stokastik Süreçler": "İstatistik", "Uygulamalı İstatistik": "İstatistik", "Regresyon Analizi": "İstatistik", "Matematiksel İstatistik": "İstatistik", "Varyans Analizi (ANOVA)": "İstatistik", "Çok Değişkenli Analizler": "İstatistik", "Örnekleme": "İstatistik", "Zaman Serileri": "İstatistik", "Yöneylem Araştırması": "İstatistik", "Parametrik Olmayan Testler": "İstatistik"
}

def build_topic_queues(allocations):
    grouped = {}
    for topic, count in allocations.items():
        if count <= 0:
            continue
        subj = SUBJECT_OF_TOPIC.get(topic)
        if not subj:
            continue
        if subj not in grouped:
            grouped[subj] = {}
        grouped[subj][topic] = count
        
    queues = {}
    for subj, topics in grouped.items():
        queue = []
        counts = dict(topics)
        while sum(counts.values()) > 0:
            for topic in sorted(counts.keys(), key=lambda k: counts[k], reverse=True):
                if counts[topic] > 0:
                    queue.append(topic)
                    counts[topic] -= 1
        queues[subj] = queue
    return queues

TOPIC_ALLOCATIONS = {}

def get_deterministic_schedule():
    schedule = (
        ["İstatistik"] * 54 +
        ["Matematik"] * 45 +
        ["Türkçe"] * 36 +
        ["Tarih"] * 27 +
        ["Coğrafya"] * 12 +
        ["Vatandaşlık"] * 6
    )
    rng = random.Random(42)
    rng.shuffle(schedule)
    return schedule

def get_active_topics_for_subject(subject_name):
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}
        
    pool = []
    backup_pool = []
    completed_pool = []
    
    if not CURRICULUM_DIR.exists():
        return pool
        
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
            
            if subj.get("subject", "") != subject_name:
                continue
                
            for t in subj.get("topics", []):
                topic_name = t.get("name", "")
                topic_slug = f"{slugify(subject_name)}-{slugify(topic_name)}"
                priority = t.get("priority", "P2")
                
                prog = raw_progress.get(topic_slug, {})
                comp_h = prog.get("completed", 0.0)
                solved_q = prog.get("solved_questions", 0)
                
                avg_q = t.get("avg_questions", 0)
                
                if subject_name == "Türkçe":
                    target_q = int(avg_q * 3.5) if avg_q > 0 else 45
                    if target_q < 45:
                        target_q = 45
                else:
                    coef = 100 if priority == "P0" else (60 if priority == "P1" else 30)
                    target_net = t.get("target_net", 0)
                    if not target_net:
                        target_net = 3 if priority == "P0" else (2 if priority == "P1" else 1)
                    target_q = int(target_net * coef)
                    if target_q < 15:
                        target_q = 15
                
                total_hours_target = t.get("estimated_hours") or t.get("hours", 0) or 8.0
                is_completed = comp_h >= total_hours_target or solved_q >= target_q
                
                topic_data = {
                    "subject": subject_name,
                    "topic": topic_name,
                    "topic_slug": topic_slug,
                    "priority": priority,
                    "avg_questions": avg_q,
                    "target_questions": target_q,
                    "target_hours": 1.5,
                    "total_hours_target": total_hours_target
                }
                
                if is_completed:
                    completed_pool.append(topic_data)
                elif topic_data["priority"] in ["P0", "P1"]:
                    pool.append(topic_data)
                else:
                    backup_pool.append(topic_data)
                    
    if pool:
        return pool
    if backup_pool:
        return backup_pool
    return completed_pool if completed_pool else []

def calculate_curriculum_requirements():
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}
        
    requirements = []
    
    if not CURRICULUM_DIR.exists():
        return requirements
        
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
            is_alan = subject_name == "İstatistik"
            
            for t in subj.get("topics", []):
                topic_name = t.get("name", "")
                topic_slug = f"{slugify(subject_name)}-{slugify(topic_name)}"
                priority = t.get("priority", "P2")
                
                prog = raw_progress.get(topic_slug, {})
                comp_h = prog.get("completed", 0.0)
                solved_q = prog.get("solved_questions", 0)
                
                target_net = t.get("target_net", 0)
                if not target_net:
                    target_net = 3 if priority == "P0" else (2 if priority == "P1" else 1)
                
                if priority == "P0":
                    q_needed = target_net * 100
                elif priority == "P1":
                    q_needed = target_net * 60
                else:
                    q_needed = target_net * 30
                
                q_remaining = max(0, q_needed - solved_q)
                sessions_needed = math.ceil(q_remaining / 45)
                
                total_hours_target = t.get("estimated_hours") or t.get("hours", 0) or 8.0
                is_completed = comp_h >= total_hours_target or solved_q >= q_needed
                if is_completed:
                    sessions_needed = 0
                
                requirements.append({
                    "subject": subject_name,
                    "topic": topic_name,
                    "topic_slug": topic_slug,
                    "priority": priority,
                    "sessions_needed": sessions_needed,
                    "q_needed": q_needed,
                    "is_alan": is_alan
                })
                
    return requirements

def round_robin_mix(allocated_list):
    by_subject = {}
    for t in allocated_list:
        subj = t["subject"]
        if subj not in by_subject:
            by_subject[subj] = []
        by_subject[subj].append(t)
        
    mixed = []
    subjects = list(by_subject.keys())
    while any(by_subject[s] for s in subjects):
        for s in subjects:
            if by_subject[s]:
                mixed.append(by_subject[s].pop(0))
    return mixed

def bin_packing_roadmap():
    random.seed("learning_os_roadmap_v1")
    global TOPIC_ALLOCATIONS
    reqs = calculate_curriculum_requirements()
    
    subject_topics = {}
    for r in reqs:
        subj = r["subject"]
        if subj not in subject_topics:
            subject_topics[subj] = []
        subject_topics[subj].append(r)
        
    required_gygk = 0
    required_alan = 0
    subject_total_required = {}
    
    for subj, topics in subject_topics.items():
        needed = sum(t["sessions_needed"] for t in topics)
        subject_total_required[subj] = needed
        if topics[0]["is_alan"]:
            required_alan += needed
        else:
            required_gygk += needed
            
    gygk_scale = min(1.0, 126.0 / required_gygk) if required_gygk > 0 else 1.0
    alan_scale = min(1.0, 54.0 / required_alan) if required_alan > 0 else 1.0
    
    gygk_allocated = []
    alan_allocated = []
    bottlenecks = {}
    subject_requirements = {}
    
    for subj, topics in subject_topics.items():
        needed = subject_total_required[subj]
        subject_requirements[subj] = needed
        
        is_alan = topics[0]["is_alan"]
        scale = alan_scale if is_alan else gygk_scale
        
        if needed > 0:
            allocated_count = max(2, math.floor(needed * scale))
            if needed < 2:
                allocated_count = needed
        else:
            allocated_count = 0
            
        bottlenecks[subj] = max(0, needed - allocated_count)
        
        priority_order = {"P0": 0, "P1": 1, "P2": 2}
        topics.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        allocated_for_subj = []
        sessions_left = allocated_count
        
        for t in topics:
            if sessions_left <= 0:
                break
            t_needed = t["sessions_needed"]
            if t_needed <= 0:
                continue
            
            take = min(t_needed, sessions_left)
            allocated_for_subj.extend([t] * take)
            sessions_left -= take
            
        if sessions_left > 0 and topics:
            allocated_for_subj.extend([topics[0]] * sessions_left)
            
        if is_alan:
            alan_allocated.extend(allocated_for_subj)
        else:
            gygk_allocated.extend(allocated_for_subj)
            
    gygk_allocated = round_robin_mix(gygk_allocated)
    
    if len(gygk_allocated) > 126:
        gygk_allocated = gygk_allocated[:126]
    elif len(gygk_allocated) < 126:
        diff = 126 - len(gygk_allocated)
        gygk_topics = [t for t in reqs if not t["is_alan"]]
        if gygk_topics:
            gygk_allocated.extend([random.choice(gygk_topics) for _ in range(diff)])
        else:
            dummy = {"subject": "Matematik", "topic": "Genel Tekrar", "target_questions": 40, "topic_slug": "matematik-genel-tekrar", "is_alan": False}
            gygk_allocated.extend([dummy] * diff)
            
    if len(alan_allocated) > 54:
        alan_allocated = alan_allocated[:54]
    elif len(alan_allocated) < 54:
        diff = 54 - len(alan_allocated)
        alan_topics = [t for t in reqs if t["is_alan"]]
        if alan_topics:
            alan_allocated.extend([random.choice(alan_topics) for _ in range(diff)])
        else:
            dummy = {"subject": "İstatistik", "topic": "Genel Tekrar", "target_questions": 40, "topic_slug": "istatistik-genel-tekrar", "is_alan": True}
            alan_allocated.extend([dummy] * diff)
            
    # Ders bazlı GERÇEK oturum sayılarını bulalım (Kırpılmış nihai listeden)
    subject_allocated_counts = {}
    for t in gygk_allocated:
        subj = t["subject"]
        subject_allocated_counts[subj] = subject_allocated_counts.get(subj, 0) + 1
    for t in alan_allocated:
        subj = t["subject"]
        subject_allocated_counts[subj] = subject_allocated_counts.get(subj, 0) + 1
        
    TOPIC_ALLOCATIONS.clear()
    
    for subj, topics in subject_topics.items():
        subject_total_sessions = subject_allocated_counts.get(subj, 0)
        
        subj_total_target_net = 0
        topic_nets = []
        for t in topics:
            t_net = t.get("target_net", 0)
            if not t_net:
                t_net = 3 if t.get("priority") == "P0" else (2 if t.get("priority") == "P1" else 1)
            subj_total_target_net += t_net
            topic_nets.append((t, t_net))
            
        if subject_total_sessions > 0 and subj_total_target_net > 0:
            temp_allocations = []
            for t, t_net in topic_nets:
                alloc = round((t_net / subj_total_target_net) * subject_total_sessions)
                temp_allocations.append({"topic_slug": t["topic_slug"], "allocated": alloc, "net": t_net})
                
            current_sum = sum(x["allocated"] for x in temp_allocations)
            diff = subject_total_sessions - current_sum
            
            if diff != 0 and temp_allocations:
                max_item = max(temp_allocations, key=lambda x: x["net"])
                max_item["allocated"] = max(0, max_item["allocated"] + diff)
                
            for item in temp_allocations:
                TOPIC_ALLOCATIONS[item["topic_slug"]] = item["allocated"]
        else:
            for t in topics:
                TOPIC_ALLOCATIONS[t["topic_slug"]] = 0
                
    return {
        "gygk_allocated": gygk_allocated,
        "alan_allocated": alan_allocated,
        "bottlenecks": bottlenecks,
        "subject_requirements": subject_requirements
    }

def get_adequacy_report():
    packing = bin_packing_roadmap()
    total_available_sessions = 180
    total_required = sum(packing["subject_requirements"].values())
    adequacy_score = round((total_available_sessions / total_required * 100), 1) if total_required > 0 else 100.0
    
    return {
        "total_available_sessions": total_available_sessions,
        "total_required_sessions": total_required,
        "adequacy_score": adequacy_score,
        "subject_requirements": packing["subject_requirements"],
        "bottlenecks": packing["bottlenecks"]
    }

def pull_valid_gygk_tasks(gygk_list, start_idx, count):
    selected = []
    curr_idx = start_idx
    
    while len(selected) < count and curr_idx < len(gygk_list):
        t = gygk_list[curr_idx]
        subj = t["subject"]
        unique_subjs = set(x["subject"] for x in selected)
        
        if len(unique_subjs) < 2 or subj in unique_subjs:
            selected.append(t)
            curr_idx += 1
        else:
            found_pos = -1
            for pos in range(curr_idx + 1, len(gygk_list)):
                if gygk_list[pos]["subject"] in unique_subjs:
                    found_pos = pos
                    break
            
            if found_pos != -1:
                val = gygk_list.pop(found_pos)
                gygk_list.insert(curr_idx, val)
                selected.append(val)
                curr_idx += 1
            else:
                selected.append(t)
                curr_idx += 1
                
    selected.sort(key=lambda x: x["subject"])
    return selected, curr_idx

def generate_daily_blocks(date_str=None, day_idx=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        
    if day_idx is None:
        today = datetime.now()
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day_idx = max(0, (dt - today).days)
        
    schedule = get_deterministic_schedule()
    
    subj1 = schedule[(day_idx * 3) % 180]
    subj2 = schedule[(day_idx * 3 + 1) % 180]
    
    seed_val = sum(ord(c) for c in date_str) + day_idx
    rng = random.Random(seed_val)
    
    genel_tasks = []
    alan_tasks = []
    selected_topics = set()
    
    for subj_name in [subj1, subj2]:
        pool = get_active_topics_for_subject(subj_name)
        available = [t for t in pool if t["topic_slug"] not in selected_topics]
        if not available:
            available = pool
            
        if available:
            p0_avail = [t for t in available if t["priority"] == "P0"]
            sel_pool = p0_avail if p0_avail else available
            
            chosen = rng.choice(sel_pool)
            selected_topics.add(chosen["topic_slug"])
            
            task_data = {
                "subject": chosen["subject"],
                "topic": chosen["topic"],
                "hours": 1.5,
                "target_questions": chosen["target_questions"],
                "topic_slug": chosen["topic_slug"]
            }
            
            if subj_name == "İstatistik":
                alan_tasks.append(task_data)
            else:
                genel_tasks.append(task_data)
                
    total_hours = sum(t["hours"] for t in genel_tasks + alan_tasks)
    
    return {
        "date": date_str,
        "phase": "calisma",
        "note": "Ağırlıklı Planlama Motoru ile üretilmiştir.",
        "genel": genel_tasks,
        "alan": alan_tasks,
        "total_hours": round(total_hours, 2)
    }

def generate_weekly_projection():
    from datetime import timedelta
    projection = []
    today = datetime.now()
    for i in range(7):
        date_str = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        projection.append(generate_daily_blocks(date_str, i))
    return projection

def get_macro_sprint():
    raw_progress = get_progress_raw()
    if not isinstance(raw_progress, dict):
        raw_progress = {}

    total_hours = 0.0
    completed_hours = 0.0
    total_questions = 0
    completed_questions = 0
    focus_topics = []

    if not CURRICULUM_DIR.exists():
        return {}

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
                priority = t.get("priority", "P2")
                if priority == "P0":
                    topic_name = t.get("name", "")
                    topic_slug = f"{slugify(subject_name)}-{slugify(topic_name)}"
                    
                    prog = raw_progress.get(topic_slug, {})
                    comp_h = prog.get("completed", 0.0)
                    solved_q = prog.get("solved_questions", 0)
                    
                    avg_q = t.get("avg_questions", 0)
                    if subject_name == "Türkçe":
                        target_q = int(avg_q * 3.5) if avg_q > 0 else 45
                        if target_q < 45:
                            target_q = 45
                    else:
                        coef = 100 if priority == "P0" else (60 if priority == "P1" else 30)
                        target_net = t.get("target_net", 0)
                        if not target_net:
                            target_net = 3 if priority == "P0" else (2 if priority == "P1" else 1)
                        target_q = int(target_net * coef)
                        if target_q < 15:
                            target_q = 15
                    
                    total_hours_target = t.get("estimated_hours") or t.get("hours", 0) or 8.0
                    
                    total_hours += total_hours_target
                    completed_hours += min(comp_h, total_hours_target)
                    total_questions += target_q
                    completed_questions += min(solved_q, target_q)
                    
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

def pop_unique_topic(subj, queues, used_topics_today):
    if not queues.get(subj):
        return "Genel Tekrar"
    for i, candidate in enumerate(queues[subj]):
        if candidate not in used_topics_today:
            topic = queues[subj].pop(i)
            used_topics_today.add(topic)
            return topic
    topic = queues[subj].pop(0)
    used_topics_today.add(topic)
    return topic

def generate_roadmap_projection():
    packing = bin_packing_roadmap()
    gygk_list = packing["gygk_allocated"]
    alan_list = packing["alan_allocated"]
    
    gygk_idx = 0
    alan_idx = 0
    
    from datetime import timedelta
    today = datetime(2026, 7, 4)
    
    days_plan = []
    queues = build_topic_queues(EXACT_ALLOCATIONS)
    
    for day_idx in range(60):
        current_date = today + timedelta(days=day_idx)
        date_str = current_date.strftime("%Y-%m-%d")
        day_of_week = current_date.weekday()
        
        is_alan_day = day_of_week in [1, 3, 5]
        
        genel_tasks = []
        alan_tasks = []
        used_topics_today = set()
        
        if is_alan_day:
            if gygk_idx < len(gygk_list):
                t = gygk_list[gygk_idx]
                gygk_idx += 1
            else:
                t = {"subject": "Matematik", "topic": "Genel Tekrar", "target_questions": 40, "topic_slug": "matematik-genel-tekrar"}
                
            subj = t["subject"]
            topic = pop_unique_topic(subj, queues, used_topics_today)
            topic_slug = f"{slugify(subj)}-{slugify(topic)}"
            
            genel_tasks.append({
                "subject": subj,
                "topic": topic,
                "hours": 1.5,
                "target_questions": t.get("target_questions", 40),
                "topic_slug": topic_slug
            })
            
            for _ in range(2):
                if alan_idx < len(alan_list):
                    t = alan_list[alan_idx]
                    alan_idx += 1
                else:
                    t = {"subject": "İstatistik", "topic": "Genel Tekrar", "target_questions": 45, "topic_slug": "istatistik-genel-tekrar"}
                    
                subj = t["subject"]
                topic = pop_unique_topic(subj, queues, used_topics_today)
                topic_slug = f"{slugify(subj)}-{slugify(topic)}"
                    
                alan_tasks.append({
                    "subject": subj,
                    "topic": topic,
                    "hours": 1.5,
                    "target_questions": t.get("target_questions", 45),
                    "topic_slug": topic_slug
                })
        else:
            pulled, next_idx = pull_valid_gygk_tasks(gygk_list, gygk_idx, 3)
            gygk_idx = next_idx
            
            for t in pulled:
                subj = t["subject"]
                topic = pop_unique_topic(subj, queues, used_topics_today)
                topic_slug = f"{slugify(subj)}-{slugify(topic)}"
                
                genel_tasks.append({
                    "subject": subj,
                    "topic": topic,
                    "hours": 1.5,
                    "target_questions": t.get("target_questions", 40),
                    "topic_slug": topic_slug
                })
                
        total_hours = sum(t["hours"] for t in genel_tasks + alan_tasks)
        days_plan.append({
            "date": date_str,
            "phase": "calisma",
            "note": "Bin Packing İhtiyaç Formülü ile üretilmiştir.",
            "genel": genel_tasks,
            "alan": alan_tasks,
            "total_hours": round(total_hours, 2)
        })
        
    weeks_data = {}
    total_gygk_hours = 0.0
    total_gygk_questions = 0
    total_alan_hours = 0.0
    total_alan_questions = 0
    subject_efforts = {}

    for day_idx, day_plan in enumerate(days_plan):
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
        day_gygk_hours = sum(t.get("hours", 0.0) for t in day_plan.get("genel", []))
        day_alan_hours = sum(t.get("hours", 0.0) for t in day_plan.get("alan", []))
        w_stats["gygk_hours"] += day_gygk_hours
        w_stats["alan_hours"] += day_alan_hours
        w_stats["total_hours"] += day_gygk_hours + day_alan_hours
        
        all_tasks = (day_plan.get("genel", []) or []) + (day_plan.get("alan", []) or [])
        for task in all_tasks:
            w_stats["total_questions"] += task.get("target_questions", 0)
            
            subj = task.get("subject", "Diğer")
            h = task.get("hours", 0.0)
            w_stats["distribution"][subj] = w_stats["distribution"].get(subj, 0.0) + h

        for task in day_plan.get("genel", []):
            h = task.get("hours", 0.0)
            q = task.get("target_questions", 0)
            total_gygk_hours += h
            total_gygk_questions += q
            
            subj = task.get("subject", "Diğer")
            if subj not in subject_efforts:
                subject_efforts[subj] = {"hours": 0.0, "questions": 0}
            subject_efforts[subj]["hours"] += h
            subject_efforts[subj]["questions"] += q
            
        for task in day_plan.get("alan", []):
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
    
    distribution = {
        "category": category_distribution,
        "subject": subject_distribution
    }
    
    return {
        "monthly_stats": monthly_stats,
        "weeks": weeks_data,
        "distribution": distribution
    }
