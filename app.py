from flask import Flask, render_template, request, jsonify
import math
import requests

app = Flask(__name__)

# =========================================================
# AFET BÖLGELERİ
# =========================================================

REGIONS = [
    {
        "id": 1,
        "name": "Hatay",
        "lat": 36.2021,
        "lon": 36.1601,
        "severity": 85,
        "population": 1700000,
        "need": 90
    },
    {
        "id": 2,
        "Kahramanmaraş": 37.5753,
        "lon": 36.9228,
        "severity": 75,
        "population": 1100000,
        "need": 80
    },
    {
        "id": 3,
        "Gaziantep": 37.0662,
        "lon": 37.3833,
        "severity": 60,
        "population": 2100000,
        "need": 65
    }
]


# =========================================================
# HASTANELER
# =========================================================

HOSPITALS = [
    {
        "id": 1,
        "name": "Hatay Eğitim ve Araştırma Hastanesi",
        "city": "Hatay",
        "lat": 36.2023,
        "lon": 36.1605,
        "capacity": 500,
        "staff_load": 65,
        "beds_available": 185
    },
    {
        "id": 2,
        "name": "Defne Devlet Hastanesi",
        "city": "Hatay",
        "lat": 36.2300,
        "lon": 36.1500,
        "capacity": 300,
        "staff_load": 40,
        "beds_available": 120
    },
    {
        "id": 3,
        "name": "Kahramanmaraş Necip Fazıl Şehir Hastanesi",
        "city": "Kahramanmaraş",
        "lat": 37.5750,
        "lon": 36.9200,
        "capacity": 600,
        "staff_load": 55,
        "beds_available": 220
    },
    {
        "id": 4,
        "name": "Gaziantep Şehir Hastanesi",
        "city": "Gaziantep",
        "lat": 37.0800,
        "lon": 37.4000,
        "capacity": 800,
        "staff_load": 70,
        "beds_available": 190
    }
]


# =========================================================
# AMBULANSLAR
# =========================================================

AMBULANCES = [
    {
        "id": "AMB-01",
        "name": "Ambulans 01",
        "lat": 36.1900,
        "lon": 36.1700,
        "status": "Müsait"
    },
    {
        "id": "AMB-02
