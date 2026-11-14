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
# Con range di importi e tempistiche per categoria
lista_categorie = { 
    "Toilettatura" :            {"costo_orario" : (30.0, 60.0), "tempo_erogazione" : (40, 80)},
    "Visita veterinaria" :      {"costo_orario" : (50.0, 90.0), "tempo_erogazione" : (20, 45)},
    "Cat sitting" :             {"costo_orario" : (15.0, 60.0), "tempo_erogazione" : (60, 240)},
    "Dog walking" :             {"costo_orario" : (20.0, 80.0), "tempo_erogazione" : (25, 100)},
    "Visita comportamentale" :  {"costo_orario" : (70.0, 100.0), "tempo_erogazione" : (60, 90)},
    "Visita nutrizionistica" :  {"costo_orario" : (60.0, 90.0), "tempo_erogazione" : (30, 60)}
}

# NOME (fornitore)
# Da implementare

# TIPO_ATTIVITA
lista_att_oper = [  
    "Customer Care",
    "Responsabile Fornitori",
    "Responsabile Pagamenti",
    "Gestione richieste"
]

# STATO
lista_stati_rich = { 
    "Nuova Richiesta" : 2,
    "Presa in carico" : 3,
    "Elaborata" : 5,
    "Annullata" : 1
}

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

# Orizzonte temporale per iscrizione clienti e data richieste
today = date.today()
last_date = today - timedelta(days = 1)
first_date = date(2024, 1, 1) 
delta_days = (today - first_date).days
total_days = ( last_date - first_date ).days


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
    # ID_FORNITORE, NOME, CATEGORIA_SERVIZIO, ZONA, COSTO_ORARIO
    lista_fornitori = []

    for i in range(1, n +1):
        id_fornitore = "FORN_" + str(i)
        nome =  "Nome_" + str(i) # Temporaneo
        categoria_servizio = random.choice(lista_categorie.keys())

        citta = list(lista_pesata_citta.keys())
        pesi = list(lista_pesata_citta.values())
        zona = random.choices(citta, weights = pesi, k = 1)

        # Calcolo costo orario
        dati_categoria = lista_categorie[categoria_servizio]
        costo_orario_min, costo_orario_max = dati_categoria["costo_orario"]
        costo_orario = round(random.uniform(costo_orario_min, costo_orario_max),2)

        lista_fornitori.append({
            "ID_FORNITORE" : id_fornitore,
            "NOME" : nome,
            "CATEGORIA_SERVIZIO" : categoria_servizio,
            "ZONA" : zona, 
            "COSTO_ORARIO" : costo_orario
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
        id_cliente = cli["ID_CLIENTE"]
        zona = cli["ZONA"]

        # Estrazione fornitore della stessa zona ( se presente )
        fornitori_zona = []
        for forn in fornitori:
            if forn["ZONA"] == zona:
                fornitori_zona.append(forn)
        fornitore = random.choice(fornitori_zona)
        id_fornitore = fornitore["ID_FORNITORE"]

        # Per comodità recupero tipologia_richiesta 
        # dalla categoria di servizio del fornitore estratto
        tipo_richiesta = fornitore["CATEGORIA_SERVIZIO"]
        dati_categoria = lista_categorie[tipo_richiesta]
        t_erogazione_min, t_erogazione_max = dati_categoria["tempo_erogazione"]
        tempo_erogazione = random.randint(t_erogazione_min, t_erogazione_max)

        # Generazione data casuale con più probabilità negli orari lavorativi per il cliente (9-18)
        # Nessuna richiesta tra le 22 e le 6 del mattino
                    # 00 01 02 03 04 05 06 07 08 09 10  11  12 13 14  15  16 17 18 19 20 21 22 23 
        pesi_orario = [0, 0, 0, 0, 0, 0, 0, 1, 1, 8, 9, 10, 10, 8, 8, 10, 10, 9, 8, 6, 5, 1, 0, 0]
        range_ore = list(range(24))

        #Scelta di un giorno casuale
        add_giorni = random.randint(0, total_days)
        data = first_date + timedelta(days = add_giorni)
        ora = random.choices( population = range_ore,
                              weights = pesi_orario,
                              k = 1
                            )[0]


        # Estrazione operatori della stessa zona (se presente )
        operatori_zona = []
        for oper in operatori:
            if oper["ZONA"] == zona:
                operatori_zona.append(oper)
        operatore = random.choice(operatori_zona)
        id_operatore = operatori_zona["ID_OPERATORE"]

        # Recupera stato richiesta dalla lista pesata
        stati = list(lista_stati_rich.keys())
        pesi_stati = list(lista_stati_rich.values())
        stato_richiesta = random.choices(stati, weights = pesi_stati, k = 1)

        lista_richieste.append({
            "ID_RICHIESTA" : id_richiesta,
            "ID_CLIENTE" : id_cliente,
            "ID_FORNITORE" : id_fornitore,
            "ID_OPERATORE" : id_operatore,
            # "ID_TEMPO" : "", # Verrà calcolato successivamente nello script ETL
            "DATA" : data,
            "ORA" : ora,
            "TIPO_RICHIESTA" : tipo_richiesta,
            #"IMPORTO_FORNITORE" :  # L'importo fornitore verrà calcolato nello script ETL in base al costo_orario del fornitore scelto
            # "RICAVO" : "", # Il ricavo verrà calcolato nello script ETL come % dell'importo pagato
            "TEMPO_EROGAZIONE" : tempo_erogazione,
            "STATO_RICHIESTA" : stato_richiesta
        })

        crea_csv("lista_richieste.csv", lista_richieste[0].keys(), lista_richieste)



## Main
clienti_creati = crea_clienti(450)
fornitori_creati = crea_fornitori(300)
operatori_creati = crea_operatori(300)
crea_richieste(600, clienti_creati, fornitori_creati, operatori_creati)