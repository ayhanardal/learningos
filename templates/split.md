# split

2 kolonlu yan yana yerleşim. Sol (`left`) ve sağ (`right`) olarak iki alt section alır.

## JSON

```json
{
  "type": "split",
  "linked": true,
  "left": {
    "type": "slide",
    "title": "KONULAR",
    "slides": [
      { "ref": "sozcuk", "key": "Sözcükte Anlam (%80)", "value": "..." },
      { "ref": "cumle", "key": "Cümlede Anlam (%90)", "value": "..." }
    ]
  },
  "right": {
    "type": "carousel",
    "questions": [
      { "ref": "sozcuk", "id": 1, "htmlContent": "..." },
      { "ref": "cumle", "id": 2, "htmlContent": "..." }
    ]
  }
}
```

## Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `left` | object | evet | Sol kolon section'ı (slide, carousel, notes, vs.) |
| `right` | object | evet | Sağ kolon section'ı |
| `linked` | boolean | hayır | `true` ise slide ↔ carousel ref bazlı filtreleme aktif |

## Linked Mode (ref ile filtreleme)

`linked: true` + `ref` alanları ile slide ve carousel bağlanır:

| Alan | Kullanım Yeri | Açıklama |
|------|---------------|----------|
| `ref` | slide `slides[]` her item'da | Slide item'ının referans anahtarı |
| `ref` | carousel `questions[]` her soruda | Sorunun hangi ref'e ait olduğu |

**Çalışma mantığı:**
- Slide ◄► ile gezinince, aktif slide item'ının `ref` değeri okunur
- Carousel'de aynı `ref`'e sahip sorular gösterilir (diğerleri gizlenir)
- Mavi etiket (tag) otomatik olarak slide item'ının `key`'inden türetilir (`(%80)` gibi kısımlar temizlenir)
- Etiket hem slide'da hem carousel'de aynı anda güncellenir

## Render

- `display: grid; grid-template-columns: 1fr 1fr; gap: 20px`
- İki kolon eşit genişlikte, üstten hizalı
- Her kolon bağımsız state'e sahiptir
- LaTeX her iki kolonda da desteklenir
