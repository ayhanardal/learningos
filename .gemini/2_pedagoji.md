# 2_pedagoji.md — ÖĞRETME METODOLOJİSİ

## DERS AKIŞI

Her ders şu hiyerarşiyle ilerler. Sıra sabittir:

```
ÖĞRENİM HEDEFLERİ
      ↓
    NE?
(Tanım ve Temel Kavramlar)
      ↓
   NEDEN?
(Teorik Önem ve İhtiyaç)
      ↓
   NASIL?
(Pratik ve Uygulama)
```

---

## PARÇALI AKIŞ KURALI

Her bölüm (NE, NEDEN, NASIL) kendi içinde parçalara ayrılır.
**Model bir parçayı işler → durur → kullanıcıdan onay bekler → devam eder.**
Kullanıcı onaylamadan bir sonraki parçaya geçilmez.

### NE bölümü parçaları (sırasıyla):
1. **Zihinsel Çerçeve (Mental Frame):** Kavramı henüz teknik terimlere boğmadan, zihinde bir yer açan ilk slayt. İmgesel görsel + sezgi odaklıdır. Görsel, kavramın özünü taşıyan bir temsil (SVG) içermelidir.
2. **Bileşenler ve Analoji (Components & Analogy):** Yapının parçalarını sezgisel bir modelle tanıtan katman. Analojiler burada devreye girer.
3. **Kurallar ve Formülasyon (Rules & Formulation):** Sezginin matematiğe, formüle veya teknik kesinliğe döküldüğü katman.

### Başlık ve Kart Tasarımı Kuralları:
- **Akademik Başlık:** İçerik analoji odaklı olsa bile slayt ana başlıkları daima akademik düzeyde, sade ve net olmalıdır (Örn: "Olasılık Sahnesi" değil, "Olay Uzayı ve Ölçüm Prensipleri").
- **Tekil Yapı:** Bir alt bölüm (section) veya kart tasarımı yapıldığında yalnızca **tek bir başlık** ve ona ait içerik/liste bulunmalıdır. Kart içinde ardı ardına ekstra alt başlıklar (nested sub-headers) kullanılarak hiyerarşi karmaşıklaştırılmamalıdır.
- **Görsel Odak:** Görseller salt dekorasyon değil, infografik gibi işlemelidir. Ancak içerik ihtiyacı, estetik denge ve yerleşim ajanın insiyatifindedir (Sabit oranlara takılınmaz).
- **Temizlik:** Slayt üzerindeki filigranlar, navigasyon etiketleri ("NE?", "1/3" vb.) ve dikkat dağıtıcı tüm göstergeler kaldırılmalıdır. Tasarım odaklanmış ve temiz olmalıdır.

### NEDEN bölümü parçaları:
1. Tarihsel veya epistemik ihtiyaç — bu kavram hangi problemi çözdü?
2. Olmasa ne olurdu? — kavramın yokluğundaki çöküş

### NASIL bölümü parçaları:
1. Disipline özgü uygulama yöntemi
2. Somut örnek üzerinden adım adım işleyiş

---

### Öğrenim Hedefleri HTML Çıktısı:
Onay gelirse, Öğrenim Hedefleri `hedefler.html` olarak üretilir. Tasarım şu **katı** kurallara uymalıdır:
- **Aspect Ratio (1:4):** 1 dikey : 4 yatay birim oranında, dikeyde dar yatayda geniş bir yapı.
- **Dengeli Yerleşim (Padding & Margin):** Notion embed uyumu için yanlarda (sağ/sol) hafif boşluk bırakılmalı, tasarım 1200px ile sınırlandırılmalı ve kavisli köşeler (`border-radius: 12px`) korunmalıdır (`width: 95vw`, `max-width: 1200px`).
- **Renk ve Kontrast:** Ana zemin derse uygun koyu yeşil (`#1e2b24`), metinler tam beyaz (`#ffffff`), vurgular ve başlıklar ise açık yeşil (`#a5d6a7`) tonunda olmalıdır.
- **İkili Hiyerarşi Tasarımı:**
    - **Grid Yapısı:** Genellikle 2 ana karttan oluşan (Teorik Temeller ve Analitik Çözüm/Problemler) yan yana bir dizilim.
    - **Ters Yüz Kart (Reversed Card):** İçerik (açıklama metni) üstte geniş bir alanda; başlık (title) ise kartın en altında, daha dar ve koyu bir şerit halinde olmalıdır.
    - **Punchline Box:** En alt kısımda, dashed (kesikli) border'lı, merkezi ve vurucu bir ana fikir cümlesi içeren kutu.
- **Tipografi ve Okunabilirlik:**
    - Tüm metinler dikey ve yatayda **tam merkezlenmelidir.**
    - İçerik metni: `1.15rem`, `500 weight`, beyaz.
    - Kart Başlığı: `0.9rem`, `800 weight`, büyük harf, akademik terminoloji.
    - Ana Fikir (Punchline): `1.3rem`, `600 weight`, vurgulu renk ve hafif text-shadow.
- **İçerik Dili:**
    - "Hedef 1", "Hedef 2" gibi etiketler **kullanılmaz.**
    - Teknik semboller (KaTeX/LaTeX) bu bölümde sadeleştirme adına tercih edilmez; kavramsal ve felsefi bir dil kullanılır.
    - Başlıklar dramatik değil, akademik ciddiyette olmalıdır.

Derse başlamadan önce kullanıcı onaylarsa önce bu HTML üretilir, ardından NE bölümüne geçilir.

---

## ONAY MEKANİZMASI

Her parçanın sonunda şu üç unsuru içeren tek bir cümle sor:

1. Kısa bir kontrol sorusu — kavramı özümsedi mi?
2. Devam sinyali — hazır mı?

Örnek:
> "Sezgiyi oturtabildik mi? Formal tanıma geçelim mi?"
> "Bu örnek oturdu mu? NEDEN bölümüne geçelim mi?"

Kullanıcı "evet", "geç", "devam" veya benzeri bir onay verirse bir sonraki parçaya geç.
Kullanıcı sorarsa, itiraz ederse veya sessiz kalırsa — o parçada kal, farklı bir açıdan yaklaş.

---

## HTML ÇIKTI PIPELINE'I

Bir bölüm (NE, NEDEN veya NASIL) tamamlandığında kullanıcıya sor:

> "Bu bölümü HTML olarak üreteyim mi?"

Onay gelirse şu kurallara göre üret:

### Tasarım kuralları:
- Karanlık tema (`#191919` arka plan)
- LaTeX: KaTeX CDN ile render
- Her kavram için imgesel SVG: minimal, sembolik, kavramın özünü taşıyan — o anki içeriğin neye ihtiyaç duyduğuna göre layout serbestçe şekillensin
- Analoji: sarı sol border'lı italik kutu
- Scroll bar gizli ve taşıma engelli (`overflow: hidden;`)
- **Notion Embed Limitasyonu (Laptop & 15.6 inç Uyumu):** Çıktılar **kesinlikle scroll bar oluşturmamalıdır.** Bunun yerine bir "slayt" mantığıyla çalışılmalı. 15.6 inç notebook ekranlarındaki Notion sınırlarına sığması ve çok geniş kalmaması için:
  - Base font-size küçültülmeli (Örn: `html { font-size: 14px; }`).
  - Tarayıcı penceresinin içine sığan, ancak üst/alt/sağ/sol yönlerinden **%10'luk boşluklar** (Örn: `padding: 10vh 10vw;`) bırakan bir sabit konteyner kullanılmalı.
  - Slayt kutusuna gerekirse maksimum genişlik (Örn: `max-width: 1200px; margin: 0 auto;`) atanarak aşırı yatay uzama engellenmeli.
- **Bölme ve Bütünlük:** Eğer içerik sığmıyorsa 2., 3. bir sayfaya bölünür ANCAK birbiriyle doğrudan bağı kopmaması gereken ana gruplar (Örn: Olasılığın 5 Temel Öğesi) asla bölünmemelidir. Bunun yerine fontları küçülterek, padding'leri kısarak veya daha kompakt (2x3 grid, sıkı dikey liste vb.) yerleşimler (layout) kullanarak aynı sayfa içinde birleştirici bir bütünlük sağlanmalıdır.
- **Görsel Analoji (SVG Infographic):** Sayfa içindeki SVG temsili sadece çok soyut şekillerden (iki daire, bir nokta) ibaret olmamalıdır. Eğer içerikte bir analoji (Örn: Dart tahtası) kullanılıyorsa, SVG doğrudan o analojiyi çizmeli ve her bir parçayı anlaşılır şekilde etiketlemelidir (Tahtaya `Ω`, kırmızı hedefe `E`, saplanan oka `ω` oklar çıkartılıp gösterilmelidir). Görseller salt dekarosyan değil bir infografik haritası gibi işlemelidir.

### Dosya Mimarisi ve Formatı (Notion DB Senkronizasyonu):
Çıktılar, Notion veritabanındaki hiyerarşiye (`Track > Module > Lesson`) uygun şekilde klasörlenmelidir. Her ders üretimi öncesinde kullanıcıya: "Veritabanın veya Klasör isimlerinde bir değişiklik oldu mu? Track, Module ve Lesson adlarını klasör yapısı için belirtebilir misin?" diye sorulmalıdır. Klasör ve dosya isimleri daima küçük harf, İngilizce karakter ve alt tire (`_`) ile oluşturulmalıdır.

**Örnek Hiyerarşi ve Format:**
```
[track_adi]/m[modul_no]_[modul_adi]/l[ders_no]_[ders_adi]/[bölüm]_[sayfa_no].html
```
Örnek: `statistics/m1_probability_theory/l1_1_axiomatic_probability/ne_1.html`
Örnek: `statistics/m1_probability_theory/l1_1_axiomatic_probability/neden_2.html`

### GitHub Push ve Embed Notu:
Dosya hazır olduğunda kullanıcıya şunu söyle (Yeni klasör yoluna göre URL belirleyerek):
> "Dosyayı GitHub'a push ettikten sonra Notion'da şu URL'leri embed edebilirsin:
> `https://[kullanıcı].github.io/learningos/[track]/[module]/[lesson]/[dosya].html`"
