# 🚨 AFAD-X

## Afet Sonrası Akıllı Kaynak Dağıtım Sistemi

AFAD-X, afet sonrasında bölgelerin ihtiyaçlarını analiz ederek
yardım kaynaklarının önceliklendirilmesine yardımcı olan
eğitim/prototip amaçlı bir karar destek sistemi projesidir.

---

## 🎯 Projenin Amacı

Afet sonrasında;

- Hangi bölgenin daha acil olduğu?
- Hangi bölgede daha fazla insan bulunduğu?
- Hangi bölgede ne kadar su gerektiği?
- Ne kadar gıda gerektiği?
- Ne kadar ilaç gerektiği?
- Ne kadar battaniye gerektiği?

gibi bilgileri tek bir panel üzerinden analiz etmeyi amaçlar.

---

## 🚀 Özellikler

- 📍 Bölgesel analiz
- 👥 Nüfus analizi
- 🚨 Afet şiddeti analizi
- 💧 Su ihtiyacı
- 🍱 Gıda ihtiyacı
- 💊 İlaç ihtiyacı
- 🛏️ Battaniye ihtiyacı
- ⭐ Öncelik skoru
- 🔴 Kritik bölge tespiti
- 📦 Akıllı kaynak dağıtımı
- 📊 Grafikler
- 📥 CSV raporu
- ⚙️ Dinamik kaynak simülasyonu

---

## 🧮 Öncelik Skoru

Sistem üç temel faktörü kullanmaktadır:

### Afet Şiddeti

**%50 ağırlık**

### Nüfus

**%20 ağırlık**

### İhtiyaç Miktarı

**%30 ağırlık**

Toplam ağırlık **%100'dür.**

Öncelik skoru aşağıdaki formül ile hesaplanmaktadır:

```text
Öncelik Skoru =
(Afet Şiddeti × 0.50)
+
(Nüfus × 0.20)
+
(İhtiyaç Miktarı × 0.30)
