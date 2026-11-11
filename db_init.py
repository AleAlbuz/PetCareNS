import sqlite3 

import os

import shutil # Per cancellazione directory e file

## SQL Statements per creazione tabelle

# Tabella Clienti
crea_tab_clienti = """ CREATE TABLE IF NOT EXISTS cliente (
                    ID_CLIENTE TEXT PRIMARY KEY,
                    ZONA TEXT NOT NULL,
                    DATA_ISCRIZIONE TEXT NOT NULL
                    )
                   """

# Tabella Fornitori
crea_tab_fornitori = """ CREATE TABLE IF NOT EXISTS FORNITORE (
                        ID_FORNITORE TEXT PRIMARY KEY,
                        NOME TEXT NOT NULL,
                        CATEGORIA_SERVIZIO TEXT NOT NULL,
                        ZONA TEXT NOT NULL
                     )
                     """

# Tabella Operatori
crea_tab_operatori = """ CREATE TABLE IF NOT EXISTS OPERATORE (
                        ID_OPERATORE TEXT PRIMARY KEY,
                        ZONA TEXT NOT NULL,
                        TIPO_ATTIVITA TEXT NOT NULL
                     )
                     """

# Tabella Tempo
crea_tab_tempo = """ CREATE TABLE IF NOT EXISTS TEMPO (
                    ID_TEMPO TEXT PRIMARY KEY,
                    DATA DATE NOT NULL,
                    GIORNO INTEGER NOT NULL,
                    MESE INTEGER NOT NULL,
                    ANNO INTEGER NOT NULL,
                    GIORNO_SETTIMANA TEXT NOT NULL
                    )
                   """

# Tabella Richieste 
crea_tab_richieste = """ CREATE TABLE IF NOT EXISTS RICHIESTA (
                        ID_RICHIESTA TEXT PRIMARY KEY,
                        ID_CLIENTE TEXT NOT NULL,
                        ID_FORNITORE TEXT NOT NULL,
                        ID_OPERATORE TEXT NOT NULL,
                        ID_TEMPO TEXT NOT NULL,
                        DATA DATE NOT NULL,
                        ORA TEXT NOT NULL,
                        IMPORTO REAL NOT NULL,
                        TEMPO_EROGAZIONE INTEGER NOT NULL,
                        STATO_RICHIESTA TEXT NOT NULL,
                        FOREIGN KEY (ID_CLIENTE)
                            REFERENCES CLIENTE(ID_CLIENTE),
                        FOREIGN KEY (ID_FORNITORE)
                            REFERENCES FORNITORE(ID_FORNITORE),
                        FOREIGN KEY (ID_OPERATORE)
                            REFERENCES OPERATORE(ID_OPERATORE),
                        FOREIGN KEY (ID_TEMPO)
                            REFERENCES TEMPO(ID_TEMPO)
                     )
                     """

# Inizializzazione cartella db (cancellazione + creazione)

if os.path.exists("db"):
    shutil.rmtree("db") # Cancella la cartella db compreso il contenuto

try:
    os.mkdir("db") # Crea directory, se esiste da exception
    print("Creata directory db")
except FileExistsError:
    print("La directory db esiste già, nessuna creazione")

# Creazione e connesione al DB
try:
    with sqlite3.connect("db/petcarens.db") as conn:
        # print(f"Aperta connesione db {sqlite3.sqlite_version}.") #Solo per test

        cursor = conn.cursor()

        # Necessario attivare le chiavi esterne, di default sono disabilitate
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute(crea_tab_clienti)
        print("Creata tab clienti")
        cursor.execute(crea_tab_fornitori)
        print("Creata tab fornitori")
        cursor.execute(crea_tab_operatori)
        print("Creata tab operatori")
        cursor.execute(crea_tab_tempo)
        print("Creata tab tempo")
        cursor.execute(crea_tab_richieste)
        print("Creata tab richieste")

        conn.commit()
        print("db/petcarens.db Inizializzato con successo")
    

except sqlite3.OperationalError as sql3_err:
    print("Errore inizializzazione database:", sql3_err)

