# Unit (Seperatör) Şablonu

Bu şablon, etkileşimli çalışma alanında üniteleri veya ana bölümleri birbirinden ayırmak için kullanılan, sayfayı yatayda %100 kaplayan şık koyu tema bir seperatör şerididir.

---

## 🤖 Yapay Zeka Asistanı İçin Talimatlar (Agent Instructions)

Kullanıcı yeni bir ünite geçişi veya ana konu ayrımı istediğinde bu şablonu (JSON) en başa veya ilgili bölümlerin arasına yerleştirmelisin.

---

## 📋 JSON Yapısı

```json
{
  "type": "unit",
  "title": "ÜNİTE - 1",
  "subtitle": "Temel Konum Kavramları ve Türkiye"
}
```

---

## 🎨 Tasarım Standartları
*   **Arka Plan:** Koyu Slate gradyanı (`linear-gradient(90deg, #0f172a 0%, #1e293b 100%)`).
*   **Yatay Genişlik:** `%100` tam genişlik (`margin: 12px -80px; width: calc(100% + 160px)`).
*   **Yükseklik:** İnce ve zarif (`min-height: 48px`).
*   **Ayraç:** Ana ve alt başlık arasında yarı saydam şık dikey bir çizgi bulunur.

---

## 🛠 Alan Detayları

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `type` | string | Evet | Her zaman `"unit"` veya `"separator"` olmalıdır. |
| `title` | string | Evet | Sol yanda büyük harflerle, kalın beyaz (`#f8fafc`) olarak yazılacak ana başlık (örn: `"ÜNİTE - 1"`). |
| `subtitle` | string | Hayır | Sağ tarafta dikey çizgiden sonra çelik mavisi (`#94a3b8`) tonda görünecek açıklayıcı alt başlık. |
