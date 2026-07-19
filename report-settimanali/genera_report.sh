#!/bin/bash
# Genera il report settimanale a partire da note-settimana.txt
# Lanciato dall'icona "2 - Genera report.bat".
#
# Non contiene percorsi fissi: lavora sempre nella cartella in cui si trova,
# quindi puoi spostare l'intera cartella dove preferisci.

CARTELLA=$(cd "$(dirname "$0")" && pwd)
NOTE="$CARTELLA/note-settimana.txt"
SETTIMANA=$(date +%G-W%V)          # es. 2026-W29
REPORT="$CARTELLA/${SETTIMANA}_report.md"

cd "$CARTELLA" || exit 1

echo ""
echo "=============================================="
echo "   GENERAZIONE REPORT SETTIMANALE $SETTIMANA"
echo "=============================================="
echo ""

# --- Controllo 1: il file delle note esiste? ---
if [ ! -f "$NOTE" ]; then
  echo "ERRORE: non trovo il file delle note:"
  echo "  $NOTE"
  echo ""
  echo "Usa prima l'icona '1 - Scrivi note'."
  read -p "Premi INVIO per chiudere..."
  exit 1
fi

# --- Controllo 2: le note sono state compilate? ---
# Conta le righe che hanno del testo dopo il trattino.
RIGHE_PIENE=$(grep -cE '^(Lunedi|Martedi|Mercoledi|Giovedi|Venerdi) *- *[^ ]' "$NOTE")
if [ "$RIGHE_PIENE" -eq 0 ]; then
  echo "Il file delle note sembra ancora vuoto."
  echo "Apri '1 - Scrivi note' e annota almeno una giornata."
  echo "(ricorda di salvare con Ctrl+S prima di chiudere)"
  echo ""
  read -p "Premi INVIO per chiudere..."
  exit 1
fi

echo "Trovate $RIGHE_PIENE giornate compilate. Genero il report..."
echo "(ci vuole circa un minuto, non chiudere questa finestra)"
echo ""

# Segnatempo: serve dopo per capire se il report e' stato scritto DAVVERO adesso
# e non e' semplicemente un file vecchio rimasto dalla volta scorsa.
MARCATORE=$(mktemp)

# --- Generazione ---
claude --permission-mode acceptEdits -p "Leggi il file note-settimana.txt in questa cartella.
Trasforma quelle note grezze in un report settimanale professionale, usando
ESATTAMENTE la stessa struttura e lo stesso tono del file _modello.md
che trovi nella stessa cartella (usalo come modello di riferimento, in sola
lettura: non modificarlo mai).

Sezioni obbligatorie:
- Riepilogo della settimana (2-3 frasi)
- Attivita completate (tabella per giorno)
- Obiettivi raggiunti
- Problemi e soluzioni (con azione suggerita per ciascuno)
- Piano prossima settimana (tabella con priorita)
- Note per il manager

Tono professionale ma accessibile. Evidenzia successi e aree di miglioramento.
Salva il risultato nel file ${SETTIMANA}_report.md in questa cartella.
Non modificare nessun altro file. Alla fine rispondi solo con: REPORT SALVATO"

# --- Esito ---
# Non basta che il file esista: potrebbe essere quello della volta scorsa.
# Controllo che sia stato modificato DOPO l'avvio di questa generazione.
echo ""
if [ -f "$REPORT" ] && [ "$REPORT" -nt "$MARCATORE" ]; then
  rm -f "$MARCATORE"
  echo "=============================================="
  echo "   FATTO! Report salvato in:"
  echo "   ${SETTIMANA}_report.md"
  echo "=============================================="
  echo ""
  read -p "Vuoi aprirlo adesso? (premi INVIO per si, oppure chiudi la finestra) "
  WINPATH=$(wslpath -w "$REPORT" 2>/dev/null)
  if [ -n "$WINPATH" ]; then
    cmd.exe /c start "" "$WINPATH" 2>/dev/null   # Windows
  else
    xdg-open "$REPORT" 2>/dev/null               # Linux
  fi
else
  rm -f "$MARCATORE"
  echo "=============================================="
  echo "   ATTENZIONE: il report NON e' stato scritto."
  echo "=============================================="
  echo ""
  echo "Nessun file nuovo e' stato salvato per la settimana $SETTIMANA."
  echo "Leggi i messaggi qui sopra: spiegano il motivo."
  echo ""
  read -p "Premi INVIO per chiudere..."
fi
