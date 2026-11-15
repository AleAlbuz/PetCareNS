import sqlite3 
import csv # Per gestione CSV
import os # Per gestione directory
import sys
from datetime import datetime
import re


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

    return testo_out


def check_data(data_in):

    # Converto data_in da stringa a datetime
    data_in_datetime = datetime.strptime(data_in, "%d/%m/%Y")
    
    data_out = data_in_datetime.strftime("%Y-%m-%d")

    return data_out


def trasforma_clienti(clienti_in):
    # ID_CLIENTE, ZONA, DATA_ISCRIZIONE
    clienti_out = []

    for cliente in clienti_in:
        id_cliente_out = check_testo(clienti_in["ID_CLIENTE"]) 
        zona_out = check_testo(clienti_in["ZONA"])
        data_iscrizione_out = check_data(clienti_in["DATA_ISCRIZIONE"])

    return clienti_out



def etl_clienti():
    # ETL clienti
    print("Avvio ETL per clienti")

# Estrazione
    lista_clienti = []
    lista_clienti = leggi_csv("lista_clienti.csv")

# Trasformazione
    lista_clienti_t = trasforma_clienti(lista_clienti)


# Caricamento


def etl_fornitori():
    # ETL fornitori
    print("Avvio ETL per Fornitori")

# Estrazione
    lista_fornitori = []
    lista_fornitori = leggi_csv("lista_fornitori.csv")

# Trasformazione


# Caricamento


def etl_operatori():
    # ETL operatori
    print("Avvio ETL per Operatori")

# Estrazione
    lista_operatori = []
    lista_operatori = leggi_csv("lista_operatori.csv")

# Trasformazione


# Caricamento


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