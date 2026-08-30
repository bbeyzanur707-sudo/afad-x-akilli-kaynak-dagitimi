# 🌿 Görüntü Hastalık Analiz Sistemi

Bu proje, yüklenen görüntüleri basit bir RGB renk analizi yöntemiyle inceleyen Flask tabanlı bir web uygulamasıdır.

> **Not:** Bu proje eğitim ve demo amaçlıdır. Gerçek bir yapay zeka veya tıbbi teşhis sistemi değildir.

---

## 📌 Projenin Amacı

Kullanıcının bir görüntü yüklemesini ve görüntünün temel renk özelliklerine göre basit bir analiz sonucu almasını sağlar.

Sistem:

1. Görüntü dosyasını kabul eder.
2. Dosya formatını kontrol eder.
3. Görüntüyü PIL ile açar.
4. Görüntüyü standart boyuta getirir.
5. Ortalama RGB değerlerini hesaplar.
6. Basit kurallara göre analiz sonucu üretir.
7. Sonucu web sayfasında gösterir.
8. Yüklenen görüntüyü `static/uploads` klasörüne kaydeder.

---

## 🛠️ Kullanılan Teknolojiler

- Python
- Flask
- Pillow
- NumPy
- HTML
- CSS
- Jinja2

---

## 📁 Proje Klasör Yapısı

```text
proje/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── uploads/
