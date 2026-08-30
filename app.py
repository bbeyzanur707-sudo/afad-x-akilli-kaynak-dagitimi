from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


# ============================================================
# ÖRNEK HASTANELER
# Veri setini daha sonra buraya / CSV'ye bağlayacağız.
# ============================================================

HOSPITALS = [
    {
        "id": "H001",
        "name": "Hatay Eğitim ve Araştırma Hastanesi",
        "lat": 36.2023,
        "lon": 36.1600,
        "capacity": 78,
        "staff_load": 72,
        "beds_available": 110
    },
    {
        "id": "H002",
        "name": "Defne Devlet Hastanesi",
        "lat": 36.2160,
        "lon": 36.1400,
        "capacity": 62,
        "staff_load": 58,
        "beds_available": 85
    },
    {
        "id": "H003",
        "name": "Hatay Mustafa Kemal Üniversitesi Hastanesi",
        "lat": 36.3610,
        "lon": 36.1800,
        "capacity": 70,
        "staff_load": 65,
        "beds_available": 70
    },
    {
        "id": "H004",
        "name": "İskenderun Devlet Hastanesi",
        "lat": 36.5800,
        "lon": 36.1700,
        "capacity": 84,
        "staff_load": 81,
        "beds_available": 35
    }
]


# ============================================================
# ÖRNEK AMBULANSLAR
# ============================================================

AMBULANCES = [
    {
        "id": "A001",
        "name": "Ambulans 01",
        "lat": 36.2000,
        "lon": 36.1700,
        "status": "Müsait"
    },
    {
        "id": "A002",
        "name": "Ambulans 02",
        "lat": 36.1900,
        "lon": 36.1700,
        "status": "Müsait"
    },
    {
        "id": "A003",
        "name": "Ambulans 03",
        "lat": 36.2200,
        "lon": 36.1500,
        "status": "Müsait"
    }
]


# ============================================================
# ANA SAYFA
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# DASHBOARD VERİLERİ
# ============================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard():

    return jsonify({
        "hospitals": HOSPITALS,
        "ambulances": AMBULANCES
    })


# ============================================================
# NORMALİZASYON
# ============================================================

def normalize(values):

    if not values:
        return []

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [50 for _ in values]

    return [
        ((value - minimum) / (maximum - minimum)) * 100
        for value in values
    ]


# ============================================================
# AFET BÖLGESİ ANALİZİ
# ============================================================

@app.route("/api/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Veri gönderilmedi."
        }), 400

    regions = data.get("regions", [])
    total_resource = float(
        data.get("total_resource", 0)
    )

    if not regions:
        return jsonify({
            "error": "En az bir afet bölgesi gerekli."
        }), 400


    populations = [
        float(region.get("population", 0))
        for region in regions
    ]

    needs = [
        float(region.get("need", 0))
        for region in regions
    ]


    population_scores = normalize(populations)
    need_scores = normalize(needs)


    results = []


    for i, region in enumerate(regions):

        severity = float(
            region.get("severity", 0)
        )

        population_score = population_scores[i]
        need_score = need_scores[i]


        # Öncelik:
        # %
