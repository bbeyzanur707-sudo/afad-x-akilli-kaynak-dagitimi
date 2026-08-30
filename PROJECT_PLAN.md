# 🚨 Afet-X Akıllı Kaynak Dağıtımı

## 📌 Proje Tanımı

Afet-X, afet bölgelerinde mevcut kaynakların ihtiyaç ve afet
şiddetine göre daha hızlı ve verimli dağıtılmasına yardımcı olan
akıllı bir karar destek sistemidir.

Sistem, farklı afet bölgelerinden alınan verileri analiz ederek
hangi bölgenin daha yüksek önceliğe sahip olduğunu belirler.

---

# 🎯 Projenin Amacı

Afet sırasında;

- Kaynakların yetersiz kalmasını önlemek
- Kritik bölgeleri hızlı şekilde belirlemek
- Kaynakların dengeli dağıtılmasını sağlamak
- Karar verme sürecini hızlandırmak
- Veri temelli kaynak dağıtımı yapmak

amaçlanmaktadır.

---

# 🧠 Sistem Nasıl Çalışır?

Kullanıcı sisteme aşağıdaki bilgileri girer:

1. Toplam kullanılabilir kaynak
2. Afet bölgesi
3. Afet şiddeti
4. Bölge nüfusu
5. Bölgenin ihtiyaç miktarı

Sistem bu verileri analiz eder.

Ardından her bölge için bir
**öncelik puanı** oluşturur.

---

# 📊 Öncelik Hesaplama

Sistemde öncelik puanı üç temel faktöre göre hesaplanmaktadır.

### Afet Şiddeti

Ağırlık:

**%50**

Afetin bölge üzerindeki etkisini temsil eder.

### Nüfus

Ağırlık:

**%20**

Daha fazla kişinin etkilendiği bölgelerin
önceliğinin belirlenmesine katkı sağlar.

### İhtiyaç

Ağırlık:

**%30**

Bölgedeki kaynak ihtiyacını temsil eder.

---

# 🚦 Öncelik Seviyeleri

| Puan | Seviye |
|---|---|
| 75-100 | 🔴 Kritik |
| 50-74 | 🟠 Acil |
| 25-49 | 🟡 Orta |
| 0-24 | 🟢 Düşük |

---

# 💰 Akıllı Kaynak Dağıtımı

Sistem toplam kullanılabilir kaynağı,
bölgelerin öncelik puanlarına göre dağıtır.

Örneğin:

Toplam kaynak:

**100.000**

olduğunda sistem bölgelerin öncelik seviyelerini
hesaplayarak her bölge için önerilen kaynak miktarını
oluşturur.

---

# 🤖 Akıllı Sistem Önerisi

Sistem analiz sonucunda en yüksek önceliğe sahip bölgeyi
belirler.

Örneğin:

> Hatay bölgesi kritik önceliktedir.
> Öncelik puanı 91/100.
> Kaynakların önemli bir bölümünün bu bölgeye
> yönlendirilmesi önerilmektedir.

Bu özellik karar vericiye hızlı bir özet sunmayı amaçlar.

---

# 🖥️ Kullanıcı Arayüzü

Sistemde:

- Kaynak giriş alanı
- Afet bölgesi ekleme
- Afet şiddeti girişi
- Nüfus girişi
- İhtiyaç girişi
- Analiz butonu
- Öncelik puanı
- Kaynak dağılımı
- Kritik bölge göstergesi
- Akıllı sistem önerisi

bulunmaktadır.

---

# 🛠️ Kullanılan Teknolojiler

- Python
- Flask
- HTML
- CSS
- JavaScript
- GitHub
- Render

---

# 📁 Proje Dosya Yapısı

```text
afet-x-akilli-kaynak-dagitimi/

├── data/
│   └── regions.csv
│
├── templates/
│   └── index.html
│
├── app.py
├── render.yaml
├── requirements.txt
├── README.md
└── PROJECT_PLAN.md
