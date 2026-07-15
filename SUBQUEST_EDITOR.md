---
name: subquest-editor
description: "Kullanıcının verdiği komutlara göre konuların oturumları için alt görevler (subquests) oluşturur."
---

# Subquest Editor Skill

Bu yetenek, KPSS Dashboard sisteminde konuların oturumları için "Alt Görevler (Subquests)" oluşturmak amacıyla kullanılır. Gerçek ilerleme (Actual Progress), ancak bir oturumun tüm alt görevleri tamamlandığında artar.

## Temel Strateji ve Kompakt Şablonlar
Subquest'ler uzun cümleler yerine **kısa, emir kipli ve kompakt** olmalıdır. "Sıfırdan Öğrenme" (Tip 1) oturumları için standart kronolojik şablonumuz aşağıdaki gibidir:
1. `[hatırlatıcı] İlerleme Kontrolü`: Eksik (beklenen) oturum var mı kontrol et.
2. `[keşif] Kaynak Tespiti`: Videoları bul, sayılarını/sürelerini hesapla.
3. `[planlama] Video Taraması`: Tahta silinme sıklığına göre slayt sayısını belirle, duraklama noktalarını (milestone) not al.
4. `[teori] İnteraktif Tüketim`: Videoyu izle, milestone'larda durup dijital slayt (page) notlarını tasarla.
5. `[kontrol] Son İnceleme`: Oluşturulan tüm notları son kez tara.

## Beklenen JSON Yapısı
Kayıtların tutulacağı şema aşağıdaki gibi olmalıdır. İhtiyaç halinde görevlerin altına `sub_items` dizisi ile kırılım eklenebilir:

```json
{
  "ders-konu-slug": {
    "sessions": [
      {
        "session_index": 1,
        "subquests": [
          {
            "id": "sq_1",
            "title": "Kaynak Tespiti",
            "text": "Mevcut konu için videoları listele.",
            "label": "keşif",
            "sub_items": [
              "Konuyla ilgili videoları bul.",
              "Video süreleri hesapla (Oturuma sığar mı?)"
            ],
            "is_completed": false
          }
        ]
      }
    ]
  }
}
```

## İşlem Akışı
1. Kullanıcıdan gelen isteği analiz et. İhtiyaca göre tekil veya toplu (batch) işlem yapabilirsin.
2. Konu adını slug formatına çevir (Örn: "Matematik Temel Kavramlar" -> `matematik-temel-kavramlar`).
3. Toplu ekleme istenmişse:
   - Eğer sadece belirli bir konu (slug) hedef alınmışsa, o konunun `sessions` dizisindeki tüm mevcut oturumlara belirtilen alt görevi (`id` benzersiz olacak şekilde) ekle.
   - Eğer tüm oturumlar hedef alınmışsa, `.tracker/session_subquests.json` dosyasındaki tüm anahtarlarda (konularda) bulunan tüm oturumlara (sessions) belirtilen alt görevi ekle.
4. Dosyaya yazma işlemini tamamla (`.tracker/session_subquests.json` dosyasını doğrudan güncelle).
5. Başarıyla kaydedildiğini kullanıcıya bildir ve hangi konulara/oturumlara hangi görevlerin eklendiğini kısaca özetle.
