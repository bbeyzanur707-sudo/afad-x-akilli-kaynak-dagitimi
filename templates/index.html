from flask import Flask, render_template, request, jsonify
import math
import requests

app = Flask(__name__)


# =========================================================
# HASTANELER
# =========================================================

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


# =========================================================
# AMBULANSLAR
# =========================================================

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


# =========================================================
# YARDIM MALZEMELERİ
# =========================================================

RESOURCE_TYPES = [
    "Su",
    "Gıda",
    "İlaç",
    "Tıbbi Malzeme",
    "Çadır",
    "Jeneratör"
]


# =========================================================
# NORMALİZASYON
# =========================================================

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


# =========================================================
# AFET ANALİZİ
# =========================================================

def analyze_regions(regions, total_resource):

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

    for index, region in enumerate(regions):

        severity = float(
            region.get("severity", 0)
        )

        priority = (
            severity * 0.50
            + population_scores[index] * 0.20
            + need_scores[index] * 0.30
        )

        results.append({
            "name": region.get("name", "Bilinmeyen Bölge"),
            "severity": round(severity, 2),
            "population": populations[index],
            "need": needs[index],
            "priority": round(priority, 2),
            "lat": region.get("lat"),
            "lon": region.get("lon")
        })

    total_priority = sum(
        item["priority"]
        for item in results
    )

    for item in results:

        if total_priority > 0:
            share = item["priority"] / total_priority
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


# =========================================================
# SİSTEM ÖNERİSİ
# =========================================================

def generate_recommendation(results):

    if not results:
        return "Analiz yapılacak bölge bulunamadı."

    top = results[0]

    return (
        f"{top['name']} bölgesi en yüksek önceliğe sahip. "
        f"Öncelik puanı {top['priority']}/100. "
        f"Kaynakların %{top['percentage']} oranının "
        f"bu bölgeye yönlendirilmesi öneriliyor."
    )


# =========================================================
# MESAFE HESABI
# =========================================================

def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# =========================================================
# OSRM ROTA
# =========================================================

def get_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon
):

    url = (
        "https://router.project-osrm.org/"
        "route/v1/driving/"
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
    )

    params = {
        "alternatives": "true",
        "overview": "full",
        "geometries": "geojson",
        "steps": "false"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=12
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            return None

        routes = []

        for route in data.get("routes", []):

            routes.append({
                "distance_km":
                    round(
                        route["distance"] / 1000,
                        2
                    ),

                "duration_min":
                    round(
                        route["duration"] / 60,
                        1
                    ),

                "geometry":
                    route.get("geometry")
            })

        return routes

    except Exception:
        return None


# =========================================================
# HASTANE UYGUNLUK PUANI
# =========================================================

def hospital_score(
    hospital,
    duration_min,
    distance_km
):

    # Daha düşük olması iyi olan değerler
    time_score = max(
        0,
        100 - duration_min * 4
    )

    distance_score = max(
        0,
        100 - distance_km * 8
    )

    capacity_score = 100 - hospital["capacity"]

    staff_score = 100 - hospital["staff_load"]

    beds_score = min(
        100,
        hospital["beds_available"] / 2
    )

    score = (
        time_score * 0.35
        + distance_score * 0.15
        + capacity_score * 0.20
        + staff_score * 0.15
        + beds_score * 0.15
    )

    return round(
        max(0, min(100, score)),
        2
    )


# =========================================================
# ANA SAYFA
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        hospitals=HOSPITALS,
        ambulances=AMBULANCES,
        resource_types=RESOURCE_TYPES
    )


# =========================================================
# AFET ANALİZİ
# =========================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Veri alınamadı."
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
            "error": "Kaynak miktarı geçersiz."
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

        "results": results,

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


# =========================================================
# HASTANELER
# =========================================================

@app.route("/hospitals")
def hospitals():

    return jsonify(HOSPITALS)


# =========================================================
# AMBULANSLAR
# =========================================================

@app.route("/ambulances")
def ambulances():

    return jsonify(AMBULANCES)


# =========================================================
# TEK ROTA
# =========================================================

@app.route(
    "/route",
    methods=["POST"]
)
def route():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Rota bilgisi bulunamadı."
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

    routes = get_route(
        start_lat,
        start_lon,
        end_lat,
        end_lon
    )

    if not routes:

        distance = haversine(
            start_lat,
            start_lon,
            end_lat,
            end_lon
        )

        estimated_time = (
            distance / 45
        ) * 60

        return jsonify({
            "source": "Tahmini",
            "routes": [{
                "distance_km":
                    round(distance, 2),
                "duration_min":
                    round(
                        estimated_time,
                        1
                    ),
                "geometry": None
            }]
        })

    return jsonify({
        "source": "OSRM",
        "routes": routes
    })


# =========================================================
# EN UYGUN HASTANE
# =========================================================

@app.route(
    "/recommend-hospital",
    methods=["POST"]
)
def recommend_hospital():

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
                "Ambulans bilgisi bulunamadı."
        }), 400

    ambulance_id = data.get(
        "ambulance_id"
    )

    ambulance = next(
        (
            a for a in AMBULANCES
            if str(a["id"]) ==
            str(ambulance_id)
        ),
        None
    )

    if not ambulance:

        return jsonify({
            "error":
                "Ambulans bulunamadı."
        }), 404

    hospital_results = []

    for hospital in HOSPITALS:

        routes = get_route(
            ambulance["lat"],
            ambulance["lon"],
            hospital["lat"],
            hospital["lon"]
        )

        if routes:

            best_route = min(
                routes,
                key=lambda r:
                r["duration_min"]
            )

            duration = best_route[
                "duration_min"
            ]

            distance = best_route[
                "distance_km"
            ]

            geometry = best_route[
                "geometry"
            ]

            route_source = "OSRM"

        else:

            distance = haversine(
                ambulance["lat"],
                ambulance["lon"],
                hospital["lat"],
                hospital["lon"]
            )

            duration = (
                distance / 45
            ) * 60

            geometry = None
            route_source = "Tahmini"

        score = hospital_score(
            hospital,
            duration,
            distance
        )

        hospital_results.append({

            "id":
                hospital["id"],

            "name":
                hospital["name"],

            "distance_km":
                round(distance, 2),

            "duration_min":
                round(duration, 1),

            "capacity":
                hospital["capacity"],

            "staff_load":
                hospital["staff_load"],

            "beds_available":
                hospital["beds_available"],

            "score":
                score,

            "route_source":
                route_source,

            "geometry":
                geometry,

            "reason": [
                f"Ulaşım süresi: {round(duration, 1)} dakika",
                f"Mesafe: {round(distance, 2)} km",
                f"Hastane doluluğu: %{hospital['capacity']}",
                f"Personel yükü: %{hospital['staff_load']}",
                f"Boş yatak: {hospital['beds_available']}"
            ]
        })

    hospital_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    best = hospital_results[0]

    return jsonify({

        "ambulance":
            ambulance,

        "recommended":
            best,

        "hospitals":
            hospital_results,

        "message":
            (
                f"{best['name']} öneriliyor. "
                f"Uygunluk puanı "
                f"{best['score']}/100."
            )
    })


# =========================================================
# SAĞLIK DURUM ÖZETİ
# =========================================================

@app.route("/health-summary")
def health_summary():

    average_capacity = (
        sum(
            h["capacity"]
            for h in HOSPITALS
        )
        / len(HOSPITALS)
    )

    average_staff = (
        sum(
            h["staff_load"]
            for h in HOSPITALS
        )
        / len(HOSPITALS)
    )

    total_beds = sum(
        h["beds_available"]
        for h in HOSPITALS
    )

    critical_hospitals = [
        h["name"]
        for h in HOSPITALS
        if (
            h["capacity"] >= 85
            or h["staff_load"] >= 85
        )
    ]

    return jsonify({

        "average_capacity":
            round(
                average_capacity,
                1
            ),

        "average_staff_load":
            round(
                average_staff,
                1
            ),

        "total_available_beds":
            total_beds,

        "critical_hospitals":
            critical_hospitals
    })


# =========================================================
# ÇALIŞTIR
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
