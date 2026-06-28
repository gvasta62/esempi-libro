# Esempi libro

Raccolta di mini-esempi che usano **API pubbliche gratuite, senza chiave API**.
Ogni esempio è autonomo: gli script Python usano solo la libreria standard (zero dipendenze
da installare), le pagine HTML si aprono direttamente nel browser.

## Requisiti

- **Script Python (`.py`)**: Python 3 (qualsiasi versione recente). Nessun `pip install`.
- **Pagine HTML (`.html`)**: un browser. Doppio clic sul file (alcuni caricano librerie da CDN, quindi serve la connessione a internet).
- Connessione a internet per tutti (interrogano servizi online).

---

## Esempi

### 1. `meteo_roma.py` — Meteo e previsioni
Meteo attuale (temperatura, percepita, umidità, vento, condizioni) + previsione dei prossimi giorni di una città, via **Open-Meteo**.

```bash
python3 meteo_roma.py            # default: Roma
python3 meteo_roma.py Milano
python3 meteo_roma.py "New York"
```

### 2. `euro_to_yen.py` — Conversione valuta
Chiede un importo in euro e lo converte in yen giapponesi, via **ExchangeRate-API** (endpoint open access).

```bash
python3 euro_to_yen.py
# poi digita l'importo, es. 100 oppure 49,90
```

### 3. `traduci_it_en.py` — Traduttore italiano → inglese
Traduce una frase dall'italiano all'inglese, via **LibreTranslate** (con fallback automatico su più istanze pubbliche).

```bash
python3 traduci_it_en.py "Buongiorno, come stai?"
python3 traduci_it_en.py          # chiede la frase in input
```

### 4. `immagine_random.html` — Immagini casuali
Mostra un'immagine casuale da **Lorem Picsum**, con pulsanti per caricarne un'altra e per scaricarla,
più opzioni di formato / bianco e nero / sfocatura.

```
Apri immagine_random.html nel browser (doppio clic).
```

### 5. `geocoder_mappa.html` — Indirizzo sulla mappa
Inserisci un indirizzo, lo geolocalizza con **Nominatim** (OpenStreetMap), mostra latitudine/longitudine
su una mappa interattiva (**Leaflet**) e fornisce un link a **Google Maps**.

```
Apri geocoder_mappa.html nel browser (doppio clic).
```

---

## Servizi usati (tutti senza chiave API)

| Esempio              | Servizio          | Endpoint                                   |
|----------------------|-------------------|--------------------------------------------|
| meteo_roma.py        | Open-Meteo        | `api.open-meteo.com`                        |
| euro_to_yen.py       | ExchangeRate-API  | `open.er-api.com`                           |
| traduci_it_en.py     | LibreTranslate    | istanze pubbliche (con fallback)            |
| immagine_random.html | Lorem Picsum      | `picsum.photos`                             |
| geocoder_mappa.html  | Nominatim + Leaflet | `nominatim.openstreetmap.org`, OSM tiles  |

> Nota: gli esempi dipendono da servizi pubblici di terze parti; la disponibilità non è garantita.
