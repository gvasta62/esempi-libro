# Report settimanali da note grezze

Scrivi (o detti) una riga al giorno su cosa hai fatto. A fine settimana premi un'icona
e ottieni un report professionale in Markdown: riepilogo, attività, obiettivi, problemi
con azioni suggerite, piano della settimana dopo e note per il manager.

> **Attenzione: questo esempio è diverso dagli altri del repo.**
> Gli altri esempi funzionano con la sola libreria standard e senza chiavi API.
> Questo invece richiede [Claude Code](https://claude.com/claude-code) installato
> e funzionante, perché è lui a scrivere il report. Su Windows serve anche WSL,
> perché le icone `.bat` richiamano lo script bash.

---

## Come si usa

**Icona `1 - Scrivi note`**
Apre il blocco note. Una riga al giorno, come vengono. Per dettare invece di scrivere:
premi **Win + H** e parla. Salva con **Ctrl + S**.

**Icona `2 - Genera report`**
Si apre una finestra nera, ci mette circa un minuto, e salva il report con il nome
della settimana ISO corrente (es. `2026-W29_report.md`). Alla fine chiede se aprirlo.

Poi svuoti `note-settimana.txt` e ricominci la settimana dopo.

Su Linux/Mac non servono le icone: `bash genera_report.sh`.

---

## I file

| File | A cosa serve |
|---|---|
| `note-settimana.txt` | dove scrivi le note grezze |
| `_modello.md` | il formato di riferimento, **sola lettura**: è la traccia che ogni report segue |
| `genera_report.sh` | il motore |
| `1 - Scrivi note.bat` | apre le note (Windows) |
| `2 - Genera report.bat` | lancia la generazione (Windows) |
| `AAAA-Wnn_report.md` | i report prodotti, uno per settimana |

Non ci sono percorsi fissi: lo script lavora sempre nella cartella in cui si trova,
quindi puoi spostare tutto dove preferisci. Le icone `.bat` funzionano se restano
nella stessa cartella; se le vuoi sul Desktop, creane un **collegamento**
(tasto destro sul `.bat` → *Invia a* → *Desktop*).

---

## Due dettagli che sembrano pignoleria ma non lo sono

Sono i due punti in cui la prima versione di questo script si è rotta durante il collaudo.

**1. Il modello e l'output devono essere file diversi.**
All'inizio il report della settimana corrente faceva sia da modello sia da destinazione:
lo stesso file. Rigenerarlo significava distruggere l'unica traccia di formato esistente.
Per questo il modello vive separato in `_modello.md` e non viene mai scritto.

**2. "Il file esiste" non vuol dire "il report è stato creato".**
Controllare con `[ -f "$REPORT" ]` sembra ragionevole, ma il file della settimana può
esistere già dalla volta precedente: lo script annuncerebbe "fatto" davanti a un report
vecchio. La versione corretta prende un segnatempo con `mktemp` prima di iniziare e poi
verifica che il report sia più recente di quello:

```bash
MARCATORE=$(mktemp)
# ... generazione ...
if [ -f "$REPORT" ] && [ "$REPORT" -nt "$MARCATORE" ]; then
```

Se non è stato scritto niente, lo dice chiaramente invece di mentire.

---

## Scrivere note che producono buoni report

Il punto debole del sistema non è il report: sono le note. Più sono concrete, meglio è.
Aggiungi quando puoi **numeri** ("3 ticket", non "qualche ticket"), **esito**
(finito / in corso / bloccato), **tempo perso e perché** — la parte più preziosa —
e i **nomi** di cliente, progetto o collega.

```
Riga buona:   Martedi - call Teams kick-off progetto Rossi. Gestionale in crash, 2h perse.
Riga povera:  Martedi - riunione e problemi vari.
```

---

## Privacy

I report contengono cose del tuo lavoro. Restano sul tuo computer: qui trovi solo
lo strumento e un `_modello.md` con contenuti inventati.

Il `.gitignore` esclude già i report generati (`*_report.md`). Il file
`note-settimana.txt` è invece incluso perché è il modulo vuoto da compilare:
se lavori direttamente in questa cartella e la tieni sotto Git, aggiungilo tu
al `.gitignore` una volta che contiene note vere.
