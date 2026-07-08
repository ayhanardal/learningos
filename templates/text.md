# text

Serbest HTML bölümü. Her türlü HTML içeriği koyulabilir.

## JSON

```json
{
  "type": "text",
  "html": "<p>Serbest HTML içerik</p><ul><li>Madde 1</li><li>Madde 2</li></ul>"
}
```

Alternatif alan adı:

```json
{
  "type": "text",
  "content": "<p>İçerik buraya</p>"
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `html` | string | hayır* | HTML içerik |
| `content` | string | hayır* | Alternatif alan adı |

\* `html` veya `content`'ten en az biri zorunlu. Öncelik `html` > `content`.

## Render

- Arka plan `var(--surface)`, border, 8px radius
- Doğrudan `innerHTML` ile basılır
- LaTeX desteklenir
