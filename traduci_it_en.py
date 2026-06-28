#!/usr/bin/env python3
"""Traduce una frase dall'italiano all'inglese usando LibreTranslate (istanze pubbliche, nessuna chiave).

Uso:
    python3 traduci_it_en.py "Buongiorno, come stai?"
    python3 traduci_it_en.py            # chiede la frase in input
"""

import json
import sys
import urllib.error
import urllib.request

# Istanze pubbliche di LibreTranslate che non richiedono chiave API.
# Vengono provate in ordine: la prima che risponde viene usata.
ISTANZE = [
    "https://translate.flossboxin.org.in/translate",
    "https://libretranslate.com/translate",
    "https://translate.fedilab.app/translate",
    "https://lt.vern.cc/translate",
]


def traduci(testo, endpoint):
    """Invia una richiesta di traduzione IT->EN a una singola istanza LibreTranslate."""
    payload = json.dumps({
        "q": testo,
        "source": "it",
        "target": "en",
        "format": "text",
    }).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        dati = json.load(resp)
    return dati["translatedText"]


def traduci_con_fallback(testo):
    """Prova le istanze in ordine finché una risponde; altrimenti solleva un errore."""
    ultimo_errore = None
    for endpoint in ISTANZE:
        try:
            return traduci(testo, endpoint), endpoint
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, TimeoutError) as e:
            ultimo_errore = f"{endpoint} -> {e}"
            continue
    raise SystemExit(f"Nessuna istanza LibreTranslate disponibile.\nUltimo errore: {ultimo_errore}")


def main():
    if len(sys.argv) > 1:
        frase = " ".join(sys.argv[1:])
    else:
        frase = input("Frase in italiano: ").strip()

    if not frase:
        raise SystemExit("Nessuna frase da tradurre.")

    traduzione, usata = traduci_con_fallback(frase)

    print()
    print(f"  Originale (IT):  {frase}")
    print(f"  Traduzione (EN): {traduzione}")
    print(f"  [via {usata}]")


if __name__ == "__main__":
    main()
