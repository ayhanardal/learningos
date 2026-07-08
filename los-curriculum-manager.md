# los-curriculum-manager

## Yetenek Tanımı

Müfredat (JSON/YAML) verilerindeki konular arasında **oturum (session) transferi** yapar, konulara
`chronologicalIndex` (int) ve `isRoutine` (bool) anahtarlarını enjekte eder.
Tüm işlemler **zero-sum** (sıfır-toplam) güvencesi altında çalışır.

---

## Mevcut Durum Analizi

### Veri Katmanı (YAML şeması)

Her ders bir `.yaml` dosyasında tanımlıdır:

| Alan | Tür | Açıklama |
|------|-----|----------|
| `subject` | string | Ders adı (örn. Coğrafya) |
| `exam` | string | Sınav kategorisi (genel-yetenek, genel-kultur, alan) |
| `total_questions` | int | Dersteki toplam soru sayısı |
| `target_net` | int | Dersteki hedef net sayısı |
| `topics[]` | array | Konu listesi |

Her konu objesi:

| Alan | Tür | Açıklama |
|------|-----|----------|
| `name` | string | Konu adı |
| `avg_questions` | int | Ortalama çıkan soru sayısı |
| `target_net` | int | Bu konudaki hedef net |
| `priority` | string | Legacy P0/P1/P2 (kullanımdan kalkacak) |
| `isRoutine` | bool | Routine (tekrarlı) konu mu? |
| `chronologicalIndex` | int | Kronolojik sıralama indeksi |
| `subtopics[]` | array | Alt konu listesi |

### Planlama Katmanı (`plan_generator.py`)

Oturum tahsisi iki aşamalı çalışır:

**1. Statik Tahsis (`EXACT_ALLOCATIONS`):**
```python
EXACT_ALLOCATIONS = {
    "Fiziki Coğrafya ve Su Örtüsü": 5,   # 5 oturum
    "Türkiye'nin Coğrafi Konumu": 2,     # 2 oturum
    # ... tüm konular için manuel tanım
}
```
Her konuya sabit sayıda oturum atanır. Toplam: Coğrafya = 18 oturum.

**2. Dinamik Tahsis (`bin_packing_roadmap`):**
- `calculate_curriculum_requirements()` ile her konunun ihtiyaç duyduğu oturum sayısı hesaplanır.
- Hesaplama formülü: `target_net * katsayı / 45`
  - P0: `target_net * 100`
  - P1: `target_net * 60`
  - P2: `target_net * 30`
- 180 oturumluk kapasite (126 GY-GK + 54 Alan) üzerinden bin-packing yapılır.

### Mevcut Önceliklendirme Sorunu

| Konu | Soru | Hedef Net | Priority | Sorun |
|------|------|-----------|----------|-------|
| Türkiye'nin Coğrafi Konumu | 1 | 0 | P2 | Temel konu, 0 net hedefi yüzünden P2, oturum alamıyor |
| Fiziki Coğrafya | 5 | 4 | P0 | Yüksek net hedefi sayesinde P0, 5 oturum alıyor |
| Geometri | 3 | 0 | P2 | 0 net hedefi, tamamen dışlanıyor |
| Paragrafta Anlam | 16 | 13 | P0 | Zaten routine+bol soru, P0 etiketi gereksiz |

**Temel sorun:** Priority etiketi (`P0/P1/P2`) aslında `target_net` değerinin bir fonksiyonu haline gelmiş.
Az soru çıkan ama temel olan konular (`Türkiye'nin Coğrafi Konumu`, `Geometri`) düşük `target_net`
yüzünden P2 etiketi alıp plan dışı kalıyor.

---

## Mimarisi

### Zero-Sum (Sıfır-Toplam) Sigortası

```
İşlem Öncesi Toplam Oturum = İşlem Sonrası Toplam Oturum
```

Her transfer işlemi öncesi/sonrası toplam oturum sayısı karşılaştırılır.
Eşitlik sağlanamazsa işlem iptal edilir ve hata fırlatılır.

```
Örnek:
Eski Toplam: 18
Transfer: Fiziki Coğrafya -1, Türkiye'nin Coğrafi Konumu +1
Yeni Toplam: 18
Güvenlik doğrulaması GEÇTİ.
```

### Oturum Veri Modeli

Her konu için oturum bilgisi iki kaynaktan gelir:

1. **Static:** `EXACT_ALLOCATIONS` -> `allocated_sessions` (data.py:271)
2. **Dynamic:** `bin_packing_roadmap()` -> `TOPIC_ALLOCATIONS` (plan_generator.py:427)

`index.html`'de görüntülenen: `t.allocated_sessions` (statik EXACT_ALLOCATIONS değeri)

### Anahtar Enjeksiyonu

Her konuya şu anahtarlar eklenebilir/güncellenebilir:

| Anahtar | Tip | Varsayılan | Açıklama |
|---------|-----|------------|----------|
| `chronologicalIndex` | int | `null` | Konunun işlenme sırası (1 = ilk, N = son) |
| `isRoutine` | bool | `false` | Routine (tekrarlı/günlük) konu mu? |

---

## Komutlar

### `transfer`

İki konu arasında oturum taşıma.

```
transfer --source "Fiziki Coğrafya ve Su Örtüsü" --source-ders Coğrafya
         --target "Türkiye'nin Coğrafi Konumu"   --target-ders Coğrafya
         --amount 1
         --dry-run
```

| Parametre | Zorunlu | Açıklama |
|-----------|---------|----------|
| `--source` | evet | Kaynak konu adı |
| `--source-ders` | evet | Kaynak konunun dersi |
| `--target` | evet | Hedef konu adı |
| `--target-ders` | hayır | Varsayılan: source ile aynı |
| `--amount` | evet | Transfer edilecek oturum sayısı (pozitif tam sayı) |
| `--dry-run` | hayır | Simülasyon modu (fiziksel yazma yapmaz) |

### `inject`

Tek bir konuya `chronologicalIndex` ve/veya `isRoutine` ata.

```
inject --ders Coğrafya --konu "Türkiye'nin Coğrafi Konumu"
       --chronological-index 1
       --dry-run
```

| Parametre | Zorunlu | Açıklama |
|-----------|---------|----------|
| `--ders` | evet | Ders adı |
| `--konu` | evet | Konu adı |
| `--chronological-index` | hayır | int değer (null gönderilirse silinir) |
| `--is-routine` | hayır | bool değer |
| `--dry-run` | hayır | Simülasyon modu |

### `validate`

Tüm müfredatın zero-sum bütünlüğünü kontrol eder.

```
validate
```

Her ders için:
- Toplam `allocated_sessions` toplamı EXACT_ALLOCATIONS ile eşleşiyor mu?
- `chronologicalIndex` değerleri benzersiz ve sıralı mı?
- Hiçbir konuda negatif oturum var mı?

---

## Simülasyon (Dry-Run) Protokolü

1. YAML/JSON dosyası **salt-okunur** açılır.
2. Değişiklikler bir `patch` objesi olarak bellekte tutulur.
3. Zero-Sum doğrulaması bellek üzerinde yapılır.
4. Fiziksel dosyaya **kesinlikle yazılmaz**.
5. Rapor üretilir: değişen alanlar, eski/yeni değerler, zero-sum logu.

### Örnek Simülasyon Akışı

```
$ transfer --source "Fiziki Coğrafya ve Su Örtüsü" --source-ders Coğrafya
           --target "Türkiye'nin Coğrafi Konumu" --amount 1 --dry-run

=== los-curriculum-manager SIMÜLASYON ===
Dosya: curriculum/genel-kultur/cografya.yaml (READ-ONLY)

[TRANSFER]
  Kaynak: Fiziki Coğrafya ve Su Örtüsü (allocated_sessions: 5 → 4)
  Hedef:  Türkiye'nin Coğrafi Konumu    (allocated_sessions: 2 → 3)
  Miktar: 1 oturum

[ZERO-SUM KONTROLÜ]
  Eski Toplam: 5 + 2 + 2 + 3 + 2 + 2 + 2 = 18
  Yeni Toplam: 4 + 2 + 2 + 3 + 2 + 2 + 3 = 18
  Güvenlik doğrulaması GEÇTİ. ✓

[ENJEKSİYON]
  Türkiye'nin Coğrafi Konumu:
    chronologicalIndex: null → 1
  Fiziki Coğrafya ve Su Örtüsü:
    chronologicalIndex: 2 → 2 (değişmedi)

[DEĞİŞEN KONULAR]
  1. Fiziki Coğrafya ve Su Örtüsü:
     { "name": "Fiziki Coğrafya ve Su Örtüsü",
       "allocated_sessions": 4,
       "chronologicalIndex": 2 }
  2. Türkiye'nin Coğrafi Konumu:
     { "name": "Türkiye'nin Coğrafi Konumu",
       "allocated_sessions": 3,
       "chronologicalIndex": 1 }

[DOSYAYA YAZILMADI] — Dry-run modu, fiziksel değişiklik yapılmadı.

los-curriculum-manager yeteneği sandbox ortamında başarıyla test edildi,
kapasite aşımı yaşanmadı.
```

---

## Mevcut Kodbase ile Entegrasyon

### EXACT_ALLOCATIONS güncelleme

`plan_generator.py:9-66` içindeki `EXACT_ALLOCATIONS` sözlüğü, `transfer` komutu
çalıştığında otomatik güncellenir (dry-run değilse):

```python
EXACT_ALLOCATIONS[kaynak_konu] -= amount
EXACT_ALLOCATIONS[hedef_konu]  += amount
```

### `data.py` tarafındaki etki

`data.py:271` satırındaki `EXACT_ALLOCATIONS.get(t_name, 0)` çağrısı,
güncellenen değerleri otomatik olarak okur:

```python
allocated = EXACT_ALLOCATIONS.get(t_name, 0)
```

### `index.html` tarafındaki etki

`index.html:2010-2020` satırlarındaki `t.allocated_sessions` değeri
`data.py` üzerinden güncellenmiş veriyi alır.

---

## Planlama Motoru İyileştirme Önerisi

Mevcut `priority (P0/P1/P2)` etiket sistemi yerine şu yaklaşım önerilir:

### Önerilen Sıralama Stratejisi

Konular şu kriterlere göre sıralanmalı (öncelik sırasına göre):

1. **Routine konular** (`isRoutine: true`) — her gün belirli oturum alır
2. **chronologicalIndex**: Düşük indeksli konular önce işlenir (temel konular)
3. **avg_questions / target_net oranı**: Yüksek getirili konular önceliklendirilir
4. **Soru başına düşen ortalama süre**: Zor konulara daha fazla oturum

Bu yaklaşımda `priority` alanı tamamen kaldırılabilir.

### Oturum Hesaplama Formülü

```
oturum = max(
    1,  # Her konu en az 1 oturum almalı
    round(
        (avg_questions / toplam_soru) * toplam_oturum  # soru ağırlığı
        * (1 + target_net / max(target_net))           # net hedefi bonusu
    )
)
```

Bu formül, az soru çıkan temel konuların (`avg_questions=1, target_net=0`) bile en az 1 oturum
almasını garanti eder.

---

## Test Edilebilirlik

Tüm komutlar `--dry-run` flag'i ile simülasyon modunda çalıştırılabilir.
Bu sayede:

- Fiziksel dosyalara zarar verilmeden test edilebilir
- Zero-Sum ihlalleri önceden tespit edilebilir
- Farklı transfer senaryoları karşılaştırılabilir
- CI/CD pipeline'ına entegre edilebilir

---

## Hızlı Başlangıç (Sandbox)

```bash
# 1. Coğrafya dersindeki tüm konuların allocated_sessions toplamını kontrol et
python los_curriculum_manager.py validate --ders Coğrafya

# 2. Fiziki Coğrafya'dan 1 oturum al, Türkiye'nin Coğrafi Konumu'na ekle (simülasyon)
python los_curriculum_manager.py transfer \
    --source "Fiziki Coğrafya ve Su Örtüsü" --source-ders Coğrafya \
    --target "Türkiye'nin Coğrafi Konumu" \
    --amount 1 --dry-run

# 3. Türkiye'nin Coğrafi Konumu'na chronologicalIndex=1 ata
python los_curriculum_manager.py inject \
    --ders Coğrafya \
    --konu "Türkiye'nin Coğrafi Konumu" \
    --chronological-index 1 --dry-run

# 4. Tüm derslerde zero-sum bütünlüğünü doğrula
python los_curriculum_manager.py validate --all
```