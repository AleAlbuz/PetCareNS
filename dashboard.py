import os
import sqlite3
import streamlit as st
import pandas as pd
import sys
import plotly.express as px # Per grafico a torta tema streamlit



# Query per estrazione tabelle
sql_get_db = """ SELECT r.ID_RICHIESTA, r.DATA, r.ORA, r.TIPO_RICHIESTA, r.IMPORTO_FORNITORE,
                    r.RICAVO, r.TEMPO_EROGAZIONE, r.STATO_RICHIESTA, r.RATING,
                    c.ID_CLIENTE, c.NOME_CLIENTE,
                    f.ID_FORNITORE, f.ZONA, f.NOME AS NOME_FORNITORE,
                    d.ID_DIPENDENTE, d.NOME AS NOME_DIPENDENTE, 
                    d.COGNOME AS COGNOME_DIPENDENTE, d.ZONA AS ZONA_DIPENDENTE, d.RUOLO AS RUOLO_DIPENDENTE,
                    o.ID_OPERATORE, 
                    t.ID_TEMPO, t.MESE, t.ANNO, t.GIORNO_SETTIMANA
                FROM RICHIESTA r
                LEFT JOIN CLIENTE c ON r.ID_CLIENTE = c.ID_CLIENTE
                LEFT JOIN FORNITORE f ON r.ID_FORNITORE = f.ID_FORNITORE
                LEFT JOIN DIPENDENTE d ON f.ID_DIPENDENTE = d.ID_DIPENDENTE
                LEFT JOIN OPERATORE o ON r.ID_OPERATORE = o.ID_OPERATORE
                LEFT JOIN TEMPO t ON r.ID_TEMPO = t.ID_TEMPO 
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
    #page_icon="🐾",
    page_icon = ":paw_prints:",
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

# Numero richieste completate
kpi_richieste_completate = (df_db_filtered["STATO_RICHIESTA"] == "ELABORATA").sum()
# Numero richieste da completare
kpi_richieste_in_carico = (df_db_filtered["STATO_RICHIESTA"] == "PRESA IN CARICO").sum()
# Numero richieste annullate
kpi_richieste_annullate = (df_db_filtered["STATO_RICHIESTA"] == "ANNULLATA").sum()

# Incassi
kpi_incassi = df_db_filtered["RICAVO"].sum()

# Fornitori attivi
kpi_clienti_attivi = df_db_filtered["ID_CLIENTE"].nunique()

# Clienti attivi
kpi_fornitori_attivi = df_db_filtered["ID_FORNITORE"].nunique()


## Visualizzazione KPI
st.subheader("KPI Principali")

kpi_rt, kpi_rc, kpi_rpc, kpi_ra = st.columns(4)
kpi_rt.metric(
     label = "Numero totale richieste",
     value = f"{kpi_tot_richieste}"
)

kpi_rc.metric(
     label = "Richieste elaborate",
     value = f"{kpi_richieste_completate}"
)

kpi_rpc.metric(
     label = "Richieste prese in carico",
     value = f"{kpi_richieste_in_carico}"
)

kpi_ra.metric(
     label = "Annullate",
     value = f"{kpi_richieste_annullate}"
)


kpi_in, kpi_ca, kpi_fa, kpi_dummy = st.columns(4)
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
df_rich_tempo = df_rich_tempo.rename(columns={"DATA" : "Mese"})
#st.line_chart(df_rich_tempo, x = "Mese", y = "Numero Richieste", color="#2E86C1")
st.bar_chart(df_rich_tempo, x = "Mese", y = "Numero Richieste", color="#2E86C1")


# Andamento ricavi mensili
st.subheader("Andamento ricavi mensili")
df_ric_mese = df_db_filtered.groupby(df_db_filtered["DATA"].dt.to_period("M"))               
df_ric_mese = df_ric_mese["RICAVO"].sum().reset_index()
df_ric_mese["DATA"] = df_ric_mese["DATA"].astype(str)
st.area_chart(df_ric_mese, x = "DATA", y = "RICAVO", color = "#00FF1E")


# Classifiche indentate in due colonne adiacenti
col_top_f, col_top_o = st.columns(2)

with col_top_f:
# Classifica dei primi dieci fornitori per incassi 
    st.subheader("Top 10 fornitori per incassi")

    top_fornitori = df_db_filtered.groupby(["ID_FORNITORE", "NOME_FORNITORE"])
    top_fornitori = top_fornitori.agg(
        NUMERO_RICHIESTE = ("ID_RICHIESTA", "count"),
        TOTALE_RICAVO = ("RICAVO", "sum")
    ).reset_index()
    top_fornitori = top_fornitori.sort_values("TOTALE_RICAVO", ascending = False).head(10)
    top_fornitori.index = range( 1, len( top_fornitori ) + 1) # Modifica indice per classifica
    st.dataframe( top_fornitori.rename( 
                                        columns = {
                                            "NOME_FORNITORE" : "Fornitore",
                                            "ZONA" : "Zona",
                                            "NUMERO_RICHIESTE" : "N. Richieste",
                                            "TOTALE_RICAVO" : "Ricavi totali(€)"
                                        }), use_container_width = True
        )

# Clienti più fedeli
    st.subheader("Top 20 clienti per numero richieste")
    top_clienti = df_db_filtered.groupby(["ID_CLIENTE", "NOME_CLIENTE", "ZONA"])
    top_clienti = top_clienti.agg(
        NUMERO_RICHIESTE = ("ID_RICHIESTA", "count"),
        TOTALE_RICAVO = ("RICAVO", "sum")
    ).reset_index()
    top_clienti = top_clienti.sort_values("NUMERO_RICHIESTE", ascending = False).head(20)
    top_clienti.index = range( 1, len( top_clienti ) + 1) # Modifica indice per classifica
    st.dataframe( top_clienti.rename( 
                                    columns = {
                                        "ID_CLIENTE" : "ID Cliente",
                                        "NOME_CLIENTE" : "Nome e Cognome",
                                        "ZONA" : "Zona",
                                        "NUMERO_RICHIESTE" : "N. Richieste",
                                        "TOTALE_RICAVO" : "Ricavo totale(€)"
                                    }), use_container_width = True
        )


with col_top_o:
    # Classifica operatori con Rating più alto
    st.subheader("Top 20 Operatori con almeno 3 richieste completate")
    top_operatori = df_db_filtered[df_db_filtered["RATING"] > 0 ].groupby(["ID_OPERATORE", "ZONA"])
    top_operatori = top_operatori.agg(
        RATING_MEDIO = ( "RATING", "mean" ),
        NUMERO_RICHIESTE = ("ID_RICHIESTA", "count")
    ).reset_index()
    top_operatori = top_operatori[ top_operatori[ "NUMERO_RICHIESTE" ] > 2 ]
    top_operatori = top_operatori.sort_values([ "RATING_MEDIO", "NUMERO_RICHIESTE"], ascending = [False, False]).head(20)
    top_operatori["RATING_MEDIO"] = top_operatori["RATING_MEDIO"].round(1)
    top_operatori.index = range( 1, len( top_operatori ) + 1) # Modifica indice per classifica
    st.dataframe( top_operatori.rename( 
                                        columns = {
                                            "ID_OPERATORE" : "ID Operatore",
                                            "ZONA" : "Zona",
                                            "ID_FORNITORE" : "Fornitore",
                                            "RATING_MEDIO" : "Rating Medio",
                                            "NUMERO_RICHIESTE" : "N. Richieste"
                                        }), use_container_width = True
            )
    
    # Dipendenti
    st.subheader("Statistiche Dipendenti")
    top_dipendenti = df_db_filtered.groupby(["ID_DIPENDENTE", "NOME_DIPENDENTE", "COGNOME_DIPENDENTE", 
                                             "ZONA_DIPENDENTE"])
    top_dipendenti = top_dipendenti.agg(
        FORNITORI = ("ID_FORNITORE", "nunique"),
        NUMERO_RICHIESTE = ("ID_RICHIESTA", "count"),
        RICAVO_TOTALE = ("RICAVO", "sum")
    ).reset_index()
    top_dipendenti = top_dipendenti.sort_values("NUMERO_RICHIESTE", ascending = False)
    top_dipendenti.index = range( 1, len( top_dipendenti ) + 1) # Modifica indice per classifica
    st.dataframe( top_dipendenti.rename( 
                                        columns = {
                                            "ID_DIPENDENTE" : "ID Dipendente",
                                            "NOME_DIPENDENTE" : "Nome",
                                            "COGNOME_DIPENDENTE" : "Cognome",
                                            "ZONA_DIPENDENTE" : "Zona",
                                            #"RUOLO_DIPENDENTE" : "Ruolo",
                                            "NUMERO_RICHIESTE" : "N. Richieste",
                                            "TOTALE_RICAVO" : "Ricavo totale(€)"
                                        }), use_container_width = True
        )




# Distribuzione delle richieste per zona
st.subheader("Distribuzione delle richieste per zona")
df_drz = df_db_filtered.groupby("ZONA")["ID_RICHIESTA"].count().reset_index()
df_drz = df_drz.rename(columns={"ID_RICHIESTA" : "Numero Richieste"})
df_drz = df_drz.rename(columns={"ZONA" : "Zona"})
st.bar_chart(df_drz, x = "Zona", y = "Numero Richieste", color = "#FF1100")

# Distribuzione delle richieste per categoria di servizio
st.subheader("Distribuzione delle richieste per categoria di servizio")
df_drcs = df_db_filtered.groupby("TIPO_RICHIESTA")["ID_RICHIESTA"].count().reset_index()
df_drcs = df_drcs.rename(columns={"ID_RICHIESTA" : "Numero Richieste"})
df_drcs = df_drcs.rename(columns={"TIPO_RICHIESTA" : "Tipo Richiesta"})
#st.bar_chart(df_drcs, x = "Tipo Richiesta", y = "Numero Richieste", color="#E67E22")

# Grafico a torta dinamico
df_drcs_pie = px.pie(
     df_drcs,
     names = "Tipo Richiesta",
     values = "Numero Richieste",
     title = "Distribuzione delle richieste per categoria di servizio",
     hole = 0.3,
     color_discrete_sequence = px.colors.qualitative.Set1,
)

# Sfondo trasparente
df_drcs_pie.update_layout(
     paper_bgcolor = "rgba( 0, 0, 0, 0)",
     plot_bgcolor = "rgba( 0, 0, 0, 0)",
     margin = dict( l = 20, r = 20, t = 40, b = 20),
)

st.plotly_chart(df_drcs_pie, use_container_width = True, theme = "streamlit")
