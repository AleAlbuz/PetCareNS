import sqlite3 
import csv # Per gestione CSV
import os # Per gestione directory
import sys
from datetime import datetime
import re


## SQL Statements per caricamento tabelle

# Tabella Clienti
carica_tab_clienti = """ INSERT INTO CLIENTE (
                    ID_CLIENTE, ZONA TEXT, DATA_ISCRIZIONE)
                    VALUES(?,?,?)
                   """
# Tabella fornitori
carica_tab_fornitori = """ INSERT INTO FORNITORE (
                    ID_FORNITORE, NOME, CATEGORIA_SERVIZIO, ZONA, COSTO_ORARIO)
                    VALUES(?,?,?,?,?)
                   """

# Tabella operatori
carica_tab_operatori = """ INSERT INTO OPERATORE (
                    ID_OPERATORE, ZONA, TIPO_ATTIVITA)
                    VALUES(?,?,?)
                   """



# GIORNO_SETTIMANA
lista_giorni = [ 
    "Lunedì",
    "Martedì",
    "Mercoledì",
    "Giovedì",
    "Venerdì",
    "Sabato",
    "Domenica"
]


def leggi_csv(filename):
    # Apre il csv in lettura e restituisce una lista di dizionari
    
    filepath = "csv/" + filename

    if not os.path.exists(filepath):
        print(f"Errore: il file {filepath} non esiste")
        return

    with open(filepath, more = "r", encoding = "utf-8-sig", newline = "") as file:
        csv_reader = csv.DictReader(file)

        lista_records = []
        for record in csv_reader:
            lista_records.append(record)

    return lista_records

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

    return data_out

def check_numero_real(numero_in):
    numero_out = 0.00

    if re.fullmatch(r"\d+(,\d+)?", numero_in):
        numero_out = float(numero_in.replace(",", "."))
    # Gestire errore

    return numero_out
    

def trasforma_clienti(clienti_in):
    # ID_CLIENTE, ZONA, DATA_ISCRIZIONE
    clienti_out = []

    for cliente in clienti_in:
        id_cliente_out = check_testo(clienti_in["ID_CLIENTE"]) 
        zona_out = check_testo(clienti_in["ZONA"])
        data_iscrizione_out = check_data(clienti_in["DATA_ISCRIZIONE"])
        
        clienti_out.append({
            "ID_CLIENTE" : id_cliente_out,
            "ZONA" : zona_out,
            "DATA_ISCRIZIONE" : data_iscrizione_out
        })
        
    return clienti_out


def carica_tab(nome_tabella, sql_statement, lista_records):

    # Creazione e connesione al DB
    try:
        with sqlite3.connect("db/petcarens.db") as conn:
            cursor = conn.cursor()

            cursor.executemany(sql_statement, lista_records)

            conn.commit()
    
    except sqlite3.OperationalError as sql3_err:
        print(f"Errore caricamento tabella: {nome_tabella}. ", sql3_err)


    
def trasforma_fornitori(fornitori_in):
    # ID_FORNITORE, NOME, CATEGORIA_SERVIZIO, ZONA, COSTO_ORARIO
    fornitori_out = []

    for fornitori in fornitori_in:
        id_fornitore_Out = check_testo(fornitori_in["ID_FORNITORE"]) 
        nome_out = check_testo(fornitori_in["NOME"]) 
        categoria_servizio_out = check_testo(fornitori_in["CATEGORIA_SERVIZIO"]) 
        zona_out = check_testo(fornitori_in["ZONA"])
        costo_orario_out = check_numero_real(fornitori_in["COSTO_ORARIO"])

        fornitori_out.append({
            "ID_FORNITORE" : id_fornitore_Out,
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
        id_operatore_Out = check_testo(operatori_in["ID_OPERATORE"]) 
        zona_out = check_testo(operatori_in["ZONA"]) 
        tipo_attivita_out = check_testo(operatori_in["TIPO_ATTIVITA"]) 
        
        operatori_out.append({
            "ID_FORNITORE" : id_operatore_Out,
            "ZONA" : zona_out,
            "TIPO_ATTIVITA" : tipo_attivita_out
        })

    return operatori_out


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


def etl_richieste():
    # ETL richieste
    print("Avvio ETL per Richieste")

# Estrazione
    lista_richieste = []
    lista_richieste = leggi_csv("lista_richieste.csv")

# Trasformazione


# Caricamento




# Lo script etl deve essere necessariamente lanciato dopo db_init e crea_random_csv
# db_inid crea il db petcarens.db mentre crea_radom_csv crea la directory csv con i file al suo interno
# Controllo di esistenza di entrambe le directory
if not os.path.exists("db/petcarens.db"):
    print("Errore: il db 'db/petcarens.db' non esiste. Eseguire prima script db_init.py")
    sys.exit()

if not os.path.exists("csv"):
    print("Errore: la directory 'csv' non esiste. Eseguire prima script crea_random_csv.py")
    sys.exit()





# Main

if __name__ == "__main__":
    try:
        etl_clienti()
        etl_fornitori()
        etl_operatori()
        etl_richieste()
    except Exception as errore:
        print(f"Errore ETL: {errore}")