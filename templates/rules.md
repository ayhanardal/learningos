# rules

2 kolonlu grid: sol kolon **kurallar**, sağ kolon **sorular**.

## JSON

```json
{
  "type": "rules",
  "title": "Kural Başlığı",
  "items": [
    { "html": "<p>Kural 1 açıklaması</p>" },
    { "html": "<p>Kural 2 açıklaması</p>" }
  ],
  "questionsTitle": "Örnek Sorular",
  "questions": [
    { "html": "<p>Soru metni</p>" },
    { "html": "<p>Soru metni</p>" }
  ]
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `title` | string | hayır | Sol kolon başlığı (varsayılan: "Kurallar") |
| `items[]` | array | evet | Kural kartları, her biri `html` alanı içerir |
| `items[].html` | string | evet | Kural içeriği (HTML, LaTeX) |
| `questionsTitle` | string | hayır | Sağ kolon başlığı (varsayılan: "Sorular") |
| `questions[]` | array | evet | Soru kartları, her biri `html` alanı içerir |
| `questions[].html` | string | evet | Soru içeriği (HTML, LaTeX) |

## Render

- `display: grid; grid-template-columns: 1fr 1fr`
- Her kart `border-radius: 6px`, arka plan `var(--bg)`
- LaTeX desteklenir
