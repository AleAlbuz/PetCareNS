import sqlite3 
import csv # Per gestione CSV
import os # Per gestione directory
import sys
from datetime import datetime
import re


## SQL Statements per caricamento tabelle

# Tabella dipendenti
carica_tab_dipendenti = """ INSERT INTO DIPENDENTE (
                    ID_DIPENDENTE, NOME, COGNOME, ZONA, RUOLO)
                    VALUES(:ID_DIPENDENTE, :NOME, :COGNOME, :ZONA, :RUOLO)
"""

# Tabella Clienti
carica_tab_clienti = """ INSERT INTO CLIENTE (
                    ID_CLIENTE, NOME_CLIENTE, ZONA, DATA_ISCRIZIONE)
                    VALUES(:ID_CLIENTE, :NOME_CLIENTE, :ZONA, :DATA_ISCRIZIONE)
                   """
# Tabella fornitori
carica_tab_fornitori = """ INSERT INTO FORNITORE (
                    ID_FORNITORE, ID_DIPENDENTE, NOME, CATEGORIA_SERVIZIO, ZONA, COSTO_ORARIO)
                    VALUES(:ID_FORNITORE, :ID_DIPENDENTE, :NOME, :CATEGORIA_SERVIZIO, :ZONA, :COSTO_ORARIO)
                   """

# Tabella operatori
carica_tab_operatori = """ INSERT INTO OPERATORE (
                    ID_OPERATORE, ZONA, TIPO_ATTIVITA)
                    VALUES(:ID_OPERATORE, :ZONA, :TIPO_ATTIVITA)
                   """

# Tabella tempo
carica_tab_tempo = """ INSERT INTO TEMPO (
                    ID_TEMPO, DATA, GIORNO, MESE, ANNO, GIORNO_SETTIMANA)
                    VALUES(:ID_TEMPO, :DATA, :GIORNO, :MESE, :ANNO, :GIORNO_SETTIMANA)
                   """

# Tabella richiesta
carica_tab_richiesta = """ INSERT INTO RICHIESTA (
                    ID_RICHIESTA, ID_CLIENTE, ID_FORNITORE, ID_OPERATORE, ID_TEMPO, 
                    DATA, ORA, TIPO_RICHIESTA, IMPORTO_FORNITORE, RICAVO, TEMPO_EROGAZIONE, STATO_RICHIESTA, RATING)
                    VALUES(:ID_RICHIESTA, :ID_CLIENTE, :ID_FORNITORE, :ID_OPERATORE, :ID_TEMPO, 
                    :DATA, :ORA, :TIPO_RICHIESTA, :IMPORTO_FORNITORE, :RICAVO, :TEMPO_EROGAZIONE, :STATO_RICHIESTA, :RATING)
                   """


# GIORNO_SETTIMANA
lista_giorni = { 
    1 : "Lunedì",
    2 : "Martedì",
    3 : "Mercoledì",
    4 : "Giovedì",
    5 : "Venerdì",
    6 : "Sabato",
    7 : "Domenica"
}

## Estrazione - INIT

def leggi_csv(filename):
    # Apre il csv in lettura e restituisce una lista di dizionari
    
    filepath = "csv/" + filename

    if not os.path.exists(filepath):
        print(f"Errore: il file {filepath} non esiste")
        return

    with open(filepath, mode = "r", encoding = "utf-8-sig", newline = "") as file:
        csv_reader = csv.DictReader(file, delimiter = ";")

        lista_records = []
        for record in csv_reader:
            lista_records.append(record)

    return lista_records

## Estrazione - END


## Caricamento - INIT

def carica_tab(nome_tabella, sql_statement, lista_records):

    # Creazione e connesione al DB
    try:
        with sqlite3.connect("db/petcarens.db") as conn:
            cursor = conn.cursor()

            # Cancellazione contenuto tabella prima del caricamento
            cursor.execute(f"DELETE FROM {nome_tabella};")

            cursor.executemany(sql_statement, lista_records)

            conn.commit()

            print(f"Tabella: {nome_tabella} caricata con successo. ")
    
    except sqlite3.OperationalError as sql3_err:
        print(f"Errore caricamento tabella: {nome_tabella}. ", sql3_err)

## Caricamento - END


## Check per fase Trasformazione - INIT

def check_testo(testo_in):

    # Rimuove caratteri speciali non consentiti "#", "§", "$", "£"
    testo_out = re.sub(r"[#§$£]", "", testo_in)

    # Rimuove eventuali spazi di troppo
    testo_out = testo_out.strip()
    testo_out = testo_out.upper()

    return testo_out


def check_data(data_in):

    # Converto data_in da stringa a datetime
    data_in_datetime = datetime.strptime(data_in, "%d/%m/%Y")
    
    data_out = data_in_datetime.strftime("%Y-%m-%d")
    #data_out = data_in_datetime.date()


    return data_out


def check_numero_real(numero_in):
     
    numero_string = numero_in.strip()
    numero_string.replace(",", ".")
    try:
        if re.fullmatch(r"\d+(,\d+)?", numero_string):
            numero_out = float(numero_string)
            return numero_out
    except ValueError:
        return "Errore: numero " + f"{numero_in}" + " non valido"


def check_numero_int(numero_in):
    numero_string = numero_in.strip()
    numero_string.replace(",", ".")

    try:
        numero_out = float(numero_string)
        return int(numero_out)
    except ValueError:
        return "Errore: numero " + f"{numero_in}" + " non intero"

## Check per fase Trasformazione - END


## Get varie - INIT

def get_date_richieste(richieste_in):
    # Creazione set univoco di data
    set_date = set()

    for richiesta in richieste_in:
        data_string = richiesta.get("DATA")
        # Rimozione eventuali spazi
        data = check_data(data_string)
        set_date.add(data)
    
    # Sort delle date
    set_date = sorted(set_date)

    return set_date


def get_id_tempo(data_in):
    id_tempo_out = ""

    sql_get_id_tempo = """SELECT ID_TEMPO 
                             FROM TEMPO
                             WHERE DATA = ?;
                            """

    data_richiesta = data_in 

    try:
        with sqlite3.connect("db/petcarens.db") as conn:
            cursor = conn.cursor()

            # Get ID_TEMPO mappato in tabella TEMPO
            cursor.execute(sql_get_id_tempo, (data_richiesta,))
            id_tempo_out = cursor.fetchone()
    
    except sqlite3.OperationalError as sql3_err:
        print(f"Errore: recupero TEMPO-ID_TEMPO:", sql3_err)

    return id_tempo_out[0]


def get_ricavo(importo_fornitore_in):
    ricavo_out = 0.00

    #Il ricavo corrisponde al 20% dell'importo pagato al fornitore
    ricavo_out = ( importo_fornitore_in * 20 ) / 100

    return ricavo_out

## Get varie - END


## Trasformazione - INIT

def trasforma_dipendenti(dipendenti_in):
    # ID_DIPENDENTE, NOME, COGNOME, ZONA, RUOLO
    dipendenti_out = []

    for dipendente in dipendenti_in:
        id_dipendente_out = check_testo(dipendente.get("ID_DIPENDENTE")) 
        nome_out = check_testo(dipendente.get("NOME"))
        cognome_out = check_testo(dipendente.get("COGNOME"))
        zona_out = check_testo(dipendente.get("ZONA"))
        ruolo_out = check_testo(dipendente.get("RUOLO"))
        
        dipendenti_out.append({
            "ID_DIPENDENTE" : id_dipendente_out,
            "NOME" : nome_out,
            "COGNOME" : cognome_out,
            "ZONA" : zona_out,
            "RUOLO" : ruolo_out
        })
        
    return dipendenti_out

def trasforma_clienti(clienti_in):
    # ID_CLIENTE, ZONA, DATA_ISCRIZIONE
    clienti_out = []

    for cliente in clienti_in:
        id_cliente_out = check_testo(cliente.get("ID_CLIENTE")) 
        nome_cliente_out = check_testo(cliente.get("NOME_CLIENTE"))
        zona_out = check_testo(cliente.get("ZONA"))
        data_iscrizione_out = check_data(cliente.get("DATA_ISCRIZIONE"))
        
        clienti_out.append({
            "ID_CLIENTE" : id_cliente_out,
            "NOME_CLIENTE" : nome_cliente_out,
            "ZONA" : zona_out,
            "DATA_ISCRIZIONE" : data_iscrizione_out
        })
        
    return clienti_out

    
def trasforma_fornitori(fornitori_in):
    # ID_FORNITORE, ID_DIPENDENTE, NOME, CATEGORIA_SERVIZIO, ZONA, COSTO_ORARIO
    fornitori_out = []

    for fornitori in fornitori_in:
        id_fornitore_out = check_testo(fornitori.get("ID_FORNITORE")) 
        id_dipendente_out = check_testo(fornitori.get("ID_DIPENDENTE")) 
        nome_out = check_testo(fornitori.get("NOME")) 
        categoria_servizio_out = check_testo(fornitori.get("CATEGORIA_SERVIZIO")) 
        zona_out = check_testo(fornitori.get("ZONA"))
        costo_orario_out = check_numero_real(fornitori.get("COSTO_ORARIO"))

        fornitori_out.append({
            "ID_FORNITORE" : id_fornitore_out,
            "ID_DIPENDENTE" : id_dipendente_out,
            "NOME" : nome_out,
            "CATEGORIA_SERVIZIO" : categoria_servizio_out,
            "ZONA" : zona_out,
            "COSTO_ORARIO" : costo_orario_out
        })

    return fornitori_out 


def trasforma_operatori(operatori_in):
    # ID_OPERATORE, ZONA, TIPO_ATTIVITA
    operatori_out = []

    for operatori in operatori_in:
        id_operatore_Out = check_testo(operatori.get("ID_OPERATORE")) 
        zona_out = check_testo(operatori.get("ZONA")) 
        tipo_attivita_out = check_testo(operatori.get("TIPO_ATTIVITA")) 
        
        operatori_out.append({
            "ID_OPERATORE" : id_operatore_Out,
            "ZONA" : zona_out,
            "TIPO_ATTIVITA" : tipo_attivita_out
        })

    return operatori_out


def trasforma_tempo(tempo_in):
    #ID_TEMPO, DATA, GIORNO, MESE, ANNO, GIORNO_SETTIMANA
    tempo_out = []

    for tempo in tempo_in:
        # Conversione tempo in datetime
        tempo_dt = datetime.strptime(tempo, "%Y-%m-%d")
        id_tempo_out = "T_" + tempo_dt.strftime("%Y%m%d")
        data_out = tempo # Stringa
        giorno_out = tempo_dt.day
        mese_out = tempo_dt.month
        anno_out = tempo_dt.year

        key_giorno = tempo_dt.isoweekday()
        giorno_settimana_out = lista_giorni[key_giorno]

        tempo_out.append({
            "ID_TEMPO" : id_tempo_out,
            "DATA" : data_out,
            "GIORNO" : giorno_out,
            "MESE" : mese_out,
            "ANNO" : anno_out,
            "GIORNO_SETTIMANA" : giorno_settimana_out
        })

    return tempo_out
    

def trasforma_richieste(richieste_in):
# "ID_RICHIESTA", "ID_CLIENTE", "ID_FORNITORE", "ID_OPERATORE", "ID_TEMPO", "DATA",
# "ORA", "TIPO_RICHIESTA", "IMPORTO_FORNITORE", "RICAVO", "TEMPO_EROGAZIONE", "STATO_RICHIESTA", "RATING"
    richieste_out = []
    id_richieste_elaborate = set()

    tot_duplicati = 0

    # Esegui prima etl TEMPO per popolare prima la tabella TEMPO e creare gli ID_TEMPO
    etl_tempo(richieste_in)

    for richiesta in richieste_in:
        # ID
        id_richiesta_out = check_testo(richiesta.get("ID_RICHIESTA"))

        if id_richiesta_out in id_richieste_elaborate:
            # Richiesta già elaborata
            tot_duplicati = tot_duplicati + 1
        else:
            # Inserimento id richiesta nel set di quelle già elaborate
            id_richieste_elaborate.add(id_richiesta_out)
            id_cliente_out = check_testo(richiesta.get("ID_CLIENTE"))
            id_fornitore_out = check_testo(richiesta.get("ID_FORNITORE"))
            id_operatore_out = check_testo(richiesta.get("ID_OPERATORE"))

            # Gestione tempo
            data_out = check_data(richiesta.get("DATA"))
            ora_out = check_testo(richiesta.get("ORA"))
            id_tempo_out = get_id_tempo(data_out)

            tipo_richiesta_out = check_testo(richiesta.get("TIPO_RICHIESTA"))
            importo_fornitore_out = check_numero_real(richiesta.get("IMPORTO_FORNITORE"))
            ricavo_out = get_ricavo(importo_fornitore_out)
            tempo_erogazione_out = check_numero_int(richiesta.get("TEMPO_EROGAZIONE"))
            stato_richiesta_out = check_testo(richiesta.get("STATO_RICHIESTA"))
            rating = check_numero_int(richiesta.get("RATING"))
            
            richieste_out.append({
                "ID_RICHIESTA" : id_richiesta_out,
                "ID_CLIENTE" : id_cliente_out,
                "ID_FORNITORE" : id_fornitore_out,
                "ID_OPERATORE" : id_operatore_out,
                "ID_TEMPO" : id_tempo_out,
                "DATA" : data_out,
                "ORA" : ora_out,
                "TIPO_RICHIESTA" : tipo_richiesta_out, 	
                "IMPORTO_FORNITORE" : importo_fornitore_out,
                "RICAVO" : ricavo_out,
                "TEMPO_EROGAZIONE" : tempo_erogazione_out,
                "STATO_RICHIESTA" : stato_richiesta_out,
                "RATING" : rating
            })

    if tot_duplicati > 0:
        print(f"Sono state rilevate e scartate {tot_duplicati} richieste duplicate")


    return richieste_out

## Trasformazione - END


## Start ETL - INIT
def etl_dipendenti():
    # ETL Dipendenti
    print("Avvio ETL per dipendenti")

    # Estrazione
    lista_dipendenti = []
    lista_dipendenti = leggi_csv("lista_dipendenti.csv")

    # Trasformazione
    lista_dipendenti_t = trasforma_dipendenti(lista_dipendenti)

# Caricamento
    carica_tab("DIPENDENTE", carica_tab_dipendenti, lista_dipendenti_t)

def etl_clienti():
    # ETL clienti
    print("Avvio ETL per clienti")

# Estrazione
    lista_clienti = []
    lista_clienti = leggi_csv("lista_clienti.csv")

# Trasformazione
    lista_clienti_t = trasforma_clienti(lista_clienti)

# Caricamento
    carica_tab("CLIENTE", carica_tab_clienti, lista_clienti_t)


def etl_fornitori():
    # ETL fornitori
    print("Avvio ETL per Fornitori")
# Estrazione
    lista_fornitori = []
    lista_fornitori = leggi_csv("lista_fornitori.csv")
# Trasformazione
    lista_fornitori_t = trasforma_fornitori(lista_fornitori)
# Caricamento
    carica_tab("FORNITORE", carica_tab_fornitori, lista_fornitori_t)


def etl_operatori():
    # ETL operatori
    print("Avvio ETL per Operatori")
    # Estrazione
    lista_operatori = []
    lista_operatori = leggi_csv("lista_operatori.csv")
    # Trasformazione
    lista_operatori_t = trasforma_operatori(lista_operatori)
    # Caricamento
    carica_tab("OPERATORE", carica_tab_operatori, lista_operatori_t)


def etl_tempo(richieste_in):
    # ETL tempo
    print("Avvio ETL Tempo")
    # Estrazione
    lista_tempo = get_date_richieste(richieste_in)
    # Trasformazione
    lista_tempo_t = trasforma_tempo(lista_tempo)
    # Caricamento
    carica_tab("TEMPO", carica_tab_tempo, lista_tempo_t)
    

def etl_richieste():
    # ETL richieste
    print("Avvio ETL per Richieste")

    # Estrazione
    lista_richieste = []
    lista_richieste = leggi_csv("lista_richieste.csv")
    # Trasformazione
    lista_richieste_t = trasforma_richieste(lista_richieste)
    # Caricamento
    carica_tab("RICHIESTA", carica_tab_richiesta, lista_richieste_t)
        

## Start ETL - INIT


## Main
if __name__ == "__main__":
    try:

# Lo script etl deve essere necessariamente lanciato dopo db_init e crea_random_csv
# db_inid crea il db petcarens.db mentre crea_radom_csv crea la directory csv con i file al suo interno
# Controllo di esistenza di entrambe le directory
        if not os.path.exists("db/petcarens.db"):
            print("Errore: il db 'db/petcarens.db' non esiste. Eseguire prima script db_init.py")
            sys.exit()

        if not os.path.exists("csv"):
            print("Errore: la directory 'csv' non esiste. Eseguire prima script crea_random_csv.py")
            sys.exit()

        etl_dipendenti()
        etl_clienti()
        etl_fornitori()
        etl_operatori()
        etl_richieste()

    except Exception as errore:
        print(f"Errore durante pipeline ETL: {errore}")