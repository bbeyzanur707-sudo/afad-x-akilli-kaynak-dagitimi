import pandas as pd
import streamlit as st

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
# VERİ
# --------------------------------------------------

df = pd.read_csv("data/regions.csv")

# --------------------------------------------------
# KAYNAK GİRİŞİ
# --------------------------------------------------

st.sidebar.header("📦 Mevcut Kaynaklar")

water = st.sidebar.number_input(
    "Su (litre)",
    min_value=0,
    value=10000,
    step=500
)

meals = st.sidebar.number_input(
    "Yemek (öğün)",
    min_value=0,
    value=5000,
    step=250
)

blankets = st.sidebar.number_input(
    "Battaniye",
    min_value=0,
    value=1000,
    step=50
)

medicine = st.sidebar.number_input(
    "İlaç paketi",
    min_value=0,
    value=500,
    step=25
)

# --------------------------------------------------
# KAYNAK DAĞITIM FONKSİYONU
# --------------------------------------------------

def allocate_resources(total, demand):
    """
    Mevcut kaynağı ihtiyaca göre oransal olarak dağıtır.
    """
    demand = demand.clip(lower=0)

    if demand.sum() == 0:
        return pd.Series([0] * len(demand), index=demand.index)

    allocation = total * demand / demand.sum()

    return allocation.round().astype(int)


# --------------------------------------------------
# ÖNCELİK HESAPLAMA
# --------------------------------------------------

df["priority_score"] = (
    0.30 * (df["earthquake_intensity"] / 8.5).clip(0, 1)
    + 0.28 * df["damage_ratio"].clip(0, 1)
    + 0.20 * (
        (df["displaced"] / df["population"]) / 0.25
    ).clip(0, 1)
    + 0.12 * (1 - df["road_access"].clip(0, 1))
    + 0.10 * (1 - df["hospital_capacity"].clip(0, 1))
)

df["priority_score"] = df["priority_score"].round(3)

df = df.sort_values(
    "priority_score",
    ascending=False
).reset_index(drop=True)

# --------------------------------------------------
# KAYNAK TAHSİSİ
# --------------------------------------------------

df["allocated_water_l"] = allocate_resources(
    water,
    df["water_l"]
)

df["allocated_meals"] = allocate_resources(
    meals,
    df["meals"]
)

df["allocated_blankets"] = allocate_resources(
    blankets,
    df["blankets"]
)

df["allocated_medicine"] = allocate_resources(
    medicine,
    df["medicine"]
)

# --------------------------------------------------
# ÖZET
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Bölge Sayısı",
    len(df)
)

col2.metric(
    "Yerinden Olan",
    f"{df['displaced'].sum():,}"
)

col3.metric(
    "En Acil Bölge",
    df.iloc[0]["region"]
)

col4.metric(
    "Ortalama Öncelik",
    f"{df['priority_score'].mean():.2f}"
)

# --------------------------------------------------
# ÖNCELİK TABLOSU
# --------------------------------------------------

st.markdown("---")
st.header("🚨 Bölge Öncelik Sıralaması")

priority_table = df[
    [
        "region",
        "priority_score",
        "population",
        "earthquake_intensity",
        "damage_ratio",
        "displaced",
        "injured",
        "road_access",
        "hospital_capacity"
    ]
].copy()

priority_table.columns = [
    "Bölge",
    "Öncelik Skoru",
    "Nüfus",
    "Afet Şiddeti",
    "Hasar Oranı",
    "Yerinden Olan",
    "Yaralı",
    "Yol Erişimi",
    "Hastane Kapasitesi"
]

st.dataframe(
    priority_table,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# KAYNAK DAĞITIMI
# --------------------------------------------------

st.markdown("---")
st.header("📦 Önerilen Kaynak Dağıtımı")

resource_table = df[
    [
        "region",
        "water_l",
        "allocated_water_l",
        "meals",
        "allocated_meals",
        "blankets",
        "allocated_blankets",
        "medicine",
        "allocated_medicine"
    ]
].copy()

resource_table.columns = [
    "Bölge",
    "Su İhtiyacı",
    "Tahsis Edilen Su",
    "Yemek İhtiyacı",
    "Tahsis Edilen Yemek",
    "Battaniye İhtiyacı",
    "Tahsis Edilen Battaniye",
    "İlaç İhtiyacı",
    "Tahsis Edilen İlaç"
]

st.dataframe(
    resource_table,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# EN ACİL 3 BÖLGE
# --------------------------------------------------

st.markdown("---")
st.header("🔴 İlk Müdahale Önerisi")

for i, row in df.head(3).iterrows():

    st.write(
        f"**{i + 1}. {row['region']}** — "
        f"Öncelik skoru: **{row['priority_score']:.3f}** | "
        f"Yerinden olan: **{row['displaced']:,}** | "
        f"Yaralı: **{row['injured']:,}**"
    )

# --------------------------------------------------
# KARAR MANTIĞI
# --------------------------------------------------

st.markdown("---")
st.header("🧠 Sistem Nasıl Karar Veriyor?")

st.write("""
Sistem bölge önceliğini beş temel faktöre göre hesaplar:

1. Afet şiddeti
2. Hasar oranı
3. Yerinden olan nüfus
4. Yol erişilebilirliği
5. Hastane kapasitesi

Bu MVP sürümünde ağırlıklı bir skor kullanılmaktadır.

İleri sürümde bu yapı gerçek verilerle eğitilmiş
makine öğrenmesi modeliyle değiştirilecektir.
""")

# --------------------------------------------------
# CSV İNDİR
# --------------------------------------------------

st.markdown("---")

csv = df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="📥 Dağıtım Planını CSV İndir",
    data=csv,
    file_name="afad_x_dagitim_plani.csv",
    mime="text/csv"
)

st.caption(
    "AFAD-X | Büyük Veri Analistliği Projesi | MVP"
)
