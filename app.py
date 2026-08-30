from flask import Flask, render_template, request, jsonify
import os
import json


# =============================================================================
# UYGULAMA
# =============================================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "afet-x-gelistirme-anahtari"
)


# =============================================================================
# SABİTLER
# =============================================================================

AFET_AGIRLIK = 0.50
NUFUS_AGIRLIK = 0.20
IHTIYAC_AGIRLIK = 0.30


# =============================================================================
# SAYI KONTROLÜ
# =============================================================================

def pozitif_sayi(deger, alan):
    """
    Değeri pozitif sayıya dönüştürür.
    """

    try:
        deger = float(str(deger).replace(",", "."))

    except (ValueError, TypeError):

        raise ValueError(
            f"{alan} geçerli bir sayı olmalıdır."
        )

    if deger < 0:

        raise ValueError(
            f"{alan} negatif olamaz."
        )

    return deger


# =============================================================================
# NORMALİZASYON
# =============================================================================

def normalize_et(deger, maksimum):
    """
    Bir değeri 0-100 arasına dönüştürür.
    """

    if maksimum <= 0:
        return 0

    return (deger / maksimum) * 100


# =============================================================================
# ÖNCELİK SEVİYESİ
# =============================================================================

def oncelik_seviyesi(skor):

    if skor >= 80:
        return "Çok Yüksek"

    if skor >= 60:
        return "Yüksek"

    if skor >= 40:
        return "Orta"

    return "Düşük"


# =============================================================================
# ÖNCELİK RENGİ
# =============================================================================

def oncelik_sinifi(skor):

    if skor >= 80:
        return "cok-yuksek"

    if skor >= 60:
        return "yuksek"

    if skor >= 40:
        return "orta"

    return "dusuk"


# =============================================================================
# BÖLGELERİ ANALİZ ET
# =============================================================================

def bolgeleri_analiz_et(bolgeler, toplam_kaynak):
    """
    Tüm afet bölgelerini analiz eder.

    Formül:

    Skor =
    Afet Şiddeti * 0.50
    +
    Normalize Nüfus * 0.20
    +
    Normalize İhtiyaç * 0.30
    """

    if not bolgeler:

        raise ValueError(
            "En az bir afet bölgesi eklemelisiniz."
        )

    # -------------------------------------------------------------------------
    # Maksimum değerler
    # -------------------------------------------------------------------------

    maksimum_nufus = max(
        bolge["nufus"]
        for bolge in bolgeler
    )

    maksimum_ihtiyac = max(
        bolge["ihtiyac"]
        for bolge in bolgeler
    )

    # -------------------------------------------------------------------------
    # Skorları hesapla
    # -------------------------------------------------------------------------

    for bolge in bolgeler:

        nufus_normalize = normalize_et(
            bolge["nufus"],
            maksimum_nufus
        )

        ihtiyac_normalize = normalize_et(
            bolge["ihtiyac"],
            maksimum_ihtiyac
        )

        afet_puani = (
            bolge["afet_siddeti"]
        )

        skor = (
            (afet_puani * AFET_AGIRLIK)
            +
            (nufus_normalize * NUFUS_AGIRLIK)
            +
            (ihtiyac_normalize * IHTIYAC_AGIRLIK)
        )

        bolge["nufus_normalize"] = round(
            nufus_normalize,
            2
        )

        bolge["ihtiyac_normalize"] = round(
            ihtiyac_normalize,
            2
        )

        bolge["skor"] = round(
            skor,
            2
        )

        bolge["seviye"] = oncelik_seviyesi(
            skor
        )

        bolge["sinif"] = oncelik_sinifi(
            skor
        )

    # -------------------------------------------------------------------------
    # Skora göre sırala
    # -------------------------------------------------------------------------

    bolgeler.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    # -------------------------------------------------------------------------
    # Sıralama numarası
    # -------------------------------------------------------------------------

    for index, bolge in enumerate(
        bolgeler,
        start=1
    ):

        bolge["sira"] = index

    # -------------------------------------------------------------------------
    # Toplam skor
    # -------------------------------------------------------------------------

    toplam_skor = sum(
        bolge["skor"]
        for bolge in bolgeler
    )

    # -------------------------------------------------------------------------
    # Kaynak dağıtımı
    # -------------------------------------------------------------------------

    for bolge in bolgeler:

        if toplam_skor > 0:

            kaynak_orani = (
                bolge["skor"]
                / toplam_skor
            )

        else:

            kaynak_orani = (
                1 / len(bolgeler)
            )

        bolge["kaynak_orani"] = round(
            kaynak_orani * 100,
            2
        )

        bolge["tahmini_kaynak"] = round(
            toplam_kaynak * kaynak_orani,
            2
        )

    return bolgeler


# =============================================================================
# ANA SAYFA
# =============================================================================

@app.route("/", methods=["GET", "POST"])
def index():

    bolgeler = []
    toplam_kaynak = 0
    hata = None
    analiz_yapildi = False

    if request.method == "POST":

        try:

            # -----------------------------------------------------------------
            # Toplam kaynak
            # -----------------------------------------------------------------

            toplam_kaynak = pozitif_sayi(
                request.form.get(
                    "toplam_kaynak",
                    0
                ),
                "Toplam kaynak"
            )

            if toplam_kaynak <= 0:

                raise ValueError(
                    "Toplam kaynak 0'dan büyük olmalıdır."
                )

            # -----------------------------------------------------------------
            # JSON olarak gönderilen bölgeleri al
            # -----------------------------------------------------------------

            bolge_json = request.form.get(
                "bolgeler_json",
                ""
            )

            if not bolge_json:

                raise ValueError(
                    "Afet bölgesi eklenmedi."
                )

            try:

                girilen_bolgeler = json.loads(
                    bolge_json
                )

            except json.JSONDecodeError:

                raise ValueError(
                    "Bölge verileri okunamadı."
                )

            if not isinstance(
                girilen_bolgeler,
                list
            ):

                raise ValueError(
                    "Bölge verileri geçersiz."
                )

            # -----------------------------------------------------------------
            # Bölge verilerini temizle
            # -----------------------------------------------------------------

            for index, veri in enumerate(
                girilen_bolgeler,
                start=1
            ):

                ad = str(
                    veri.get(
                        "ad",
                        ""
                    )
                ).strip()

                if not ad:

                    raise ValueError(
                        f"{index}. bölgenin adı boş."
                    )

                afet_siddeti = pozitif_sayi(
                    veri.get(
                        "afet_siddeti",
                        0
                    ),
                    f"{ad} - Afet Şiddeti"
                )

                nufus = pozitif_sayi(
                    veri.get(
                        "nufus",
                        0
                    ),
                    f"{ad} - Nüfus"
                )

                ihtiyac = pozitif_sayi(
                    veri.get(
                        "ihtiyac",
                        0
                    ),
                    f"{ad} - İhtiyaç"
                )

                if afet_siddeti > 100:

                    raise ValueError(
                        f"{ad} için afet şiddeti "
                        "100'den büyük olamaz."
                    )

                if nufus <= 0:

                    raise ValueError(
                        f"{ad} için nüfus 0'dan büyük olmalıdır."
                    )

                if ihtiyac <= 0:

                    raise ValueError(
                        f"{ad} için ihtiyaç 0'dan büyük olmalıdır."
                    )

                bolgeler.append({

                    "ad": ad,

                    "afet_siddeti": round(
                        afet_siddeti,
                        2
                    ),

                    "nufus": round(
                        nufus,
                        2
                    ),

                    "ihtiyac": round(
                        ihtiyac,
                        2
                    )

                })

            # -----------------------------------------------------------------
            # Analiz
            # -----------------------------------------------------------------

            bolgeler = bolgeleri_analiz_et(
                bolgeler,
                toplam_kaynak
            )

            analiz_yapildi = True

        except ValueError as e:

            hata = str(e)

        except Exception as e:

            hata = (
                "Beklenmeyen bir hata oluştu: "
                + str(e)
            )

    return render_template(
        "index.html",
        bolgeler=bolgeler,
        toplam_kaynak=toplam_kaynak,
        hata=hata,
        analiz_yapildi=analiz_yapildi
    )


# =============================================================================
# JSON API
# =============================================================================

@app.route("/api/health")
def health():

    return jsonify({

        "status": "ok",

        "project": (
            "Afet-X Akıllı Kaynak Dağıtımı"
        ),

        "version": "2.0"

    })


@app.route("/api/hesapla", methods=["POST"])
def api_hesapla():

    try:

        veri = request.get_json()

        if not veri:

            return jsonify({
                "basarili": False,
                "hata": "JSON verisi gönderilmedi."
            }), 400

        toplam_kaynak = pozitif_sayi(
            veri.get(
                "toplam_kaynak",
                0
            ),
            "Toplam kaynak"
        )

        bolgeler = veri.get(
            "bolgeler",
            []
        )

        temiz_bolgeler = []

        for bolge in bolgeler:

            ad = str(
                bolge.get(
                    "ad",
                    ""
                )
            ).strip()

            afet_siddeti = pozitif_sayi(
                bolge.get(
                    "afet_siddeti",
                    0
                ),
                "Afet Şiddeti"
            )

            nufus = pozitif_sayi(
                bolge.get(
                    "nufus",
                    0
                ),
                "Nüfus"
            )

            ihtiyac = pozitif_sayi(
                bolge.get(
                    "ihtiyac",
                    0
                ),
                "İhtiyaç"
            )

            if not ad:
                raise ValueError(
                    "Bölge adı boş olamaz."
                )

            if afet_siddeti > 100:
                raise ValueError(
                    "Afet şiddeti 100'den büyük olamaz."
                )

            temiz_bolgeler.append({

                "ad": ad,

                "afet_siddeti": afet_siddeti,

                "nufus": nufus,

                "ihtiyac": ihtiyac

            })

        sonuc = bolgeleri_analiz_et(
            temiz_bolgeler,
            toplam_kaynak
        )

        return jsonify({

            "basarili": True,

            "toplam_kaynak": toplam_kaynak,

            "bolge_sayisi": len(sonuc),

            "sonuclar": sonuc

        })

    except ValueError as e:

        return jsonify({

            "basarili": False,

            "hata": str(e)

        }), 400

    except Exception as e:

        return jsonify({

            "basarili": False,

            "hata": (
                "Sunucu hatası: "
                + str(e)
            )

        }), 500


# =============================================================================
# UYGULAMA
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
