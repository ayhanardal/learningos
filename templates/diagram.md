# diagram

Renkli bilgi kutularını yatay sıralar. En fazla 4-5 kutu önerilir.

## JSON

```json
{
  "type": "diagram",
  "title": "Konu Başlığı",
  "boxes": [
    { "title": "Başlık 1", "desc": "Açıklama", "color": "#3b82f6" },
    { "title": "Başlık 2", "desc": "Açıklama", "color": "#ef4444" }
  ]
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `title` | string | evet | Başlık metni |
| `boxes[]` | array | evet | En az 1 kutu |
| `boxes[].title` | string | evet | Kutu başlığı |
| `boxes[].desc` | string | evet | Kutu açıklaması |
| `boxes[].color` | string | evet | CSS rengi (`#hex`, `rgb()`, `blue`) |

## Render

- Başlık üstte (`<h3>`)
- Kutular `display: flex` ile yan yana, eşit genişlik
- Her kutunun üstünde 4px renkli border
- LaTeX desteklenir (`$...$` / `$$...$$`)
