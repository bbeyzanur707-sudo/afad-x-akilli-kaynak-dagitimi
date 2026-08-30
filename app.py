from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)


# -------------------------------------------------
# ÖRNEK HASTANELER
# Gerçek projede bu bilgiler resmi verilerle
# güncellenebilir.
# -------------------------------------------------

HOSPITALS = [
    {
        "id": 1,
        "name": "Hatay Şehir Hastanesi",
        "lat": 36.2023,
        "lon": 36.1600,
        "capacity": 78,
        "staff_load": 72,
        "beds_available": 110
    },
    {
        "id": 2,
        "name": "Hatay Eğitim ve Araştırma Hastanesi",
        "lat": 36.1980,
        "lon": 36.1500,
        "capacity": 61,
        "staff_load": 55,
        "beds_available": 185
    },
    {
        "id": 3,
        "name": "Defne Devlet Hastanesi",
        "lat": 36.2160,
        "lon": 36.1400,
        "capacity": 42,
        "staff_load": 35,
        "beds_available": 260
    }
]


# -------------------------------------------------
# ÖRNEK AMBULANSLAR
# -------------------------------------------------

AMBULANCES = [
    {
        "id": "AMB-01",
        "name": "Ambulans 01",
        "lat": 36.2100,
        "lon": 36.1450,
        "status": "Müsait"
    },
    {
        "id": "AMB-02",
        "name": "Ambulans 02",
        "lat": 36.1900,
        "lon": 36.1700,
        "status": "Müsait"
    },
    {
        "id": "AMB-03",
        "name": "Ambulans 03",
        "lat": 36.2200,
        "lon": 36.1250,
        "status": "Görevde"
    }
]


# -------------------------------------------------
# NORMALİZASYON
# -------------------------------------------------

def normalize(values):

    if not values:
        return []

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [50 for _ in values]

    return [
        ((value - minimum) /
         (maximum - minimum)) * 100
        for value in values
    ]


# -------------------------------------------------
# AFET BÖLGESİ ANALİZİ
# -------------------------------------------------

def analyze_regions(regions, total_resource):

    populations = [
        float(region.get("population", 0))
        for region in regions
    ]

    needs = [
        float(region.get("need", 0))
        for region in regions
    ]

    normalized_population = normalize(
        populations
    )

    normalized_need = normalize(
        needs
    )

    results = []

    for index, region in enumerate(regions):

        severity = float(
            region.get("severity", 0)
        )

        priority = (
            severity * 0.50
            + normalized_population[index] * 0.20
            + normalized_need[index] * 0.30
        )

        results.append({
            "name": region.get(
                "name",
                "Bilinmeyen Bölge"
            ),

            "severity": round(
                severity,
                2
            ),

            "population":
                populations[index],

            "need":
                needs[index],

            "priority":
                round(priority, 2),

            "lat":
                region.get("lat"),

            "lon":
                region.get("lon")
        })

    total_priority = sum(
        item["priority"]
        for item in results
    )

    for item in results:

        if total_priority > 0:
            share = (
                item["priority"]
                / total_priority
            )
        else:
            share = 0

        item["percentage"] = round(
            share * 100,
            2
        )

        item["allocated_resource"] = round(
            total_resource * share,
            2
        )

        if item["priority"] >= 75:
            item["status"] = "Kritik"

        elif item["priority"] >= 50:
            item["status"] = "Acil"

        elif item["priority"] >= 25:
            item["status"] = "Orta"

        else:
            item["status"] = "Düşük"

    results.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    return results


# -------------------------------------------------
# YAPAY ZEKA TARZI ÖNERİ
# -------------------------------------------------

def generate_recommendation(results):

    if not results:
        return "Analiz yapılacak bölge bulunamadı."

    top = results[0]

    if top["status"] == "Kritik":

        return (
            f"{top['name']} bölgesi kritik "
            f"önceliktedir. Öncelik puanı "
            f"{top['priority']}/100. "
            f"Kaynakların yaklaşık "
            f"%{top['percentage']} oranının "
            f"bu bölgeye yönlendirilmesi "
            f"önerilmektedir."
        )

    if top["status"] == "Acil":

        return (
            f"{top['name']} bölgesi acil "
            f"müdahale gerektiriyor. "
            f"Öncelik puanı "
            f"{top['priority']}/100."
        )

    return (
        f"{top['name']} mevcut veriler "
        f"içinde en yüksek önceliğe "
        f"sahiptir."
    )


# -------------------------------------------------
# ANA SAYFA
# -------------------------------------------------

@app.route("/")
def index():

    return render_template(
        "index.html",
        hospitals=HOSPITALS,
        ambulances=AMBULANCES
    )


# -------------------------------------------------
# AFET ANALİZİ
# -------------------------------------------------

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
                "Veri alınamadı."
        }), 400

    regions = data.get(
        "regions",
        []
    )

    try:

        total_resource = float(
            data.get(
                "total_resource",
                0
            )
        )

    except (ValueError, TypeError):

        return jsonify({
            "error":
                "Kaynak miktarı geçersiz."
        }), 400

    if total_resource <= 0:

        return jsonify({
            "error":
                "Toplam kaynak 0'dan büyük olmalıdır."
        }), 400

    if not regions:

        return jsonify({
            "error":
                "En az bir afet bölgesi ekleyin."
        }), 400

    results = analyze_regions(
        regions,
        total_resource
    )

    critical_count = sum(
        1
        for item in results
        if item["status"] == "Kritik"
    )

    average_priority = (
        sum(
            item["priority"]
            for item in results
        )
        / len(results)
    )

    return jsonify({

        "results":
            results,

        "critical_count":
            critical_count,

        "average_priority":
            round(
                average_priority,
                2
            ),

        "ai_recommendation":
            generate_recommendation(
                results
            )
    })


# -------------------------------------------------
# HASTANELER
# -------------------------------------------------

@app.route("/hospitals")
def hospitals():

    return jsonify(
        HOSPITALS
    )


# -------------------------------------------------
# AMBULANSLAR
# -------------------------------------------------

@app.route("/ambulances")
def ambulances():

    return jsonify(
        AMBULANCES
    )


# -------------------------------------------------
# ROTA HESAPLAMA
#
# OSRM açık rota servisi kullanılır.
# Prototip için uygundur.
# -------------------------------------------------

@app.route(
    "/route",
    methods=["POST"]
)
def route():

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
                "Rota bilgisi bulunamadı."
        }), 400

    try:

        start_lat = float(
            data["start_lat"]
        )

        start_lon = float(
            data["start_lon"]
        )

        end_lat = float(
            data["end_lat"]
        )

        end_lon = float(
            data["end_lon"]
        )

    except (
        KeyError,
        ValueError,
        TypeError
    ):

        return jsonify({
            "error":
                "Konum bilgileri geçersiz."
        }), 400


    url = (
        "https://router.project-osrm.org/"
        f"route/v1/driving/"
        f"{start_lon},{start_lat};"
