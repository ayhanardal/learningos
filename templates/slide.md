# slide

Key-value slayt gösterisi. ◄► ile slaytlar arasında gezin. ÖSYM tarzı beyaz arka plan.

## JSON

```json
{
  "type": "slide",
  "title": "BÖLÜM BAŞLIĞI",
  "slides": [
    {
      "ref": "anahtar",
      "key": "Terim / Kavram",
      "value": "Açıklama metni. HTML ve LaTeX desteklenir. $$P(A) = \\frac{|A|}{|\\Omega|}$$"
    }
  ]
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `title` | string | hayır | Üstte gri uppercase başlık |
| `slides[]` | array | evet | En az 1 slayt |
| `slides[].ref` | string | linked için evet | `split` + `linked: true` ile kullanılır. Carousel filtreleme anahtarı |
| `slides[].key` | string | evet | Kalın büyük başlık (22px). Aynı zamanda etiket metni olarak kullanılır (`(%80)` temizlenir) |
| `slides[].value` | string | evet | Açıklama metni (15px, justify). HTML/LaTeX destekler |

## Render

- Beyaz zemin, ince border, hafif gölge. Mavi etiket (`#slide-tag-{idx}`) otomatik eklenir
- `split` + `linked` modunda etiket dinamiktir — slide gezinince güncellenir
- Key büyük ve kalın (22px, `#1a1a1a`)
- İnce ayraç çizgisi
- Value justify, max 640px genişlik, ortalanmış
- LaTeX desteklenir

## Navigasyon

`changeSlide(sectionIdx, direction)` — slide'ı değiştirir, `split` + `linked` ise carousel filtresini ve etiketleri otomatik günceller.
