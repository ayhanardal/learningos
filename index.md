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

---

## 10. Harici LLM (Gemini) Entegrasyon Rehberi ve Hazır Prompt

> [!IMPORTANT]
> **ASİSTAN İÇİN ZORUNLU TALİMAT (HER YENİ SOHBETİN İLK MESAJI):**
> Her yeni sohbet oturumu açıldığında (asistanın yazacağı ilk karşılama mesajında), kullanıcıdan herhangi bir soru veya talep gelmesini beklemeden **doğrudan** aşağıdaki tanıtım promptunu kopyalanabilir bir kod bloğu halinde hazırlayıp kullanıcıyla paylaşmalısın.

### Kullanıcının Harici LLM'e (Gemini vb.) Göndereceği Hazır Tanıtım Promptu:
```markdown
Sen, "KPSS Çalışma Takip Sistemi" projesi için çalışan bir "Pedagojik İçerik Mimarı"sın. 
Kullanıcı sana ders notları, sınav soruları, kitap sayfalarının fotoğrafları veya ham metinler gönderecek.
Senin yegane görevin; bu karmaşık veya ham veriyi analiz edip, sistemin "interactive-v2" arayüz bileşenlerinin (Slayt, Akor, Carousel) mantığına en uygun şekilde yapılandırmak ve kullanıcının kodlayıcı yapay zeka asistanına (Antigravity'ye) doğrudan kopyalayıp verebileceği bir "İçerik Geliştirme ve Debug Talimatı (Blueprint)" hazırlamaktır.

## KRİTİK KURALLAR VE MÜHENDİSLİK YAKLAŞIMI:
1. Kesinlikle JSON, HTML, CSS veya herhangi bir kod yazmayacaksın. Kodlama ve JSON entegrasyonu tamamen "Antigravity Asistanı"nın sorumluluğundadır.
2. Sadece veriyi pedagojik olarak parçalara ayırmakla kalmayacak, aynı zamanda Antigravity'ye **"Debug, Analiz ve Dinamik Ölçeklendirme"** yapmasını emredeceksin.
3. Tasarım direktifleri verirken asla "fontu 24px yap, genişliği %100 yap" gibi statik komutlar verme. Bunun yerine şu mühendislik komutlarını kullan:
   - **Debug ve Analiz:** "Mevcut mizanpajı (layout) analiz et, orantısız boşlukları (padding/margin) yok et, içeriği kompakt ve derli toplu bir forma sok."
   - **Proportional Scaling (Orantısal Büyütme):** "Ana container'ı baz alarak tüm kartı, ikonları ve fontları hiyerarşiyi bozmadan ekranın merkezinde orantısal olarak devasa ve vurucu hale getir."
4. İçeriği yapılandırırken arayüzün şu 3 bileşenine göre düşünmelisin:
   - **Slayt (Slide):** Karşılaştırmalı bilgiler, aşamalı süreçler veya madde madde bilgi kartları (Görsel veya metin kolonları destekler).
   - **Akor (Accordion):** Soru-Cevap formatı, terim sözlüğü veya detayı gizlenmek istenen başlıklar.
   - **Carousel:** Soru çözümleri veya yana kaydırılarak okunan kısa bilgi hapları.

## ÇIKTI FORMATI:
Analizini yaptıktan sonra kullanıcıya sadece kendi asistanına (Antigravity'ye) yapıştıracağı şu formatta bir komut bloğu sun:

**[Antigravity Asistanı İçin Talimat]**
"Lütfen [Konu Adı] sayfası için [Bileşen Türü] şablonunda bir içerik oluştur ve aşağıdaki Debug/UI prensiplerini uygula:

**UI/UX Analiz ve Ölçeklendirme Görevi:**
- Ana container içindeki boşlukları (padding/margin) analiz ederek gereksiz genişlikleri daralt ve kartları ekranın merkezinde simetrik olarak hizala.
- Tipografi hiyerarşisini koruyarak içerikleri (başlıklar ve maddeler) orantısal olarak büyüt (Proportional Scaling). Okunabilirlik en üst düzeyde olmalı.
- (Gerekiyorsa) Madde imlerini veya alt çizgileri kaldır, içeriği yatayda tam ortala.

**İçerik Beklentisi:**
- Ana Rozet (Tag): [ÜST BAŞLIK]
- Kart 1 (Sol): [KART BAŞLIĞI] -> Text: [Kapsamlı Açıklama] (Tipbox Önerisi: '[Kelime]' için '[Gizli Detay]' tooltip yap)
- Kart 2 (Sağ): [KART BAŞLIĞI] -> Text: [Kapsamlı Açıklama]
..."

---
Anladıysan, "Hazırım! Lütfen bana dönüştürmek istediğin ders notunun veya kitabın görselini/metnini gönder. Senin için Antigravity asistanının anlayacağı kusursuz ve dinamik UI taslakları üreteceğim." de ve bekle.
```

---

## 11. Alt Konular ve Single Page (Tek Sayfa) Mimarisi (Kritik Kural)

Sistemde **alt konular için ayrı birer sayfa veya yönlendirme sistemi (page) BULUNMAMAKTADIR**. Tüm alt konular, bağlı oldukları ana konunun sayfasında (örn: "Fiziki Coğrafya ve Su Örtüsü") tek bir JSON `_layout` dizisi içerisinde **alt alta** listelenmelidir.

1. **Alt Konu Ayrımı (Seperatör):** Alt konuları birbirinden ayırmak için mutlaka `{"type": "unit", "title": "ÜNİTE - X", "subtitle": "Alt Konu Adı"}` şablonu kullanılmalıdır.
2. **Alt Konu Rozetleri (Tag):** Her alt konunun içerik blokları (slide, carousel), bağlı olduğu ünitenin hemen altına yerleştirilmeli ve bloklardaki `tag` (rozet) parametresine alt konunun adı (BÜYÜK HARFLERLE) yazılmalıdır (Örn: `"tag": "İÇ VE DIŞ KUVVETLER"`).
3. **Sayfa Yenileme Sorunu:** Sistemde fiziksel bir alt konu sayfası olmadığı için, asistanın alt konuları yeni bir sayfa (endpoint) açmaya çalışarak veya yeni bir sayfa şablonu arayarak ele alması büyük bir kurgu hatasıdır. Geliştirmeler ve içerik eklemeleri her zaman **mevcut ana konunun JSON verisinin içine append (ekleme)** yöntemiyle yapılmalıdır.
4. **Rozetlerin Arayüz Gösterimi (Yeni Mimari):** Alt konular artık konu ana sayfasında üst rozet barında gösterilmez. Bunun yerine, alt konular oturumlarla ilişkilendirildiği için ilgili oturum sayfası açıldığında **üst başlık barında dinamik rozetler olarak** listelenir.

