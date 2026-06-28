#!/usr/bin/env python3
"""Converte un importo da Euro a Yen giapponesi usando ExchangeRate-API (endpoint gratuito senza chiave)."""

import json
import urllib.request

# Endpoint "open access" di ExchangeRate-API: nessuna chiave richiesta
URL = "https://open.er-api.com/v6/latest/EUR"


def chiedi_importo():
    """Chiede all'utente un importo in euro e lo restituisce come float (>= 0)."""
    while True:
        testo = input("Importo in euro (EUR): ").strip().replace(",", ".").replace("€", "")
        try:
            valore = float(testo)
            if valore < 0:
                print("  Inserisci un valore non negativo.")
                continue
            return valore
        except ValueError:
            print("  Importo non valido, riprova (es. 100 oppure 49,90).")


def get_tasso_eur_jpy():
    """Recupera il tasso di cambio EUR -> JPY e la data di aggiornamento."""
    with urllib.request.urlopen(URL, timeout=10) as resp:
        dati = json.load(resp)
    if dati.get("result") != "success":
        raise SystemExit("Errore nel recupero dei tassi di cambio.")
    return dati["rates"]["JPY"], dati.get("time_last_update_utc", "n/d")


def main():
    importo = chiedi_importo()
    tasso, aggiornato = get_tasso_eur_jpy()
    yen = importo * tasso

    print()
    print(f"  {importo:,.2f} EUR  =  {yen:,.2f} JPY")
    print(f"  (tasso: 1 EUR = {tasso:,.2f} JPY)")
    print(f"  Aggiornato al: {aggiornato}")


if __name__ == "__main__":
    main()
