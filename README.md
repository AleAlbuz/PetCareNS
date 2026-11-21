### PetCareNS
Progetto universitario - Alessandro Albuzzi - Pet Care No Stress. 
Prototipo in Python e SQLite

## Requisiti 
    Python 3.10 o superiore

## Installazione
    Creare ed attivare l'ambiente virtuale (consigliato):
        - Linux:  / macOS: python3 -m venv venv && source venv/bin/activate
        - Windows: python -m venv venv && venv\Scripts\activate
    Installare dipendenze:
        pip install -r requirements.txt
        

## Sequenza di esecuzione:
    1 - py db_init.py: Per inizializzare il database nella cartella db;
    2 - py crea_random_csv.py: Per creare i csv delle entità nella cartella csv;
    3 - py etl.py: Per lanciare la pipeline ETL che legge i csv, pulisce e trasforma i dati e li salva nel db;
    4 - streamlit run dashboard.py: Per lanciare la dashboard interattiva.

    L'applicazione sarà visibile nel browser all'indirizzo http://localhost:8501