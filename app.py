from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import io
import numpy as np
import os
import uuid


# =============================================================================
# FLASK UYGULAMASI
# =============================================================================

app = Flask(__name__)

# Maksimum dosya boyutu: 16 MB
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Yüklenen dosyaların kaydedileceği klasör
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Klasör yoksa oluştur
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =============================================================================
# İZİN VERİLEN DOSYA UZANTILARI
# =============================================================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):
    """
    Dosya uzantısının izin verilen türlerden biri olup olmadığını kontrol eder.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =============================================================================
# GÖRÜNTÜ ANALİZİ
# =============================================================================

def analiz_et(image_bytes):
    """
    Görüntü üzerinde basit RGB tabanlı analiz yapar.

    NOT:
    Bu gerçek bir yapay zeka hastalık teşhis sistemi değildir.
    Eğitim/demo amaçlı basit bir görüntü analizidir.
    """

    try:

        # ---------------------------------------------------------------------
        # Görüntüyü aç
        # ---------------------------------------------------------------------

        img = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        # Orijinal görüntü boyutu
        orijinal_genislik, orijinal_yukseklik = img.size

        # ---------------------------------------------------------------------
        # Analiz için standart boyuta getir
        # ---------------------------------------------------------------------

        img_resized = img.resize(
            (224, 224)
        )

        # ---------------------------------------------------------------------
        # NumPy dizisine dönüştür
        # ---------------------------------------------------------------------

        img_array = np.asarray(
            img_resized,
            dtype=np.float32
        )

        # ---------------------------------------------------------------------
        # Ortalama RGB değerleri
        # ---------------------------------------------------------------------

        ortalama_renk = np.mean(
            img_array,
            axis=(0, 1)
        )

        r = float(ortalama_renk[0])
        g = float(ortalama_renk[1])
        b = float(ortalama_renk[2])

        # ---------------------------------------------------------------------
        # Renk toplamı
        # ---------------------------------------------------------------------

        toplam = r + g + b

        if toplam <= 0:

            return {
                "hata": "Görüntünün renk değerleri analiz edilemedi."
            }

        # ---------------------------------------------------------------------
        # RGB yüzdeleri
        # ---------------------------------------------------------------------

        r_oran = (r / toplam) * 100
        g_oran = (g / toplam) * 100
        b_oran = (b / toplam) * 100

        # ---------------------------------------------------------------------
        # Basit analiz
        # ---------------------------------------------------------------------

        if g > r and g > b:

            durum = "Sağlıklı Doku"

            skor = g_oran

            detay = (
                "Görüntüde yeşil renk baskın görünüyor. "
                "Bu sonuç normal veya sağlıklı pigmentasyon "
                "ile uyumlu olabilir."
            )

        elif r > g and r > b:

            durum = "Enfeksiyon / Nekroz Belirtisi"

            skor = r_oran

            detay = (
                "Görüntüde kırmızı renk baskın görünüyor. "
                "Kızarıklık, kuruma veya doku değişikliği "
                "bulunabilir."
            )

        else:

            durum = "Mantar / Lekelenme Riski"

            skor = b_oran

            detay = (
                "Görüntüde belirgin bir yeşil veya kırmızı "
                "baskınlığı bulunmuyor. Renk değişikliği, "
                "lekelenme veya başka bir anormallik "
                "bulunabilir."
            )

        # ---------------------------------------------------------------------
        # Sonuç
        # ---------------------------------------------------------------------

        return {

            "durum": durum,

            "guven_skoru": f"%{skor:.2f}",

            "detay": detay,

            "boyut": (
                f"{orijinal_genislik}x"
                f"{orijinal_yukseklik}"
            ),

            "rgb": {

                "kirmizi": round(r, 2),

                "yesil": round(g, 2),

                "mavi": round(b, 2)

            }

        }

    except UnidentifiedImageError:

        return {
            "hata": "Yüklenen dosya geçerli bir görüntü değil."
        }

    except Exception as e:

        return {
            "hata": (
                "Görüntü analiz edilirken hata oluştu: "
                f"{str(e)}"
            )
        }


# =============================================================================
# ANA SAYFA
# =============================================================================

@app.route("/", methods=["GET", "POST"])
def index():

    # -------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------

    if request.method == "GET":

        return render_template(
            "index.html"
        )

    # -------------------------------------------------------------------------
    # POST - Dosya kontrolü
    # -------------------------------------------------------------------------

    if "file" not in request.files:

        return render_template(
            "index.html",
            hata="Formda dosya bulunamadı."
        )

    file = request.files["file"]

    # -------------------------------------------------------------------------
    # Dosya seçilmiş mi?
    # -------------------------------------------------------------------------

    if file.filename == "":

        return render_template(
            "index.html",
            hata="Herhangi bir resim seçilmedi."
        )

    # -------------------------------------------------------------------------
    # Uzantı kontrolü
    # -------------------------------------------------------------------------

    if not allowed_file(file.filename):

        return render_template(
            "index.html",
            hata=(
                "Geçersiz dosya formatı! "
                "Sadece PNG, JPG ve JPEG dosyaları "
                "yükleyebilirsiniz."
            )
        )

    # -------------------------------------------------------------------------
    # Dosyayı oku
    # -------------------------------------------------------------------------

    try:

        file_bytes = file.read()

    except Exception as e:

        return render_template(
            "index.html",
            hata=f"Dosya okunamadı: {str(e)}"
        )

    # -------------------------------------------------------------------------
    # Boş dosya kontrolü
    # -------------------------------------------------------------------------

    if not file_bytes:

        return render_template(
            "index.html",
            hata="Yüklenen dosya boş."
        )

    # -------------------------------------------------------------------------
    # Gerçek görüntü dosyası mı?
    # -------------------------------------------------------------------------

    try:

        image = Image.open(
            io.BytesIO(file_bytes)
        )

        # Dosyanın gerçekten okunabilir olduğunu kontrol et
        image.verify()

        # verify sonrasında görüntüyü yeniden aç
        image = Image.open(
            io.BytesIO(file_bytes)
        ).convert("RGB")

    except UnidentifiedImageError:

        return render_template(
            "index.html",
            hata="Dosya geçerli bir görüntü değil."
        )

    except Exception as e:

        return render_template(
            "index.html",
            hata=f"Görüntü dosyası okunamadı: {str(e)}"
        )

    # -------------------------------------------------------------------------
    # Görüntüyü analiz et
    # -------------------------------------------------------------------------

    analiz_sonucu = analiz_et(
        file_bytes
    )

    # -------------------------------------------------------------------------
    # Benzersiz dosya adı
    # -------------------------------------------------------------------------

    guvenli_dosya_adi = secure_filename(
        file.filename
    )

    if "." in guvenli_dosya_adi:

        uzanti = guvenli_dosya_adi.rsplit(
            ".",
            1
        )[1].lower()

    else:

        uzanti = "jpg"

    # UUID kullanarak benzersiz isim oluştur
    yeni_dosya_adi = (
        f"{uuid.uuid4().hex}.{uzanti}"
    )

    # -------------------------------------------------------------------------
    # Dosya yolu
    # -------------------------------------------------------------------------

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        yeni_dosya_adi
    )

    # -------------------------------------------------------------------------
    # Görüntüyü kaydet
    # -------------------------------------------------------------------------

    try:

        # JPEG olarak kaydet
        image.save(
            filepath,
            "JPEG",
            quality=90
        )

    except Exception as e:

        return render_template(
            "index.html",
            hata=(
                "Görüntü kaydedilemedi: "
                f"{str(e)}"
            )
        )

    # -------------------------------------------------------------------------
    # Tarayıcıda gösterilecek URL
    # -------------------------------------------------------------------------

    resim_yolu = url_for(
        "static",
        filename=f"uploads/{yeni_dosya_adi}"
    )

    # -------------------------------------------------------------------------
    # Sonucu gönder
    # -------------------------------------------------------------------------

    return render_template(
        "index.html",
        sonuc=analiz_sonucu,
        resim_yolu=resim_yolu
    )


# =============================================================================
# DOSYA ÇOK BÜYÜK HATASI
# =============================================================================

@app.errorhandler(413)
def dosya_cok_buyuk(error):

    return render_template(
        "index.html",
        hata=(
            "Dosya çok büyük! "
            "Maksimum dosya boyutu 16 MB olabilir."
        )
    ), 413


# =============================================================================
# GENEL HATA YAKALAMA
# =============================================================================

@app.errorhandler(500)
def sunucu_hatasi(error):

    return render_template(
        "index.html",
        hata=(
            "Sunucu tarafında beklenmeyen "
            "bir hata oluştu."
        )
    ), 500


# =============================================================================
# UYGULAMAYI BAŞLAT
# =============================================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
