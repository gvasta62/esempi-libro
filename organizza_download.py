# -*- coding: utf-8 -*-
# ============================================================================
#  ORGANIZZA DOWNLOAD
#  Sposta i file della cartella Download in sottocartelle divise per tipo.
#
#  Usa solo librerie standard di Python: nessuna installazione necessaria.
#  Mostra sempre un'anteprima e chiede conferma prima di spostare qualcosa.
# ============================================================================

import os        # serve per leggere cartelle, unire percorsi, controllare se un file esiste
import shutil    # serve per spostare i file da una cartella all'altra
import datetime  # serve per scrivere data e ora dentro il file di log


# ============================================================================
#  IMPOSTAZIONI - questa e' l'unica parte che ti conviene modificare
# ============================================================================

# Cartella da riordinare.
# os.path.expanduser("~") restituisce la tua cartella utente (es. C:\Users\gvast)
# os.path.join unisce i pezzi del percorso mettendo il \ giusto da solo.
CARTELLA_DA_ORGANIZZARE = os.path.join(os.path.expanduser("~"), "Downloads")

# Le categorie: a sinistra il nome della sottocartella da creare,
# a destra l'elenco delle estensioni che finiscono in quella sottocartella.
# Le estensioni si scrivono minuscole e senza il punto.
CATEGORIE = {
    "Immagini":  ["jpg", "jpeg", "png", "gif", "webp"],
    "Documenti": ["pdf", "doc", "docx", "txt", "xlsx", "ppt", "pptx"],
    "Video":     ["mp4", "avi", "mkv", "mov"],
    "Audio":     ["mp3", "wav", "flac"],
    "PCCAN":     ["trc"],
    "Archivi":   ["zip", "rar", "7z"],
}

# Nome della sottocartella dove finisce tutto cio' che non rientra nelle categorie sopra.
CATEGORIA_ALTRI = "Altri"

# Nome del file di log che verra' creato dentro la cartella organizzata.
NOME_FILE_LOG = "_log_organizzazione.txt"

# File che lo script deve ignorare sempre.
# .crdownload e .part sono download ancora in corso: spostarli li romperebbe.
ESTENSIONI_DA_IGNORARE = ["crdownload", "part", "tmp"]


# ============================================================================
#  FUNZIONI DI SUPPORTO
#  Una funzione e' un pezzo di codice con un nome, che possiamo richiamare.
# ============================================================================

def trova_categoria(nome_file):
    """Dato il nome di un file, restituisce il nome della cartella dove va messo."""

    # os.path.splitext divide "foto.JPG" in ("foto", ".JPG"); [1] prende la seconda parte.
    estensione = os.path.splitext(nome_file)[1]

    # .lower() rende tutto minuscolo (cosi' .JPG e .jpg sono trattati uguale)
    # .lstrip(".") toglie il punto iniziale, lasciando solo "jpg".
    estensione = estensione.lower().lstrip(".")

    # Scorriamo tutte le categorie una per una.
    for nome_categoria, elenco_estensioni in CATEGORIE.items():

        # Se l'estensione di questo file compare nell'elenco di questa categoria...
        if estensione in elenco_estensioni:

            # ...abbiamo trovato la risposta ed usciamo subito dalla funzione.
            return nome_categoria

    # Se il ciclo finisce senza aver trovato nulla, il file va in "Altri".
    return CATEGORIA_ALTRI


def trova_nome_libero(cartella_destinazione, nome_file):
    """Se nella cartella di destinazione esiste gia' un file con lo stesso nome,
    restituisce un nome nuovo tipo 'documento (1).pdf' per non sovrascrivere niente."""

    # Dividiamo il nome dalla sua estensione: "documento.pdf" -> "documento" e ".pdf"
    nome_senza_estensione, estensione = os.path.splitext(nome_file)

    # Partiamo provando il nome originale, senza modifiche.
    nome_candidato = nome_file

    # Contatore che useremo per il numero tra parentesi.
    contatore = 1

    # Finche' esiste gia' un file con il nome che stiamo proponendo...
    while os.path.exists(os.path.join(cartella_destinazione, nome_candidato)):

        # ...costruiamo un nome nuovo aggiungendo il contatore tra parentesi.
        nome_candidato = nome_senza_estensione + " (" + str(contatore) + ")" + estensione

        # Aumentiamo il contatore, cosi' al giro dopo proviamo (2), poi (3), ecc.
        contatore = contatore + 1

    # Quando il while si ferma vuol dire che il nome e' libero: lo restituiamo.
    return nome_candidato


def elenca_file_da_spostare(cartella):
    """Legge la cartella e restituisce l'elenco dei soli file da spostare,
    saltando le sottocartelle, il log e i download ancora in corso."""

    # Qui accumuleremo i nomi dei file buoni.
    file_validi = []

    # os.listdir restituisce i nomi di tutto cio' che c'e' dentro la cartella.
    for nome in os.listdir(cartella):

        # Costruiamo il percorso completo, es. C:\Users\gvast\Downloads\foto.jpg
        percorso_completo = os.path.join(cartella, nome)

        # os.path.isfile e' False per le cartelle: cosi' saltiamo le sottocartelle.
        if not os.path.isfile(percorso_completo):
            continue  # "continue" salta al prossimo elemento del ciclo

        # Saltiamo il file di log, altrimenti lo sposterebbe in "Altri".
        if nome == NOME_FILE_LOG:
            continue

        # Saltiamo questo stesso script, se per caso lo hai messo dentro Download.
        if nome == os.path.basename(__file__):
            continue

        # Ricaviamo l'estensione per controllare se e' un download incompleto.
        estensione = os.path.splitext(nome)[1].lower().lstrip(".")

        # Se e' un file temporaneo di download, lo lasciamo stare.
        if estensione in ESTENSIONI_DA_IGNORARE:
            continue

        # Se il file ha superato tutti i controlli, lo aggiungiamo all'elenco.
        file_validi.append(nome)

    # Restituiamo l'elenco ordinato alfabeticamente, cosi' l'anteprima e' leggibile.
    return sorted(file_validi)


def scrivi_log(cartella, righe):
    """Aggiunge in fondo al file di log l'elenco degli spostamenti appena fatti."""

    # Percorso completo del file di log.
    percorso_log = os.path.join(cartella, NOME_FILE_LOG)

    # Data e ora di adesso, in formato leggibile tipo 2026-07-19 15:30:12
    adesso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # open(..., "a") apre il file in modalita' "append": aggiunge in fondo
    # senza cancellare quello che c'era prima.
    # encoding="utf-8" serve per gestire correttamente accenti e caratteri speciali.
    with open(percorso_log, "a", encoding="utf-8") as file_log:

        # Scriviamo un'intestazione che separa questa esecuzione dalle precedenti.
        file_log.write("\n=== Esecuzione del " + adesso + " ===\n")

        # Scriviamo una riga per ogni spostamento effettuato.
        for riga in righe:
            file_log.write(riga + "\n")


# ============================================================================
#  PROGRAMMA PRINCIPALE
# ============================================================================

def main():
    """Funzione principale: e' quella che viene eseguita quando lanci lo script."""

    # --- Intestazione a schermo -------------------------------------------
    print("=" * 60)
    print("  ORGANIZZA DOWNLOAD")
    print("=" * 60)
    print("Cartella da organizzare:")
    print("  " + CARTELLA_DA_ORGANIZZARE)
    print()

    # --- Controllo che la cartella esista davvero -------------------------
    if not os.path.isdir(CARTELLA_DA_ORGANIZZARE):
        print("ERRORE: questa cartella non esiste.")
        print("Apri lo script e correggi la riga CARTELLA_DA_ORGANIZZARE.")
        return  # "return" interrompe la funzione: il programma finisce qui

    # --- Leggiamo l'elenco dei file ---------------------------------------
    print("Sto leggendo il contenuto della cartella...")
    file_da_spostare = elenca_file_da_spostare(CARTELLA_DA_ORGANIZZARE)

    # Se non c'e' niente da fare, avvisiamo e usciamo.
    if len(file_da_spostare) == 0:
        print("Non ho trovato file da spostare. La cartella e' gia' in ordine!")
        return

    print("Ho trovato " + str(len(file_da_spostare)) + " file.")
    print()

    # --- ANTEPRIMA: decidiamo dove andra' ogni file, senza spostare nulla --

    # Dizionario che raggruppa i file per categoria, solo per mostrarli ordinati.
    # Esempio: {"Immagini": ["foto.jpg", "logo.png"], "Video": ["clip.mp4"]}
    anteprima = {}

    for nome_file in file_da_spostare:

        # Chiediamo alla nostra funzione in che categoria va questo file.
        categoria = trova_categoria(nome_file)

        # Se e' la prima volta che incontriamo questa categoria, creiamo la lista vuota.
        if categoria not in anteprima:
            anteprima[categoria] = []

        # Aggiungiamo il file alla lista della sua categoria.
        anteprima[categoria].append(nome_file)

    # Stampiamo l'anteprima a schermo, categoria per categoria.
    print("-" * 60)
    print("ANTEPRIMA - ecco cosa farei (non ho ancora spostato niente):")
    print("-" * 60)

    # sorted() mette le categorie in ordine alfabetico.
    for categoria in sorted(anteprima.keys()):

        # Nome della categoria e quanti file contiene.
        print()
        print("[" + categoria + "]  ->  " + str(len(anteprima[categoria])) + " file")

        # Elenchiamo i file di questa categoria, rientrati di qualche spazio.
        for nome_file in anteprima[categoria]:
            print("    " + nome_file)

    print()
    print("-" * 60)

    # --- CONFERMA: chiediamo il permesso prima di toccare i file ----------

    # input() ferma il programma e aspetta che tu scriva qualcosa e prema INVIO.
    risposta = input("Vuoi procedere? Scrivi SI e premi INVIO (qualsiasi altra cosa annulla): ")

    # .strip() toglie gli spazi accidentali, .upper() rende tutto maiuscolo.
    if risposta.strip().upper() != "SI":
        print()
        print("Operazione annullata. Non ho spostato nessun file.")
        return

    # --- SPOSTAMENTO EFFETTIVO --------------------------------------------

    print()
    print("-" * 60)
    print("Inizio a spostare i file...")
    print("-" * 60)

    # Qui accumuliamo le righe da scrivere nel log.
    righe_di_log = []

    # Contatori per il riepilogo finale.
    spostati_ok = 0
    errori = 0

    for nome_file in file_da_spostare:

        # Ricalcoliamo la categoria di questo file.
        categoria = trova_categoria(nome_file)

        # Percorso della sottocartella di destinazione, es. C:\...\Downloads\Immagini
        cartella_destinazione = os.path.join(CARTELLA_DA_ORGANIZZARE, categoria)

        # os.makedirs crea la cartella; exist_ok=True evita l'errore se esiste gia'.
        os.makedirs(cartella_destinazione, exist_ok=True)

        # Controlliamo se il nome e' gia' occupato e nel caso ne otteniamo uno nuovo.
        nome_finale = trova_nome_libero(cartella_destinazione, nome_file)

        # Percorso di partenza (dove il file si trova adesso).
        percorso_origine = os.path.join(CARTELLA_DA_ORGANIZZARE, nome_file)

        # Percorso di arrivo (dove vogliamo portarlo).
        percorso_arrivo = os.path.join(cartella_destinazione, nome_finale)

        # try/except: proviamo a fare una cosa e, se va male, gestiamo l'errore
        # invece di far crashare tutto il programma.
        try:
            # shutil.move sposta davvero il file.
            shutil.move(percorso_origine, percorso_arrivo)

            # Prepariamo il messaggio da mostrare e da salvare nel log.
            if nome_finale != nome_file:
                # Caso in cui abbiamo dovuto rinominare per non sovrascrivere.
                messaggio = "SPOSTATO E RINOMINATO: " + nome_file + "  ->  " + categoria + "\\" + nome_finale
            else:
                # Caso normale.
                messaggio = "SPOSTATO: " + nome_file + "  ->  " + categoria + "\\"

            # Lo mostriamo a schermo in tempo reale.
            print("  " + messaggio)

            # E lo mettiamo da parte per il log.
            righe_di_log.append(messaggio)

            # Aggiorniamo il contatore dei successi.
            spostati_ok = spostati_ok + 1

        except Exception as errore:
            # Se qualcosa va storto (file aperto in un programma, permessi mancanti...)
            # lo segnaliamo e proseguiamo con il file successivo.
            messaggio = "ERRORE su " + nome_file + ": " + str(errore)
            print("  " + messaggio)
            righe_di_log.append(messaggio)
            errori = errori + 1

    # --- SALVATAGGIO DEL LOG ----------------------------------------------

    scrivi_log(CARTELLA_DA_ORGANIZZARE, righe_di_log)

    # --- RIEPILOGO FINALE -------------------------------------------------

    print()
    print("=" * 60)
    print("FATTO!")
    print("  File spostati correttamente: " + str(spostati_ok))
    print("  Errori: " + str(errori))
    print("  Log salvato in: " + os.path.join(CARTELLA_DA_ORGANIZZARE, NOME_FILE_LOG))
    print("=" * 60)


# Questa riga fa partire la funzione main() quando lanci il file con Python.
# Serve per convenzione: se un giorno importerai questo file dentro un altro
# script, il programma non partira' da solo.
if __name__ == "__main__":
    main()

    # Tiene la finestra aperta finche' non premi INVIO, cosi' fai in tempo a leggere
    # il risultato anche se hai lanciato lo script con un doppio clic.
    input("\nPremi INVIO per chiudere...")
