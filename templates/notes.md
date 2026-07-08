# notes

Düz metin taktik notu. Sade ve okunabilir.

## JSON

```json
{
  "type": "notes",
  "text": "TAKTIK: Buraya taktik metni yaz.\n\n1. Madde 1\n2. Madde 2"
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `text` | string | evet | Düz metin (HTML yok, LaTeX yok). `\n` ile satır atlanır |

## Render

- `<pre style="white-space: pre-wrap">` ile gösterilir
- Satır sonları ve boşluklar korunur
- LaTeX işlenmez
