# 🚨 Afet-X Akıllı Kaynak Dağıtımı

Afet-X, afet bölgelerinde mevcut kaynakların ihtiyaçlara göre
önceliklendirilmesine yardımcı olmak amacıyla geliştirilmiş
Flask tabanlı bir karar destek sistemidir.

---

## 🎯 Projenin Amacı

Afet sonrasında kaynakların hangi bölgelere öncelikli olarak
gönderilmesi gerektiğini belirlemek önemli bir problemdir.

Afet-X bu problemi üç temel kriter üzerinden ele alır:

- Afet Şiddeti
- Nüfus
- İhtiyaç Miktarı

Bu kriterler belirlenen ağırlıklarla birleştirilerek her bölge
için 0-100 arasında bir öncelik skoru hesaplanır.

---

## 🧮 Öncelik Skoru

Sistemde kullanılan formül:

```text
Öncelik Skoru =
(Afet Şiddeti × 0.50)
+
(Nüfus × 0.20)
+
(İhtiyaç Miktarı × 0.30)
