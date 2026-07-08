# Carousel Şablonları

İki tip carousel oluşturma seçeneği vardır. İhtiyacınıza uygun olan yapıyı seçip doğrudan kullanın.

---

## Seçenek 1: Tek Kolon (Tam Genişlik)

Sarmalayıcı container'ın tam genişliğini (%100) kaplayacak şekilde render edilir. Split layout içinde veya tek başına kullanıldığında bulunduğu kolonu tamamen doldurur. Boşluksuz ve temiz bir yerleşim sunar.

```json
{
  "type": "carousel",
  "tag": "ETİKET / KONU BAŞLIĞI",
  "questions": [
    {
      "id": 1,
      "htmlContent": "<b>Soru 1:</b> Soru metni buraya gelecek...<br><br>A) Şık 1<br>B) Şık 2<br>C) Şık 3<br>D) Şık 4<br>E) Şık 5<br><br><b>Cevap:</b> X (Açıklama)"
    },
    {
      "id": 2,
      "htmlContent": "<b>Soru 2:</b> Diğer soru metni...<br><br>A) ...<br>B) ...<br>C) ...<br>D) ...<br>E) ...<br><br><b>Cevap:</b> Y"
    }
  ]
}
```

---

## Seçenek 2: Çift Kolon (ÖSYM Kitapçık Modu)

Sayfayı ortadan dikey şeftali rengi (`#fcd5b4`) bir ayraç çizgisi ile ikiye böler. Sorular tek bir `questions` dizisinde toplanır. Navigasyon senkronize çalışır (Sayfa çevirme mantığı):
- **Sayfa 1'de:** Sol tarafta 1. Soru (questions[0]), sağ tarafta 2. Soru (questions[1]) gösterilir.
- **Sayfa 2'de:** Sol tarafta 3. Soru (questions[2]), sağ tarafta 4. Soru (questions[3]) gösterilir.

Bu modun aktif olması için `"doubleColumn": true` parametresi zorunludur.

```json
{
  "type": "carousel",
  "doubleColumn": true,
  "tag": "SINAV KİTAPÇIĞI BAŞLIĞI",
  "questions": [
    {
      "id": 1,
      "htmlContent": "<b>Soru 1:</b> Sol kolonda ilk gösterilecek soru...<br><br>A) ...<br>B) ...<br>C) ...<br>D) ...<br>E) ...<br><br><b>Cevap:</b> X"
    },
    {
      "id": 2,
      "htmlContent": "<b>Soru 2:</b> Sağ kolonda ilk gösterilecek soru...<br><br>A) ...<br>B) ...<br>C) ...<br>D) ...<br>E) ...<br><br><b>Cevap:</b> Y"
    },
    {
      "id": 3,
      "htmlContent": "<b>Soru 3:</b> Sayfa değiştirilince sol kolonda çıkacak soru...<br><br>A) ...<br>B) ...<br>C) ...<br>D) ...<br>E) ...<br><br><b>Cevap:</b> Z"
    },
    {
      "id": 4,
      "htmlContent": "<b>Soru 4:</b> Sayfa değiştirilince sağ kolonda çıkacak soru...<br><br>A) ...<br>B) ...<br>C) ...<br>D) ...<br>E) ...<br><br><b>Cevap:</b> W"
    }
  ]
}
```

---

## Kurallar ve Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `type` | string | evet | Sadece `"carousel"` olmalıdır. |
| `doubleColumn` | boolean | hayır | Çift kolon (ÖSYM kitapçık) modunu açmak için `true` verilmelidir. |
| `tag` | string | hayır | Sağ üst köşedeki minimalist navigasyon alanının yanında görünecek başlık. |
| `questions[]` | array | evet | Soru nesnelerini içeren dizi. |
| `questions[].id` | number | hayır | Soru numarası. |
| `questions[].htmlContent` | string | evet | HTML ve LaTeX destekleyen soru ve cevap içeriği. |
| `questions[].ref` | string | linked için evet | `split` layout ile kullanıldığında filtreleme anahtarı. |
