# Report di attività da note libere

Annoti una riga per ogni cosa — quello che hai fatto, con la data, e quello che
devi fare, con una scadenza o un "asap". Premi un'icona e ottieni un report
professionale **in Markdown e in Word**: consuntivo di quello che è stato fatto,
più uno scadenzario ordinato per urgenza con le scadenze scadute in evidenza.

> **Attenzione: questo esempio è diverso dagli altri del repo.**
> Gli altri funzionano con la sola libreria standard e senza chiavi API.
> Questo invece richiede [Claude Code](https://claude.com/claude-code) installato
> e funzionante, perché è lui a leggere le note e scrivere il report.
> Su Windows serve anche WSL, perché le icone `.bat` richiamano lo script bash.
> Per l'uscita in Word serve inoltre `pip install python-docx`.

---

## Come si usa

**Icona `1 - Scrivi note`**
Apre il blocco note. Una riga per cosa, quando ti pare. Per dettare invece di
scrivere: **Win + H** e parli. Salva con **Ctrl + S**.

**Icona `2 - Genera report`**
Ci mette circa un minuto e salva il report con il nome del periodo davvero
coperto dalle note, in due formati:

```
report_2026-07-15_2026-07-30.md      formato di lavoro
report_2026-07-15_2026-07-30.docx    da girare agli altri
```

Poi apre il Word.

Su Linux/Mac non servono le icone: `bash genera_report.sh`.

### Il documento Word

Titoli veri di Word (quindi riquadro di spostamento e sommario automatico
funzionano), tabelle con intestazione colorata e bordi, elenchi puntati,
grassetti — e **le scadenze scadute in rosso**, riga intera.

La conversione la fa `md_to_docx.py` con [python-docx](https://pypi.org/project/python-docx/),
l'unica dipendenza esterna di questo esempio:

```bash
pip install python-docx
```

Non serve avere Word installato, e la conversione non apre nessuna finestra: puoi
lanciarla mentre stai lavorando. Se fallisce, lo script te lo dice e il Markdown
resta comunque salvato.

Il convertitore funziona anche da solo, su qualsiasi report già prodotto:

```bash
python3 md_to_docx.py report_2026-07-15_2026-07-30.md
python3 md_to_docx.py report.md nome_a_scelta.docx
```

Non è un convertitore Markdown universale: gestisce titoli, paragrafi, tabelle,
elenchi, grassetto, corsivo e codice inline — cioè esattamente quello che il
report usa. È una scelta voluta: meno codice e nessuna sorpresa su costrutti che
non compariranno mai.

---

## Come si scrive una riga

| Scrivi così | Significa |
|---|---|
| `15/07 - ...` | cosa **fatta** il 15 luglio |
| `oggi - ...` / `ieri - ...` | cosa **fatta** (la data viene calcolata) |
| `asap - ...` | da fare **il prima possibile** |
| `entro 25/07 - ...` | da fare con **scadenza** |
| `entro venerdi - ...` | va bene anche così |
| `30/07 - ...` | data futura: trattata come **da fare** |

Le date si scrivono come vengono: `15/07`, `15-07`, `15 luglio`, `lunedi`,
`venerdi prossimo`, `fine mese`. Le righe che iniziano con `#` sono ignorate.

```
15/07 - finita presentazione cliente ABC, consegnata in tempo
16/07 - call Teams kick-off progetto Rossi. Gestionale in crash, 2h perse
ieri - chiusi 3 ticket supporto
entro 18/07 - inviare consuntivo costi al controllo di gestione
asap - richiamare fornitore Bianchi, blocca il contratto
entro 25/07 - consegnare slide budget Q2
30/07 - visita deposito Terni
```

Da queste sette righe escono: un consuntivo delle quattro attività svolte, la
segnalazione che il consuntivo costi **è scaduto da un giorno**, e uno scadenzario
con Bianchi in cima, poi 25/07 e 30/07.

---

## I file

| File | A cosa serve |
|---|---|
| `note.txt` | dove scrivi le note |
| `_modello.md` | il formato di riferimento, **sola lettura**: è la traccia che ogni report segue |
| `genera_report.sh` | il motore |
| `md_to_docx.py` | converte il report in Word (richiede `python-docx`) |
| `1 - Scrivi note.bat` | apre le note (Windows) |
| `2 - Genera report.bat` | lancia la generazione (Windows) |
| `report_AAAA-MM-GG_AAAA-MM-GG.md` | i report prodotti (formato di lavoro) |
| `report_AAAA-MM-GG_AAAA-MM-GG.docx` | gli stessi report in Word |

Non ci sono percorsi fissi: lo script lavora nella cartella in cui si trova.
Le icone `.bat` devono restare lì dentro; se le vuoi sul Desktop, creane un
**collegamento** (tasto destro → *Invia a* → *Desktop*).

---

## Tre dettagli che sembrano pignoleria ma non lo sono

Sono i punti in cui questo script si è rotto, o avrebbe potuto rompersi, durante il collaudo.

**1. Il modello e l'output devono essere file diversi.**
Nella prima versione il report della settimana corrente faceva sia da modello sia
da destinazione: lo stesso file. Rigenerarlo significava distruggere l'unica traccia
di formato esistente, e infatti la generazione si bloccava da sola per non farlo.
Per questo il modello vive separato in `_modello.md` e non viene mai scritto.

**2. "Il file esiste" non vuol dire "il report è stato creato".**
Controllare con `[ -f "$REPORT" ]` sembra ragionevole, ma il file può esistere già
dalla volta precedente: lo script annuncerebbe "fatto" davanti a un report vecchio.
Serve un segnatempo preso *prima* di iniziare.

**3. Se il nome del file non lo decidi tu, non puoi cercarlo per nome.**
Da quando il periodo dipende dalle date scritte nelle note, il nome del report non
è più prevedibile dallo script. La verifica quindi non cerca un nome atteso, ma
*qualsiasi* report più recente del segnatempo:

```bash
MARCATORE=$(mktemp)
# ... generazione, il nome del file lo compone Claude ...
NUOVI=$(find "$CARTELLA" -maxdepth 1 -name 'report_*.md' -newer "$MARCATORE" -printf '%f\n')
if [ -n "$NUOVI" ]; then ...
```

Se non è stato scritto niente, lo dice chiaramente invece di mentire.

---

## Scrivere note che producono buoni report

Il punto debole del sistema non è il report: sono le note. Più sono concrete,
meglio è. Aggiungi quando puoi **numeri** ("3 ticket", non "qualche ticket"),
**esito** (finito / in corso / bloccato), **tempo perso e perché**, i **nomi** di
cliente e progetto, e soprattutto **cosa blocca cosa** — è quello che permette di
ordinare le priorità in modo sensato invece che per sola data.

```
Riga buona:   16/07 - call Teams kick-off progetto Rossi. Gestionale in crash, 2h perse.
Riga povera:  16/07 - riunione e problemi vari.
```

---

## Privacy

I report contengono cose del tuo lavoro. Restano sul tuo computer: qui trovi solo
lo strumento e un `_modello.md` con contenuti inventati.

Il `.gitignore` esclude già i report generati (`report_*.md`, `report_*.docx`, `*.pdf`). Il file `note.txt`
è invece incluso perché è il modulo vuoto da compilare: se lavori direttamente in
questa cartella e la tieni sotto Git, aggiungilo tu al `.gitignore` una volta che
contiene note vere.
