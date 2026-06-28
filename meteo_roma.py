#!/usr/bin/env python3
"""Mostra il meteo attuale di una città usando l'API gratuita Open-Meteo (nessuna chiave API).

Uso:
    python3 meteo_roma.py            # default: Roma
    python3 meteo_roma.py Milano
    python3 meteo_roma.py "New York"
"""

import json
import sys
import urllib.parse
import urllib.request

# Mappa dei codici meteo WMO -> descrizione in italiano
WMO_CODES = {
    0: "Cielo sereno",
    1: "Prevalentemente sereno",
    2: "Parzialmente nuvoloso",
    3: "Coperto",
    45: "Nebbia",
    48: "Nebbia con brina",
    51: "Pioviggine leggera",
    53: "Pioviggine moderata",
    55: "Pioviggine intensa",
    56: "Pioviggine gelata leggera",
    57: "Pioviggine gelata intensa",
    61: "Pioggia leggera",
    63: "Pioggia moderata",
    65: "Pioggia forte",
    66: "Pioggia gelata leggera",
    67: "Pioggia gelata forte",
    71: "Neve leggera",
    73: "Neve moderata",
    75: "Neve forte",
    77: "Granuli di neve",
    80: "Rovesci leggeri",
    81: "Rovesci moderati",
    82: "Rovesci violenti",
    85: "Rovesci di neve leggeri",
    86: "Rovesci di neve forti",
    95: "Temporale",
    96: "Temporale con grandine leggera",
    99: "Temporale con grandine forte",
}


def geocoding(citta):
    """Trova latitudine/longitudine di una città tramite Open-Meteo Geocoding (nessuna chiave)."""
    q = urllib.parse.urlencode({"name": citta, "count": 1, "language": "it", "format": "json"})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{q}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        dati = json.load(resp)
    risultati = dati.get("results")
    if not risultati:
        raise SystemExit(f"Città non trovata: {citta!r}")
    r = risultati[0]
    nome = ", ".join(filter(None, [r.get("name"), r.get("admin1"), r.get("country")]))
    return r["latitude"], r["longitude"], nome


def get_meteo(lat, lon, giorni=5):
    """Interroga Open-Meteo e restituisce meteo corrente + previsione giornaliera."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        "weather_code,wind_speed_10m,wind_direction_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
        "precipitation_probability_max"
        f"&forecast_days={giorni}"
        "&timezone=auto"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def nome_giorno(data_iso):
    """Converte una data ISO (YYYY-MM-DD) nel nome del giorno in italiano."""
    import datetime

    giorni = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
    d = datetime.date.fromisoformat(data_iso)
    return f"{giorni[d.weekday()].capitalize()} {d.day:02d}/{d.month:02d}"


def direzione_vento(gradi):
    """Converte i gradi della direzione del vento nel punto cardinale corrispondente."""
    punti = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    return punti[round(gradi / 45) % 8]


def main():
    citta = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Roma"
    lat, lon, nome = geocoding(citta)

    dati = get_meteo(lat, lon)
    corrente = dati["current"]
    unita = dati["current_units"]

    descrizione = WMO_CODES.get(corrente["weather_code"], f"Codice meteo {corrente['weather_code']}")
    vento_dir = direzione_vento(corrente["wind_direction_10m"])

    print(f"Meteo attuale a {nome}")
    print("-" * 40)
    print(f"Temperatura: {corrente['temperature_2m']} {unita['temperature_2m']}")
    print(f"Percepita:   {corrente['apparent_temperature']} {unita['apparent_temperature']}")
    print(f"Umidità:     {corrente['relative_humidity_2m']} {unita['relative_humidity_2m']}")
    print(f"Vento:       {corrente['wind_speed_10m']} {unita['wind_speed_10m']} da {vento_dir}")
    print(f"Condizioni:  {descrizione}")

    # Previsione dei prossimi giorni
    daily = dati["daily"]
    udaily = dati["daily_units"]
    print()
    print("Previsione prossimi giorni")
    print("-" * 40)
    for i, data in enumerate(daily["time"]):
        cond = WMO_CODES.get(daily["weather_code"][i], "?")
        tmin = daily["temperature_2m_min"][i]
        tmax = daily["temperature_2m_max"][i]
        pioggia = daily["precipitation_probability_max"][i]
        u = udaily["temperature_2m_max"]
        etichetta = "Oggi" if i == 0 else nome_giorno(data)
        temp = f"{tmin:.0f}/{tmax:.0f} {u}"
        print(f"{etichetta:<16}{temp:>9}  pioggia {pioggia:>3}%  {cond}")


if __name__ == "__main__":
    main()
