# Statik / Etkileşimsiz Türkiye Haritası (map)

Türkiye'nin 7 coğrafi bölgesini SVG harita üzerinde doğrudan kendi statik renkleriyle görselleştirmek için kullanılır. Herhangi bir tıklama olayı (interaktivite) veya yan bilgi paneli barındırmaz; harita kartı sarmalayıcı panelin (workspace panel) tam yarısı kadar en kaplayacak şekilde (`width: 50%; max-width: 50%;`) sola hizalı render edilir. Çalışma paneli sayfanın %50'sini (yarısını) kapladığından, harita da bu panelin yarısını kaplayarak sayfanın çeyreği oranında şık ve dengeli bir görünüm sunar. Bölgeler için opsiyonel olarak sağ üst, sol üst veya sol alt köşede devasa, gölgeli ve yan yana/alt alta sıralanabilen hap (pill/badge) biçiminde özel etiketler atanabilir.

---

## JSON Formatı

```json
{
  "type": "map",
  "title": "TÜRKİYE COĞRAFİ BÖLGELERİ VE BÖLGESEL NİTELİKLER",
  "regions": [
    {
      "name": "Marmara Bölgesi",
      "color": "#3b82f6",
      "badge": ["Alçak", "Zengin", "Kalabalık"]
    },
    {
      "name": "Karadeniz Bölgesi",
      "color": "#06b6d4",
      "badge": "Ters"
    }
  ]
}
```

---

## Alanlar ve Açıklamalar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `type` | string | evet | Sadece `"map"` olmalıdır. |
| `title` | string | hayır | Kartın en üstünde gösterilecek büyük başlık (ÖSYM kitapçık stili). |
| `regions[]` | array | evet | Harita üzerinde renk ve etiket atanacak bölgelerin listesi. |
| `regions[].name` | string | evet | Bölgenin SVG verisindeki tam adı. `Marmara Bölgesi`, `Ege Bölgesi`, `Akdeniz Bölgesi`, `Karadeniz Bölgesi`, `İç Anadolu Bölgesi`, `Doğu Anadolu Bölgesi`, `Güneydoğu Anadolu Bölgesi` olmalıdır. |
| `regions[].color` | string | hayır | Bölgenin harita üzerinde boyanacağı statik HEX renk kodu (varsayılan: `#cbd5e0`). |
| `regions[].badge` | string veya array | hayır | Bölge isminin sağ üst köşesinde gösterilecek hap biçimli etiket(ler). Tekil etiket için string (`"Karstik"`), çoklu etiket için dizi (`["Alçak", "Zengin", "Kalabalık"]`) olarak gönderilebilir. Çoklu etiketler yan yana şık bir şekilde sıralanır. |

---

## Davranış ve Render Özellikleri

- **Yarı Genişlik Sol Düzen:** Sağ taraftaki yan panel tamamen kaldırılmıştır. Harita kartı sarmalayıcı container'ın yarısını kaplayacak biçimde (`width: 50%`) sola yaslı (`margin-right: auto`) render edilir.
- **Sıfır İnteraktivite:** Bölge tıklama (click) olayları ve hover efektleri tamamen kaldırılmıştır. Harita salt okunur, statik ve sade bir grafik şeması olarak davranır.
- **Dinamik Yönelimli Büyük Hap Etiketler (Badge):** Eğer `badge` alanı tanımlanmışsa, ilgili bölgenin `dir` yönelimine göre (`left-up`, `left-down`, `right-up`, `right-down`), metnin bitişinden biraz uzak ve yüksek kontrastlı (büyük boyutta 16px bold metin, `#e11d48` kırmızı zemin, 36px dev yükseklik ve hafif gölgeli) bir veya birden fazla hap dikey olarak alt alta çizilir.
