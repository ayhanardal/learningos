# Slide Şablonu (Slayt & Kart Bileşeni)

Bu şablon, etkileşimli çalışma alanında estetik slaytlar veya dikey kart grupları oluşturmak için kullanılır. HTML ve LaTeX desteğine sahiptir.

---

## 🤖 Yapay Zeka Asistanı İçin Talimatlar (Agent Instructions)

Bu şablonu kullanarak yeni bir konu içeriği veya slayt paneli oluşturmak istediğinde, **kullanıcıya başka hiçbir şey yapmadan önce mutlaka aşağıdaki soruları sorarak onay almalısın**:

1.  **Yerleşim Türü:** *"Görsel + İçerik (image + content) şeklinde 3 kolonlu bir yapı mı olsun, yoksa sadece İçerik (only content) mi barındırsın?"*
2.  **Akış Tarzı:** *"Slaytlar arasında yön butonlarıyla mı gezinilsin, yoksa kartlar dikey olarak alt alta mı sıralansın (Stacked mod)?"*
3.  **Tipbox (Tooltip) Desteği:** *"İçerikteki kritik kelimeler için fareyle üzerine gelindiğinde açılan Tipbox (Bilgi Kutucuğu) özelliği ekleyelim mi?"*

Kullanıcının kararlarına göre aşağıdaki hazır alt şablon yapılarından (JSON) birini üretmelisin.

---

## 📋 Alt Şablon JSON Yapıları

### 1. Şablon: Görsel + Metin (3 Kolonlu Yapı)
Sol tarafta dosya yükleyici/görsel, sağında ise yan yana 2 adet detaylı madde kolonu oluşturur.
```json
{
  "type": "slide",
  "tag": "BAŞLIK (ÖRN: TÜRKİYE'NİN MUTLAK KONUMU)",
  "slides": [
    {
      "key": "", 
      "image": "", 
      "items": [
        {
          "label": "1. Sütun Başlığı",
          "text": "<ul><li>Detaylı madde 1...</li><li>Detaylı madde 2...</li></ul>"
        },
        {
          "label": "2. Sütun Başlığı",
          "text": "<ul><li>Detaylı madde 1...</li><li>Detaylı madde 2...</li></ul>"
        }
      ]
    }
  ]
}
```

### 2. Şablon: Stacked Dikey Kartlar (Keyword : Desc Yapısı)
Header'ı gizler, slayt geçiş tuşlarını kaldırır ve kartları yan yana "Terim | Açıklama" olacak şekilde dikeyde alt alta ortalanmış olarak dizer.
```json
{
  "type": "slide",
  "stack": true,
  "slides": [
    {
      "key": "Terim / Kavram 1",
      "value": "Kavramın detaylı açıklaması buraya yazılır."
    },
    {
      "key": "Terim / Kavram 2",
      "value": "Kavramın detaylı açıklaması buraya yazılır."
    }
  ]
}
```

### 3. Şablon: Sadece Görsel Yükleme Alanı (Metinsiz)
```json
{
  "type": "slide",
  "tag": "BÖLGELER VE NİTELİKLERİ",
  "slides": [
    {
      "image": ""
    }
  ]
}
```

---

## 💡 Tipbox (Tooltip) Özelliğinin Kullanımı
Eğer kullanıcı **Tipbox** özelliği isterse veya kritik terimlerin derin detaylarını gizli tutmak istersen, `value` veya `items[].text` alanlarındaki kelimeleri şu HTML etiketiyle sarmalamalısın:

```html
<span class="app-tooltip" data-tooltip="Bilgi kutucuğunda belirecek olan açıklama metni.">Kritik Terim</span>
```

---

## 🛠 Alan Detayları

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `type` | string | Evet | Her zaman `"slide"` olmalıdır. |
| `tag` | string | Hayır | Üstteki kibar mavi renkli başlık alanıdır. |
| `stack` | boolean | Hayır | `true` ise slayt geçiş tuşları kalkar, tüm slaytlar dikey kartlar olarak alt alta listelenir. |
| `slides[].key` | string | Hayır | Büyük üst başlık (çizgili). Orijinal kartlarda anahtar kelime sütunudur. |
| `slides[].image` | string | Hayır | Resmin sunucudaki statik URL'idir. Boş bırakılırsa dosya seçici gösterilir. |
| `slides[].value` | string | Hayır | Tek kolonlu veya Stacked moddaki açıklama içeriğidir. |
| `slides[].items` | array | Hayır | Çok kolonlu slayt maddelerini barındırır. |
