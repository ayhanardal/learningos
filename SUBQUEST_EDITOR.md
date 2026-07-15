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
            "text": "Konu anlatımı izle",
            "is_completed": false
          },
          {
            "id": "q2",
            "text": "15 soru çöz",
            "is_completed": false
          }
        ]
      }
    ]
  }
}
```

## İşlem Akışı
1. Kullanıcıdan gelen "X konusu Y oturumu için şu görevleri ekle" şeklindeki isteği al.
2. Konu adını slug formatına çevir (Örn: "Matematik Temel Kavramlar" -> `matematik-temel-kavramlar`).
3. Eğer API hazırsa `POST /api/subquests/save` üzerinden, hazır değilse `.tracker/session_subquests.json` dosyasına okuma/yazma yaparak görevleri ekle.
4. Başarıyla kaydedildiğini kullanıcıya bildir ve yeni görevlerin işlendiği JSON/veri yapısını kısaca göster.
