# splitCard (T3)

EditorJS bloğu — sadece EditorJS içinde kullanılır, `_layout` dizisine girmez. İki kolon: sol ipuçları, sağ sorular.

## JSON (EditorJS block data)

```json
{
  "type": "splitCard",
  "data": {
    "tips": ["İpucu 1", "İpucu 2"],
    "questions": [
      {
        "tag": "Konu Etiketi",
        "question": "Soru kökü?",
        "options": ["A) Seçenek 1", "B) Seçenek 2", "C) Seçenek 3", "D) Seçenek 4", "E) Seçenek 5"]
      }
    ]
  }
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `tips[]` | string[] | evet | Sol kolon ipuçları (◄► ile gezin) |
| `questions[]` | array | evet | Sağ kolon soruları (◄► ile gezin) |
| `questions[].tag` | string | evet | Konu/etiket (küçük gri badge) |
| `questions[].question` | string | evet | Soru kökü metni |
| `questions[].options[]` | string[] | evet | 5 seçenek (A-E) |

## Render

- `display: flex; flex-direction: row; gap: 40px`
- Sol: ipuçları kartı, ◄► navigasyon
- Sağ: soru kartı, seçenekler, ◄► navigasyon
- Beyaz zemin, gölge, yuvarlak köşeler
- Her iki kolon bağımsız gezinir
- LaTeX desteklenir (`renderMath`)
