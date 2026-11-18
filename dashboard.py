import os
import sqlite3
import streamlit as st
import pandas as pd
import sys

# Query per estrazione tabelle
sql_get_db = """ SELECT r.ID_RICHIESTA, r.DATA, r.ORA, r.TIPO_RICHIESTA, r.IMPORTO_FORNITORE,
                    r.RICAVO, r.TEMPO_EROGAZIONE, r.STATO_RICHIESTA,
                    c.ID_CLIENTE, 
                    f.ID_FORNITORE, f.ZONA, f.NOME AS NOME_FORNITORE,
                    o.ID_OPERATORE, 
                    t.ID_TEMPO, t.MESE, t.ANNO, t.GIORNO_SETTIMANA
                FROM RICHIESTA r
                LEFT JOIN CLIENTE c   ON r.ID_CLIENTE = c.ID_CLIENTE
                LEFT JOIN FORNITORE f ON r.ID_FORNITORE = f.ID_FORNITORE
                LEFT JOIN OPERATORE o ON r.ID_OPERATORE = o.ID_OPERATORE
                LEFT JOIN TEMPO t     ON r.ID_TEMPO = t.ID_TEMPO 
         """


# Estrazione dati da DB
def get_db():

# Creazione e connesione al DB
    try:
        with sqlite3.connect("db/petcarens.db") as conn:

            df_db = pd.read_sql_query(sql_get_db, conn)

            return df_db

    except sqlite3.OperationalError as sql3_err:
            print("Errore lettura 'db/petcarens.db'.", sql3_err)
            sys.exit()
    

## Main

st.title("Pet Care NoStress")
st.header("Dashboard Interattiva")
# st.write("")

# Prima della dashboard devono essere necessariamente eseguiti in seguenza:
# 1) db_init.py
# 2) crea_random_csv.py
# 3) etl.py
# Verifica esistenza file creati dai primi due step:
if not os.path.exists("db/petcarens.db"):
    st.error("Errore: il db 'db/petcarens.db' non esiste. Eseguire prima script db_init.py")
    st.stop()

if not os.path.exists("csv"):
    st.error("Errore: la directory 'csv' non esiste. Eseguire prima script crea_random_csv.py")
    st.stop()

# Recupera dati salvati su db/petcarens.db
df_db = get_db()
if df_db is None or df_db.empty:
     st.error("Il db è vuoto. Eseguire prima script etl.py")
     st.stop()

## Calcolo KPI
# Numero totale richieste
kpi_tot_richieste = len(df_db)
# Incassi
kpi_incassi = df_db["RICAVO"].sum()
# Tempo medio di erogazione

# Clienti attivi
kpi_clienti_attivi = df_db["ID_CLIENTE"].nunique()


## Visualizzazione KPI
st.subheader("KPI Principali")

kpi_rt, kpi_in, kpi_ca = st.columns(3)
kpi_rt.metric(
     label = "Numero totale richieste",
     value = f"{kpi_tot_richieste}"
)

kpi_in.metric(
     label = "Incassi",
     value = f"{kpi_incassi:,.2f}"
)

kpi_ca.metric(
     label = "Clienti attivi",
     value = f"{kpi_clienti_attivi}"
)


## Grafici
# Andamento delle richieste nel tempo 
st.subheader("Andamento delle richieste nel tempo")

# Classifica dei primi cinque fornitori per incassi 
st.subheader("Classifica dei primi cinque fornitori per incassi")


# Distribuzione delle richieste per zona e categoria di servizio

st.subheader("Distribuzione delle richieste per zona")
df_drz = df_db.groupby("ZONA")["ID_RICHIESTA"].count().reset_index()
df_drz = df_drz.rename(columns={"ID_RICHIESTA" : "NUMERO_RICHIESTE"})
st.bar_chart(df_drz, x = "ZONA", y = "NUMERO_RICHIESTE")


st.subheader("Distribuzione delle richieste per categoria di servizio")
df_drcs = df_db.groupby("TIPO_RICHIESTA")["ID_RICHIESTA"].count().reset_index()
df_drcs = df_drcs.rename(columns={"ID_RICHIESTA" : "NUMERO_RICHIESTE"})
st.bar_chart(df_drcs, x = "TIPO_RICHIESTA", y = "NUMERO_RICHIESTE", color="#E67E22")
