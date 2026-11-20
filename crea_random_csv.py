import random # Per generazione numeri casuali
import csv # Per gestione CSV
import os # Per gestione directory
import shutil # Per cancellazione directory
from datetime import datetime, date, timedelta # Per generazione date casuali


## Liste valori per generazione dati random
lista_nomi = nomi = [ 
    "Alessandro", "Andrea", "Marco", "Matteo", "Luca",
    "Francesco", "Davide", "Simone", "Riccardo", "Federico",
    "Stefano", "Paolo", "Giuseppe", "Antonio", "Roberto",
    "Enrico", "Fabio", "Daniele", "Massimo", "Nicola",
    "Giorgio", "Christian", "Emanuele", "Leonardo", "Pietro",
    "Giulia", "Sofia", "Martina", "Chiara", "Sara",
    "Valentina", "Elena", "Francesca", "Alessia", "Giorgia",
    "Federica", "Alice", "Beatrice", "Irene", "Laura",
    "Marta", "Silvia", "Claudia", "Elisa", "Veronica",
    "Cristina", "Anna", "Angela", "Paola", "Monica"
]

lista_cognomi = [ 
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi",
    "Romano", "Colombo", "Ricci", "Marino", "Greco",
    "Bruno", "Gallo", "Conti", "De Luca", "Costa",
    "Giordano", "Mancini", "Rizzo", "Lombardi", "Moretti",
    "Barbieri", "Fontana", "Santoro", "Mariani", "Rinaldi",
    "Caruso", "Ferrara", "Galli", "Martini", "Leone",
    "Longo", "Gentile", "Martinelli", "Vitale", "Lombardo",
    "Serra", "Coppola", "De Santis", "D'Angelo", "Marchetti",
    "Parisi", "Villa", "Conte", "Ferraro", "Ferri",
    "Fabbri", "Bianco", "Bellini", "Grasso", "Valentini"
]

# RUOLO
lista_ruoli = [  
    "Responsabile Fornitori"
]

# Lista prefissi per fornitori
lista_prefissi_fornitore = [
    "Pet Service", "Pet Center", "Spazio Pet", "Mondo Pet", "Centro Pet", "Pet Point", "Pet Hub",
    "Pet Zone", "Pet Village", "Set Services", "Pet House", "Pet Club", "Amici Animali", "Love Pelosetti",
    "Zampa Felice", "Paw Club", "Paw Services", "Paw Pets", "Musetti Felici", "4 Zampe", "Pet & Friends",
    "Centro Animali", "Zampe Felici", "Vet & Services", "Vet Zone", "Pet Help", "Vet Friends",
    "Vet Specialist", "Clinica", "Spazio Cani e Gatti", "Vet House", "Servizi per Animali", "Amici a 4 Zampe"
]

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
    "Toilettatura" :            {"costo_orario" : (50.0, 80.0),  "tempo_erogazione" : (60, 80)},
    "Visita veterinaria" :      {"costo_orario" : (50.0, 100.0), "tempo_erogazione" : (30, 60)},
    "Cat sitting" :             {"costo_orario" : (20.0, 40.0),  "tempo_erogazione" : (60, 480)},
    "Dog walking" :             {"costo_orario" : (20.0, 40.0),  "tempo_erogazione" : (30, 60)},
    "Visita comportamentale" :  {"costo_orario" : (100.0, 150.0), "tempo_erogazione" : (60, 90)},
    "Visita nutrizionistica" :  {"costo_orario" : (100.0, 150.0), "tempo_erogazione" : (40, 60)}
}

# NOME (fornitore)
# Da implementare


# STATO
lista_stati_rich = { 
    "Nuova Richiesta" : 1,
    "Presa in carico" : 5,
    "Elaborata" : 20,
    "Annullata" : 1
}


# Orizzonte temporale per iscrizione clienti e data richieste
#today = date.today()
#last_date = today - timedelta(days = 1)
last_date = date(2026, 11, 30)
first_date = date(2025, 8, 1) 
#delta_days = (today - first_date).days
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

# Creazione lista zone
def crea_lista_zone(n):
    # Crea una lista di n zone assicurando di avere almeno 1 occorrenza per ogni zona presente nella lista
    citta = list(lista_pesata_citta.keys())
    pesi = list(lista_pesata_citta.values())

    citta_distinct = citta.copy()
    random.shuffle(citta_distinct) #Per avere anche le prime 20 occorrenze estratte sempre random

    lista_zone = []

    for i in range(1, n + 1):
        if len(citta_distinct) > 0:
            zona = citta_distinct.pop(0) # Estrae la prima città della lista
        else:
            zona = random.choices(citta, weights = pesi, k = 1)[0]

        lista_zone.append(zona)
    
    return lista_zone


# Creazione dipendenti
def crea_dipendenti():
    lista_dipendenti = []

    # Per semplicità 1 dipendente per ogni zona
    n = len(lista_pesata_citta)
    lista_zone = crea_lista_zone(n)

    for i in range(1, n + 1):
        id_dipendente = "DIP_" + str(i)
        nome = random.choice(lista_nomi)
        cognome = random.choice(lista_cognomi)
        zona = lista_zone.pop(0)
        ruolo = random.choice(lista_ruoli) # Solo responsabile fornitori

        lista_dipendenti.append({
            "ID_DIPENDENTE" : id_dipendente,
            "NOME" : nome,
            "COGNOME" : cognome,
            "ZONA" : zona,
            "RUOLO" : ruolo
        })
    
    crea_csv("lista_dipendenti.csv", lista_dipendenti[0].keys(), lista_dipendenti)   
    return lista_dipendenti


# Creazione lista clienti
def crea_clienti(n):
    # ID_CLIENTE, ZONA, DATA_ISCRIZIONE
    lista_clienti = []
    lista_zone = crea_lista_zone(n)

    for i in range(1, n + 1):
        id_cliente = "CLI_" + str(i)
        nome = random.choice(lista_nomi)
        cognome = random.choice(lista_cognomi)
        nome_cliente = f"{nome} {cognome}"
        zona = lista_zone.pop(0)

        # Clienti iscritti da quando è nata la startup fino a 5 giorni prima dell'ultima data delle richieste
        delta_days = total_days - 5
        days_to_add = random.randint(0, delta_days)
        data_iscrizione = first_date + timedelta(days_to_add)

        # Salvataggio data in formato "errato" dd/mm/yyyy 
        # in modo che lo script ETL possa pulirla e salvarla in tabella nel formato corretto
        data_iscrizione = data_iscrizione.strftime("%d/%m/%Y")

        lista_clienti.append({
            "ID_CLIENTE" : id_cliente,
            "NOME_CLIENTE" : nome_cliente,
            "ZONA" : zona ,
            "DATA_ISCRIZIONE" : data_iscrizione
        })

    crea_csv("lista_clienti.csv", lista_clienti[0].keys(), lista_clienti)

    return lista_clienti

# Creazione lista fornitori
def crea_fornitori(n, dipendenti_in):
    # ID_FORNITORE, NOME, CATEGORIA_SERVIZIO, ZONA, COSTO_ORARIO
    lista_fornitori = []
    lista_zone = crea_lista_zone(n)

    for i in range(1, n +1):
        id_fornitore = "FORN_" + str(i)
        prefisso = random.choice(lista_prefissi_fornitore)
        cognome = random.choice(lista_cognomi)
        nome = f"{prefisso} {cognome}"
        categoria_servizio = random.choice(list(lista_categorie.keys()))

        zona = lista_zone.pop(0)
        # Recupera il dipendente della zona
        dipendente = [d for d in dipendenti_in if d["ZONA"] == zona][0]
        id_dipendente = dipendente["ID_DIPENDENTE"]

        # Calcolo costo orario
        dati_categoria = lista_categorie[categoria_servizio]
        costo_orario_min, costo_orario_max = dati_categoria["costo_orario"]
        costo_orario = round(random.uniform(costo_orario_min, costo_orario_max))

        lista_fornitori.append({
            "ID_FORNITORE" : id_fornitore,
            "ID_DIPENDENTE" : id_dipendente,
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
    lista_zone = crea_lista_zone(n)

    for i in range(1, n +1):
        id_operatore = "OPER_" + str(i)
        tipo_attivita = random.choice(list(lista_categorie.keys()))

        zona = lista_zone.pop(0)

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

    # Generazione data casuale con più probabilità negli orari lavorativi per il cliente (9-18)
    # Nessuna richiesta tra le 22 e le 6 del mattino
                # 00 01 02 03 04 05 06 07 08 09 10  11  12 13 14  15  16 17 18 19 20 21 22 23 
    pesi_orario = [0, 0, 0, 0, 0, 0, 0, 1, 1, 8, 9, 10, 10, 8, 8, 10, 10, 9, 8, 6, 5, 1, 0, 0]
    range_ore = list(range(24))

    # RATING RICHIESTE
    lista_rating = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lista_pesi_rating = [ 1, 1, 1, 1, 2, 8, 10, 15, 20, 7]

    for i in range(1, n + 1):
        id_richiesta = "RIC_" + str(i)
        # Estrazione cliente che ha effettuato la richiesta
        cli = random.choice(clienti)
        id_cliente = cli["ID_CLIENTE"]
        zona = cli["ZONA"]
        data_iscrizione_cli = cli["DATA_ISCRIZIONE"]
        # Converto data_in da stringa a datetime
        data_iscrizione_cli = datetime.strptime(data_iscrizione_cli, "%d/%m/%Y").date()

        # Estrazione fornitore della stessa zona
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
        costo_orario = fornitore["COSTO_ORARIO"]
        importo_fornitore = round(( costo_orario / 60 ) * tempo_erogazione)


        #Scelta di un giorno casuale successivo alla data iscrizione del cliente
        delta_days = ( last_date - data_iscrizione_cli ).days
        add_giorni = random.randint(0, delta_days)
        data = data_iscrizione_cli + timedelta(days = add_giorni)
        ora = random.choices( population = range_ore,
                              weights = pesi_orario,
                              k = 1
                            )[0]

        # Salvataggio data in formato "errato" dd/mm/yyyy 
        # in modo che lo script ETL possa pulirla e salvarla in tabella nel formato corretto
        data = data.strftime("%d/%m/%Y")

        # Estrazione operatori della stessa zona
        operatori_zona = []
        for oper in operatori:
            if oper["ZONA"] == zona:
                operatori_zona.append(oper)
        operatore = random.choice(operatori_zona)
        id_operatore = operatore["ID_OPERATORE"]

        # Recupera stato richiesta dalla lista pesata
        stati = list(lista_stati_rich.keys())
        pesi_stati = list(lista_stati_rich.values())
        stato_richiesta = random.choices(stati, weights = pesi_stati, k = 1)[0]

        rating = 0
        if stato_richiesta == "Elaborata":
            rating = random.choices(lista_rating, weights = lista_pesi_rating, k = 1 )[0]
  

        lista_richieste.append({
            "ID_RICHIESTA" : id_richiesta,
            "ID_CLIENTE" : id_cliente,
            "ID_FORNITORE" : id_fornitore,
            "ID_OPERATORE" : id_operatore,
            # "ID_TEMPO" : "", # Verrà calcolato successivamente nello script ETL
            "DATA" : data,
            "ORA" : ora,
            "TIPO_RICHIESTA" : tipo_richiesta,
            "IMPORTO_FORNITORE" :  importo_fornitore,
            # "RICAVO" : "", # Il ricavo verrà calcolato nello script ETL come % dell'importo pagato
            "TEMPO_EROGAZIONE" : tempo_erogazione,
            "STATO_RICHIESTA" : stato_richiesta,
            "RATING" : rating
        })

    crea_csv("lista_richieste.csv", lista_richieste[0].keys(), lista_richieste)



## Main
if __name__ == "__main__":
    dipendenti_creati = crea_dipendenti()
    clienti_creati = crea_clienti(350)
    fornitori_creati = crea_fornitori(300, dipendenti_creati)
    operatori_creati = crea_operatori(300)
    crea_richieste(2500, clienti_creati, fornitori_creati, operatori_creati)