# İçerik Üretme/Yönetme Kılavuzu

## Mimari Özet

- **Frontend:** Tek sayfa (`backend/app/static/index.html`), Vanilla JS, EditorJS
- **Backend:** FastAPI, Postgres DB (`/api/notes` endpoint)
- **İçerik Depolama:** Postgres DB'de `UserNote` tablosu (`subject` + `topic` key)

---

## 1. İçerik Türleri

### A. Interactive Study View (Önerilen)
Görsel diyagram + soru carousel'i + taktik notları. Backend'e kaydedilir, otomatik yüklenir.

### B. Regular EditorJS (Standart Not)
Sadece localStorage'a kaydedilir. **Tavsiye edilmez** çünkü backend'e kaydedilmez.

---

## 2. Yeni Konuyu Interactive Yapma

Herhangi bir konuyu interactive yapmak için 2 adım:

### Adım 1: Frontend'de kayıt
`backend/app/static/index.html` dosyasında `INTERACTIVE_TOPICS` sabitine konuyu ekle:

```javascript
const INTERACTIVE_TOPICS = {
    "Türkçe": ["Paragrafta Yapı", "Sözcükte ve Cümlede Anlam", "YENI_KONU"],
    "Matematik": ["Problemler", "YENI_KONU"],
    "Tarih": ["YENI_KONU"],
    "Coğrafya": ["YENI_KONU"],
    "Vatandaşlık": ["YENI_KONU"],
    "İstatistik": ["YENI_KONU"]
};
```

### Adım 2: İçeriği backend'e POST et

```bash
curl -X POST http://localhost:8001/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "DersAdı",
    "topic": "KonuAdı",
    "content": {
      "_template": "interactive-v1",
      "diagram": { ... },
      "carousel": { ... },
      "notes": { "text": "..." }
    }
  }'
```

---

## 3. Interactive Content JSON Formatı

```json
{
  "_template": "interactive-v1",
  "diagram": {
    "title": "Görsel başlık",
    "boxes": [
      {
        "title": "Kutu başlığı",
        "desc": "Kutu açıklaması",
        "color": "#hexrenk"
      }
    ]
  },
  "carousel": {
    "activeIndex": 0,
    "questions": [
      {
        "id": 1,
        "htmlContent": "<b>Soru metni</b><br>Cevap: ...<br>Açıklama: ..."
      }
    ]
  },
  "notes": {
    "text": "Taktik notları..."
  }
}
```

---

## 4. İçerik Güncelleme

Aynı `subject` + `topic` kombinasyonuyla tekrar POST yap. Backend mevcut kaydı bulup üzerine yazar (upsert).

```bash
curl -X POST http://localhost:8001/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Türkçe",
    "topic": "Sözcükte ve Cümlede Anlam",
    "content": { GUNCEL_ICEERK }
  }'
```

---

## 5. İçerik Silme

Database'e doğrudan müdahale gerekir. Postgres'e bağlanıp:

```bash
docker exec -it learningos-db psql -U learningos -d learningos -c "DELETE FROM user_notes WHERE subject='Türkçe' AND topic='Sözcükte ve Cümlede Anlam';"
```

---

## 6. Doğrulama

İçerik kaydedildikten sonra kontrol:

```bash
# GET ile kontrol
curl -s "http://localhost:8001/api/notes?subject=DersAdı&topic=KonuAdı" | python3 -m json.tool

# Yapıyı özetle
curl -s "http://localhost:8001/api/notes?subject=Türkçe&topic=Sözcükte ve Cümlede Anlam" | python3 -c "
import json, sys
data = json.load(sys.stdin)
c = data['content']
print('Template:', c.get('_template'))
print('Questions:', len(c.get('carousel',{}).get('questions',[])))
print('OK')
"
```

---

## 7. Gerektiğinde Yapılacaklar

| İşlem | Ne yapmalı |
|-------|-----------|
| Yeni konu ekleme | `INTERACTIVE_TOPICS` + `POST /api/notes` |
| İçerik güncelleme | `POST /api/notes` (aynı subject+topic) |
| İçerik silme | `docker exec ... DELETE FROM user_notes` |
| İçerik okuma | `GET /api/notes?subject=...&topic=...` |
| Yeni ders (subject) ekleme | Önce curriculum YAML'ı + `INTERACTIVE_TOPICS`'e dersi ekle |

---

## 8. Test Edilmiş Örnek

**Ders:** Türkçe
**Konu:** Sözcükte ve Cümlede Anlam
**Durum:** ✅ Çalışıyor (5 soru, 3 kutulu diyagram, taktik notları)
**Endpoint:** `POST /api/notes` ile kaydedildi, `GET /api/notes?subject=Türkçe&topic=Sözcükte ve Cümlede Anlam` ile doğrulandı.
