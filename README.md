# 🚨 Afet-X

## Akıllı Afet Kaynak ve Ambulans Karar Destek Sistemi

Afet-X, afet sırasında sınırlı kaynakların doğru bölgelere
yönlendirilmesine ve ambulansların uygun hastanelere
ulaştırılmasına yardımcı olmak amacıyla geliştirilen
bir karar destek sistemi prototipidir.

## 🎯 Amaç

Afet anında karar verme sürecini hızlandırmak.

Sistem;

- Afet bölgelerini analiz eder.
- Öncelik puanı oluşturur.
- Kaynak dağılımı önerir.
- Kritik bölgeleri belirler.
- Hastanelerin kapasitesini gösterir.
- Personel yükünü gösterir.
- Ambulansları haritada gösterir.
- Alternatif rotaları karşılaştırır.
- Uygun hastane önerisi oluşturur.

## 🧠 Afet Öncelik Modeli

Afet şiddeti: %50

Nüfus: %20

İhtiyaç: %30

## 🚑 Ambulans Karar Sistemi

Sistem ambulansın konumundan hastaneleri karşılaştırır.

Değerlendirilen faktörler:

- Tahmini ulaşım süresi
- Hastane doluluk oranı
- Personel yükü
- Kullanılabilir yatak

Sistem bu bilgiler üzerinden uygun hastaneyi önerir.

## 🛣️ Rota Sistemi

Prototipte OpenStreetMap tabanlı OSRM rota servisi
kullanılmaktadır.

Sistem alternatif güzergahları karşılaştırarak
tahmini mesafe ve ulaşım süresini gösterir.

## 🏥 Hastane Durumu

Her hastane için:

- Doluluk
- Personel yükü/yorgunluk skoru
- Kullanılabilir yatak

gösterilir.

> Personel yükü/yorgunluk değeri prototip verisidir.
> Gerçek sistemde sağlık kuruluşlarından gelen
> güncel verilerle güncellenmelidir.

## 🗺️ Harita

Haritada:

- Ambulanslar
- Hastaneler
- Afet bölgeleri
- Rotalar

gösterilir.

## 🛠️ Teknolojiler

- Python
- Flask
- HTML
- CSS
- JavaScript
- Leaflet
- OpenStreetMap
- OSRM
- GitHub
- Render

## 📁 Proje Yapısı

afet-x-akilli-kaynak-dagitimi/

├── data/

│   └── regions.csv

├── templates/

│   └── index.html

├── app.py

├── render.yaml

├── requirements.txt

├── README.md

└── PROJECT_PLAN.md

## 🚀 Gelecek Geliştirmeler

- Gerçek zamanlı trafik
- Gerçek yol kapanmaları
- Gerçek hastane kapasite verileri
- Gerçek ambulans konumları
- Gerçek personel yükü verileri
- Hava durumu
- Deprem ve afet API'leri
- İlaç ve tıbbi malzeme dağıtımı
- Yapay zekâ ile tahmin
- Hastane-hastane kaynak transferi
- Mobil uygulama
