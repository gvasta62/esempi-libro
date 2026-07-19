#!/bin/bash
# Genera un report di attivita' a partire dalle note libere in note.txt
# Lanciato dall'icona "2 - Genera report.bat".
#
# Il periodo coperto NON e' deciso qui: dipende dalle date che hai scritto
# nelle note. Il nome del file lo compone il generatore.

CARTELLA=$(cd "$(dirname "$0")" && pwd)
NOTE="$CARTELLA/note.txt"
OGGI=$(date +%d/%m/%Y)
OGGI_ESTESO=$(date +"%A %d %B %Y")

cd "$CARTELLA" || exit 1

echo ""
echo "=============================================="
echo "   GENERAZIONE REPORT ATTIVITA'"
echo "   Oggi e' $OGGI_ESTESO"
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

# --- Controllo 2: ci sono note vere? ---
# Conta le righe non vuote che non sono commenti (#).
RIGHE_PIENE=$(grep -vE '^[[:space:]]*(#|$)' "$NOTE" | wc -l)
if [ "$RIGHE_PIENE" -eq 0 ]; then
  echo "Il file delle note non contiene ancora nulla."
  echo "Apri '1 - Scrivi note' e annota almeno una riga."
  echo "(ricorda di salvare con Ctrl+S prima di chiudere)"
  echo ""
  read -p "Premi INVIO per chiudere..."
  exit 1
fi

echo "Trovate $RIGHE_PIENE note. Genero il report..."
echo "(ci vuole circa un minuto, non chiudere questa finestra)"
echo ""

# Segnatempo: serve dopo per riconoscere i report scritti DAVVERO adesso.
MARCATORE=$(mktemp)

# --- Generazione ---
# Nota: il nome del file di destinazione lo decide il generatore, perche'
# dipende dalle date presenti nelle note. Per questo dopo non cerchiamo un
# nome preciso, ma "qualsiasi report piu' recente del marcatore".
claude --permission-mode acceptEdits -p "Oggi e' $OGGI (giorno/mese/anno). Usa questa data per
risolvere i riferimenti relativi come 'oggi', 'ieri', 'venerdi', 'entro fine mese'.

Leggi il file note.txt in questa cartella. Contiene note libere, una per riga.
Ignora le righe che iniziano con #.

Ogni riga puo' essere:
- una attivita' GIA' SVOLTA, se ha una data passata o dice oggi/ieri
- una attivita' DA FARE, se dice 'asap' / 'il prima possibile', oppure
  'entro <data>', oppure ha una data futura

Interpreta le date con flessibilita': 15/07, 15-07, 15 luglio, lunedi, venerdi
prossimo, fine mese. Se una riga non ha nessun riferimento temporale e non e'
chiaramente conclusa, trattala come da fare senza scadenza.

Scrivi un report professionale con la stessa struttura e lo stesso tono del file
_modello.md di questa cartella (usalo come riferimento, in SOLA LETTURA: non
modificarlo mai). Struttura richiesta:

- Titolo con il periodo effettivamente coperto dalle note
- Riepilogo del periodo (2-3 frasi)
- Attivita' svolte (tabella ordinata per data crescente)
- Obiettivi raggiunti
- Problemi e soluzioni (con azione suggerita per ciascuno)
- Da fare (tabella ordinata per urgenza: prima 'il prima possibile',
  poi le scadenze dalla piu' vicina alla piu' lontana; segnala in modo
  evidente le scadenze gia' scadute o a rischio)
- Note per il manager

Tono professionale ma accessibile. Evidenzia successi e aree di miglioramento.

SALVATAGGIO: calcola la data piu' antica e la piu' recente presenti nelle note
(considerando sia le attivita' svolte sia le scadenze) e salva il report in un
file chiamato esattamente:
   report_AAAA-MM-GG_AAAA-MM-GG.md
dove la prima data e' la piu' antica e la seconda la piu' recente.
Esempio: report_2026-07-15_2026-07-30.md
Non modificare nessun altro file. Alla fine rispondi solo con il nome del file salvato."

# --- Esito ---
# Cerchiamo qualsiasi report creato o modificato dopo il marcatore.
echo ""
NUOVI=$(find "$CARTELLA" -maxdepth 1 -name 'report_*.md' -newer "$MARCATORE" -printf '%f\n' 2>/dev/null)
rm -f "$MARCATORE"

if [ -n "$NUOVI" ]; then
  echo "=============================================="
  echo "   FATTO! Report salvato:"
  echo "$NUOVI" | sed 's/^/   /'
  echo "=============================================="
  echo ""
  PRIMO=$(echo "$NUOVI" | head -1)
  read -p "Vuoi aprirlo adesso? (premi INVIO per si, oppure chiudi la finestra) "
  WINPATH=$(wslpath -w "$CARTELLA/$PRIMO" 2>/dev/null)
  if [ -n "$WINPATH" ]; then
    cmd.exe /c start "" "$WINPATH" 2>/dev/null   # Windows
  else
    xdg-open "$CARTELLA/$PRIMO" 2>/dev/null      # Linux
  fi
else
  echo "=============================================="
  echo "   ATTENZIONE: il report NON e' stato scritto."
  echo "=============================================="
  echo ""
  echo "Nessun file report_*.md nuovo in questa cartella."
  echo "Leggi i messaggi qui sopra: spiegano il motivo."
  echo ""
  read -p "Premi INVIO per chiudere..."
fi
