import streamlit as st
import pandas as pd
import numpy as np
import os

# Sayfa Yapılandırması
st.set_page_config(
    page_title="AFAD-X",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AFAD-X")
st.subheader("Afet Sonrası Akıllı Kaynak Dağıtım Sistemi")

st.info(
    "Bu uygulama eğitim/prototip amaçlıdır. "
    "Gerçek afet operasyonlarında resmi kurum verileri ve uzman doğrulaması gerekir."
)

# --------------------------------------------------
# VERİ YÜKLEME VE HATA KONTROLÜ
# --------------------------------------------------
csv_path = "data/regions.csv"

# Eğer data/regions.csv dosyası yoksa uygulamanın çökmemesi için otomatik örnek veri oluşturur
if not os.path.exists(csv_path):
    os.makedirs("data", exist_ok=True)
    sample_data = {
        "region": ["Bölge A", "Bölge B", "Bölge C", "Bölge D"],
        "population":,
        "earthquake_intensity": [7.4, 6.5, 7.1, 5.8],
        "damage_ratio": [0.65, 0.20, 0.45, 0.10],
        "displaced":,
        "injured":,
        "road_access": [0.4, 0.9, 0.6, 1.0], # 0: kapalı, 1: açık
        "hospital_capacity": [0.2, 0.8, 0.5, 0.9], # 0: yetersiz, 1: tam kapasite
        "water_l":,
        "meals":,
        "blankets":,
        "medicine": [400, 50, 200, 30]
    }
    pd.DataFrame(sample_data).to_csv(csv_path, index=False)

df = pd.read_csv(csv_path)

# --------------------------------------------------
# KAYNAK GİRİŞİ (SIDEBAR)
# --------------------------------------------------
st.sidebar.header("📦 Mevcut Kaynaklar")

water = st.sidebar.number_input("Su (litre)", min_value=0, value=10000, step=500)
meals = st.sidebar.number_input("Yemek (öğün)", min_value=0, value=5000, step=250)
blankets = st.sidebar.number_input("Battaniye", min_value=0, value=1000, step=50)
medicine = st.sidebar.number_input("İlaç paketi", min_value=0, value=500, step=25)

# --------------------------------------------------
# GELİŞTİRİLMİŞ KAYNAK DAĞITIM FONKSİYONU
# --------------------------------------------------
def allocate_resources(total, demand):
    """
    Mevcut kaynağı ihtiyaca göre oransal olarak dağıtır. Sıfıra bölünme hatasını engeller.
    """
    demand = demand.clip(lower=0)
    total_demand = demand.sum()
    
    if total_demand == 0 or total == 0:
        return pd.Series([0] * len(demand), index=demand.index)
        
    allocation = total * (demand / total_demand)
    return allocation.round().astype(int)

# --------------------------------------------------
# ÖNCELİK HESAPLAMA
# --------------------------------------------------
# Sütun isimlerinin doğruluğundan emin olmak için kontrol
required_columns = ["earthquake_intensity", "damage_ratio", "displaced", "population", "road_access", "hospital_capacity"]
if all(col in df.columns for col in required_columns):
    df["priority_score"] = (
        0.30 * (df["earthquake_intensity"] / 8.5).clip(0, 1)
        + 0.28 * df["damage_ratio"].clip(0, 1)
        + 0.20 * ((df["displaced"] / df["population"].replace(0, 1)) / 0.25).clip(0, 1) # Sıfıra bölme koruması
        + 0.12 * (1 - df["road_access"].clip(0, 1))
        + 0.10 * (1 - df["hospital_capacity"].clip(0, 1))
    )
    df["priority_score"] = df["priority_score"].round(3)
    df = df.sort_values("priority_score", ascending=False).reset_index(drop=True)
else:
    st.error("CSV dosyasındaki sütun isimleri eksik veya hatalı!")

# --------------------------------------------------
# KAYNAK TAHSİSİ TETİKLEME
# --------------------------------------------------
df["allocated_water_l"] = allocate_resources(water, df["water_l"])
df["allocated_meals"] = allocate_resources(meals, df["meals"])
df["allocated_blankets"] = allocate_resources(blankets, df["blankets"])
df["allocated_medicine"] = allocate_resources(medicine, df["medicine"])

# --------------------------------------------------
# ÖZET METRİKLERİ
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Bölge Sayısı", len(df))
col2.metric("Toplam Yerinden Olan", f"{df['displaced'].sum():,}")
col3.metric("En Kritik Bölge", df.iloc[0]["region"] if not df.empty else "Bilinmiyor")
col4.metric("Ortalama Öncelik Skoru", f"{df['priority_score'].mean():.2f}" if not df.empty else "0.00")

# Stok Yetersizlik Uyarı Sistemi
if water < df["water_l"].sum() or meals < df["meals"].sum():
    st.warning("⚠️ Dikkat: Mevcut kaynaklar, toplam bölge ihtiyaçlarını tam olarak karşılayamıyor! Oransal dağıtım yapıldı.")

# --------------------------------------------------
# TABLOLAR VE GÖSTERİMLER
# --------------------------------------------------
st.markdown("---")
st.header("🚨 Bölge Öncelik Sıralaması")

priority_table = df[[
    "region", "priority_score", "population", "earthquake_intensity", 
    "damage_ratio", "displaced", "injured", "road_access", "hospital_capacity"
]].copy()

priority_table.columns = [
    "Bölge", "Öncelik Skoru", "Nüfus", "Afet Şiddeti", 
    "Hasar Oranı", "Yerinden Olan", "Yaralı", "Yol Erişimi", "Hastane Kapasitesi"
]

st.dataframe(priority_table, use_container_width=True, hide_index=True)

st.markdown("---")
st.header("📦 Önerilen Kaynak Dağıtımı")

resource_table = df[[
    "region", "water_l", "allocated_water_l", "meals", "allocated_meals", 
    "blankets", "allocated_blankets", "medicine", "allocated_medicine"
]].copy()

resource_table.columns = [
    "Bölge", "Su İhtiyacı", "Tahsis Edilen Su", "Yemek İhtiyacı", 
    "Tahsis Edilen Yemek", "Battaniye İhtiyacı", "Tahsis Edilen Battaniye", "İlaç İhtiyacı", "Tahsis Edilen İlaç"
]

st.dataframe(resource_table, use_container_width=True, hide_index=True)

# --------------------------------------------------
# EN ACİL 3 BÖLGE DETAYI
# --------------------------------------------------
st.markdown("---")
st.header("🔴 İlk Müdahale Önerilen Kritik Bölgeler")

for i, row in df.head(3).iterrows():
    st.error(
        f"**{i + 1}. {row['region']}** — "
        f"Öncelik Skoru: **{row['priority_score']:.3f}** | "
        f"Yerinden Olan: **{row['displaced']:,} Kişi** | "
        f"Yaralı: **{row['injured']:,} Kişi**"
    )

# --------------------------------------------------
# KARAR MANTIĞI AÇIKLAMASI
# --------------------------------------------------
st.markdown("---")
st.header("🧠 Sistem Nasıl Karar Veriyor?")
st.write("""
Sistem, afet bölgelerinin aciliyet durumunu 5 ana kriterin ağırlıklandırılması algoritması ile hesaplar:
1. **Afet Şiddeti (%30)**
2. **Hasar Oranı (%28)**
3. **Yerinden Olan Nüfus Oranı (%20)**
4. **Yol Erişilebilirliği Kısıtı (%12)**
5. **Hastane Kapasitesi Yetersizliği (%10)**

Hesaplanan öncelik skoruna göre lojistik kaynaklar (Su, Yemek, Battaniye, İlaç) bölgelerin ihtiyaç oranına göre adil şekilde paylaştırılır.
""")

# --------------------------------------------------
# VERİ İNDİRME BUTONU
# --------------------------------------------------
st.markdown("---")
csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="📥 Dağıtım Planını CSV Olarak İndir",
    data=csv,
    file_name="afad_x_dagitim_plani.csv",
    mime="text/csv"
)

st.caption("AFAD-X | Büyük Veri Analistliği Projesi | MVP v1.1")
