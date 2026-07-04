#!/usr/bin/env python3
"""KPSS 60 Günlük Çalışma Planı Oluşturucu - Data-driven, configurable."""

import yaml, json, os
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CURRICULUM_DIR = BASE_DIR / "curriculum"
OUTPUT_DIR = BASE_DIR / "study-plans"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CONFIG = {
    "start_date": "2026-07-03",
    "genel_exam": "2026-09-06",
    "alan_exam": "2026-09-12",
    "hours_per_day": 7,
    "break_every": 6,
    "system_build_days": 2,
    "mock_exam_interval_days": 10,
}

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def load_curriculum():
    subjects = []
    for root, _, files in os.walk(CURRICULUM_DIR):
        for f in files:
            if f.endswith(".yaml"):
                path = Path(root) / f
                with open(path) as fh:
                    data = yaml.safe_load(fh)
                    data["_source"] = str(path.relative_to(CURRICULUM_DIR))
                    subjects.append(data)
    return subjects


def generate(subjects):
    start = datetime.strptime(CONFIG["start_date"], "%Y-%m-%d")
    genel_exam = datetime.strptime(CONFIG["genel_exam"], "%Y-%m-%d")
    alan_exam = datetime.strptime(CONFIG["alan_exam"], "%Y-%m-%d")
    total_days = (alan_exam - start).days
    genel_days = (genel_exam - start).days

    genel_subjects = [s for s in subjects if s.get("exam") in ("genel-yetenek", "genel-kultur")]
    alan_subjects = [s for s in subjects if s.get("exam") == "alan"]

    genel_hours = sum(s["total_estimated_hours"] for s in genel_subjects)
    alan_hours = sum(s["total_estimated_hours"] for s in alan_subjects)
    total_hours = genel_hours + alan_hours

    sb = CONFIG["system_build_days"]
    study_days = total_days - sb
    daily_genel = genel_hours / study_days if study_days > 0 else 0
    daily_alan = alan_hours / study_days if study_days > 0 else 0

    plan = []
    mock_date = start + timedelta(days=sb + CONFIG["mock_exam_interval_days"])

    def normalize_topic(t, subject, exam):
        h = t.get("estimated_hours") or t.get("hours", 0)
        return {**t, "subject": subject, "exam": exam, "hours": h}

    genel_topics = []
    for s in sorted(genel_subjects, key=lambda x: PRIORITY_ORDER.get(x.get("priority", "P2"))):
        for t in s["topics"]:
            genel_topics.append(normalize_topic(t, s["subject"], s["exam"]))

    alan_topics = []
    for s in sorted(alan_subjects, key=lambda x: PRIORITY_ORDER.get(x.get("priority", "P2"))):
        for t in s["topics"]:
            alan_topics.append(normalize_topic(t, s["subject"], s["exam"]))

    gi, ai = 0, 0
    genel_remaining_hours = {t["subject"] + "|" + t["name"]: t["hours"] for t in genel_topics}
    alan_remaining_hours = {t["subject"] + "|" + t["name"]: t["hours"] for t in alan_topics}

    def pick_topic(pool, remaining, idx):
        if not pool or idx >= len(pool):
            return None, idx
        key = pool[idx]["subject"] + "|" + pool[idx]["name"]
        if remaining.get(key, 0) <= 0:
            return None, idx + 1
        return pool[idx], idx

    mock_count = 0

    for day_offset in range(total_days):
        date = start + timedelta(days=day_offset)
        day_num = day_offset + 1
        is_break = (day_offset >= sb) and ((day_offset - sb) % CONFIG["break_every"] == CONFIG["break_every"] - 1)
        is_system_phase = day_offset < sb

        entry = {
            "day": day_num,
            "date": date.strftime("%Y-%m-%d"),
            "weekday": date.strftime("%A"),
            "phase": "sistem-kurulumu" if is_system_phase else "calisma",
            "genel": [],
            "alan": [],
            "total_hours": 0,
            "mock_exam": False,
            "note": "",
        }

        if is_break and not is_system_phase:
            entry["phase"] = "dinlenme"
            entry["note"] = "Dinlenme günü - tekrar ve eksik konular"
            plan.append(entry)
            continue

        if not is_system_phase and date >= mock_date:
            entry["mock_exam"] = True
            mock_count += 1
            entry["note"] = f"Deneme Sınavı #{mock_count}"
            mock_date = date + timedelta(days=CONFIG["mock_exam_interval_days"])
            plan.append(entry)
            continue

        if is_system_phase:
            tasks = []
            if day_offset == 0:
                tasks.append({"subject": "Sistem Kurulumu", "topic": "Müfredat yapılandırması", "hours": 2})
            elif day_offset == 1:
                tasks.append({"subject": "Sistem Kurulumu", "topic": "Çalışma planı oluşturma + kaynak düzeni", "hours": 2})
            entry["genel"] = tasks
            entry["total_hours"] = 2
            plan.append(entry)
            continue

        genel_hours_today = 0
        alan_hours_today = 0

        while genel_hours_today < daily_genel and any(v > 0 for v in genel_remaining_hours.values()):
            topic, gi = pick_topic(genel_topics, genel_remaining_hours, gi)
            if not topic:
                gi = 0
                topic, gi = pick_topic(genel_topics, genel_remaining_hours, gi)
            if not topic:
                break
            key = topic["subject"] + "|" + topic["name"]
            avail = min(topic["hours"], genel_remaining_hours.get(key, 0))
            assign = min(avail, daily_genel - genel_hours_today)
            if assign <= 0:
                break
            genel_remaining_hours[key] -= assign
            genel_hours_today += assign
            entry["genel"].append({"subject": topic["subject"], "topic": topic["name"], "hours": round(assign, 1)})

        while alan_hours_today < daily_alan and any(v > 0 for v in alan_remaining_hours.values()):
            topic, ai = pick_topic(alan_topics, alan_remaining_hours, ai)
            if not topic:
                ai = 0
                topic, ai = pick_topic(alan_topics, alan_remaining_hours, ai)
            if not topic:
                break
            key = topic["subject"] + "|" + topic["name"]
            avail = min(topic["hours"], alan_remaining_hours.get(key, 0))
            assign = min(avail, daily_alan - alan_hours_today)
            if assign <= 0:
                break
            alan_remaining_hours[key] -= assign
            alan_hours_today += assign
            entry["alan"].append({"subject": topic["subject"], "topic": topic["name"], "hours": round(assign, 1)})

        entry["total_hours"] = round(genel_hours_today + alan_hours_today, 1)
        plan.append(entry)

    return plan, {"genel_hours": genel_hours, "alan_hours": alan_hours, "total_hours": total_hours, "study_days": study_days}


def render_markdown(plan, stats):
    lines = []
    lines.append("# KPSS Çalışma Planı\n")
    lines.append(f"- **Başlangıç:** {CONFIG['start_date']}")
    lines.append(f"- **Genel Kültür-Yetenek Sınavı:** {CONFIG['genel_exam']} ({(datetime.strptime(CONFIG['genel_exam'], '%Y-%m-%d') - datetime.strptime(CONFIG['start_date'], '%Y-%m-%d')).days} gün)")
    lines.append(f"- **Alan Bilgisi (İstatistik) Sınavı:** {CONFIG['alan_exam']} ({(datetime.strptime(CONFIG['alan_exam'], '%Y-%m-%d') - datetime.strptime(CONFIG['start_date'], '%Y-%m-%d')).days} gün)")
    lines.append(f"- **Toplam Ders Saati:** Genel {stats['genel_hours']}s + Alan {stats['alan_hours']}s = {stats['total_hours']}s")
    lines.append(f"- **Günlük Ortalama:** ~{CONFIG['hours_per_day']} saat")
    lines.append("")

    for entry in plan:
        lines.append(f"## Gün {entry['day']} — {entry['date']} ({entry['weekday']})")
        phase_icons = {"sistem-kurulumu": "🔧", "calisma": "📖", "dinlenme": "☕"}
        lines.append(f"**{phase_icons.get(entry['phase'], '📌')} {entry['phase'].upper()}**")

        if entry["note"]:
            lines.append(f"> {entry['note']}")

        if entry["genel"]:
            lines.append("\n### Genel Kültür-Yetenek")
            for t in entry["genel"]:
                lines.append(f"  - {t['subject']} — {t['topic']} ({t['hours']}s)")

        if entry["alan"]:
            lines.append("\n### Alan Bilgisi (İstatistik)")
            for t in entry["alan"]:
                lines.append(f"  - {t['subject']} — {t['topic']} ({t['hours']}s)")

        if entry["mock_exam"]:
            lines.append("  ⏱ Deneme sınavı + analiz")

        lines.append(f"\n  `Toplam: {entry['total_hours']} saat`\n")
        lines.append("---\n")

    return "\n".join(lines)


def render_json(plan, stats):
    return json.dumps({"config": CONFIG, "stats": stats, "plan": plan}, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    subjects = load_curriculum()
    print(f"Loaded {len(subjects)} curriculum files:")
    for s in subjects:
        print(f"  - {s['subject']} ({s['exam']}) — {s['total_estimated_hours']}s")
    print()

    plan, stats = generate(subjects)

    md = render_markdown(plan, stats)
    md_path = OUTPUT_DIR / "60-gunluk-plan.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"Markdown plan: {md_path}")

    js = render_json(plan, stats)
    js_path = OUTPUT_DIR / "60-gunluk-plan.json"
    js_path.write_text(js, encoding="utf-8")
    print(f"JSON plan: {js_path}")

    print(f"\nStats: Genel {stats['genel_hours']}s + Alan {stats['alan_hours']}s = {stats['total_hours']}s")
    print(f"Planlanan gün: {len(plan)} gün")
