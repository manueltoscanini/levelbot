import requests
from datetime import datetime
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*"
}

def calendario(month, year):
    url = (
        "https://www.flylevel.com/nwe/flights/api/calendar/"
        f"?triptype=RT"
        f"&origin=EZE"
        f"&destination=BCN"
        f"&month={month:02d}"
        f"&year={year}"
        f"&currencyCode=USD"
        f"&originType=flights"
    )

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    return r.json()["data"]["dayPrices"]

def vueltas(outbound_date, month, year):
    url = (
        "https://www.flylevel.com/nwe/flights/api/calendar/"
        f"?triptype=RT"
        f"&origin=EZE"
        f"&destination=BCN"
        f"&outboundDate={outbound_date}"
        f"&month={month:02d}"
        f"&year={year}"
        f"&currencyCode=USD"
        f"&originType=flights"
    )

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    return r.json()["data"]["dayPrices"]

def telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=30
    )
print("\n================================")
print("Ejecutando búsqueda:", datetime.now())
print("================================")
# Dic + Ene
idas_1 = calendario(12, 2026)

# Feb + Mar
idas_2 = calendario(2, 2027)

todas = idas_1 + idas_2

mejor = min(todas, key=lambda x: x["price"])

print("\nMEJOR IDA")
print("Fecha:", mejor["date"])
print("Precio:", mejor["price"])

if mejor["price"] < 150:
    telegram(
        f"✈️ IDA BARATA\n"
        f"Fecha: {mejor['date']}\n"
        f"Precio: USD {mejor['price']}"
    )

print("\nBuscando vueltas...")

retornos = []

retornos += vueltas(mejor["date"], 1, 2027)
retornos += vueltas(mejor["date"], 2, 2027)

mejor_vuelta = min(retornos, key=lambda x: x["price"])

print("\nMEJOR VUELTA")
print("Fecha:", mejor_vuelta["date"])
print("Precio:", mejor_vuelta["price"])

if mejor_vuelta["price"] < 150:
    telegram(
        f"🔁 VUELTA BARATA\n"
        f"Fecha: {mejor_vuelta['date']}\n"
        f"Precio: USD {mejor_vuelta['price']}"
    )