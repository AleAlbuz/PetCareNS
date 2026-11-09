import sqlite3 

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
                    DATA
                    ORA
                    GIORNO
                    MESE
                    ANNO
                    GIORNO_SETTIMANA
                    )
                   """

# Tabella Richieste 
crea_tab_richieste = """ CREATE TABLE IF NOT EXISTS RICHIESTA (
                        ID_RICHIESTA TEXT PRIMARY KEY,
                        ID_CLIENTE TEXT NOT NULL,
                        ID_FORNITORE TEXT NOT NULL,
                        ID_OPERATORE TEXT NOT NULL,
                        ID_TEMPO TEXT NOT NULL,
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


# Creazione e connesione al DB

try:
    with sqlite3.connect("db/petcarens.db") as conn:
        print(f"Aperta connesione db {sqlite3.sqlite_version}.")

    cursor = conn.cursor()

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

    

except sqlite3.OperationalError as sql3_err:
    print("Failed to open database:", sql3_err)

