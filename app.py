from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)


def calculate_priority(region):
    """
    Afet bölgesinin öncelik puanını hesaplar.

    Afet şiddeti: %50
    Nüfus: %20
    İhtiyaç: %30
    """

    try:
        severity = float(region.get("severity", 0))
        population = float(region.get("population", 0))
        need = float(region.get("need", 0))

        severity = max(0, min(100, severity))

        return {
            "severity": severity,
            "population": population,
            "need": need
        }

    except (ValueError, TypeError):
        return {
            "severity": 0,
            "population": 0,
            "need": 0
        }


def normalize(values):
    """Değerleri 0-100 arasına dönüştürür."""

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


def analyze_regions(regions, total_resource):
    """Bütün bölgeleri analiz eder ve kaynak dağılımı oluşturur."""

    if not regions:
        return []

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

        severity = float(region.get("severity", 0))

        priority = (
            severity * 0.50
            + normalized_population[index] * 0.20
            + normalized_need[index] * 0.30
        )

        results.append({
            "name": region.get("name", "Bilinmeyen Bölge"),
            "severity": round(severity, 2),
            "population": populations[index],
            "need": needs[index],
            "priority": round(priority, 2)
        })

    total_priority = sum(item["priority"] for item in results)

    for item in results:

        if total_priority > 0:
            share = item["priority"] / total_priority
        else:
            share = 0

        item["percentage"] = round(share * 100, 2)
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Veri alınamadı."
        }), 400

    regions = data.get("regions", [])
    total_resource = float(
        data.get("total_resource", 0)
    )

    if total_resource <= 0:
        return jsonify({
            "error": "Toplam kullanılabilir kaynak 0'dan büyük olmalıdır."
        }), 400

    if not regions:
        return jsonify({
            "error": "En az bir afet bölgesi ekleyin."
        }), 400

    results = analyze_regions(
        regions,
        total_resource
    )

    critical_count = sum(
        1 for item in results
        if item["status"] == "Kritik"
    )

    average_priority = (
        sum(item["priority"] for item in results)
        / len(results)
    )

    ai_message = generate_recommendation(results)

    return jsonify({
        "results": results,
        "critical_count": critical_count,
        "average_priority": round(
            average_priority,
            2
        ),
        "ai_recommendation": ai_message
    })


def generate_recommendation(results):
    """Analiz sonucuna göre açıklayıcı sistem önerisi üretir."""

    if not results:
        return "Analiz yapılacak bölge bulunamadı."

    top = results[0]

    if top["status"] == "Kritik":
        return (
            f"{top['name']} bölgesi en yüksek önceliğe sahip. "
            f"Öncelik puanı {top['priority']}/100. "
            f"Mevcut kaynakların yaklaşık %{top['percentage']} "
            f"oranının bu bölgeye yönlendirilmesi öneriliyor."
        )

    if top["status"] == "Acil":
        return (
            f"{top['name']} bölgesi acil müdahale gerektiriyor. "
            f"Öncelik puanı {top['priority']}/100. "
            f"Kaynak dağıtımında bu bölge öncelikli değerlendirilmeli."
        )

    return (
        f"{top['name']} bölgesi mevcut veriler içinde "
        f"en yüksek önceliğe sahip. "
        f"Öncelik puanı {top['priority']}/100."
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "project": "Afet-X Akıllı Kaynak Dağıtımı"
    })


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
