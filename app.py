import os
import pandas as pd
import streamlit as st


# ============================================================
# SAYFA AYARLARI
# ============================================================

st.set_page_config(
    page_title="AFAD-X",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# TASARIM
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(
            135deg,
            #b71c1c,
            #e53935
        );
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        margin-top: 5px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #eef4ff;
        border-left: 5px solid #1565c0;
        margin-bottom: 20px;
    }

    .success-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
    }

    .danger-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #ffebee;
        border-left: 5px solid #c62828;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BAŞLIK
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🚨 AFAD-X</h1>
        <p>Afet Sonrası Akıllı Kaynak Dağıtım Sistemi</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        <b>ℹ️ Sistem hakkında</b><br>
        AFAD-X, afet bölgelerindeki ihtiyaçları analiz ederek
        mevcut kaynakların önceliklendirilmesine yardımcı olan
        eğitim/prototip amaçlı bir karar destek sistemidir.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VERİ YÜKLEME
# ============================================================

CSV_PATH = "data/regions.csv"


@st.cache_data
def load_data():

    if os.path.exists(CSV_PATH):

        try:
            df = pd.read_csv(CSV_PATH)

            required_columns = [
                "region",
                "population",
                "severity",
                "water_need",
                "food_need",
                "medicine_need",
                "blanket_need"
            ]

            if all(column in df.columns for column in required_columns):
                return df

        except Exception:
            pass

    # CSV bulunamazsa örnek veri oluştur
    data = {
        "region": [
            "Hatay",
            "Kahramanmaraş",
            "Adıyaman",
            "Malatya",
            "Gaziantep",
            "Osmaniye",
            "Adana",
            "Şanlıurfa"
        ],

        "population": [
            500000,
            450000,
            300000,
            350000,
            600000,
            250000,
            700000,
            650000
        ],

        "severity": [
            9,
            8,
            9,
            7,
            6,
            8,
            5,
            6
        ],

        "water_need": [
            400,
            350,
            300,
            250,
            200,
            220,
            180,
            200
        ],

        "food_need": [
            500,
            450,
            350,
            300,
            250,
            280,
            200,
            230
        ],

        "medicine_need": [
            200,
            180,
            160,
            140,
            100,
            130,
            90,
            100
        ],

        "blanket_need": [
            300,
            280,
            250,
            200,
            150,
            180,
            120,
            140
        ]
    }

    return pd.DataFrame(data)


df = load_data()


# ============================================================
# ÖNCELİK SKORU
# ============================================================

def calculate_priority(row):

    population_score = min(row["population"] / 100000, 10)

    severity_score = row["severity"]

    total_need = (
        row["water_need"]
        + row["food_need"]
        + row["medicine_need"]
        + row["blanket_need"]
    )

    need_score = min(total_need / 100, 10)

    priority = (
        severity_score * 0.50
        + population_score * 0.20
        + need_score * 0.30
    )

    return round(priority, 2)


df["priority_score"] = df.apply(
    calculate_priority,
    axis=1
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Kontrol Paneli")

st.sidebar.markdown(
    "Kaynak dağıtımını aşağıdaki seçeneklerle simüle edebilirsiniz."
)

selected_region = st.sidebar.selectbox(
    "📍 Bölge seç",
    ["Tüm Bölgeler"] + sorted(df["region"].unique().tolist())
)

st.sidebar.divider()

water_available = st.sidebar.number_input(
    "💧 Mevcut su",
    min_value=0,
    value=1000,
    step=50
)

food_available = st.sidebar.number_input(
    "🍱 Mevcut gıda",
    min_value=0,
    value=1200,
    step=50
)

medicine_available = st.sidebar.number_input(
    "💊 Mevcut ilaç",
    min_value=0,
    value=600,
    step=50
)

blanket_available = st.sidebar.number_input(
    "🛏️ Mevcut battaniye",
    min_value=0,
    value=800,
    step=50
)


# ============================================================
# ÜST METRİKLER
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📍 Bölge Sayısı",
        len(df)
    )

with col2:
    st.metric(
        "👥 Toplam Nüfus",
        f"{df['population'].sum():,.0f}"
    )

with col3:
    st.metric(
        "🚨 Ortalama Şiddet",
        f"{df['severity'].mean():.1f}/10"
    )

with col4:
    st.metric(
        "⭐ En Yüksek Öncelik",
        df["priority_score"].max()
    )


st.divider()


# ============================================================
# BÖLGE FİLTRESİ
# ============================================================

if selected_region != "Tüm Bölgeler":

    display_df = df[
        df["region"] == selected_region
    ].copy()

else:

    display_df = df.copy()


# ============================================================
# ÖNCELİKLENDİRME
# ============================================================

st.subheader("🚨 Afet Bölgesi Önceliklendirmesi")

priority_df = display_df.sort_values(
    "priority_score",
    ascending=False
).reset_index(drop=True)

priority_df.insert(
    0,
    "Sıra",
    range(1, len(priority_df) + 1)
)


st.dataframe(
    priority_df[
        [
            "Sıra",
            "region",
            "population",
            "severity",
            "priority_score"
        ]
    ].rename(
        columns={
            "region": "Bölge",
            "population": "Nüfus",
            "severity": "Afet Şiddeti",
            "priority_score": "Öncelik Skoru"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# KAYNAK DAĞITIM ALGORİTMASI
# ============================================================

def distribute_resources(data):

    result = data.copy()

    total_priority = result["priority_score"].sum()

    if total_priority == 0:
        return result

    result["water_allocated"] = (
        result["priority_score"]
        / total_priority
        * water_available
    )

    result["food_allocated"] = (
        result["priority_score"]
        / total_priority
        * food_available
    )

    result["medicine_allocated"] = (
        result["priority_score"]
        / total_priority
        * medicine_available
    )

    result["blanket_allocated"] = (
        result["priority_score"]
        / total_priority
        * blanket_available
    )

    return result


allocation_df = distribute_resources(priority_df)


# ============================================================
# KAYNAK DAĞITIMI
# ============================================================

st.subheader("📦 Akıllı Kaynak Dağıtımı")

st.caption(
    "Kaynaklar, afet şiddeti, nüfus ve ihtiyaç miktarına "
    "göre hesaplanan öncelik skoruna göre paylaştırılmıştır."
)


st.dataframe(
    allocation_df[
        [
            "region",
            "priority_score",
            "water_allocated",
            "food_allocated",
            "medicine_allocated",
            "blanket_allocated"
        ]
    ].rename(
        columns={
            "region": "Bölge",
            "priority_score": "Öncelik",
            "water_allocated": "Su",
            "food_allocated": "Gıda",
            "medicine_allocated": "İlaç",
            "blanket_allocated": "Battaniye"
        }
    ).round(1),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SEÇİLEN BÖLGE ANALİZİ
# ============================================================

st.divider()

st.subheader("🔎 Bölge Analizi")


analysis_region = st.selectbox(
    "Analiz edilecek bölge",
    df["region"].tolist()
)

region_data = df[
    df["region"] == analysis_region
].iloc[0]


c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "👥 Nüfus",
        f"{region_data['population']:,.0f}"
    )

    st.metric(
        "🚨 Afet Şiddeti",
        f"{region_data['severity']}/10"
    )


with c2:

    st.metric(
        "💧 Su İhtiyacı",
        f"{region_data['water_need']}"
    )

    st.metric(
        "🍱 Gıda İhtiyacı",
        f"{region_data['food_need']}"
    )


with c3:

    st.metric(
        "💊 İlaç İhtiyacı",
        f"{region_data['medicine_need']}"
    )

    st.metric(
        "🛏️ Battaniye İhtiyacı",
        f"{region_data['blanket_need']}"
    )


# ============================================================
# İHTİYAÇ GRAFİĞİ
# ============================================================

st.subheader("📊 İhtiyaç Dağılımı")

need_chart = pd.DataFrame(
    {
        "Kaynak": [
            "Su",
            "Gıda",
            "İlaç",
            "Battaniye"
        ],

        "İhtiyaç": [
            region_data["water_need"],
            region_data["food_need"],
            region_data["medicine_need"],
            region_data["blanket_need"]
        ]
    }
)

st.bar_chart(
    need_chart.set_index("Kaynak")
)


# ============================================================
# KRİTİK BÖLGELER
# ============================================================

st.divider()

st.subheader("🔴 Kritik Bölgeler")

critical_regions = df[
    (df["severity"] >= 8)
    | (df["priority_score"] >= 7)
].sort_values(
    "priority_score",
    ascending=False
)


if len(critical_regions) > 0:

    st.markdown(
        """
        <div class="danger-box">
        <b>⚠️ Dikkat:</b>
        Bu bölgeler yüksek afet şiddeti veya yüksek kaynak
        ihtiyacı nedeniyle öncelikli olarak değerlendirilmelidir.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        critical_regions[
            [
                "region",
                "severity",
                "priority_score"
            ]
        ].rename(
            columns={
                "region": "Bölge",
                "severity": "Afet Şiddeti",
                "priority_score": "Öncelik Skoru"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "Kritik seviyede bölge bulunmamaktadır."
    )


# ============================================================
# SİSTEM DURUMU
# ============================================================

st.divider()

st.subheader("🟢 Sistem Durumu")

status_col1, status_col2 = st.columns(2)

with status_col1:

    st.markdown(
        """
        <div class="success-box">
        <b>✓ Veri sistemi aktif</b><br>
        Bölgesel ihtiyaç verileri başarıyla işlendi.
        </div>
        """,
        unsafe_allow_html=True
    )

with status_col2:

    st.markdown(
        """
        <div class="success-box">
        <b>✓ Dağıtım algoritması aktif</b><br>
        Kaynak önceliklendirme işlemi tamamlandı.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CSV İNDİRME
# ============================================================

st.divider()

st.subheader("⬇️ Rapor")

csv_data = allocation_df.to_csv(
    index=False
).encode("utf-8-sig")


st.download_button(
    label="📥 Kaynak Dağıtım Raporunu İndir",
    data=csv_data,
    file_name="afad_x_kaynak_dagitimi.csv",
    mime="text/csv"
)


# ============================================================
# ALT BİLGİ
# ============================================================

st.divider()

st.caption(
    "🚨 AFAD-X | Eğitim ve prototip amaçlı karar destek sistemi"
)

st.caption(
    "Not: Bu uygulamadaki hesaplamalar gerçek afet operasyonlarında "
    "tek başına karar verme amacıyla kullanılmamalıdır."
)
