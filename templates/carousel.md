# carousel

Soru carousel — ◄► ile sorular arasında gezin. İki modu vardır: **tek kolon** (standart) ve **çift kolon** (yan yana 2 carousel).

## Tek Kolon (standart)

```json
{
  "type": "carousel",
  "questions": [
    { "ref": "anahtar", "id": 1, "htmlContent": "<b>Soru</b><br>A) ...<br><br>Cevap: X" }
  ]
}
```

## Çift Kolon (yan yana)

```json
{
  "type": "carousel",
  "columns": [
    {
      "title": "Sol Kolon",
      "questions": [
        { "id": 1, "htmlContent": "..." }
      ]
    },
    {
      "title": "Sağ Kolon",
      "questions": [
        { "id": 2, "htmlContent": "..." }
      ]
    }
  ]
}
```

## Alanlar

### Tek kolon

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `questions[]` | array | evet | Soru listesi |
| `questions[].id` | number | hayır | Soru numarası |
| `questions[].htmlContent` | string | evet | Soru içeriği (HTML, LaTeX) |
| `questions[].ref` | string | linked için evet | `split` + `linked: true` ile filtreleme anahtarı |

### Çift kolon

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `columns[]` | array | evet | 2 adet kolon objesi |
| `columns[].title` | string | hayır | Kolon başlığı (uppercase gösterilir) |
| `columns[].questions[]` | array | evet | Her kolon kendi soru listesine sahiptir |
| `columns[].questions[].htmlContent` | string | evet | Soru içeriği |

## Linked Mode (split ile)

`split` içinde `linked: true` ile kullanılınca:
- Sorular `ref` alanına göre filtrelenir
- Slide'da konu değişince carousel otomatik güncellenir
- Mavi etiket (`#carousel-tag-{idx}`) slide'daki aktif konuyu gösterir
- Carousel içinde ◄► ile sadece filtrelenmiş sorular arasında gezinilir

## Render

- Beyaz zemin, ince border, hafif gölge. Mavi etiket (`#carousel-tag`) dinamik
- `columns` varsa `display: grid; grid-template-columns: 1fr 1fr` ile yan yana
- Her kolonun bağımsız ◄▶ navigasyonu vardır
- LaTeX desteklenir

## Navigasyon

`changeMultiCarousel(sectionIdx, direction)` — filtrelenmiş sorular arasında gezinir.
