# KPSS LearningOS Sistemi

## Mimari

```
learningos/
├── curriculum/                     # Data-driven müfredat (YAML)
│   ├── genel-yetenek/turkce.yaml   # 40 saat
│   ├── genel-yetenek/matematik.yaml # 35 saat
│   ├── genel-kultur/tarih.yaml     # 35 saat
│   ├── genel-kultur/cografya.yaml  # 25 saat
│   ├── genel-kultur/vatandaslik.yaml # 15 saat
│   └── alan/istatistik.yaml        # 100 saat (KPSS Alan)
│
├── scripts/
│   ├── plan_generator.py           # YAML'den 71 günlük plan üretir
│   └── progress.py                 # CLI ile çalışma takibi
│
├── study-plans/
│   └── 60-gunluk-plan.json         # Plan çıktısı (dashboard okur)
│
├── .tracker/
│   ├── log.json                    # Saat bazlı log kayıtları
│   └── topics_status.json          # Konu bazında tamamlanan saat
│
└── backend/                        # FastAPI + Docker
    ├── Dockerfile
    ├── pyproject.toml
    └── app/
        ├── main.py                 # FastAPI uygulama
        ├── api/routes/dashboard.py # API endpoints
        ├── services/data.py        # JSON dosya I/O
        └── static/index.html       # Dashboard frontend
```

## Akış

### 1. Müfredat Tanımı (YAML)
Her ders için bir YAML dosyası:
```yaml
subject: Türkçe
exam: genel-yetenek
total_estimated_hours: 40
priority: P1
topics:
  - name: Sözcükte Anlam
    hours: 3
    subtopics: [Sözcük Anlamı, Deyimler, Söz Sanatları]
  - name: Paragraf
    hours: 12
    subtopics: [Yapı, Anlatım, Düşünce]
```

### 2. Plan Generator (Python)
- Tüm YAML dosyalarını okur
- Toplam 250 saat (Genel 150s + Alan 100s)
- 71 güne dağıtır (2 gün sistem kurulumu + 69 çalışma günü)
- Her 10 günde bir deneme sınavı
- Her 6 günde bir dinlenme günü
- Öncelik sırası: P0(İstatistik) > P1(Türkçe, Matematik) > P2(Tarih, Coğrafya) > P3(Vatandaşlık)
- Çıktı: JSON + Markdown

### 3. Dashboard (FastAPI + Docker)
- Port 8001'de çalışır
- API endpoints:
  - `GET /api/stats` — geri sayım, saat istatistikleri
  - `GET /api/today` — bugünün ders programı
  - `GET /api/plan` — 71 günlük planın tamamı
  - `GET /api/progress` — konu bazında ilerleme
  - `POST /api/log` — çalışma kaydet
- Frontend: tek HTML sayfa, Vanilla JS, dark tema
- Her 30 saniyede bir otomatik güncellenir
- Haftalık takvim, tıklanabilir gün detayları

### 4. Progress Tracker (Python CLI)
```bash
python3 scripts/progress.py status   # Durum göster
python3 scripts/progress.py log "Türkçe" 2  # Kayıt ekle
python3 scripts/progress.py report   # Haftalık rapor
```

## Önemli Prensipler
- **Data-driven:** Müfredat YAML'de, kod değil
- **Self-contained:** JSON dosyalar üzerinden çalışır, DB yok
- **Dockerized:** `docker compose up -d` ile tek komutta ayağa kalkar
- **AgentOS entegre:** AgentOS API'si üzerinden karar/issue/session kaydı tutulur

## Sınav Takvimi
- **Genel Sınav:** 6 Eylül 2026 (Pazar) — Türkçe + Matematik + Tarih + Coğrafya + Vatandaşlık
- **Alan Sınavı:** 12 Eylül 2026 (Cumartesi) — İstatistik
