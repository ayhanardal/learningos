---
name: subquest-editor
description: "Kullanıcının verdiği komutlara göre konuların oturumları için alt görevler (subquests) oluşturur."
---

# Subquest Editor Skill

Bu yetenek, KPSS Dashboard sisteminde konuların oturumları için "Alt Görevler (Subquests)" oluşturmak amacıyla kullanılır. Gerçek ilerleme (Actual Progress), ancak bir oturumun tüm alt görevleri tamamlandığında artar.

## Kullanım Amacı
Kullanıcı bir konuya çalışmaya başlayacağında, o anki oturum için yapılması gereken görevleri (örneğin: video izle, 15 soru çöz, not çıkar vb.) sana söyler. Sen de bu bilgileri alıp `.tracker/session_subquests.json` dosyasına (veya ilgili API'ye) doğru bir JSON formatında kaydedersin.

## Beklenen JSON Yapısı
Kayıtların tutulacağı şema aşağıdaki gibi olmalıdır:

```json
{
  "ders-konu-slug": {
    "sessions": [
      {
        "session_index": 1,
        "subquests": [
          {
            "id": "q1",
            "title": "Paragrafta Yapı",
            "text": "Konu anlatımı izle",
            "label": "alt konu",
            "is_completed": false
          },
          {
            "id": "q2",
            "title": "Soru Çözümü",
            "text": "15 soru çöz",
            "label": "soru",
            "value": 15,
            "is_completed": false
          }
        ]
      }
    ]
  }
}
```

## İşlem Akışı
1. Kullanıcıdan gelen isteği analiz et. İhtiyaca göre tekil veya toplu (batch) işlem yapabilirsin:
   - **Tekil Ekleme:** "X konusu Y oturumu için şu görevleri ekle."
   - **Konu Bazlı Toplu Ekleme:** "Şu konunun tüm oturumlarına şu görevi ekle."
   - **Genel Toplu Ekleme:** "Mevcut tüm derslerin tüm oturumlarına şu görevi (örn: Not edinmek) ekle."
2. Konu adını slug formatına çevir (Örn: "Matematik Temel Kavramlar" -> `matematik-temel-kavramlar`).
3. Toplu ekleme istenmişse:
   - Eğer sadece belirli bir konu (slug) hedef alınmışsa, o konunun `sessions` dizisindeki tüm mevcut oturumlara belirtilen alt görevi (`id` benzersiz olacak şekilde) ekle.
   - Eğer tüm oturumlar hedef alınmışsa, `.tracker/session_subquests.json` dosyasındaki tüm anahtarlarda (konularda) bulunan tüm oturumlara (sessions) belirtilen alt görevi ekle.
4. Dosyaya yazma işlemini tamamla (`.tracker/session_subquests.json` dosyasını doğrudan güncelle).
5. Başarıyla kaydedildiğini kullanıcıya bildir ve hangi konulara/oturumlara hangi görevlerin eklendiğini kısaca özetle.
