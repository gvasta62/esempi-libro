# Esempi libro

Raccolta di mini-esempi che usano **API pubbliche gratuite, senza chiave API**,
più qualche esempio che funziona **completamente offline**.
Ogni esempio è autonomo: gli script Python usano solo la libreria standard (zero dipendenze
da installare), le pagine HTML si aprono direttamente nel browser.

## Requisiti

- **Script Python (`.py`)**: Python 3 (qualsiasi versione recente). Nessun `pip install`.
- **Pagine HTML (`.html`)**: un browser. Doppio clic sul file (alcuni caricano librerie da CDN, quindi serve la connessione a internet).
- Connessione a internet per quasi tutti (interrogano servizi online). Fa eccezione
  `organizza_download.py`, che lavora solo sui file del tuo computer.

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

### 6. `organizza_download.py` — Riordina la cartella Download
Smista i file della cartella Download in sottocartelle per tipo (Immagini, Documenti, Video,
Audio, PCCAN, Archivi, Altri). **Non usa nessun servizio online**: lavora solo sui file locali.

Mostra sempre un'anteprima e chiede conferma prima di spostare qualcosa; non sovrascrive mai
un file esistente (rinomina in `nome (1).ext`) e scrive un log di tutti gli spostamenti.

```bash
python3 organizza_download.py     # su Windows: python organizza_download.py
# mostra l'anteprima, poi scrivi SI per confermare
```

Per usarlo su un'altra cartella, modifica `CARTELLA_DA_ORGANIZZARE` in cima al file:

```python
CARTELLA_DA_ORGANIZZARE = r"C:\Users\tuonome\Desktop"
```

---

## Extra — richiede Claude Code

### 7. [`report-settimanali/`](report-settimanali/) — Report settimanali da note grezze
Scrivi (o detti con **Win + H**) una riga al giorno su cosa hai fatto; a fine settimana
un'icona trasforma le note in un report professionale in Markdown, con problemi,
azioni suggerite e piano della settimana successiva.

A differenza degli altri esempi **non è autonomo**: richiede [Claude Code](https://claude.com/claude-code)
installato, ed è lui a scrivere il report. Su Windows serve anche WSL.

```
1 - Scrivi note.bat      → annoti la giornata
2 - Genera report.bat    → esce AAAA-Wnn_report.md
```

Il [README della cartella](report-settimanali/README.md) racconta anche i due bug
emersi in collaudo — modello e output sullo stesso file, e il falso "fatto!" quando
si verifica l'esistenza di un file invece della sua data di modifica.

---

## Servizi usati (tutti senza chiave API)

| Esempio              | Servizio          | Endpoint                                   |
|----------------------|-------------------|--------------------------------------------|
| meteo_roma.py        | Open-Meteo        | `api.open-meteo.com`                        |
| euro_to_yen.py       | ExchangeRate-API  | `open.er-api.com`                           |
| traduci_it_en.py     | LibreTranslate    | istanze pubbliche (con fallback)            |
| immagine_random.html | Lorem Picsum      | `picsum.photos`                             |
| geocoder_mappa.html  | Nominatim + Leaflet | `nominatim.openstreetmap.org`, OSM tiles  |
| organizza_download.py | nessuno          | funziona offline, solo file locali          |

> Nota: gli esempi dipendono da servizi pubblici di terze parti; la disponibilità non è garantita.
