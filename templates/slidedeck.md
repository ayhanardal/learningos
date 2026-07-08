# slideDeck (T4)

EditorJS bloğu — sadece EditorJS içinde kullanılır, `_layout` dizisine girmez. Slayt gösterisi: görsel alanı + madde işaretleri.

## JSON (EditorJS block data)

```json
{
  "type": "slideDeck",
  "data": {
    "title": "Slayt Başlığı",
    "slides": [
      {
        "imagePlaceholder": "Görsel etiketi",
        "bullets": ["Hap bilgi 1", "Hap bilgi 2"]
      },
      {
        "imagePlaceholder": "Görsel etiketi",
        "bullets": ["Hap bilgi 1"]
      }
    ]
  }
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `title` | string | evet | Slayt başlığı (üstte kalın) |
| `slides[]` | array | evet | En az 1 slayt |
| `slides[].imagePlaceholder` | string | hayır | Görsel alanında gösterilen etiket (henüz gerçek görsel yok) |
| `slides[].bullets[]` | string[] | evet | Madde işaretli liste |

## Render

- Beyaz zemin, gölge, yuvarlak köşeler
- Üstte başlık + ◄► navigasyon
- İçerik: sol görsel alanı (kesik border, gri zemin) + sağ madde listesi
- LaTeX desteklenir
