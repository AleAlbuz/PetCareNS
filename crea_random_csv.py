import random # Per generazione numeri casuali

import csv # Per gestione CSV

import os # Per gestione directory

import shutil # Per cancellazione directory

from datetime import date, timedelta # Per generazione date casuali


## Liste valori per generazione dati random

# ZONA
# Città italiane più popolose secondo Wikipedia
lista_pesata_citta = {
    "Roma": 2744528,
    "Milano": 1363713,
    "Napoli": 903998,
    "Torino": 855948,
    "Palermo": 625765,
    "Genova": 566569,
    "Bologna": 391724,
    "Firenze": 361574,
    "Bari": 316175,
    "Catania": 296855,
    "Verona": 255313,
    "Venezia": 249434,
    "Messina": 216324,
    "Padova": 208360,
    "Brescia": 201622,
    "Parma": 199705,
    "Prato": 198777,
    "Trieste": 198552,
    "Taranto": 184840,
    "Modena": 184445
}


# CATEGORIA_SERVIZIO
lista_categorie = [ "Toilettatura",
                    "Visita veterinaria",
                    "Cat sitting",
                    "Dog walking",
                    "Visita comportamentale",
                    "Visita nutrizionistica" 
]

# NOME (fornitore)
# Da implementare

# TIPO_ATTIVITA
lista_att_oper = [  "Customer Care",
                    "Responsabile Fornitori",
                    "Responsabile Pagamenti",
                    "Gestione richieste"
]

# STATO
lista_stati_rich = [ "Nuova Richiesta",
                     "Presa in carico",
                     "Elaborata",
                     "Annullata"
]

# GIORNO_SETTIMANA
lista_giorni = [ "Lunedì",
                 "Martedì",
                 "Mercoledì",
                 "Giovedì",
                 "Venerdì",
                 "Sabato",
                 "Domenica"
]

# Creazione file csv
def crea_csv(nome_file, lista_labels, lista_records):
    nome_file_dir = "csv/" + nome_file
    with open(nome_file_dir, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=lista_labels,
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(lista_records)


random.seed(24) # Numero di partenza sempre uguale per generare sempre gli stessi dati


# Inizializzazione directory csv (cancellazione + creazione)
if os.path.exists("csv"):
    shutil.rmtree("csv") # Cancella la directory ed il suo contenuto

try:
    os.mkdir("csv") # Crea directory, se esiste da exception
    print("Creata directory csv")
except FileExistsError:
    print("La directory csv esiste già, nessuna creazione")


## Creazione dati random

# Creazione lista clienti
def crea_clienti(n):
    # ID_CLIENTE, ZONA, DATA_ISCRIZIONE
    lista_clienti = []

    # Clienti iscritti da quando è nata la startup 01.01.2024
    today = date.today()
    first_date = date(2024, 1, 1) 
    delta_days = (today - first_date).days

    for i in range(1, n +1):
        id_cliente = "CLI_" + str(i)

        citta = list(lista_pesata_citta.keys())
        pesi = list(lista_pesata_citta.values())
        zona = random.choices(citta, weights = pesi, k = 1)

        days_to_add = random.randint(0, delta_days)
        data_iscrizione = first_date + timedelta(days_to_add)

        lista_clienti.append({
            "ID_CLIENTE" : id_cliente,
            "ZONA" : zona ,
            "DATA_ISCRIZIONE" : data_iscrizione
        })

    crea_csv("lista_clienti.csv", lista_clienti[0].keys(), lista_clienti)

    return lista_clienti

# Creazione lista fornitori
def crea_fornitori(n):
    # ID_FORNITORE, NOME, CATEGORIA_SERVIZIO, ZONA
    lista_fornitori = []

    for i in range(1, n +1):
        id_fornitore = "FORN_" + str(i)
        nome =  "Nome_" + str(i) # Temporaneo
        categoria_servizio = random.choice(lista_categorie)

        citta = list(lista_pesata_citta.keys())
        pesi = list(lista_pesata_citta.values())
        zona = random.choices(citta, weights = pesi, k = 1)

        lista_fornitori.append({
            "ID_FORNITORE" : id_fornitore,
            "NOME" : nome,
            "CATEGORIA_SERVIZIO" : categoria_servizio,
            "ZONA" : zona 
        })

    crea_csv("lista_fornitori.csv", lista_fornitori[0].keys(), lista_fornitori)

    return lista_fornitori


# Creazione lista operatori
def crea_operatori(n):
    # ID_OPERATORE, ZONA, TIPO_ATTIVITA
    lista_operatori = []

    for i in range(1, n +1):
        id_operatore = "OPER_" + str(i)
        tipo_attivita = random.choice(lista_att_oper)

        citta = list(lista_pesata_citta.keys())
        pesi = list(lista_pesata_citta.values())
        zona = random.choices(citta, weights = pesi, k = 1)

        lista_operatori.append({
            "ID_OPERATORE" : id_operatore,
            "ZONA" : zona,
            "TIPO_ATTIVITA" : tipo_attivita 
        })

    crea_csv("lista_operatori.csv", lista_operatori[0].keys(), lista_operatori)

    return lista_operatori


# Creazione lista richieste
def crea_richieste(n, clienti, fornitori, operatori):
    # ID_RICHIESTA, ID_CLIENTE, ID_FORNITORE, ID_OPERATORE, ID_TEMPO, 
    # DATA, ORA, TIPO_RICHIESTA, IMPORTO_FORNITORE, RICAVO, TEMPO_EROGAZIONE, STATO_RICHIESTA
    lista_richieste = []

    for i in range(1, n + 1):
    
        id_richiesta = "RIC_" + str(i)

        # Estrazione cliente che ha effettuato la richiesta
        cli = random.choice(clienti)
        id_cliente = cli[id_cliente]
        zona = cli[zona]

        # Estrazione fornitore della stessa zona ( se presente )
        fornitori_zona = []
        for forn in fornitori:
            if forn[zona] == zona:
                fornitori_zona.append(forn)
        fornitore = random.choice(fornitori_zona)
        id_fornitore = fornitori_zona[id_fornitore]

        # Estrazione operatori della stessa zona (se presente )
        operatori_zona = []
        for oper in operatori:
            if oper[zona] == zona:
                operatori_zona.append(oper)
        operatore = random.choice(operatori_zona)
        id_operatore = operatori_zona[id_operatore]


        lista_richieste.append({
            "ID_RICHIESTA" : id_richiesta,
            "ID_CLIENTE" : id_cliente,
            "ID_FORNITORE" : id_fornitore,
            "ID_OPERATORE" : id_operatore,
            # "ID_TEMPO" : "", # Verrà calcolato successivamente nello script ETL
            "DATA" : "",
            "ORA" : "",
            "TIPO_RICHIESTA" : "",
            "IMPORTO_FORNITORE" : "",
            "RICAVO" : "",
            "TEMPO_EROGAZIONE" : "",
            "STATO_RICHIESTA" : ""
        })

        crea_csv("lista_richieste.csv", lista_richieste[0].keys(), lista_richieste)



## Main
clienti_creati = crea_clienti(450)
fornitori_creati = crea_fornitori(300)
operatori_creati = crea_operatori(300)
crea_richieste(600, clienti_creati, fornitori_creati, operatori_creati)