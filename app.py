from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# =========================================================
# ÖRNEK HASTANELER
# =========================================================

HOSPITALS = [
    {
        "id": 1,
        "name": "Hatay Şehir Hastanesi",
        "lat": 36.2023,
        "lon": 36.1600,
        "capacity": 78,
        "staff_load": 72,
        "fatigue": 72,
        "beds_available": 110
    },
    {
        "id": 2,
        "name": "Hatay Eğitim ve Araştırma Hastanesi",
        "lat": 36.1980,
        "lon": 36.1500,
        "capacity": 61,
        "staff_load": 55,
        "fatigue": 55,
        "beds_available": 185
    },
    {
        "id": 3,
        "name": "Defne Devlet Hastanesi",
        "lat": 36.2160,
        "lon": 36.1400,
        "capacity": 42,
        "staff_load": 35,
        "fatigue": 35,
        "beds_available": 260
    }
]

# =========================================================
# ÖRNEK AMBULANSLAR
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
# AFET BÖLGELERİ ANALİZİ
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

    normalized_population = normalize(populations)
    normalized_need = normalize(needs)

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

            "population": populations[index],

            "need": needs[index],

            "priority": round(
                priority,
                2
            ),

            "lat": region.get("lat"),

            "lon": region.get("lon")
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


# =========================================================
# SİSTEM ÖNERİSİ
# =========================================================

def generate_recommendation(results):

    if not results:
        return "Analiz yapılacak bölge bulunamadı."

    top = results[0]

    return (
        f"{top['name']} bölgesi en yüksek "
        f"önceliğe sahip. Öncelik puanı "
        f"{top['priority']}/100. "
        f"Kaynakların yaklaşık "
        f"%{top['percentage']} oranının "
        f"bu bölgeye yönlendirilmesi öneriliyor."
    )


# =========================================================
# ANA SAYFA
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        hospitals=HOSPITALS,
        ambulances=AMBULANCES
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

def get_osrm_route(
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
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
        "alternatives": "true"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# AMBULANS → HASTANE ROTA ANALİZİ
# =========================================================

@app.route(
    "/hospital-recommendation",
    methods=["POST"]
)
def hospital_recommendation():

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
            if a["id"] == ambulance_id
        ),
        None
    )

    if not ambulance:

        return jsonify({
            "error":
                "Ambulans bulunamadı."
        }), 404

    if ambulance["status"] != "Müsait":

        return jsonify({
            "error":
                "Seçilen ambulans şu anda görevde."
        }), 400

    candidates = []

    for hospital in HOSPITALS:

        try:

            route_data = get_osrm_route(
                ambulance["lat"],
                ambulance["lon"],
                hospital["lat"],
                hospital["lon"]
            )

            routes = route_data.get(
                "routes",
                []
            )

            if not routes:
                continue

            best_route = min(
                routes,
                key=lambda r: r["duration"]
            )

            duration_minutes = (
                best_route["duration"] / 60
            )

            distance_km = (
                best_route["distance"] / 1000
            )

            # -------------------------------------------------
            # HASTANE UYGUNLUK PUANI
            #
            # Süre          %45
            # Boş yatak     %25
            # Doluluk       %15
            # Yorgunluk     %15
            # -------------------------------------------------

            time_score = max(
                0,
                100 - duration_minutes * 3
            )

            bed_score = min(
                hospital["beds_available"] / 300 * 100,
                100
            )

            occupancy_score = (
                100 - hospital["capacity"]
            )

            fatigue_score = (
                100 - hospital["fatigue"]
            )

            suitability = (
                time_score * 0.45
                + bed_score * 0.25
                + occupancy_score * 0.15
                + fatigue_score * 0.15
            )

            candidates.append({

                "hospital": hospital,

                "duration_minutes":
                    round(
                        duration_minutes,
                        1
                    ),

                "distance_km":
                    round(
                        distance_km,
                        2
                    ),

                "suitability":
                    round(
                        suitability,
                        2
                    ),

                "route": best_route,

                "alternatives":
                    routes
            })

        except Exception as error:

            print(
                "Rota hatası:",
                error
            )

    if not candidates:

        return jsonify({
            "error":
                "Rota hesaplanamadı. Harita servisi şu anda kullanılamıyor."
        }), 503

    candidates.sort(
        key=lambda x:
            x["suitability"],
        reverse=True
    )

    best = candidates[0]

    return jsonify({

        "ambulance": ambulance,

        "recommended": best,

        "hospitals": candidates,

        "message": (
            f"{best['hospital']['name']} "
            f"öneriliyor. Tahmini ulaşım "
            f"süresi {best['duration_minutes']} dakika."
        )
    })


# =========================================================
# SAĞLIK DURUMU
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "project": "Afet-X",
        "version": "2.0"
    })


# =========================================================
# UYGULAMAYI ÇALIŞTIR
# =========================================================

if __name__ == "__main__":

    port = 5000

    try:
        import os

        port = int(
            os.environ.get(
                "PORT",
                5000
            )
        )

    except Exception:
        pass

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
