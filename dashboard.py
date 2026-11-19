import os
import sqlite3
import streamlit as st
import pandas as pd
import sys

# Query per estrazione tabelle
sql_get_db = """ SELECT r.ID_RICHIESTA, r.DATA, r.ORA, r.TIPO_RICHIESTA, r.IMPORTO_FORNITORE,
                    r.RICAVO, r.TEMPO_EROGAZIONE, r.STATO_RICHIESTA,
                    c.ID_CLIENTE, c.NOME_CLIENTE,
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

            # Conversione campo data da stringa a datetime
            df_db["DATA"] = pd.to_datetime(df_db["DATA"])
            
            return df_db

    except sqlite3.OperationalError as sql3_err:
            print("Errore lettura 'db/petcarens.db'.", sql3_err)
            sys.exit()
    

## Main

st.set_page_config(
    page_title="PetCareNS - Dashboard Interattiva",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


## Filtri
st.sidebar.header("Filtri interattivi")

# Range di date
first_date = df_db["DATA"].min().date()
last_date = df_db["DATA"].max().date()
range_date = st.sidebar.date_input(
     "Seleziona periodo",
     value = (first_date, last_date),
     min_value = first_date,
     max_value = last_date
)

# Zona
lista_zone = df_db["ZONA"].dropna().unique().tolist()
lista_zone_filtered = st.sidebar.multiselect(
    "Selezione zona",
    options = lista_zone,
    default = lista_zone
)

# Tipo Richiesta
lista_tipo_r = df_db["TIPO_RICHIESTA"].dropna().unique().tolist()
lista_tipo_r_filtered = st.sidebar.multiselect(
    "Selezione Tipo Richiesta",
    options = lista_tipo_r,
    default = lista_tipo_r
)


if len(range_date) == 2:
    start_date = range_date[0] 
    end_date = range_date[1]
else:
     start_date = first_date
     end_date = last_date

# Applicazione filtro
df_db_filtered = df_db[
     ( df_db["DATA"].dt.date >= start_date ) &
     ( df_db["DATA"].dt.date <= end_date ) & 
     ( df_db["ZONA"].isin(lista_zone_filtered) ) & 
     ( df_db["TIPO_RICHIESTA"].isin(lista_tipo_r_filtered) )
]


## Calcolo KPI
# Numero totale richieste
kpi_tot_richieste = len(df_db_filtered)
# Incassi
kpi_incassi = df_db_filtered["RICAVO"].sum()

# Fornitori attivi
kpi_clienti_attivi = df_db_filtered["ID_CLIENTE"].nunique()

# Clienti attivi
kpi_fornitori_attivi = df_db_filtered["ID_FORNITORE"].nunique()


## Visualizzazione KPI
st.subheader("KPI Principali")

kpi_rt, kpi_in, kpi_ca, kpi_fa = st.columns(4)
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

kpi_fa.metric(
     label = "Fornitori attivi",
     value = f"{kpi_fornitori_attivi}"
)


## Grafici
# Andamento delle richieste nel tempo 
st.subheader("Andamento delle richieste nel tempo")
range_date_rich = df_db_filtered.groupby(df_db_filtered["DATA"].dt.to_period("M"))
df_rich_tempo = range_date_rich["ID_RICHIESTA"].count().reset_index()
df_rich_tempo["DATA"] = df_rich_tempo["DATA"].astype(str) # Conversione Datetime a Stringa
df_rich_tempo = df_rich_tempo.rename(columns={"ID_RICHIESTA" : "Numero Richieste"})
df_rich_tempo = df_rich_tempo.rename(columns={"DATA" : "Data"})
st.line_chart(df_rich_tempo, x = "Data", y = "Numero Richieste", color="#2E86C1")

col_top_f, col_top_c = st.columns(2)

with col_top_f:
# Classifica dei primi cinque fornitori per incassi 
    st.subheader("Classifica dei primi cinque fornitori per incassi")

    top_fornitori = df_db_filtered.groupby(["ID_FORNITORE", "NOME_FORNITORE"])
    top_fornitori = top_fornitori.agg(
        NUMERO_RICHIESTE = ("ID_RICHIESTA", "count"),
        TOTALE_RICAVO = ("RICAVO", "sum")
    ).reset_index()
    top_fornitori = top_fornitori.sort_values("TOTALE_RICAVO", ascending = False).head(5)

    st.dataframe( top_fornitori.rename( 
                                        columns = {
                                            "NOME_FORNITORE" : "Fornitore",
                                            "NUMERO_RICHIESTE" : "N. Richieste",
                                            "TOTALE_RICAVO" : "Ricavi totali(€)"
                                        }), use_container_width = True
        )

with col_top_c:
# Clienti più fedeli
    st.subheader("Classifica dei primi 20 clienti per numero richieste")
    top_clienti = df_db_filtered.groupby(["ID_CLIENTE", "NOME_CLIENTE"])
    top_clienti = top_clienti.agg(
        NUMERO_RICHIESTE = ("ID_RICHIESTA", "count"),
        TOTALE_RICAVO = ("RICAVO", "sum")
    ).reset_index()
    top_clienti = top_clienti.sort_values("NUMERO_RICHIESTE", ascending = False).head(20)

    st.dataframe( top_clienti.rename( 
                                    columns = {
                                        "NOME_CLIENTE" : "Nome Cliente",
                                        "NUMERO_RICHIESTE" : "N. Richieste",
                                        "TOTALE_RICAVO" : "Ricavi totali(€)"
                                    }), use_container_width = True
        )

# Ricavi per mese
st.subheader("Ricavi per mese")
df_ric_mese = df_db_filtered.groupby(df_db_filtered["DATA"].dt.to_period("M"))               
df_ric_mese = df_ric_mese["RICAVO"].sum().reset_index()
df_ric_mese["DATA"] = df_ric_mese["DATA"].astype(str)
st.area_chart(df_ric_mese, x = "DATA", y = "RICAVO", color = "#2E86C1")


# Distribuzione delle richieste per zona
st.subheader("Distribuzione delle richieste per zona")
df_drz = df_db_filtered.groupby("ZONA")["ID_RICHIESTA"].count().reset_index()
df_drz = df_drz.rename(columns={"ID_RICHIESTA" : "Numero Richieste"})
df_drz = df_drz.rename(columns={"ZONA" : "Zona"})
st.bar_chart(df_drz, x = "Zona", y = "Numero Richieste")

# Distribuzione delle richieste per categoria di servizio
st.subheader("Distribuzione delle richieste per categoria di servizio")
df_drcs = df_db_filtered.groupby("TIPO_RICHIESTA")["ID_RICHIESTA"].count().reset_index()
df_drcs = df_drcs.rename(columns={"ID_RICHIESTA" : "Numero Richieste"})
df_drcs = df_drcs.rename(columns={"TIPO_RICHIESTA" : "Tipo Richiesta"})
st.bar_chart(df_drcs, x = "Tipo Richiesta", y = "Numero Richieste", color="#E67E22")
