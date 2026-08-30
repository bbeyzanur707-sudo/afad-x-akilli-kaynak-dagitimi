# Afet-X Akıllı Kaynak Dağıtımı

## 1. Projenin Amacı

Afet-X, afet bölgelerindeki ihtiyaçları analiz ederek kaynakların,
ambulansların ve hastanelerin daha hızlı ve verimli şekilde
yönetilmesini amaçlayan akıllı karar destek sistemidir.

Sistem;

- Afet bölgelerinin önceliklerini belirler.
- Kaynakların hangi bölgeye gönderileceğini hesaplar.
- Ambulans için en hızlı rotayı belirlemeye yardımcı olur.
- Hastanelerdeki yoğunluk ve mevcut kapasiteyi gösterir.
- Hastanelerdeki personel yorgunluğunu takip eder.
- Yol durumuna göre alternatif güzergah önerir.
- Afet yöneticilerine karar desteği sağlar.

---

## 2. Temel Sistem

Sistem beş ana bölümden oluşur:

1. Afet Analizi
2. Akıllı Kaynak Dağıtımı
3. Ambulans ve Rota Yönetimi
4. Hastane Durum Analizi
5. Harita ve Karar Destek Sistemi

---

## 3. Afet Analizi

Her afet bölgesi için;

- Afet şiddeti
- Nüfus
- İhtiyaç miktarı
- Bölgenin öncelik seviyesi

hesaplanır.

Öncelik hesabında;

- Afet şiddeti: %50
- Nüfus: %20
- İhtiyaç: %30

ağırlıkları kullanılır.

Sistem bölgeleri karşılaştırarak en yüksek önceliğe sahip
bölgeleri belirler.

---

## 4. Akıllı Kaynak Dağıtımı

Toplam kullanılabilir kaynak sisteme girilir.

Sistem hesaplanan öncelik puanlarına göre kaynakları
bölgelere dağıtır.

Amaç;

- Kaynak israfını azaltmak
- Kritik bölgelere daha hızlı ulaşmak
- Kaynakların dengeli dağıtılmasını sağlamak
- Karar verme süresini azaltmak

---

## 5. Ambulans ve Rota Yönetimi

Sistem ambulansların hastaya ulaşması için uygun rotayı
belirlemeye yardımcı olur.

Rota değerlendirilirken;

- Mesafe
- Tahmini ulaşım süresi
- Yol durumu
- Trafik yoğunluğu
- Yolun kullanılabilirliği

gibi bilgiler dikkate alınır.

Sistem mümkün olduğunda en hızlı ve güvenli rotayı önerir.

---

## 6. Hastane Durum Analizi

Sistemde hastanelerin mevcut durumu takip edilir.

Her hastane için;

- Hasta sayısı
- Yatak kapasitesi
- Boş yatak sayısı
- Personel sayısı
- Personel yorgunluk seviyesi
- Acil servis yoğunluğu

gibi bilgiler gösterilebilir.

Böylece ambulansın hangi hastaneye yönlendirilmesinin
daha uygun olabileceği konusunda karar desteği sağlanır.

---

## 7. Personel Yorgunluk Analizi

Afet sırasında sağlık çalışanlarının çalışma yoğunluğu
takip edilir.

Yorgunluk seviyesi;

- Düşük
- Orta
- Yüksek
- Kritik

şeklinde sınıflandırılabilir.

Yorgunluğu yüksek hastanelerde sistem yöneticiyi uyarır.

Bu özellik, personel dağılımının daha dengeli yapılmasına
yardımcı olur.

---

## 8. Harita Sistemi

Sistem afet bölgelerini, hastaneleri ve ambulansları
harita üzerinde gösterecek şekilde geliştirilebilir.

Haritada;

- Afet bölgeleri
- Hastaneler
- Ambulanslar
- Ana yollar
- Alternatif yollar
- Riskli yollar

gösterilebilir.

Kullanıcı bir bölge seçtiğinde sistem o bölgeye ilişkin
önemli bilgileri gösterebilir.

---

## 9. Akıllı Yol Seçimi

Birden fazla yol bulunduğunda sistem yolları
karşılaştırabilir.

Örneğin:

Yol A:
- 12 km
- Tahmini süre: 18 dakika
- Trafik: Orta

Yol B:
- 15 km
- Tahmini süre: 12 dakika
- Trafik: Düşük

Bu durumda sistem sadece mesafeye bakmak yerine
tahmini ulaşım süresini ve yol durumunu da değerlendirerek
Yol B'yi önerebilir.

---

## 10. Ambulans İçin Hastane Seçimi

Ambulans hastaya ulaştıktan sonra sistem uygun hastaneyi
belirlemeye yardımcı olabilir.

Hastane seçilirken;

- Hastaneye ulaşım süresi
- Boş yatak sayısı
- Acil servis yoğunluğu
- Personel yorgunluğu
- Hastanenin mevcut kapasitesi

değerlendirilir.

Böylece sadece en yakın hastane değil,
duruma göre en uygun hastane önerilebilir.

---

## 11. Karar Destek Sistemi

Sistem yöneticilere otomatik öneriler sunabilir.

Örneğin:

> "Bölge 2 yüksek önceliklidir."

> "Ambulans için alternatif rota daha hızlıdır."

> "Hastane A'nın yoğunluğu kritik seviyededir."

> "Hastane B'de daha fazla boş yatak bulunmaktadır."

> "Hastane C'de personel yorgunluğu yüksektir."

Bu uyarılar afet sırasında karar verme sürecini
hızlandırmayı amaçlar.

---

## 12. Gelecekte Eklenebilecek Özellikler

Projenin ilerleyen aşamalarında;

- Gerçek zamanlı trafik verisi
- Gerçek zamanlı harita
- GPS destekli ambulans takibi
- Hava durumu verileri
- Yapay zeka tabanlı talep tahmini
- Hastane yoğunluk tahmini
- Otomatik rota güncelleme
- Mobil uygulama
- Gerçek zamanlı bildirim sistemi

eklenebilir.

---

## 13. Projenin Yenilikçi Yönü

Afet-X yalnızca kaynak dağıtımı yapan bir sistem değildir.

Kaynak dağıtımı, ambulans rotası, hastane kapasitesi,
personel yorgunluğu ve harita tabanlı karar desteğini
tek bir sistem içerisinde birleştirmeyi amaçlamaktadır.

Bu sayede afet sırasında daha hızlı, dengeli ve
veriye dayalı karar alınmasına yardımcı olması hedeflenmektedir.
