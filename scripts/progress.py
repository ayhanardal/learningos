#!/usr/bin/env python3
"""Çalışma ilerleme takip sistemi.

Kullanım:
  python3 progress.py status          # Son durumu göster
  python3 progress.py log <topic> <hours>  # Ders kaydet
  python3 progress.py report          # Haftalık rapor
"""

import json, sys, os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / ".tracker"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DATA_DIR / "log.json"
TOPICS_FILE = DATA_DIR / "topics_status.json"


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


def save_log(entries):
    LOG_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False))


def load_topics():
    default = {
        "turkce": {"completed": 0, "total": 40},
        "matematik": {"completed": 0, "total": 35},
        "tarih": {"completed": 0, "total": 35},
        "cografya": {"completed": 0, "total": 25},
        "vatandaslik": {"completed": 0, "total": 15},
        "istatistik": {"completed": 0, "total": 100},
    }
    if TOPICS_FILE.exists():
        data = json.loads(TOPICS_FILE.read_text())
        for k in default:
            if k in data:
                default[k].update(data[k])
        return default
    return default


def save_topics(data):
    TOPICS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_status():
    log = load_log()
    topics = load_topics()
    today = datetime.now().strftime("%Y-%m-%d")

    today_total = sum(e["hours"] for e in log if e["date"] == today)
    week_total = sum(
        e["hours"] for e in log
        if (datetime.now() - datetime.strptime(e["date"], "%Y-%m-%d")).days < 7
    )
    grand_total = sum(e["hours"] for e in log)

    print(f"=== KPSS İlerleme ({today}) ===\n")
    print(f"Bugün: {today_total:.1f} saat")
    print(f"Son 7 gün: {week_total:.1f} saat")
    print(f"Toplam: {grand_total:.1f} saat\n")

    names = {"turkce": "Türkçe", "matematik": "Matematik", "tarih": "Tarih",
             "cografya": "Coğrafya", "vatandaslik": "Vatandaşlık", "istatistik": "İstatistik"}
    print("Konu Bazında İlerleme:")
    for subj, data in sorted(topics.items()):
        pct = (data["completed"] / data["total"] * 100) if data["total"] else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        label = names.get(subj, subj.capitalize())
        print(f"  {label:15s} {bar} {data['completed']:.1f}/{data['total']}s (%{pct:.0f})")


def cmd_log(subject, hours):
    log = load_log()
    topics = load_topics()

    subject_key = subject.lower().replace("ı", "i").replace("ü", "u").replace("ö", "o").replace("ç", "c")
    # map Turkish subject names to keys
    mapping = {
        "turkce": "turkce", "türkçe": "turkce",
        "matematik": "matematik",
        "tarih": "tarih",
        "cografya": "cografya", "coğrafya": "cografya",
        "vatandaslik": "vatandaslik", "vatandaşlık": "vatandaslik",
        "istatistik": "istatistik",
    }
    key = mapping.get(subject_key, subject_key)
    if key in topics:
        topics[key]["completed"] = topics[key].get("completed", 0) + hours
        save_topics(topics)

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "subject": subject,
        "hours": hours,
    }
    log.append(entry)
    save_log(log)
    print(f"Kaydedildi: {subject} ({hours}s)")


def cmd_report():
    log = load_log()
    topics = load_topics()

    weeks = {}
    for e in log:
        d = datetime.strptime(e["date"], "%Y-%m-%d")
        wk = d.isocalendar()[1]
        year = d.year
        key = f"{year}-H{wk}"
        weeks.setdefault(key, []).append(e)

    print("=== Haftalık Rapor ===\n")
    for wk in sorted(weeks.keys()):
        entries = weeks[wk]
        total = sum(e["hours"] for e in entries)
        subjects = {}
        for e in entries:
            subjects[e["subject"]] = subjects.get(e["subject"], 0) + e["hours"]
        subj_str = " | ".join(f"{s}: {h:.1f}s" for s, h in sorted(subjects.items()))
        print(f"{wk}: {total:.1f}s → {subj_str}")

    print("\nKalan Tahmin:")
    remaining = sum(max(0, topics.get(k, {}).get("total", 0) - topics.get(k, {}).get("completed", 0))
                   for k in topics)
    print(f"  Tamamlanan: {sum(e['hours'] for e in log):.1f}s")
    print(f"  Kalan: {remaining:.1f}s")
    days_left = (datetime(2026, 9, 6) - datetime.now()).days
    if days_left > 0:
        daily_needed = remaining / max(days_left, 1)
        print(f"  Kalan gün: {days_left}")
        print(f"  Günlük ihtiyaç: {daily_needed:.1f}s")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 progress.py [status|log <konu> <saat>|report]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "status":
        cmd_status()
    elif cmd == "log" and len(sys.argv) >= 4:
        cmd_log(sys.argv[2], float(sys.argv[3]))
    elif cmd == "report":
        cmd_report()
    else:
        print("Bilinmeyen komut. Kullanım: status / log <konu> <saat> / report")
