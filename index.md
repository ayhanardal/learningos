# KPSS Dashboard — İçerik Yönetim Sistemi

Her yeni oturumda oku ve tüm CRUD işlemlerini buraya göre yap.

---

## 1. Mimari

| Katman | Teknoloji | Detay |
|--------|-----------|-------|
| Frontend | Vanilla JS SPA | `backend/app/static/index.html` |
| Backend | FastAPI | `app/main.py`, port 8001 (Docker) |
| DB | PostgreSQL | `user_notes` tablosu (`subject` + `topic` key) |
| Curriculum | YAML | `curriculum/genel-yetenek/`, `genel-kultur/`, `alan/` |
| Çalışma | Docker | `learningos-dashboard` container, `backend/ → /app` mount |

**Önemli:** `archive/`, `scripts/`, `notes/` KPSS dışıdır, dokunma.

---

## 2. Template Şablonları

SADECE T0 (Multi-Layout) formatı kullanılır. T1/T2 kaldırıldı.

Her section `_layout[]` dizisine eklenir:
```json
{
  "_template": "interactive-v2",
  "_layout": [ { "type": "...", ... } ]
}
```

| Type | Açıklama | Şablon Dosyası |
|------|----------|----------------|
| `diagram` | Renkli bilgi kutuları | [`templates/diagram.md`](templates/diagram.md) |
| `rules` | 2 kolon: kurallar + sorular | [`templates/rules.md`](templates/rules.md) |
| `carousel` | Soru carousel (tek/çift kolon) | [`templates/carousel.md`](templates/carousel.md) |
| `slide` | Key-value slayt gösterisi | [`templates/slide.md`](templates/slide.md) |
| `notes` | Düz metin taktik notu | [`templates/notes.md`](templates/notes.md) |
| `text` | Serbest HTML | [`templates/text.md`](templates/text.md) |
| `split` | 2 yan yana section, `linked` ile ref filtreleme | [`templates/split.md`](templates/split.md) |
| `map` | Etkileşimli Türkiye haritası ve bölgesel nitelikler | [`templates/map.md`](templates/map.md) |

EditorJS blokları (T3/T4) sadece EditorJS içinde kullanılır, `_layout`'a girmez:

| Type | Açıklama | Şablon Dosyası |
|------|----------|----------------|
| `splitCard` | İki kolon: ipucu + soru | [`templates/splitcard.md`](templates/splitcard.md) |
| `slideDeck` | Görsel + madde slaytları | [`templates/slidedeck.md`](templates/slidedeck.md) |

---

## 3. LaTeX / KaTeX

`$...$` (inline) ve `$$...$$` (display) tüm section tiplerinde çalışır. Escape: `\\frac`, `\\sum`, `\\cap`, `\\cup`, `\\Omega`.

---

## 4. INTERACTIVE_TOPICS Kaydı (ZORUNLU)

Yeni konu eklerken önce frontend'e kaydet: `backend/app/static/index.html` (~satır 1028)

```javascript
const INTERACTIVE_TOPICS = {
  "Türkçe": ["Paragrafta Yapı", ...],
  ...
};
```

---

## 5. CRUD İşlemleri

### CREATE / UPDATE (upsert)
```bash
curl -X POST http://localhost:8001/api/notes \
  -H "Content-Type: application/json" \
  -d '{"subject":"...","topic":"...","content":{JSON}}'
```

### READ
```bash
curl -s "http://localhost:8001/api/notes?subject=...&topic=..."
```

### DELETE
```bash
docker exec -i learningos-db psql -U learningos -d learningos \
  -c "DELETE FROM user_notes WHERE subject='...' AND topic='...';"
```

### LIST
```bash
docker exec -i learningos-db psql -U learningos -d learningos \
  -c "SELECT subject, topic FROM user_notes;"
```

---

## 6. Workflow

1. Curriculum YAML'da konu var mı kontrol et
2. `INTERACTIVE_TOPICS`'e yoksa ekle
3. T0 formatında JSON oluştur (section tipleri için `templates/*.md`'e bak)
4. `POST /api/notes` ile kaydet
5. `GET /api/notes` ile doğrula

Güncelleme: GET ile mevcut içeriği oku → güncelle → POST.

---

## 7. Kritik Uyarılar

- `saveWorkspaceNote()` sadece localStorage'a yazar. KULLANMA.
- SADECE `saveInteractiveNote()` backend'e yazılır.
- Docker container restart gerekmez (bind mount).
- `--reload` Python dosyalarında otomatik restart yapar.

---

## 8. Not Alma Rehberi ve Ders Standartları

Her dersin not alma stilini, kullanılan şablon türlerini ve pedagojik yaklaşım standartlarını [NOT_ALMA_REHBERI.md](NOT_ALMA_REHBERI.md) dosyasından takip et. Yeni içerik üretirken bu kılavuza sadık kal.

---

## 9. Geliştirme Kuralları ve Tasarım İzolasyonu

- **Konu İsimlendirme Tutarlılığı (Veri Kaybı Önleme):** Konu isimleri, müfredat YAML dosyaları (`turkce.yaml` vb.), veritabanı `topic` kolonu ve `INTERACTIVE_TOPICS` listesi ile birebir eşleşmelidir. Konu adlarında yapılacak en ufak harf/karakter değişikliği (örn: `Paragrafta Anlam` yerine `Paragrafta Yapı` yazılması) veritabanındaki not verilerine erişimin tamamen kopmasına neden olur.
- **Bileşen Seviyesinde İzolasyon (Global Tasarım Çökmelerini Önleme):** Arayüz monolitik bir yapıda (`index.html` içinde) geliştirilmiştir. Yapılan görsel tasarımlar kesinlikle global CSS kuralları ile ezilmemelidir. Tasarım değişiklikleri sadece ilgili şablon fonksiyonunun ürettiği HTML etiketlerinde inline stillerle veya spesifik sınıf seçicileriyle sınırlandırılmalıdır. Aksi takdirde, bir konunun tasarımı güncellenirken diğer tüm sayfaların ölçek ve yerleşim yapısı bozulur.
- **Global Tasarım Değişikliği ve Kullanıcı Onayı:** Sistem genelini veya diğer sayfaları etkileyecek herhangi bir global tasarım/arayüz değişikliği yapılmadan önce **kesinlikle kullanıcıdan onay alınmalıdır.** 
- **Global Tasarım Değişikliği Talebi Kısıtı:** Genel kural olarak, sistemde global tasarım değişiklikleri **istenmeyecektir**. Ajanlar kendiliğinden veya dolaylı olarak global arayüz kurallarını değiştirmeye kalkışmamalı, her geliştirme talebini sadece ilgili sayfa/bileşen kapsamında izole bir şekilde çözmelidir.
