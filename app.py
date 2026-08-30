from flask import Flask, render_template, request
import os


# =============================================================================
# FLASK UYGULAMASI
# =============================================================================

app = Flask(__name__)


# =============================================================================
# UYGULAMA AYARLARI
# =============================================================================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "afad-x-gelistirme-anahtari"
)


# =============================================================================
# ÖNCELİK SKORU HESAPLAMA
# =============================================================================

def oncelik_skoru_hesapla(afet_siddeti, nufus, ihtiyac_miktari):
    """
    Afet bölgesinin öncelik skorunu hesaplar.

    Ağırlıklar:
    - Afet Şiddeti: %50
    - Nüfus: %20
    - İhtiyaç Miktarı: %30

    Tüm değerlerin 0-100 arasında olması beklenir.
    """

    skor = (
        (afet_siddeti * 0.50)
        + (nufus * 0.20)
        + (ihtiyac_miktari * 0.30)
    )

    return round(skor, 2)


# =============================================================================
# ÖNCELİK SEVİYESİ
# =============================================================================

def oncelik_seviyesi_belirle(skor):
    """
    Hesaplanan skora göre öncelik seviyesini belirler.
    """

    if skor >= 80:
        return "Çok Yüksek"

    elif skor >= 60:
        return "Yüksek"

    elif skor >= 40:
        return "Orta"

    else:
        return "Düşük"


# =============================================================================
# KAYNAK DAĞITIMI
# =============================================================================

def kaynak_dagit(sonuclar, toplam_kaynak):
    """
    Toplam kaynağı bölgelerin öncelik skorlarına göre dağıtır.

    Her bölgenin aldığı kaynak:
    
    Bölge Skoru / Toplam Skor × Toplam Kaynak
    """

    if not sonuclar:
        return []

    toplam_skor = sum(
        sonuc["skor"]
        for sonuc in sonuclar
    )

    if toplam_skor <= 0:
        return sonuclar

    for sonuc in sonuclar:

        pay = (
            sonuc["skor"]
            / toplam_skor
        )

        sonuc["kaynak_orani"] = round(
            pay * 100,
            2
        )

        sonuc["tahmini_kaynak"] = round(
            toplam_kaynak * pay,
            2
        )

    return sonuclar


# =============================================================================
# FORM VERİSİ KONTROLÜ
# =============================================================================

def sayi_al(form, alan_adi):
    """
    Formdan sayısal değer alır.
    """

    try:

        return float(
            form.get(alan_adi, "").replace(",", ".")
        )

    except (ValueError, AttributeError):

        raise ValueError(
            f"{alan_adi} alanı geçerli bir sayı olmalıdır."
        )


def yuzluk_deger_kontrol(deger, alan_adi):
    """
    Değerin 0-100 arasında olup olmadığını kontrol eder.
    """

    if deger < 0 or deger > 100:

        raise ValueError(
            f"{alan_adi} 0 ile 100 arasında olmalıdır."
        )


# =============================================================================
# ANA SAYFA
# =============================================================================

@app.route("/", methods=["GET", "POST"])
def index():

    sonuc = None
    hata = None

    if request.method == "POST":

        try:

            # -------------------------------------------------------------
            # Form bilgilerini al
            # -------------------------------------------------------------

            bolge_adi = request.form.get(
                "bolge_adi",
                ""
            ).strip()

            if not bolge_adi:

                raise ValueError(
                    "Afet bölgesi adı boş bırakılamaz."
                )

            # -------------------------------------------------------------
            # Değerleri al
            # -------------------------------------------------------------

            afet_siddeti = sayi_al(
                request.form,
                "afet_siddeti"
            )

            nufus = sayi_al(
                request.form,
                "nufus"
            )

            ihtiyac_miktari = sayi_al(
                request.form,
                "ihtiyac_miktari"
            )

            toplam_kaynak = sayi_al(
                request.form,
                "toplam_kaynak"
            )

            # -------------------------------------------------------------
            # Değerleri kontrol et
            # -------------------------------------------------------------

            yuzluk_deger_kontrol(
                afet_siddeti,
                "Afet Şiddeti"
            )

            yuzluk_deger_kontrol(
                nufus,
                "Nüfus"
            )

            yuzluk_deger_kontrol(
                ihtiyac_miktari,
                "İhtiyaç Miktarı"
            )

            if toplam_kaynak <= 0:

                raise ValueError(
                    "Toplam kaynak 0'dan büyük olmalıdır."
                )

            # -------------------------------------------------------------
            # Öncelik skoru
            # -------------------------------------------------------------

            skor = oncelik_skoru_hesapla(
                afet_siddeti,
                nufus,
                ihtiyac_miktari
            )

            seviye = oncelik_seviyesi_belirle(
                skor
            )

            # -------------------------------------------------------------
            # Sonuç
            # -------------------------------------------------------------

            sonuc = {
                "bolge_adi": bolge_adi,

                "afet_siddeti": afet_siddeti,

                "nufus": nufus,

                "ihtiyac_miktari": ihtiyac_miktari,

                "toplam_kaynak": toplam_kaynak,

                "skor": skor,

                "seviye": seviye
            }

            # -------------------------------------------------------------
            # Tek bölge için kaynak miktarı
            #
            # Tek bölge olduğundan mevcut kaynağın tamamı
            # bu bölgeye ayrılır.
            # -------------------------------------------------------------

            sonuc["kaynak_orani"] = 100

            sonuc["tahmini_kaynak"] = toplam_kaynak

        except ValueError as e:

            hata = str(e)

        except Exception as e:

            hata = (
                "Beklenmeyen bir hata oluştu: "
                + str(e)
            )

    return render_template(
        "index.html",
        sonuc=sonuc,
        hata=hata
    )


# =============================================================================
# SAĞLIK KONTROLÜ
# =============================================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "project": "Afet-X Akıllı Kaynak Dağıtımı"
    }


# =============================================================================
# UYGULAMAYI ÇALIŞTIR
# =============================================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
