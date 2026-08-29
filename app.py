import os
import pandas as pd
import streamlit as st

# 1. Veri Klasörü ve Dosya Yolu Kontrolü
csv_path = "data/regions.csv"

# Eğer data/regions.csv dosyası yoksa otomatik örnek veri oluşturur
if not os.path.exists(csv_path):
    os.makedirs("data", exist_ok=True)
    
    # Görseldeki güncellenmiş yeni değerler (400, 50, 200, 30)
    sample_data = {
        "water_1":,   # Örnek sütunlar ve değerler
        "meals":,
        "blankets":,
        "medicine": [400, 50, 200, 30]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv(csv_path, index=False)
else:
    # Dosya varsa mevcut dosyayı oku
    df = pd.read_csv(csv_path)


# 2. Kaynak Dağıtım Fonksiyonu
def allocate_resources(total, demand):
    # col3 ve col4 metrik göstergeleri
    if not df.empty:
        col3.metric("En Kritik Bölge", df.loc[0, "region"])
    else:
        col3.metric("En Kritik Bölge", "Bilinmiyor")
        
    col4.metric("Ortalama Öncelik Skoru", f"{df['priority_score'].mean():.2f}")


# 3. Stok Yetersizlik Uyarı Sistemi
# Not: 'water' ve 'meals' değişkenlerinin yukarıdaki kodlarda tanımlanmış olması gerekir.
# Eğer bu değişkenler kullanıcı girdisinden geliyorsa sayısal (int/float) formatta olmalıdır.
if 'water' in locals() and 'meals' in locals():
    if water < df["water_1"].sum() or meals < df["meals"].sum():
        st.warning("⚠️ Dikkat: Mevcut kaynaklar, toplam bölge ihtiyaçlarını tam olarak karşılamıyor!")
        st.warning("⚠️ Dikkat: Mevcut kaynaklar toplam ihtiyacı karşılamıyor! Oranları kontrol edin.")
