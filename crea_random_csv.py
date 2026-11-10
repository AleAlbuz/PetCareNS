import random # Per generazione numeri casuali

import csv # Per gestione CSV

import os # Per gestione cartelle

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
    with open(nome_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=lista_labels,
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(lista_records)


random.seed(24) # Numero di partenza sempre uguale per generare sempre gli stessi dati


# Check e creazione cartella CSV se non presente


## Creazione dati random

# Creazione lista clienti

# Creazione lista fornitori
def crea_fornitori(n):
    # ID_FORNITORE, NOME, CATEGORIA_SERVIZIO, ZONA
    lista_fornitori = []

    for i in range(1, n +1):
        id_fornitore = "FORN_" + str(n)
        nome =  "Nome_" + str(n) # Temporaneo
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

# Creazione lista operatori

# Creazione lista tempo

# Creazione lista richieste


## Main
crea_fornitori(300)